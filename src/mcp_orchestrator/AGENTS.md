# Core Orchestrator Module Guide

**Purpose:** Guide for working with the core mcp_orchestrator module.

**Parent:** See [../../AGENTS.md](../../AGENTS.md) for project overview.

---

## Quick Reference

- **Module structure:** See "Directory Structure" below
- **Add submodule:** Create new directory, add AGENTS.md
- **Testing:** `pytest tests/unit/test_orchestrator.py`
- **Architecture overview:** See "Module Overview"

---

## Module Overview

**Path:** `src/mcp_orchestrator/`

**Responsibility:** Orchestrate MCP client configuration lifecycle - retrieval, validation, signing, diff, and distribution.

**Architecture Pattern:** Layered orchestration with clear separation of concerns.

### Directory Structure

```
src/mcp_orchestrator/
├── __init__.py           # Package metadata, version (__version__)
├── cli.py                # CLI entry point (mcp-orchestration)
├── cli_init.py           # Initialization command (init-configs)
├── telemetry.py          # Telemetry, logging, error handling
├── crypto/               # Ed25519 signing/verification
│   └── AGENTS.md
├── storage/              # Content-addressable storage
│   └── AGENTS.md
├── registry/             # Client/server registry
│   └── AGENTS.md
├── diff/                 # Configuration diff engine
│   └── AGENTS.md
├── mcp/                  # MCP server implementation
│   └── AGENTS.md
└── servers/              # MCP server registry (Wave 1.1)
    └── AGENTS.md
```

---

## Submodule Interaction Flow

### Config Retrieval Flow (get_config tool)

```
1. MCP Server (mcp/)
   └─> Receives tool call: get_config(client_id="claude-desktop", profile_id="default")

2. Registry (registry/)
   └─> Resolves: client_id + profile_id → artifact_id
   └─> Returns: artifact_id = "aabbccddee..."

3. Storage (storage/)
   └─> Retrieves: artifact by content hash (SHA-256)
   └─> Returns: artifact payload + metadata

4. Crypto (crypto/)
   └─> Verifies: Ed25519 signature
   └─> Validates: artifact_id matches SHA-256(payload)

5. MCP Server (mcp/)
   └─> Returns: Validated artifact to client
```

### Diff Flow (diff_config tool)

```
1. MCP Server (mcp/)
   └─> Receives: diff_config(client_id, profile_id, local_payload)

2. Registry (registry/)
   └─> Resolves: client_id + profile_id → canonical artifact_id

3. Storage (storage/)
   └─> Retrieves: canonical artifact

4. Diff Engine (diff/)
   └─> Compares: local_payload vs. canonical_payload
   └─> Classifies: changes (added/removed/modified)
   └─> Categorizes: semantic impact (breaking/compatible/cosmetic)

5. MCP Server (mcp/)
   └─> Returns: DiffResult (status, changes, recommendation)
```

### Initialization Flow (mcp-orchestration init-configs)

```
1. CLI Init (cli_init.py)
   └─> Generates: Ed25519 keypair

2. Crypto (crypto/)
   └─> Stores: keys at ~/.mcp-orchestration/keys/
   └─> Sets: permissions 0600 (private key)

3. Registry (registry/)
   └─> Loads: sample configs for supported clients

4. Storage (storage/)
   └─> Saves: signed artifacts to content-addressable storage
   └─> Computes: artifact_id = SHA-256(payload)

5. CLI Init (cli_init.py)
   └─> Displays: success message, next steps
```

---

## Adding New Submodules

**When to add:** New capability layer (e.g., validation engine, policy engine in Wave 2).

**Steps:**

1. **Create directory:** `src/mcp_orchestrator/[module]/`
2. **Add `__init__.py`** with public API:
   ```python
   """[Module] - [Brief description]."""
   __all__ = ["function_a", "function_b", "ClassC"]

   from .module_impl import function_a, function_b, ClassC
   ```

3. **Create `AGENTS.md`** (use template below)
4. **Add tests:** `tests/unit/test_[module].py`
5. **Update this file:** Add to Directory Structure, Submodule Interaction Flow
6. **Update root:** Add to [../../AGENTS.md](../../AGENTS.md) navigation table

### AGENTS.md Template for Submodules

```markdown
# [Module Name] Guide

**Purpose:** [Brief description of module responsibility]

**Parent:** See [../AGENTS.md](../AGENTS.md) for core orchestrator overview.

---

## Quick Reference
- **Key files:** [List main files]
- **Testing:** pytest tests/unit/test_[module].py

## Architecture
[Module-specific architecture, design patterns]

## Common Tasks
[Module-specific workflows, operations]

## Memory Integration
**Emit events for:**
- [Event 1]: [When/why]
- [Event 2]: [When/why]

**Tag pattern:** [module], [operation], [context]

## Related Documentation
- **[../AGENTS.md](../AGENTS.md)** - Core orchestrator
- **[../../AGENTS.md](../../AGENTS.md)** - Project overview
- **[Related module AGENTS.md]** - Related functionality
```

---

## Code Style Conventions

**Naming:**
- **Functions/variables:** `snake_case` (PEP 8)
- **Classes:** `PascalCase` (e.g., `ConfigArtifact`, `DiffEngine`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `DEFAULT_STORAGE_PATH`)
- **Private:** `_leading_underscore` (e.g., `_internal_helper`)

**Type Hints (Required):**
```python
def get_artifact(artifact_id: str) -> dict:
    """Retrieve artifact by ID.

    Args:
        artifact_id: SHA-256 hash of artifact content

    Returns:
        Artifact dictionary with payload, signature, metadata

    Raises:
        ArtifactNotFoundError: If artifact_id not in storage
    """
    ...
```

**Docstrings (Google Style):**
- **Modules:** Brief description at top
- **Classes:** Description, attributes, example usage
- **Functions:** Args, Returns, Raises, Examples
- See [DOCUMENTATION_STANDARD.md](../../DOCUMENTATION_STANDARD.md)

**Error Handling:**
```python
from mcp_orchestrator.telemetry import OrchestratorError

class ArtifactNotFoundError(OrchestratorError):
    """Raised when artifact not found in storage."""
    pass

# Usage
if artifact_id not in storage:
    raise ArtifactNotFoundError(f"Artifact {artifact_id} not found")
```

---

## Testing Requirements

**Coverage Targets:**
- **Overall:** ≥85%
- **Crypto module:** 100% (security-critical)
- **Core orchestration:** ≥90%

**Test Categories:**

1. **Unit Tests:** Isolate external dependencies
   ```python
   # tests/unit/test_orchestrator.py
   from unittest.mock import Mock, patch

   @patch('mcp_orchestrator.storage.get_artifact')
   def test_orchestrator_retrieves_artifact(mock_get_artifact):
       mock_get_artifact.return_value = {"payload": "data"}
       result = orchestrator.get_config("client", "profile")
       assert result["payload"] == "data"
   ```

2. **Integration Tests:** Full orchestration flows
   ```python
   # tests/integration/test_orchestration_flow.py
   def test_full_config_retrieval_flow():
       # End-to-end: registry → storage → crypto → response
       artifact = orchestrator.get_config("claude-desktop", "default")
       assert artifact["artifact_id"] is not None
       assert crypto.verify_signature(artifact)
   ```

3. **Super-Tests:** System-level validation (see [tests/AGENTS.md](../../tests/AGENTS.md))
   ```python
   # tests/super/test_orchestration_lifecycle.py
   def test_orchestration_lifecycle():
       # Initialize → Retrieve → Diff → Update
       init_configs()
       artifact = get_config("claude-desktop", "default")
       diff = diff_config("claude-desktop", "default", local_payload)
       assert diff.status in ["up-to-date", "outdated", "diverged"]
   ```

---

## Memory Integration

**Emit events for orchestration operations:**

```python
from mcp_orchestrator.memory import emit_event, TraceContext

# Multi-step workflow with trace context
with TraceContext() as trace_id:
    emit_event(
        "orchestrator.config_retrieval_started",
        trace_id=trace_id,
        status="pending",
        metadata={"client_id": client_id, "profile_id": profile_id}
    )

    try:
        # Orchestration logic
        artifact = _retrieve_and_verify_artifact(client_id, profile_id)

        emit_event(
            "orchestrator.config_retrieval_completed",
            trace_id=trace_id,
            status="success",
            metadata={"artifact_id": artifact["artifact_id"]}
        )
        return artifact
    except Exception as e:
        emit_event(
            "orchestrator.config_retrieval_failed",
            trace_id=trace_id,
            status="failure",
            metadata={"error": str(e), "error_type": type(e).__name__}
        )
        raise
```

**Tag pattern:** `orchestrator`, `[submodule]`, `[operation]`

**Create knowledge notes for:**
- Orchestration workflow optimizations
- Integration patterns discovered
- Cross-module interaction learnings

---

## Related Documentation

- **[../../AGENTS.md](../../AGENTS.md)** - Project overview, architecture, PR workflow
- **[../../dev-docs/AGENTS.md](../../dev-docs/AGENTS.md)** - Development workflows
- **[crypto/AGENTS.md](crypto/AGENTS.md)** - Cryptographic operations
- **[storage/AGENTS.md](storage/AGENTS.md)** - Storage layer
- **[registry/AGENTS.md](registry/AGENTS.md)** - Client registry
- **[diff/AGENTS.md](diff/AGENTS.md)** - Diff engine
- **[mcp/AGENTS.md](mcp/AGENTS.md)** - MCP server
- **[servers/AGENTS.md](servers/AGENTS.md)** - Server registry (Wave 1.1)

---

## Common Tasks

### Run Orchestrator Locally

```bash
# Initialize configs
mcp-orchestration init-configs

# Start MCP server (stdio mode)
mcp-orchestration

# Or programmatically
python -m mcp_orchestrator.mcp.server
```

### Debug Orchestration Flow

```bash
# Enable debug logging
export MCP_ORCHESTRATION_DEBUG=1
export MCP_ORCHESTRATION_LOG_LEVEL=DEBUG

# Run with verbose output
mcp-orchestration 2>&1 | tee orchestration.log

# Check memory events
mcp-orchestration-memory query --type orchestrator --since 1h
```

### Add New Client Family

See [registry/AGENTS.md](registry/AGENTS.md) for detailed registry operations.

### Profile Management

See [registry/AGENTS.md](registry/AGENTS.md) for profile operations.

---

## Troubleshooting

### Orchestrator Won't Start

```bash
# Check Python version
python --version  # Must be 3.12+

# Check virtual environment
which python  # Should be .venv/bin/python

# Reinstall dependencies
pip install -e ".[dev]"

# Check environment variables
env | grep MCP_ORCHESTRATION
```

### Module Import Errors

```bash
# Verify package structure
python -c "import mcp_orchestrator; print(mcp_orchestrator.__version__)"

# Check PYTHONPATH
echo $PYTHONPATH

# Reinstall editable
pip install -e .
```

### Submodule Integration Issues

```bash
# Test individual modules
python -c "from mcp_orchestrator.crypto import sign_artifact; print('Crypto OK')"
python -c "from mcp_orchestrator.storage import get_artifact; print('Storage OK')"
python -c "from mcp_orchestrator.registry import list_clients; print('Registry OK')"

# Check integration tests
pytest tests/integration/test_orchestration_flow.py -v
```

---

**End of Core Orchestrator Guide**

For questions not covered here, see [../../AGENTS.md](../../AGENTS.md) or consult submodule-specific guides.
