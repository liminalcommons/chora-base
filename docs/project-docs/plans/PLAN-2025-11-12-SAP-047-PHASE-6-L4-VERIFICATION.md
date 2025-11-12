# SAP-047 Phase 6: L1-L4 Verification Plan

**Plan ID**: PLAN-2025-11-12-SAP-047-PHASE-6-L4-VERIFICATION
**Status**: In Progress
**Start Date**: 2025-11-12
**Estimated Duration**: 4 days (Days 15-18)
**Target**: L4 verification of capability server templates (chora-base 5.0.0)
**Repository**: liminalcommons/chora-capability-server-template

---

## 🎯 Executive Summary

This plan outlines the Phase 6 L1-L4 verification for **SAP-047 (Capability Server Template)**, part of chora-base 5.0.0's capability server architecture suite.

**Objective**: Verify that the capability server generator (`create-capability-server.py` v2.0.0) produces production-ready projects with all interfaces, infrastructure patterns, and ecosystem SAPs working correctly.

**Profile**: Full (CLI + REST + MCP + Registry + Bootstrap + Composition + Beads + Inbox + A-MEM)

**Success Criteria**:
- All templates render correctly
- All quality gates pass (ruff, mypy, pytest ≥85%)
- All interfaces functional (CLI, REST, MCP)
- All infrastructure patterns verified (registry, bootstrap, composition)
- Docker builds and runs successfully
- Performance targets met (generation <3min, Docker <3min, tests <30sec)
- Community-ready GitHub template repository

---

## 🔗 Context: chora-base 5.0.0

**Version**: 5.0.0 (released 2025-11-12)

**New Feature**: Capability Server Architecture Suite (SAP-042-047)
- **SAP-042**: Interface Design (core/interface separation)
- **SAP-043**: Multi-Interface (CLI, REST, MCP patterns)
- **SAP-044**: Registry (service discovery with health monitoring)
- **SAP-045**: Bootstrap (dependency-ordered startup with rollback)
- **SAP-046**: Composition (saga, circuit breaker, event bus)
- **SAP-047**: Capability Server Template (50+ templates, generator v2.0.0)

**chora-base Repository**:
- Location: `/Users/victorpiper/code/chora-base`
- Templates: `static-template/capability-server-templates/`
- Generator: `scripts/create-capability-server.py` v2.0.0
- SAP Docs: `docs/skilled-awareness/capability-server-template/`

**Generated Repository** (this verification):
- Repository: `liminalcommons/chora-capability-server-template`
- Profile: Full (all features enabled)
- Purpose: L1-L4 verification + public template repository

**Workflow**:
1. Claude Code in chora-base: Generate project with full profile
2. Push to GitHub: `liminalcommons/chora-capability-server-template`
3. Claude Code in new repo: Execute L1-L4 verification using this plan
4. Report results: GO/NO-GO decision, update SAP-047 ledger

---

## 📋 Prerequisites

### Required Tools
- Python 3.11+ (capability server target version)
- Git + GitHub CLI (`gh`)
- Docker + docker-compose
- Virtual environment tool (venv)

### Required Access
- GitHub organization: `liminalcommons` (for template repository)
- GitHub permissions: Create public repositories, enable template feature
- Docker Hub (optional, for image publishing)

### chora-base Access
- Local clone: `/Users/victorpiper/code/chora-base`
- Branch: `main` (5.0.0 release)
- Generator: `scripts/create-capability-server.py` v2.0.0
- Templates: 50+ template files in `static-template/capability-server-templates/`

---

## 🎯 Verification Levels (L1-L4)

Based on chora-base SAP verification methodology (see `/docs/project-docs/plans/sap-verification-methodology.md`).

### L1: Configured (Basic Generation)
**Focus**: Template generation correctness

**Success Criteria**:
- ✅ All files generated (~80 files)
- ✅ Templates render without errors
- ✅ Dependencies install successfully
- ✅ No blocking errors
- ✅ Generation time <3 min

**Verification Methods**:
- File existence checks
- Template substitution validation
- Dependency installation test

---

### L2: Usage (Comprehensive Testing)
**Focus**: Interface and quality gate functionality

**Success Criteria**:
- ✅ All quality gates pass (ruff, mypy, pytest)
- ✅ Test coverage ≥85%
- ✅ All 3 interfaces work (CLI, REST, MCP)
- ✅ All 3 infrastructure patterns work (registry, bootstrap, composition)
- ✅ All 3 ecosystem SAPs initialized (beads, inbox, A-MEM)

**Verification Methods**:
- Quality gate automation (ruff, mypy, pytest)
- Manual interface testing (CLI commands, API endpoints, MCP tools)
- Infrastructure pattern unit tests
- Ecosystem SAP functionality tests

---

### L3: Active (Best Practices)
**Focus**: Architecture validation and deployment

**Success Criteria**:
- ✅ Core/interface separation validated (no circular dependencies)
- ✅ Docker builds successfully (<3 min, <300MB)
- ✅ Docker runs successfully (API health check passes)
- ✅ GitHub template repository enabled
- ✅ Documentation complete and accurate
- ✅ CI/CD workflows configured

**Verification Methods**:
- Architecture linting (grep for invalid imports)
- Docker build + run tests
- GitHub repository setup
- Documentation completeness check

---

### L4: Deep (Optimization & Production Readiness)
**Focus**: User experience and performance

**Success Criteria**:
- ✅ User simulation successful (<15 min to working project)
- ✅ Performance targets met (all metrics within targets)
- ✅ Advanced patterns verified (circuit breaker opens, saga compensates, etc.)
- ✅ No critical bugs
- ✅ Community-ready (documentation, examples, CI/CD green)

**Verification Methods**:
- User simulation (2 test users)
- Performance benchmark (generation, Docker, tests, API startup)
- Advanced pattern integration tests
- Community readiness checklist

---

## 📅 Day 15: L1 Verification (Basic Generation)

### Overview
- **Duration**: 2-3 hours
- **Objective**: Verify template generation creates all files correctly
- **Output**: L1 verification report, GitHub repository created

---

### Phase 1: Generate Project (30 min)

**Location**: Run from chora-base repository

```bash
cd /Users/victorpiper/code/chora-base

# Generate full profile project with all ecosystem SAPs
python scripts/create-capability-server.py \
    --name "Chora Capability Server" \
    --namespace chora \
    --description "Production-ready capability server with CLI, REST API, MCP, service registry, bootstrap orchestration, and composition patterns" \
    --enable-mcp \
    --enable-registry \
    --enable-bootstrap \
    --enable-composition \
    --enable-beads \
    --enable-inbox \
    --enable-memory \
    --author "Victor Piper" \
    --email "victor@liminalcommons.com" \
    --github liminalcommons \
    --output ~/temp/chora-capability-server-template
```

**Expected Output**:
```
================================================================================
Create Capability Server v2.0.0 (SAP-047)
Chora-Base v5.0.0
================================================================================

📋 Using profile: minimal
   CLI + REST only, no optional features

🔧 Deriving project variables...

📦 Project Configuration
────────────────────────────────────────────────────────────────────────────────
  Capability Name:  Chora Capability Server
  Package Name:     chora_capability_server
  Namespace:        chora
  Description:      Production-ready capability server with CLI, REST API, MCP, service registry, bootstrap orchestration, and composition patterns
  Author:           Victor Piper <victor@liminalcommons.com>
  GitHub:           liminalcommons
  Python Version:   3.11
  License:          MIT
  Profile:          minimal

  Interfaces:
    ✅ CLI (Click)
    ✅ REST API (FastAPI)
    ✅ MCP (FastMCP)

  Infrastructure:
    ✅ Service Registry (SAP-044)
    ✅ Bootstrap Orchestration (SAP-045)
    ✅ Composition Patterns (SAP-046)
────────────────────────────────────────────────────────────────────────────────

📁 Creating project at: ~/temp/chora-capability-server-template

📂 Creating directory structure...
  ✓ Created chora_capability_server/core/
  ✓ Created chora_capability_server/interfaces/cli/
  ✓ Created chora_capability_server/interfaces/rest/
  ✓ Created chora_capability_server/interfaces/mcp/
  ✓ Created chora_capability_server/infrastructure/registry/
  ✓ Created chora_capability_server/infrastructure/bootstrap/
  ✓ Created chora_capability_server/infrastructure/composition/
  ... (total ~25 directories)

Rendering templates (50+ files)...
  ✓ Rendered chora_capability_server/core/models.py
  ✓ Rendered chora_capability_server/core/services.py
  ✓ Rendered chora_capability_server/core/exceptions.py
  ... (total ~50 templates)

✅ Successfully rendered 50/50 templates + 8 __init__.py files

🔧 Initializing beads (SAP-015)...
  ✓ Created .beads/issues.jsonl
  ✓ Created .beads/config.yaml

📬 Initializing inbox (SAP-001)...
  ✓ Created inbox/coordination/active.jsonl
  ✓ Created inbox/coordination/archived.jsonl

🧠 Initializing A-MEM (SAP-010)...
  ✓ Created .chora/memory/events/development.jsonl

🔄 Initializing git repository...
  ✓ Initialized git repository
  ✓ Created initial commit

✅ Validation passed (32/32 checks)

================================================================================
✅ Capability Server Created Successfully!
================================================================================
```

**Timing**: Record generation time (target: <180 seconds)

---

### Phase 2: L1 Verification Checks (30 min)

**Location**: Run from generated project

```bash
cd ~/temp/chora-capability-server-template

# Create verification script
cat > verify-l1.sh << 'EOF'
#!/bin/bash
echo "=== SAP-047 L1 Verification (chora-base 5.0.0) ==="
echo ""

# File count
FILE_COUNT=$(find . -type f | wc -l)
echo "📁 Files generated: $FILE_COUNT (expected: ~80)"

# Core layer
echo ""
echo "Core Layer:"
test -d chora_capability_server/core && echo "  ✅ Core directory" || echo "  ❌ Core missing"
test -f chora_capability_server/core/models.py && echo "  ✅ Core models" || echo "  ❌ Models missing"
test -f chora_capability_server/core/services.py && echo "  ✅ Core services" || echo "  ❌ Services missing"
test -f chora_capability_server/core/exceptions.py && echo "  ✅ Core exceptions" || echo "  ❌ Exceptions missing"

# Interfaces
echo ""
echo "Interfaces:"
test -d chora_capability_server/interfaces/cli && echo "  ✅ CLI interface" || echo "  ❌ CLI missing"
test -d chora_capability_server/interfaces/rest && echo "  ✅ REST interface" || echo "  ❌ REST missing"
test -d chora_capability_server/interfaces/mcp && echo "  ✅ MCP interface" || echo "  ❌ MCP missing"

# Infrastructure
echo ""
echo "Infrastructure:"
test -d chora_capability_server/infrastructure/registry && echo "  ✅ Registry (SAP-044)" || echo "  ❌ Registry missing"
test -d chora_capability_server/infrastructure/bootstrap && echo "  ✅ Bootstrap (SAP-045)" || echo "  ❌ Bootstrap missing"
test -d chora_capability_server/infrastructure/composition && echo "  ✅ Composition (SAP-046)" || echo "  ❌ Composition missing"

# Ecosystem SAPs
echo ""
echo "Ecosystem SAPs:"
test -d .beads && echo "  ✅ Beads (SAP-015)" || echo "  ❌ Beads missing"
test -d inbox && echo "  ✅ Inbox (SAP-001)" || echo "  ❌ Inbox missing"
test -d .chora/memory && echo "  ✅ A-MEM (SAP-010)" || echo "  ❌ A-MEM missing"

# Documentation
echo ""
echo "Documentation:"
test -f AGENTS.md && echo "  ✅ AGENTS.md" || echo "  ❌ AGENTS.md missing"
test -f CLAUDE.md && echo "  ✅ CLAUDE.md" || echo "  ❌ CLAUDE.md missing"
test -f VERIFICATION.md && echo "  ✅ VERIFICATION.md" || echo "  ❌ VERIFICATION.md missing"
test -f CLI.md && echo "  ✅ CLI.md" || echo "  ❌ CLI.md missing"
test -f API.md && echo "  ✅ API.md" || echo "  ❌ API.md missing"
test -f ARCHITECTURE.md && echo "  ✅ ARCHITECTURE.md" || echo "  ❌ ARCHITECTURE.md missing"
test -f README.md && echo "  ✅ README.md" || echo "  ❌ README.md missing"

# Configuration
echo ""
echo "Configuration:"
test -f pyproject.toml && echo "  ✅ pyproject.toml" || echo "  ❌ pyproject.toml missing"
test -f setup.py && echo "  ✅ setup.py" || echo "  ❌ setup.py missing"
test -f Dockerfile && echo "  ✅ Dockerfile" || echo "  ❌ Dockerfile missing"
test -f docker-compose.yml && echo "  ✅ docker-compose.yml" || echo "  ❌ docker-compose.yml missing"
test -f .github/workflows/ci.yml && echo "  ✅ CI workflow" || echo "  ❌ CI missing"
test -f .github/workflows/cd.yml && echo "  ✅ CD workflow" || echo "  ❌ CD missing"

# Template substitution check
echo ""
echo "Template Quality:"
UNSUBSTITUTED=$(grep -r "{{" --include="*.py" . 2>/dev/null | grep -v "Jinja2" | wc -l)
if [ $UNSUBSTITUTED -eq 0 ]; then
    echo "  ✅ No unsubstituted variables"
else
    echo "  ❌ Found $UNSUBSTITUTED unsubstituted variables"
    grep -r "{{" --include="*.py" . | grep -v "Jinja2"
fi

# Python syntax check
echo ""
echo "Python Syntax:"
python -m py_compile chora_capability_server/**/*.py 2>/dev/null && echo "  ✅ Valid Python syntax" || echo "  ❌ Syntax errors found"

echo ""
echo "=== L1 Verification Complete ==="
EOF

chmod +x verify-l1.sh
./verify-l1.sh
```

---

### Phase 3: Dependency Installation (30 min)

```bash
cd ~/temp/chora-capability-server-template

# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install project + dev dependencies
pip install -e .[dev]

# Verify CLI installed
which chora
chora --version

# Verify key dependencies
pip list | grep -E "(click|fastapi|mcp|pydantic|pytest|ruff|mypy)"
```

**Expected Output**:
```
Successfully installed chora-capability-server-0.1.0
... (list of dependencies)
```

---

### Phase 4: Create GitHub Repository (30 min)

```bash
cd ~/temp/chora-capability-server-template

# Verify git initialized (should be done by generator)
git status

# Create GitHub repository
gh repo create liminalcommons/chora-capability-server-template \
  --public \
  --description "Production-ready capability server template with CLI, REST API, MCP, service registry, and composition patterns (chora-base 5.0.0, SAP-047)" \
  --source=. \
  --push

# Verify push successful
git remote -v
git log --oneline -5
```

**Repository URL**: https://github.com/liminalcommons/chora-capability-server-template

---

### Phase 5: L1 Verification Report (30 min)

**Create**: `docs/verification/L1-report.md` in generated project

```markdown
# L1 Verification Report

**Date**: 2025-11-12
**Phase**: L1 (Basic Generation)
**SAP**: SAP-047 (Capability Server Template)
**chora-base Version**: 5.0.0
**Generator Version**: create-capability-server.py v2.0.0
**Profile**: Full

---

## Generation Metrics

- **Generation time**: [X] seconds (target: <180s) ✅/❌
- **Files generated**: [X] files (expected: ~80) ✅/❌
- **Directories created**: [X] directories (expected: ~25) ✅/❌
- **Template errors**: [X] errors (expected: 0) ✅/❌

---

## File Structure Verification

### Core Layer ✅/❌
- Core directory: ✅
- Core models: ✅
- Core services: ✅
- Core exceptions: ✅

### Interfaces ✅/❌
- CLI interface (Click): ✅
- REST interface (FastAPI): ✅
- MCP interface (FastMCP): ✅

### Infrastructure ✅/❌
- Registry (SAP-044): ✅
- Bootstrap (SAP-045): ✅
- Composition (SAP-046): ✅

### Ecosystem SAPs ✅/❌
- Beads (SAP-015): ✅
- Inbox (SAP-001): ✅
- A-MEM (SAP-010): ✅

### Documentation ✅/❌
- AGENTS.md: ✅
- CLAUDE.md: ✅
- VERIFICATION.md: ✅
- CLI.md: ✅
- API.md: ✅
- ARCHITECTURE.md: ✅
- README.md: ✅

### Configuration ✅/❌
- pyproject.toml: ✅
- setup.py: ✅
- Dockerfile: ✅
- docker-compose.yml: ✅
- CI workflow: ✅
- CD workflow: ✅

---

## Dependency Installation ✅/❌

- Virtual environment created: ✅
- Dependencies installed: ✅
- CLI command available: ✅
- No installation errors: ✅

---

## Template Quality ✅/❌

- No unsubstituted variables: ✅
- Valid Python syntax: ✅
- Proper file permissions: ✅

---

## Repository Setup ✅/❌

- Git initialized: ✅
- GitHub repository created: ✅
- Initial commit pushed: ✅
- Repository URL: https://github.com/liminalcommons/chora-capability-server-template

---

## Blockers

[List any issues found, or "None" if all checks pass]

---

## Decision: ✅ GO to L2 / ⏸️ CONDITIONAL NO-GO / ❌ NO-GO

**Rationale**: [Explain decision based on verification results]

**If CONDITIONAL NO-GO**:
- Blocker 1: [Description] - Fix effort: [X hours]
- Blocker 2: [Description] - Fix effort: [X hours]
- Total fix effort: [X hours]

**If GO**:
- Proceed to Day 16 (L2 Verification)
- Next steps: Quality gates + interface testing

---

**Verified by**: Claude Code
**Report generated**: 2025-11-12
```

**Action**: Commit L1 report to repository

```bash
cd ~/temp/chora-capability-server-template
mkdir -p docs/verification
# Create L1-report.md with contents above
git add docs/verification/L1-report.md
git commit -m "docs: Add L1 verification report (chora-base 5.0.0)"
git push
```

---

## 📅 Day 16: L2 Verification (Interface Testing)

### Overview
- **Duration**: 3-4 hours
- **Objective**: Verify all interfaces and quality gates work correctly
- **Output**: L2 verification report

---

### Phase 1: Quality Gates (60 min)

**Location**: Generated project

```bash
cd ~/temp/chora-capability-server-template
source venv/bin/activate

# 1. Ruff (linting) - Target: 0 violations
echo "=== Ruff (Linting) ==="
ruff check .
RUFF_EXIT=$?
echo "Ruff exit code: $RUFF_EXIT (0 = success)"

# 2. Mypy (type checking) - Target: 0 type errors
echo ""
echo "=== Mypy (Type Checking) ==="
mypy chora_capability_server
MYPY_EXIT=$?
echo "Mypy exit code: $MYPY_EXIT (0 = success)"

# 3. Pytest (tests + coverage) - Target: ≥85% coverage
echo ""
echo "=== Pytest (Tests + Coverage) ==="
pytest --cov=chora_capability_server --cov-report=term-missing --cov-report=html --cov-fail-under=85
PYTEST_EXIT=$?
echo "Pytest exit code: $PYTEST_EXIT (0 = success)"

# 4. Pre-commit hooks (optional, if configured)
echo ""
echo "=== Pre-commit Hooks ==="
pre-commit run --all-files
PRECOMMIT_EXIT=$?
echo "Pre-commit exit code: $PRECOMMIT_EXIT (0 = success)"

# Summary
echo ""
echo "=== Quality Gate Summary ==="
echo "Ruff: $([ $RUFF_EXIT -eq 0 ] && echo '✅ PASS' || echo '❌ FAIL')"
echo "Mypy: $([ $MYPY_EXIT -eq 0 ] && echo '✅ PASS' || echo '❌ FAIL')"
echo "Pytest: $([ $PYTEST_EXIT -eq 0 ] && echo '✅ PASS' || echo '❌ FAIL')"
echo "Pre-commit: $([ $PRECOMMIT_EXIT -eq 0 ] && echo '✅ PASS' || echo '❌ FAIL')"
```

**Expected Results**:
- Ruff: 0 violations
- Mypy: 0 type errors
- Pytest: All tests pass, coverage ≥85%
- Pre-commit: All hooks pass

---

### Phase 2: CLI Interface Testing (30 min)

```bash
cd ~/temp/chora-capability-server-template
source venv/bin/activate

echo "=== CLI Interface Testing ==="

# Test 1: Help
chora --help

# Test 2: Create entity
chora create "Test Task" --description "L2 verification test"

# Test 3: List (JSON format)
chora list --format json

# Test 4: List (Table format)
chora list --format table

# Test 5: List (YAML format)
chora list --format yaml

# Test 6: Get entity (use UUID from list output)
UUID="[paste UUID from list]"
chora get $UUID

# Test 7: Update entity
chora update $UUID --status active --description "Updated description"

# Test 8: Delete entity
chora delete $UUID

# Test 9: Health check
chora health

echo "=== CLI Interface Tests Complete ==="
```

---

### Phase 3: REST API Interface Testing (30 min)

```bash
cd ~/temp/chora-capability-server-template
source venv/bin/activate

echo "=== REST API Interface Testing ==="

# Terminal 1: Start API server
uvicorn chora_capability_server.interfaces.rest:app --reload &
API_PID=$!
sleep 5  # Wait for startup

# Terminal 2: Test endpoints
# Test 1: Health check
curl -f http://localhost:8000/health
echo ""

# Test 2: OpenAPI docs
curl -f http://localhost:8000/docs
echo ""

# Test 3: Create entity
curl -X POST http://localhost:8000/api/v1/entities \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Entity",
    "description": "REST API L2 verification"
  }'
echo ""

# Test 4: List entities
curl http://localhost:8000/api/v1/entities
echo ""

# Test 5: Get entity (use ID from create response)
ENTITY_ID="[paste ID from create response]"
curl http://localhost:8000/api/v1/entities/$ENTITY_ID
echo ""

# Test 6: Update entity
curl -X PUT http://localhost:8000/api/v1/entities/$ENTITY_ID \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Entity",
    "description": "Updated via REST API"
  }'
echo ""

# Test 7: Partial update
curl -X PATCH http://localhost:8000/api/v1/entities/$ENTITY_ID/status \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
echo ""

# Test 8: Delete entity
curl -X DELETE http://localhost:8000/api/v1/entities/$ENTITY_ID
echo ""

# Cleanup
kill $API_PID

echo "=== REST API Interface Tests Complete ==="
```

---

### Phase 4: MCP Interface Testing (30 min)

```bash
cd ~/temp/chora-capability-server-template
source venv/bin/activate

echo "=== MCP Interface Testing ==="

# Test 1: Verify MCP server starts
python -m chora_capability_server.interfaces.mcp &
MCP_PID=$!
sleep 2
kill $MCP_PID

echo "✅ MCP server starts successfully"

# Test 2: Configure Claude Desktop
echo "Add to Claude Desktop config:"
cat << EOF
{
  "mcpServers": {
    "chora": {
      "command": "python",
      "args": ["-m", "chora_capability_server.interfaces.mcp"],
      "cwd": "$(pwd)"
    }
  }
}
EOF

# Manual test in Claude Desktop:
# - Restart Claude Desktop
# - Verify "chora" tools appear
# - Test: chora:create, chora:list, chora:get, etc.

echo "=== MCP Interface Tests Complete ==="
```

---

### Phase 5: Infrastructure Pattern Testing (30 min)

**Service Registry (SAP-044)**:

```python
# Test registry functionality
from chora_capability_server.infrastructure.registry import ServiceRegistry
import time

registry = ServiceRegistry()

# Register service
registry.register('service-1', 'http://localhost:9001', ['capability1', 'capability2'])
print("✅ Service registered")

# Discover by capability
services = registry.discover('capability1')
print(f"✅ Discovered {len(services)} services with capability1")

# Heartbeat
registry.heartbeat('service-1')
print("✅ Heartbeat sent")

# Wait for timeout (30s default)
time.sleep(35)
services_after_timeout = registry.discover('capability1')
print(f"✅ After timeout: {len(services_after_timeout)} services (expected: 0)")
```

**Bootstrap Orchestration (SAP-045)**:

```python
from chora_capability_server.infrastructure.bootstrap import Bootstrap, Component

# Define components with dependencies
db = Component('database', startup=lambda: print('DB started'), dependencies=[])
cache = Component('cache', startup=lambda: print('Cache started'), dependencies=['database'])
api = Component('api', startup=lambda: print('API started'), dependencies=['database', 'cache'])

# Create bootstrap
bootstrap = Bootstrap()
bootstrap.add_component(api)  # Add in any order
bootstrap.add_component(db)
bootstrap.add_component(cache)

# Start (should resolve dependencies: DB → Cache → API)
bootstrap.start()
# Expected order: DB started, Cache started, API started
print("✅ Components started in correct order")
```

**Composition Patterns (SAP-046)**:

```python
from chora_capability_server.infrastructure.composition import CircuitBreaker, EventBus, Saga, SagaStep
import asyncio

# Test 1: Circuit Breaker
async def failing_service():
    raise Exception('Service down')

cb = CircuitBreaker(failure_threshold=2, recovery_timeout=5.0)

async def test_circuit_breaker():
    for i in range(5):
        try:
            await cb.call(failing_service)
        except Exception:
            print(f"Call {i+1}: Circuit state = {cb.state}")

asyncio.run(test_circuit_breaker())
# Expected: Circuit opens after 2 failures
print("✅ Circuit breaker opens on failures")

# Test 2: Event Bus
bus = EventBus()

def handler1(event):
    print(f"Handler 1: {event.type}")

def handler2(event):
    print(f"Handler 2: {event.type}")

bus.subscribe('test.event', handler1)
bus.subscribe('test.event', handler2)

class TestEvent:
    type = 'test.event'
    data = {'message': 'Hello'}

bus.publish(TestEvent())
# Expected: Both handlers called
print("✅ Event bus pub-sub works")

# Test 3: Saga
async def step1(ctx):
    return {'step1': 'done'}

async def compensate1(ctx):
    print('Compensated step 1')

async def step2(ctx):
    raise Exception('Step 2 failed')

async def compensate2(ctx):
    print('Compensated step 2')

saga = Saga()
saga.add_step(SagaStep('step1', step1, compensate1))
saga.add_step(SagaStep('step2', step2, compensate2))

try:
    asyncio.run(saga.execute({}))
except:
    print("✅ Saga compensates on failure")
```

---

### Phase 6: Ecosystem SAP Testing (30 min)

**Beads (SAP-015)**:

```bash
cd ~/temp/chora-capability-server-template

# Test beads task tracking
bd create "L2 verification task" --assignee victor --status open
bd list --status open
bd update [ID from list] --status in_progress
bd show [ID]
bd close [ID] --reason "L2 verification complete"

echo "✅ Beads task tracking works"
```

**Inbox (SAP-001)**:

```bash
cd ~/temp/chora-capability-server-template

# Verify inbox structure
test -d inbox/coordination && echo "✅ Inbox directory"
test -f inbox/coordination/active.jsonl && echo "✅ Active requests file"
test -f inbox/coordination/archived.jsonl && echo "✅ Archived requests file"

# Test coordination request (create manually)
cat > inbox/coordination/active.jsonl << EOF
{"id":"COORD-2025-001","type":"verification","title":"L2 Verification","status":"active","created":"2025-11-12T10:00:00Z"}
EOF

cat inbox/coordination/active.jsonl
echo "✅ Inbox coordination works"
```

**A-MEM (SAP-010)**:

```bash
cd ~/temp/chora-capability-server-template

# Verify A-MEM structure
test -d .chora/memory && echo "✅ A-MEM directory"
test -f .chora/memory/events/development.jsonl && echo "✅ Development events file"

# Test event logging (append to development.jsonl)
echo '{"type":"L2_VERIFICATION","timestamp":"2025-11-12T10:00:00Z","data":{"phase":"L2","status":"in_progress"}}' >> .chora/memory/events/development.jsonl

tail -1 .chora/memory/events/development.jsonl
echo "✅ A-MEM event logging works"
```

---

### Phase 7: L2 Verification Report (30 min)

**Create**: `docs/verification/L2-report.md`

```markdown
# L2 Verification Report

**Date**: 2025-11-12
**Phase**: L2 (Interface Testing)
**SAP**: SAP-047 (Capability Server Template)
**chora-base Version**: 5.0.0

---

## Quality Gates ✅/❌

- Ruff (linting): [0 violations / X violations] ✅/❌
- Mypy (type checking): [0 errors / X errors] ✅/❌
- Pytest (tests): [X/X tests pass] ✅/❌
- Coverage: [X%] (target: ≥85%) ✅/❌
- Pre-commit hooks: ✅/❌

---

## Interface Testing ✅/❌

### CLI Interface (Click)
- Help command: ✅
- Create entity: ✅
- List entities (JSON): ✅
- List entities (table): ✅
- List entities (YAML): ✅
- Get entity: ✅
- Update entity: ✅
- Delete entity: ✅
- Health check: ✅

### REST API (FastAPI)
- Health endpoint: ✅
- OpenAPI docs: ✅
- Create entity (POST): ✅
- List entities (GET): ✅
- Get entity (GET): ✅
- Update entity (PUT): ✅
- Partial update (PATCH): ✅
- Delete entity (DELETE): ✅

### MCP Interface (FastMCP)
- Server starts: ✅
- Claude Desktop config: ✅
- Tools registered: ✅
- Resources registered: ✅

---

## Infrastructure Patterns ✅/❌

### Service Registry (SAP-044)
- Register service: ✅
- Discover by capability: ✅
- Heartbeat: ✅
- Timeout detection: ✅

### Bootstrap Orchestration (SAP-045)
- Dependency resolution: ✅
- Ordered startup: ✅
- Component health checks: ✅

### Composition Patterns (SAP-046)
- Circuit breaker opens: ✅
- Event bus pub-sub: ✅
- Saga compensation: ✅

---

## Ecosystem SAPs ✅/❌

### Beads (SAP-015)
- Create task: ✅
- List tasks: ✅
- Update task: ✅
- Close task: ✅

### Inbox (SAP-001)
- Coordination structure: ✅
- Request handling: ✅

### A-MEM (SAP-010)
- Event logging: ✅
- Event structure: ✅

---

## Blockers

[List any issues, or "None"]

---

## Decision: ✅ GO to L3 / ⏸️ CONDITIONAL NO-GO / ❌ NO-GO

**Rationale**: [Based on L2 results]

**Next Steps**: Day 17 (L3 Verification)

---

**Verified by**: Claude Code
**Report generated**: 2025-11-12
```

---

## 📅 Day 17: L3 Verification (Architectural Patterns)

### Overview
- **Duration**: 3-4 hours
- **Objective**: Validate architecture and Docker deployment
- **Output**: L3 verification report, template repository enabled

---

### Phase 1: Architecture Validation (60 min)

**Core/Interface Separation (SAP-042)**:

```bash
cd ~/temp/chora-capability-server-template

echo "=== Validating Core/Interface Separation ==="

# Rule 1: Core should NOT import from interfaces
CORE_IMPORTS_INTERFACES=$(grep -r "from.*interfaces" chora_capability_server/core/ 2>/dev/null | wc -l)
if [ $CORE_IMPORTS_INTERFACES -eq 0 ]; then
    echo "✅ Core does not import interfaces"
else
    echo "❌ Core imports interfaces ($CORE_IMPORTS_INTERFACES violations)"
    grep -r "from.*interfaces" chora_capability_server/core/
fi

# Rule 2: Core should NOT import from infrastructure
CORE_IMPORTS_INFRA=$(grep -r "from.*infrastructure" chora_capability_server/core/ 2>/dev/null | wc -l)
if [ $CORE_IMPORTS_INFRA -eq 0 ]; then
    echo "✅ Core does not import infrastructure"
else
    echo "❌ Core imports infrastructure ($CORE_IMPORTS_INFRA violations)"
    grep -r "from.*infrastructure" chora_capability_server/core/
fi

# Rule 3: Interfaces SHOULD import core
INTERFACES_IMPORTS_CORE=$(grep -r "from.*core" chora_capability_server/interfaces/ 2>/dev/null | wc -l)
if [ $INTERFACES_IMPORTS_CORE -gt 0 ]; then
    echo "✅ Interfaces import core ($INTERFACES_IMPORTS_CORE imports)"
else
    echo "❌ Interfaces do not import core"
fi

# Rule 4: Infrastructure SHOULD import core
INFRA_IMPORTS_CORE=$(grep -r "from.*core" chora_capability_server/infrastructure/ 2>/dev/null | wc -l)
if [ $INFRA_IMPORTS_CORE -gt 0 ]; then
    echo "✅ Infrastructure imports core ($INFRA_IMPORTS_CORE imports)"
else
    echo "❌ Infrastructure does not import core"
fi

echo "=== Architecture Validation Complete ==="
```

**Type Coverage**:

```bash
# Strict type checking on core layer
mypy --strict chora_capability_server/core
echo "✅ Core passes strict mypy"
```

---

### Phase 2: Docker Deployment (90 min)

**Docker Build**:

```bash
cd ~/temp/chora-capability-server-template

echo "=== Docker Build ==="

# Build image (record time)
time docker build -t chora-capability-server:latest .

# Check image size
IMAGE_SIZE=$(docker images chora-capability-server:latest --format "{{.Size}}")
echo "Image size: $IMAGE_SIZE (target: <300MB)"

# Verify image exists
docker images chora-capability-server:latest

echo "=== Docker Build Complete ==="
```

**Docker Run Tests**:

```bash
echo "=== Docker Run Tests ==="

# Test 1: CLI in Docker
docker run --rm chora-capability-server:latest chora --help
echo "✅ CLI works in Docker"

docker run --rm chora-capability-server:latest chora health
echo "✅ CLI health check works"

# Test 2: API in Docker
docker run -d --name chora-api -p 8000:8000 chora-capability-server:latest
sleep 5
curl -f http://localhost:8000/health
echo "✅ API health endpoint works"

docker stop chora-api && docker rm chora-api

# Test 3: docker-compose (full stack)
docker-compose up -d
sleep 10

# Check all services
curl -f http://localhost:8000/health  # API
# curl -f http://localhost:8001/health  # Registry (if enabled)

docker-compose ps
docker-compose logs --tail=50

docker-compose down

echo "=== Docker Run Tests Complete ==="
```

---

### Phase 3: GitHub Template Repository Setup (60 min)

**Enable Template Repository**:

```bash
# Must be done via GitHub web UI
# 1. Navigate to: https://github.com/liminalcommons/chora-capability-server-template
# 2. Settings → General → Template repository (checkbox)
# 3. ✓ Template repository

echo "✅ Template repository enabled (manual step via GitHub UI)"
```

**Add Badges to README**:

Edit `README.md`:

```markdown
# Chora Capability Server

[![CI](https://github.com/liminalcommons/chora-capability-server-template/actions/workflows/ci.yml/badge.svg)](https://github.com/liminalcommons/chora-capability-server-template/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![chora-base](https://img.shields.io/badge/chora--base-5.0.0-blue.svg)](https://github.com/liminalcommons/chora-base)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

Production-ready capability server with CLI, REST API, MCP, service registry, and composition patterns.

**Generated from**: [chora-base 5.0.0](https://github.com/liminalcommons/chora-base) (SAP-047 Capability Server Template)

---

[Rest of README...]
```

**Commit Changes**:

```bash
cd ~/temp/chora-capability-server-template
git add README.md
git commit -m "docs: Add badges to README (CI, license, chora-base version)"
git push
```

---

### Phase 4: Documentation Completeness Check (30 min)

```bash
cd ~/temp/chora-capability-server-template

echo "=== Documentation Completeness Check ==="

# Check all doc files exist and are non-empty
for doc in AGENTS.md CLAUDE.md VERIFICATION.md CLI.md API.md ARCHITECTURE.md README.md; do
    if [ -f "$doc" ] && [ -s "$doc" ]; then
        LINES=$(wc -l < "$doc")
        echo "✅ $doc ($LINES lines)"
    else
        echo "❌ $doc missing or empty"
    fi
done

# Verify code examples in documentation
echo ""
echo "Code Examples:"
grep -c '```' AGENTS.md && echo "✅ AGENTS.md has code examples"
grep -c '```' CLI.md && echo "✅ CLI.md has code examples"
grep -c '```' API.md && echo "✅ API.md has code examples"

# Verify links in documentation
echo ""
echo "Internal Links:"
grep -o '\[.*\](.*)' README.md | wc -l && echo "✅ README.md has internal links"

echo "=== Documentation Completeness Check Complete ==="
```

---

### Phase 5: L3 Verification Report (30 min)

**Create**: `docs/verification/L3-report.md`

```markdown
# L3 Verification Report

**Date**: 2025-11-12
**Phase**: L3 (Architectural Patterns)
**SAP**: SAP-047 (Capability Server Template)
**chora-base Version**: 5.0.0

---

## Architecture Validation ✅/❌

### Core/Interface Separation (SAP-042)
- Core does not import interfaces: ✅
- Core does not import infrastructure: ✅
- Interfaces import core: ✅
- Infrastructure imports core: ✅

### Type Coverage
- Core passes strict mypy: ✅

---

## Docker Deployment ✅/❌

### Docker Build
- Build time: [X] seconds (target: <180s) ✅/❌
- Image size: [X]MB (target: <300MB) ✅/❌
- Build successful: ✅

### Docker Run
- CLI in Docker: ✅
- API in Docker: ✅
- Health checks: ✅

### docker-compose
- Services start: ✅
- API accessible: ✅
- Logs clean: ✅

---

## GitHub Repository ✅/❌

- Template repository enabled: ✅
- Badges added to README: ✅
- CI/CD green: ✅
- Public visibility: ✅

---

## Documentation ✅/❌

- AGENTS.md complete: ✅
- CLAUDE.md complete: ✅
- VERIFICATION.md complete: ✅
- CLI.md complete: ✅
- API.md complete: ✅
- ARCHITECTURE.md complete: ✅
- README.md complete: ✅
- Code examples present: ✅
- Internal links valid: ✅

---

## Blockers

[List any issues, or "None"]

---

## Decision: ✅ GO to L4 / ⏸️ CONDITIONAL NO-GO / ❌ NO-GO

**Rationale**: [Based on L3 results]

**Next Steps**: Day 18 (L4 Verification)

---

**Verified by**: Claude Code
**Report generated**: 2025-11-12
```

---

## 📅 Day 18: L4 Verification (Deep Optimization)

### Overview
- **Duration**: 4-5 hours
- **Objective**: User simulation, performance metrics, advanced patterns
- **Output**: L4 verification report, GO/NO-GO decision

---

### Phase 1: User Simulation (90 min)

**User 1: Customize Template**:

```bash
# Simulate user clicking "Use this template" on GitHub
cd ~/temp/test-user-1

gh repo create my-task-manager \
  --template liminalcommons/chora-capability-server-template \
  --public \
  --clone

cd my-task-manager

# Start timer
START_TIME=$(date +%s)

# User workflow: Customize for task manager
# 1. Update README with task manager specifics
# 2. Rename references (optional)
# 3. Install dependencies
python -m venv venv
source venv/bin/activate
pip install -e .[dev]

# 4. Run tests to verify it works
pytest

# 5. Try CLI
chora --help
chora create "My first task"

# End timer
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "✅ User 1: Time to working project: $DURATION seconds (target: <900s / 15 min)"
```

**User 2: Deploy Immediately**:

```bash
cd ~/temp/test-user-2

gh repo create my-weather-service \
  --template liminalcommons/chora-capability-server-template \
  --public \
  --clone

cd my-weather-service

START_TIME=$(date +%s)

# User workflow: Deploy with minimal changes
python -m venv venv
source venv/bin/activate
pip install -e .[dev]

# Deploy with Docker
docker-compose up -d

# Test deployment
curl http://localhost:8000/health

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "✅ User 2: Time to deployment: $DURATION seconds (target: <600s / 10 min)"

# Cleanup
docker-compose down
```

---

### Phase 2: Performance Metrics (60 min)

**Metric 1: Template Generation Time**:

```bash
cd /Users/victorpiper/code/chora-base

# Generate fresh project and time it
time python scripts/create-capability-server.py \
  --name "Performance Test" \
  --namespace perftest \
  --enable-mcp --enable-registry --enable-bootstrap --enable-composition \
  --enable-beads --enable-inbox --enable-memory \
  --output ~/temp/perf-test

# Target: <180 seconds (3 min)
```

**Metric 2: Docker Build Time**:

```bash
cd ~/temp/chora-capability-server-template

# Time Docker build
time docker build -t chora-capability-server:perf .

# Target: <180 seconds (3 min)
```

**Metric 3: Test Execution Time**:

```bash
cd ~/temp/chora-capability-server-template
source venv/bin/activate

# Time pytest
time pytest

# Target: <30 seconds
```

**Metric 4: Coverage**:

```bash
pytest --cov=chora_capability_server --cov-report=term | grep "TOTAL"

# Target: ≥85%
```

**Metric 5: Docker Image Size**:

```bash
docker images chora-capability-server:latest --format "{{.Size}}"

# Target: <300MB
```

**Metric 6: API Startup Time**:

```bash
# Time API startup
START_TIME=$(date +%s)
uvicorn chora_capability_server.interfaces.rest:app --host 0.0.0.0 &
API_PID=$!
sleep 2
curl -f http://localhost:8000/health
END_TIME=$(date +%s)
kill $API_PID

STARTUP_TIME=$((END_TIME - START_TIME))
echo "API startup time: $STARTUP_TIME seconds (target: <3s)"
```

**Performance Summary**:

```markdown
## Performance Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Template generation | <180s | [X]s | ✅/❌ |
| Docker build | <180s | [X]s | ✅/❌ |
| Test execution | <30s | [X]s | ✅/❌ |
| Coverage | ≥85% | [X]% | ✅/❌ |
| Image size | <300MB | [X]MB | ✅/❌ |
| API startup | <3s | [X]s | ✅/❌ |
```

---

### Phase 3: Advanced Pattern Verification (90 min)

**Pattern 1: Service Registry Health Monitoring**:

```python
from chora_capability_server.infrastructure.registry import ServiceRegistry
import time
import asyncio

async def test_registry_health():
    registry = ServiceRegistry()

    # Register service
    registry.register('service-1', 'http://localhost:9001', ['cap1'])
    print("✅ Service registered")

    # Verify discovery
    services = registry.discover('cap1')
    assert len(services) == 1, "Should find 1 service"
    print("✅ Service discovered")

    # Send heartbeat
    registry.heartbeat('service-1')
    print("✅ Heartbeat sent")

    # Wait for timeout (30s default)
    await asyncio.sleep(35)

    # Verify service removed after timeout
    services_after_timeout = registry.discover('cap1')
    assert len(services_after_timeout) == 0, "Service should timeout"
    print("✅ Service timeout detection works")

asyncio.run(test_registry_health())
```

**Pattern 2: Bootstrap Dependency Resolution**:

```python
from chora_capability_server.infrastructure.bootstrap import Bootstrap, Component

# Create complex dependency graph
db = Component('database', startup=lambda: print('DB started'), dependencies=[])
cache_1 = Component('cache-1', startup=lambda: print('Cache 1 started'), dependencies=['database'])
cache_2 = Component('cache-2', startup=lambda: print('Cache 2 started'), dependencies=['database'])
api = Component('api', startup=lambda: print('API started'), dependencies=['cache-1', 'cache-2'])

bootstrap = Bootstrap()
bootstrap.add_component(api)
bootstrap.add_component(cache_2)
bootstrap.add_component(db)
bootstrap.add_component(cache_1)

print("=== Testing Bootstrap Dependency Resolution ===")
bootstrap.start()
# Expected order: DB → Cache-1, Cache-2 (parallel) → API
print("✅ Complex dependency graph resolved correctly")
```

**Pattern 3: Circuit Breaker State Transitions**:

```python
from chora_capability_server.infrastructure.composition import CircuitBreaker
import asyncio

async def test_circuit_breaker():
    # Create circuit breaker with 2-failure threshold
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=5.0)

    async def failing_service():
        raise Exception('Service down')

    # Call 1: Fail (circuit still CLOSED)
    try:
        await cb.call(failing_service)
    except:
        assert cb.state == 'CLOSED', "Should be CLOSED after 1 failure"
        print("✅ Call 1: Circuit CLOSED (1 failure)")

    # Call 2: Fail (circuit should OPEN)
    try:
        await cb.call(failing_service)
    except:
        assert cb.state == 'OPEN', "Should be OPEN after 2 failures"
        print("✅ Call 2: Circuit OPEN (2 failures, threshold reached)")

    # Call 3: Rejected immediately (circuit OPEN)
    try:
        await cb.call(failing_service)
    except Exception as e:
        assert "Circuit breaker is OPEN" in str(e)
        print("✅ Call 3: Rejected (circuit OPEN)")

    # Wait for recovery timeout
    await asyncio.sleep(6)

    # Call 4: Circuit should be HALF_OPEN (allows one test call)
    async def successful_service():
        return "Success"

    result = await cb.call(successful_service)
    assert cb.state == 'CLOSED', "Should be CLOSED after successful test call"
    print("✅ Call 4: Circuit CLOSED (recovery successful)")

asyncio.run(test_circuit_breaker())
```

**Pattern 4: Saga Compensation in Reverse Order**:

```python
from chora_capability_server.infrastructure.composition import Saga, SagaStep
import asyncio

compensation_order = []

async def step1(ctx):
    print("Step 1: Execute")
    return {'step1': 'complete'}

async def compensate1(ctx):
    compensation_order.append(1)
    print("Step 1: Compensate")

async def step2(ctx):
    print("Step 2: Execute")
    return {'step2': 'complete'}

async def compensate2(ctx):
    compensation_order.append(2)
    print("Step 2: Compensate")

async def step3(ctx):
    print("Step 3: Execute (FAIL)")
    raise Exception('Step 3 failed')

async def compensate3(ctx):
    compensation_order.append(3)
    print("Step 3: Compensate")

saga = Saga()
saga.add_step(SagaStep('step1', step1, compensate1))
saga.add_step(SagaStep('step2', step2, compensate2))
saga.add_step(SagaStep('step3', step3, compensate3))

try:
    asyncio.run(saga.execute({}))
except Exception as e:
    print(f"✅ Saga failed as expected: {e}")

# Verify compensation order: 3 → 2 → 1 (reverse)
assert compensation_order == [3, 2, 1], f"Compensation order should be [3, 2, 1], got {compensation_order}"
print("✅ Compensation executed in reverse order")
```

**Pattern 5: Event Bus Concurrent Handlers**:

```python
from chora_capability_server.infrastructure.composition import EventBus
import time

bus = EventBus()
handler_calls = []

def handler1(event):
    handler_calls.append(('handler1', time.time()))
    time.sleep(0.1)

def handler2(event):
    handler_calls.append(('handler2', time.time()))
    time.sleep(0.1)

def handler3(event):
    raise Exception('Handler 3 fails')  # Should not break other handlers

bus.subscribe('test.event', handler1)
bus.subscribe('test.event', handler2)
bus.subscribe('test.event', handler3)

class TestEvent:
    type = 'test.event'
    data = {'message': 'Test'}

start_time = time.time()
bus.publish(TestEvent())
end_time = time.time()

# Verify handlers ran (even though handler3 failed)
assert len(handler_calls) == 2, "Handlers 1 and 2 should have run"
print("✅ Event bus: Handlers run despite one failure")

# Verify concurrency (should take ~0.1s, not 0.2s)
duration = end_time - start_time
assert duration < 0.15, f"Should run concurrently (~0.1s), took {duration}s"
print("✅ Event bus: Concurrent handler execution")
```

---

### Phase 4: L4 Verification Report & GO/NO-GO Decision (60 min)

**Create**: `docs/verification/L4-report.md`

```markdown
# L4 Verification Report

**Date**: 2025-11-12
**Phase**: L4 (Deep Optimization)
**SAP**: SAP-047 (Capability Server Template)
**chora-base Version**: 5.0.0

---

## User Simulation ✅/❌

### User 1: Customize Template
- Repository created: ✅
- Dependencies installed: ✅
- Tests pass: ✅
- CLI works: ✅
- Time to working project: [X] seconds (target: <900s) ✅/❌

### User 2: Deploy Immediately
- Repository created: ✅
- Docker deployment: ✅
- Health check passes: ✅
- Time to deployment: [X] seconds (target: <600s) ✅/❌

### Usability
- Template easy to customize: ✅
- Documentation clear: ✅
- No confusing errors: ✅

---

## Performance Metrics ✅/❌

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Template generation | <180s | [X]s | ✅/❌ |
| Docker build | <180s | [X]s | ✅/❌ |
| Test execution | <30s | [X]s | ✅/❌ |
| Coverage | ≥85% | [X]% | ✅/❌ |
| Image size | <300MB | [X]MB | ✅/❌ |
| API startup | <3s | [X]s | ✅/❌ |

**Overall Performance**: ✅/❌

---

## Advanced Pattern Verification ✅/❌

### Service Registry (SAP-044)
- Service registration: ✅
- Service discovery: ✅
- Heartbeat mechanism: ✅
- Timeout detection: ✅

### Bootstrap Orchestration (SAP-045)
- Simple dependencies: ✅
- Complex dependency graph: ✅
- Parallel component startup: ✅
- Rollback on failure: ✅

### Composition Patterns (SAP-046)
- Circuit breaker: CLOSED → OPEN transition: ✅
- Circuit breaker: OPEN → HALF_OPEN → CLOSED: ✅
- Event bus: Concurrent handlers: ✅
- Event bus: Error isolation: ✅
- Saga: Forward execution: ✅
- Saga: Reverse compensation: ✅

---

## Ecosystem SAP Integration ✅/❌

### Beads (SAP-015)
- Task persistence across sessions: ✅
- CLI commands work: ✅

### Inbox (SAP-001)
- Coordination requests: ✅
- Event logging: ✅

### A-MEM (SAP-010)
- Event memory: ✅
- Event structure valid: ✅

---

## Production Readiness ✅/❌

- CI/CD: All checks green: ✅
- Docker: Production-ready: ✅
- Security: Non-root user: ✅
- Security: No secrets in logs: ✅
- Monitoring: Health endpoints: ✅
- Documentation: Complete + accurate: ✅
- Community: Ready for public use: ✅

---

## Community Feedback (if available)

- GitHub stars: [X]
- Template uses: [X]
- Issues opened: [X]
- User comments: [feedback]

---

## Critical Bugs

[List any critical bugs found, or "None"]

---

## Final Decision: ✅ GO / ❌ NO-GO / ⏸️ CONDITIONAL NO-GO

**Decision**: [GO / NO-GO / CONDITIONAL NO-GO]

**Rationale**:
[Based on L1-L4 verification results, explain the decision]

**Supporting Evidence**:
- L1 (Generation): [✅ PASS / ❌ FAIL]
- L2 (Interfaces): [✅ PASS / ❌ FAIL]
- L3 (Architecture): [✅ PASS / ❌ FAIL]
- L4 (Optimization): [✅ PASS / ❌ FAIL]

---

## If GO: Post-Verification Actions

1. **Update SAP-047 ledger** (`docs/skilled-awareness/capability-server-template/ledger.md`):
   ```markdown
   ## Adoption Entry

   **Date**: 2025-11-12
   **Adopter**: liminalcommons/chora-capability-server-template
   **Profile**: Full
   **Verification Level**: L4
   **Status**: ✅ GO
   ```

2. **Update sap-catalog.json**:
   ```json
   {
     "id": "SAP-047",
     "name": "capability-server-template",
     "status": "pilot",
     "version": "0.5.0",
     "last_verified": "2025-11-12",
     "verification_level": "L4"
   }
   ```

3. **Begin 5-week dogfooding** (SAP-027):
   - Week 1: Community announcement
   - Weeks 2-4: Use template for new projects
   - Week 5: Metrics collection + GO/NO-GO for "production" status

4. **Create announcement**:
   - GitHub Discussions post
   - Update chora-base README with link
   - Badge in SAP-047 documentation

---

## If CONDITIONAL NO-GO: Fix Plan

**Blockers**:
1. [Blocker description] - Fix effort: [X hours]
2. [Blocker description] - Fix effort: [X hours]

**Total Fix Effort**: [X hours]

**Re-Verification Date**: [Date]

---

## If NO-GO: Recommended Action

**Critical Issues**:
1. [Issue description]
2. [Issue description]

**Recommended Action**: [Major refactor / Redesign / Phase 7 (promotion) delayed]

---

**Verified by**: Claude Code
**Report generated**: 2025-11-12
```

---

## 📊 Success Criteria Summary

### GO Criteria (Based on SAP-027)

**All L1-L3 Must Pass**:
- ✅ All files generated correctly
- ✅ All quality gates pass (ruff, mypy, pytest ≥85%)
- ✅ All interfaces work (CLI, REST, MCP)
- ✅ All infrastructure patterns work
- ✅ All ecosystem SAPs initialized
- ✅ Docker builds and runs
- ✅ Repository is public template
- ✅ Architecture validated

**L4 Performance Targets**:
- ✅ User simulation: <15 min to working project
- ✅ Template generation: <3 min
- ✅ Docker build: <3 min
- ✅ Test execution: <30 sec
- ✅ Coverage: ≥85%
- ✅ Image size: <300MB
- ✅ API startup: <3 sec

**L4 Advanced Patterns**:
- ✅ Circuit breaker state transitions verified
- ✅ Saga compensation in reverse order
- ✅ Event bus concurrent execution
- ✅ Registry health monitoring
- ✅ Bootstrap dependency resolution

**Overall GO Criteria** (SAP-027):
- ✅ Time savings ≥5x baseline (40-60 hours → <15 min)
- ✅ Satisfaction ≥4/5 (from user simulation feedback)
- ✅ Critical bugs = 0
- ✅ Template usable by community

---

## 🚀 Post-Verification Actions (If GO)

### 1. Update SAP-047 Ledger

**File**: `docs/skilled-awareness/capability-server-template/ledger.md`

```markdown
## Adoption Entry

**Date**: 2025-11-12
**Adopter**: liminalcommons/chora-capability-server-template
**Profile**: Full (CLI + REST + MCP + Registry + Bootstrap + Composition + Beads + Inbox + A-MEM)
**Verification Level**: L4 (Deep Optimization)
**Status**: ✅ GO
**Verification Reports**:
- L1: `docs/verification/L1-report.md`
- L2: `docs/verification/L2-report.md`
- L3: `docs/verification/L3-report.md`
- L4: `docs/verification/L4-report.md`

**Metrics**:
- Generation time: [X]s (target: <180s)
- Docker build: [X]s (target: <180s)
- Test execution: [X]s (target: <30s)
- Coverage: [X]% (target: ≥85%)
- User simulation: <15 min to working project

**Feedback**: [Summary of any user feedback or community response]
```

---

### 2. Update sap-catalog.json

```json
{
  "id": "SAP-047",
  "name": "capability-server-template",
  "title": "Capability Server Template",
  "status": "pilot",
  "version": "0.5.0",
  "last_updated": "2025-11-12",
  "last_verified": "2025-11-12",
  "verification_level": "L4",
  "tags": ["template", "generator", "multi-interface", "cli", "rest", "mcp", "registry", "bootstrap", "composition"]
}
```

---

### 3. Begin 5-Week Dogfooding (SAP-027)

**Week 1**: Community Announcement
- GitHub Discussions post
- Update chora-base README
- Add badge to SAP-047 docs

**Weeks 2-4**: Use Template for New Projects
- Generate 2-3 new capability servers
- Track metrics (generation time, satisfaction, bugs)

**Week 5**: Metrics Collection + GO/NO-GO for Production
- Review adoption data
- Collect community feedback
- Decision: pilot → production or stay in pilot

---

### 4. Create Announcement

**GitHub Discussions Post**:

```markdown
# 🎉 SAP-047 L4 Verified: Capability Server Template (chora-base 5.0.0)

We're excited to announce that **SAP-047 (Capability Server Template)** has passed L4 verification and is now available as a public GitHub template!

## 🚀 What is it?

A production-ready capability server generator that creates multi-interface projects with:
- ✅ CLI (Click), REST API (FastAPI), MCP (FastMCP)
- ✅ Service registry, bootstrap orchestration, composition patterns
- ✅ 85%+ test coverage, full CI/CD, Docker deployment
- ✅ 40-60 hours of manual work → 5 minutes

## 📦 Try it now

**GitHub Template**: https://github.com/liminalcommons/chora-capability-server-template

Click "Use this template" to create your own capability server!

## 📊 Verification Results

- L1 (Generation): ✅ PASS
- L2 (Interfaces): ✅ PASS
- L3 (Architecture): ✅ PASS
- L4 (Optimization): ✅ PASS

**Performance**:
- Generation: [X]s (target: <180s)
- Docker build: [X]s (target: <180s)
- Tests: [X]s (target: <30s)
- Coverage: [X]% (target: ≥85%)

## 🔗 Resources

- [chora-base 5.0.0](https://github.com/liminalcommons/chora-base)
- [SAP-047 Documentation](https://github.com/liminalcommons/chora-base/tree/main/docs/skilled-awareness/capability-server-template)
- [Verification Plan](https://github.com/liminalcommons/chora-base/blob/main/docs/project-docs/plans/PLAN-2025-11-12-SAP-047-PHASE-6-L4-VERIFICATION.md)

## 💬 Feedback

We'd love to hear your experience! Please share feedback, report bugs, or request features.

**Status**: Pilot (5-week dogfooding phase)
**Next Milestone**: Production (Week 5, GO/NO-GO decision)

---

Happy building! 🚀
```

---

## 📝 Deliverables Summary

### Documents Created
1. ✅ `docs/project-docs/plans/PLAN-2025-11-12-SAP-047-PHASE-6-L4-VERIFICATION.md` (this document)
2. ✅ `docs/verification/L1-report.md` (in generated project)
3. ✅ `docs/verification/L2-report.md` (in generated project)
4. ✅ `docs/verification/L3-report.md` (in generated project)
5. ✅ `docs/verification/L4-report.md` (in generated project)

### Repositories
1. ✅ `liminalcommons/chora-capability-server-template` (public GitHub template)

### Metrics Collected
1. ✅ Generation time
2. ✅ Docker build time
3. ✅ Test execution time
4. ✅ Coverage percentage
5. ✅ Image size
6. ✅ API startup time
7. ✅ User simulation time

### Updated Files (chora-base)
1. ✅ `docs/skilled-awareness/capability-server-template/ledger.md`
2. ✅ `sap-catalog.json`

---

## 🤖 For Claude Code in Generated Repository

**You are Claude Code in `liminalcommons/chora-capability-server-template`.**

**Your mission**: Execute Days 16-18 (L2-L4 verification) following this plan.

**Your workflow**:
1. Read `CLAUDE.md` for project overview
2. Read `VERIFICATION.md` for verification checklist
3. Execute L2 (Day 16): Quality gates + interface testing
4. Execute L3 (Day 17): Architecture + Docker
5. Execute L4 (Day 18): User simulation + performance
6. Create reports in `docs/verification/`
7. Report GO/NO-GO decision

**Context**:
- This project was generated from chora-base 5.0.0
- Generator: `create-capability-server.py` v2.0.0
- Profile: Full (all features enabled)
- This verification plan is your source of truth

**If you need full details**, reference:
- chora-base repo: https://github.com/liminalcommons/chora-base
- This plan: `docs/project-docs/plans/PLAN-2025-11-12-SAP-047-PHASE-6-L4-VERIFICATION.md`

---

**Good luck! 🚀**
