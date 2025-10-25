# Developer Guide for Contributors

**Purpose:** Guide for contributing to mcp-orchestration (code, docs, tests, workflows).

**Parent:** See [../AGENTS.md](../AGENTS.md) for project overview and architecture.

---

## Quick Reference

- **Setup:** `./scripts/setup.sh` or see [CONTRIBUTING.md](CONTRIBUTING.md)
- **Discover tasks:** `just --list`
- **Run tests:** `just test`
- **Pre-merge checks:** `just pre-merge` (required before PR)
- **Code style:** PEP 8, Black formatter, Ruff linter
- **Test coverage:** ≥85% (≥100% for crypto module)
- **Troubleshooting:** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## Directory Structure

```
dev-docs/
├── AGENTS.md           # This file - developer guide
├── README.md           # Directory overview
├── CONTRIBUTING.md     # Contribution guidelines
├── DEVELOPMENT.md      # Developer setup and architecture [future]
├── TROUBLESHOOTING.md  # Common issues and solutions [future]
├── vision/             # Strategic vision documents
│   └── AGENTS.md       # Vision documents guide
├── research/           # Research documents
└── workflows/          # Development workflows [future]
```

---

## Development Workflow (DDD → BDD → TDD)

### Overview

**mcp-orchestration follows a documentation-driven development workflow:**

1. **DDD (Documentation-Driven Development)** - Write docs first
2. **BDD (Behavior-Driven Development)** - Define behavior with tests
3. **TDD (Test-Driven Development)** - Write failing tests, then implement

**Benefits:**
- Clear requirements before coding
- Testable specifications
- Documentation always up-to-date
- Reduced rework

### Workflow Steps

**Step 1: Document (DDD)**

Before writing code, document the feature:

```markdown
# In relevant AGENTS.md or user docs

## New Feature: [Feature Name]

**Purpose:** [What problem does this solve]

**Usage:**
```python
from mcp_orchestrator import new_feature

result = new_feature(param="value")
# Returns: {...}
```

**Input:** [Parameter description]
**Output:** [Return value description]
**Errors:** [Exception cases]
```

**Step 2: Define Behavior (BDD)**

Write behavioral tests describing what the feature should do:

```python
# tests/integration/test_new_feature.py
import pytest
from mcp_orchestrator import new_feature

def test_new_feature_returns_expected_result():
    """Feature should return correct result for valid input."""
    result = new_feature(param="value")

    assert result["success"] is True
    assert result["data"] == "expected value"

def test_new_feature_raises_on_invalid_input():
    """Feature should raise ValueError for invalid input."""
    with pytest.raises(ValueError, match="param must be non-empty"):
        new_feature(param="")

def test_new_feature_integrates_with_existing_system():
    """Feature should work with existing orchestrator components."""
    # Setup existing system state
    existing_component = setup_existing()

    # Call new feature
    result = new_feature(param="value")

    # Verify integration
    assert existing_component.is_compatible(result)
```

**Step 3: Implement (TDD)**

Write code to make tests pass:

```python
# src/mcp_orchestrator/new_feature.py
from mcp_orchestrator.memory import emit_event, TraceContext

def new_feature(param: str) -> dict:
    """Implement the new feature.

    Args:
        param: Description of parameter

    Returns:
        Dictionary with success status and data

    Raises:
        ValueError: If param is empty or invalid
    """
    # Validate input
    if not param:
        raise ValueError("param must be non-empty")

    # Emit start event
    with TraceContext() as trace_id:
        emit_event("new_feature.started", trace_id=trace_id,
                   status="pending", metadata={"param": param})

        try:
            # Implement feature logic
            data = _process(param)

            # Emit success event
            emit_event("new_feature.completed", trace_id=trace_id,
                       status="success", metadata={"data": data})

            return {"success": True, "data": data}

        except Exception as e:
            # Emit failure event
            emit_event("new_feature.failed", trace_id=trace_id,
                       status="failure", metadata={"error": str(e)})
            raise

def _process(param: str) -> str:
    """Private helper for processing logic."""
    return f"processed: {param}"
```

**Step 4: Verify**

Run tests and checks:

```bash
# Run tests
just test

# Run all pre-merge checks
just pre-merge
```

**Step 5: Document Learnings**

Create knowledge notes for future reference:

```python
from mcp_orchestrator.memory import create_note

create_note(
    content="Implementation of new_feature required X pattern because Y",
    tags=["new-feature", "implementation", "lesson-learned"],
    references=["src/mcp_orchestrator/new_feature.py"]
)
```

---

## Code Style Guide

### Python Style (PEP 8)

**Follow PEP 8 with these project conventions:**

**Naming:**
```python
# Modules: snake_case
import module_name

# Classes: PascalCase
class ConfigOrchestrator:
    pass

# Functions/variables: snake_case
def get_config(client_id: str) -> dict:
    artifact_id = resolve_artifact_id(client_id)
    return artifact_id

# Constants: UPPER_SNAKE_CASE
DEFAULT_STORAGE_PATH = "~/.mcp-orchestration"
```

**Type Hints:**
```python
# Always use type hints for function signatures
def sign_artifact(artifact: dict, private_key: bytes) -> dict:
    """Sign artifact with private key.

    Args:
        artifact: Artifact dictionary to sign
        private_key: Ed25519 private key bytes

    Returns:
        Artifact with signature added
    """
    signature = _generate_signature(artifact, private_key)
    return {**artifact, "signature": signature}
```

**Docstrings (Google Style):**
```python
def complex_function(param1: str, param2: int) -> tuple[bool, str]:
    """One-line summary of function.

    Longer description if needed. Explain the "why" not just the "what".
    Multiple paragraphs are fine.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter, can be
            multi-line if needed

    Returns:
        Tuple of (success_status, result_message)

    Raises:
        ValueError: If param1 is empty
        SecurityError: If signature verification fails

    Example:
        >>> success, msg = complex_function("test", 42)
        >>> assert success is True
    """
    pass
```

**Imports:**
```python
# Standard library
import os
import sys
from pathlib import Path

# Third-party
import pytest
from cryptography.hazmat.primitives import serialization

# Local modules
from mcp_orchestrator.storage import get_artifact
from mcp_orchestrator.crypto import sign_artifact
```

### Formatting

**Use Black and Ruff:**

```bash
# Format code
just format

# Or manually
black src/mcp_orchestration tests
ruff check --fix src/mcp_orchestration tests
```

**Black settings (in pyproject.toml):**
- Line length: 100
- String quotes: Double quotes
- Python version: 3.11+

---

## Testing Requirements

### Coverage Targets

**Project-wide:** ≥85% coverage
**Crypto module:** 100% coverage (security-critical)

### Test Structure

```
tests/
├── unit/                 # Unit tests (isolated, fast)
│   ├── test_crypto.py
│   ├── test_storage.py
│   └── test_registry.py
├── integration/          # Integration tests (multiple modules)
│   ├── test_config_flow.py
│   └── test_mcp_server.py
└── super_tests/          # System-level tests (end-to-end)
    └── test_wave1_scenarios.py
```

### Unit Tests

**Test individual functions/classes in isolation:**

```python
# tests/unit/test_crypto.py
import pytest
from mcp_orchestrator.crypto import sign_artifact, verify_signature

def test_sign_artifact_adds_signature():
    """sign_artifact should add signature field to artifact."""
    artifact = {"payload": {"key": "value"}}
    private_key = load_test_private_key()

    signed = sign_artifact(artifact, private_key)

    assert "signature" in signed
    assert signed["signature"]["algorithm"] == "ed25519"
    assert len(signed["signature"]["value"]) > 0

def test_verify_signature_accepts_valid():
    """verify_signature should return True for valid signature."""
    artifact = create_signed_test_artifact()
    public_key = load_test_public_key()

    is_valid = verify_signature(artifact, public_key)

    assert is_valid is True

def test_verify_signature_rejects_tampered():
    """verify_signature should return False for tampered artifact."""
    artifact = create_signed_test_artifact()
    artifact["payload"]["key"] = "tampered"  # Modify payload
    public_key = load_test_public_key()

    is_valid = verify_signature(artifact, public_key)

    assert is_valid is False
```

### Integration Tests

**Test multiple modules working together:**

```python
# tests/integration/test_config_flow.py
import pytest
from mcp_orchestrator.registry import get_profile
from mcp_orchestrator.storage import get_artifact
from mcp_orchestrator.crypto import verify_signature

def test_config_retrieval_flow():
    """Full config retrieval should get, verify, and return artifact."""
    # 1. Get profile (registry)
    profile = get_profile("claude-desktop", "default")
    artifact_id = profile["artifact_id"]

    # 2. Retrieve artifact (storage)
    artifact = get_artifact(artifact_id)

    # 3. Verify signature (crypto)
    is_valid = verify_signature(artifact)
    assert is_valid is True

    # 4. Validate structure
    assert artifact["client_id"] == "claude-desktop"
    assert "payload" in artifact
    assert "signature" in artifact
```

### Super-Tests

**End-to-end system validation (Section 2.2 of research PDF):**

```python
# tests/super_tests/test_wave1_scenarios.py
import pytest
from mcp_orchestrator.mcp.server import create_server

@pytest.mark.super_test
def test_user_discovers_and_retrieves_config():
    """
    USER STORY: As a user, I want to discover available clients,
    list their profiles, and retrieve a signed config.

    SCENARIO: Happy path config retrieval
    """
    server = create_server()

    # 1. User discovers clients
    clients_result = await server.call_tool("list_clients", {})
    assert clients_result["count"] >= 2
    claude_desktop = [c for c in clients_result["clients"]
                      if c["client_id"] == "claude-desktop"][0]

    # 2. User lists profiles for Claude Desktop
    profiles_result = await server.call_tool("list_profiles", {
        "client_id": "claude-desktop"
    })
    assert "default" in [p["profile_id"] for p in profiles_result["profiles"]]

    # 3. User retrieves config
    config_result = await server.call_tool("get_config", {
        "client_id": "claude-desktop",
        "profile_id": "default"
    })

    # 4. Validate config structure and signature
    assert config_result["artifact_id"] is not None
    assert config_result["payload"] is not None
    assert config_result["signature"]["algorithm"] == "ed25519"

    # 5. User can use config immediately (valid JSON)
    payload = config_result["payload"]
    assert isinstance(payload, dict)
    assert "mcpServers" in payload
```

### Running Tests

```bash
# All tests
just test

# Specific test file
pytest tests/unit/test_crypto.py

# Specific test
pytest tests/unit/test_crypto.py::test_sign_artifact_adds_signature

# With coverage
just test-coverage

# Super-tests only
pytest -m super_test

# Watch mode (re-run on file changes)
pytest-watch
```

---

## Pull Request Process

### Before Creating PR

**1. Ensure all checks pass:**
```bash
just pre-merge
```

This runs:
- Linting (`ruff check`)
- Type checking (`mypy`)
- Formatting check (`black --check`)
- Full test suite
- Coverage check (≥85%)

**2. Update documentation:**
- Update relevant AGENTS.md files
- Update user docs if user-facing changes
- Add examples to docstrings

**3. Create or update tests:**
- Unit tests for new functions
- Integration tests for new workflows
- Super-tests for new user scenarios

**4. Check wave alignment:**
- Read [project-docs/WAVE_1X_PLAN.md](../project-docs/WAVE_1X_PLAN.md)
- Ensure PR contributes to current wave
- Don't implement future wave features

### Creating the PR

**1. Create feature branch:**
```bash
git checkout -b feature/your-feature-name
```

**2. Commit changes:**
```bash
git add .
git commit -m "feat: add your feature

- Implemented X
- Added tests for Y
- Updated docs for Z"
```

**Commit message format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `chore:` - Build/tooling changes

**3. Push and create PR:**
```bash
git push origin feature/your-feature-name
```

Then create PR on GitHub.

**4. PR template:**
```markdown
## Description
[Clear description of what this PR does]

## Wave
[Which wave does this contribute to? Wave 1.1, Wave 1.2, etc.]

## Changes
- [ ] Feature 1 implemented
- [ ] Tests added
- [ ] Documentation updated

## Testing
[How to test these changes]

## Checklist
- [ ] `just pre-merge` passes
- [ ] Tests added/updated
- [ ] AGENTS.md files updated
- [ ] User docs updated (if user-facing)
- [ ] Wave alignment verified

## Screenshots/Examples
[If applicable, show before/after or usage examples]
```

### PR Review Process

**Maintainers will review for:**
1. **Code quality** - Style, readability, maintainability
2. **Tests** - Coverage, edge cases, integration
3. **Documentation** - AGENTS.md, docstrings, user docs
4. **Wave alignment** - Fits current wave scope
5. **Performance** - No significant regressions

**Review feedback:**
- Address all review comments
- Push new commits (don't force-push during review)
- Re-request review when ready

**Approval and merge:**
- 1 approval required from maintainer
- CI must pass
- Squash and merge (default)

---

## Issue Guidelines

### Reporting Bugs

**Use bug report template:**

```markdown
**Bug Description:**
[Clear, concise description of the bug]

**Steps to Reproduce:**
1. Run command X
2. Observe Y
3. See error Z

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happened]

**Environment:**
- OS: [macOS, Windows, Linux]
- Python version: [3.11, 3.12, etc.]
- mcp-orchestration version: [0.1.0, etc.]

**Logs/Screenshots:**
[Paste logs or attach screenshots]

**Additional Context:**
[Any other relevant information]
```

### Feature Requests

**Use feature request template:**

```markdown
**Feature Description:**
[Clear description of the proposed feature]

**Problem Solved:**
[What user problem does this solve?]

**Proposed Solution:**
[How should this work?]

**Wave Alignment:**
[Which wave should this be in? Why?]

**Alternatives Considered:**
[Other approaches you've thought about]

**Additional Context:**
[Mockups, examples, references]
```

### Asking Questions

**For questions, use GitHub Discussions instead of issues.**

---

## Architecture Overview

**See [../AGENTS.md](../AGENTS.md) for full architecture details.**

### Key Principles

1. **Layered Architecture** - Storage → Crypto → Registry → MCP
2. **Immutable Artifacts** - Content-addressable storage, no mutations
3. **Cryptographic Verification** - Ed25519 signatures for integrity
4. **Protocol Compliance** - MCP specification 2024-11-05
5. **Memory Integration** - A-MEM patterns for cross-session learning

### Module Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                     MCP Layer                                │
│   (src/mcp_orchestrator/mcp/)                               │
│   - MCP tools                                                │
│   - MCP resources                                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐   ┌──────────┐
    │ Registry │    │   Diff   │   │  Crypto  │
    │ (clients)│    │ (compare)│   │  (sign)  │
    └────┬─────┘    └────┬─────┘   └────┬─────┘
         └──────▼───────────────▼──────┘
         ┌───────────────────────────┐
         │     Storage Layer         │
         │  (Content-Addressable)    │
         └───────────────────────────┘
```

**When adding features:**
- Respect layer boundaries (don't bypass layers)
- Keep modules loosely coupled
- Use dependency injection for testability

---

## Memory Integration (A-MEM)

**mcp-orchestration uses A-MEM patterns from research PDF Section 4.**

### Emit Events

**Emit events for important operations:**

```python
from mcp_orchestrator.memory import emit_event, TraceContext

with TraceContext() as trace_id:
    emit_event(
        "module.operation_started",
        trace_id=trace_id,
        status="pending",
        metadata={"param": value}
    )

    try:
        result = perform_operation()
        emit_event(
            "module.operation_completed",
            trace_id=trace_id,
            status="success",
            metadata={"result": result}
        )
    except Exception as e:
        emit_event(
            "module.operation_failed",
            trace_id=trace_id,
            status="failure",
            metadata={"error": str(e), "error_type": type(e).__name__}
        )
        raise
```

### Create Knowledge Notes

**Document learnings for future reference:**

```python
from mcp_orchestrator.memory import create_note

create_note(
    content="Discovered that X pattern works better than Y because Z",
    tags=["performance", "optimization", "lesson-learned"],
    references=["src/mcp_orchestrator/module.py:123"]
)
```

### Query Past Events

**Learn from history:**

```python
from mcp_orchestrator.memory import query_events

# Find all failures in last 24 hours
recent_failures = query_events(
    status="failure",
    since_hours=24
)

# Analyze patterns
for event in recent_failures:
    print(f"Failed: {event['event_type']} - {event['metadata']['error']}")
```

---

## Related Documentation

- **[../AGENTS.md](../AGENTS.md)** - Project overview
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Full contribution guidelines
- **[../project-docs/AGENTS.md](../project-docs/AGENTS.md)** - Wave planning
- **[vision/AGENTS.md](vision/AGENTS.md)** - Vision documents
- **[../scripts/AGENTS.md](../scripts/AGENTS.md)** - Automation scripts
- **[../tests/AGENTS.md](../tests/AGENTS.md)** - Testing guide

---

## Common Tasks for Contributors

### Task 1: Add a New MCP Tool

1. Read [../src/mcp_orchestrator/mcp/AGENTS.md](../src/mcp_orchestrator/mcp/AGENTS.md)
2. Check wave alignment ([../project-docs/WAVE_1X_PLAN.md](../project-docs/WAVE_1X_PLAN.md))
3. Document tool in AGENTS.md (DDD)
4. Write behavioral tests (BDD)
5. Implement tool in [server.py](../src/mcp_orchestrator/mcp/server.py)
6. Add integration tests
7. Update documentation
8. Run `just pre-merge`
9. Create PR

### Task 2: Fix a Bug

1. Reproduce bug with test
2. Write failing test capturing bug
3. Fix bug (make test pass)
4. Verify no regressions (`just test`)
5. Update docs if needed
6. Run `just pre-merge`
7. Create PR with "fix:" prefix

### Task 3: Add New Client Support

1. Read [../src/mcp_orchestrator/registry/AGENTS.md](../src/mcp_orchestrator/registry/AGENTS.md)
2. Define client metadata in `registry/clients.py`
3. Create default profile artifact
4. Register profile in registry
5. Add unit tests
6. Add integration tests
7. Update user docs
8. Run `just pre-merge`
9. Create PR

### Task 4: Improve Documentation

1. Identify documentation gap
2. Read relevant AGENTS.md for context
3. Update documentation (AGENTS.md, user-docs, docstrings)
4. Verify examples work (`pytest --doctest-modules`)
5. Check links not broken
6. Run `just pre-merge`
7. Create PR with "docs:" prefix

### Task 5: Optimize Performance

1. Identify performance bottleneck
2. Write benchmark test
3. Implement optimization
4. Verify benchmark improvement
5. Check no correctness regressions
6. Document optimization in knowledge note
7. Run `just pre-merge`
8. Create PR with "perf:" prefix

---

## Troubleshooting

**For common development issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) (when created).**

### Quick Fixes

**Tests failing:**
```bash
# Clean and reinstall
./scripts/venv-clean.sh
./scripts/venv-create.sh
pip install -e ".[dev]"
just test
```

**Linting errors:**
```bash
# Auto-fix most issues
just lint-fix
```

**Type errors:**
```bash
# Check what mypy sees
just typecheck
```

**Pre-commit hook issues:**
```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install
```

---

**End of Developer Guide**

For questions not covered here, see [CONTRIBUTING.md](CONTRIBUTING.md) or ask in GitHub Discussions.
