# CLAUDE.md - mcp-orchestration

**MCP Server for centralized configuration management with cryptographic signatures**

Read first: [AGENTS.md](AGENTS.md) for generic AI agent guidance.
This file provides Claude-specific optimizations for mcp-orchestration.

---

## Quick Start for Claude

### Project Specifics
- **Domain:** MCP configuration orchestration, cryptographic signing, content-addressable storage
- **Key Dependencies:** fastmcp>=0.3.0, pydantic>=2.0.0, cryptography>=41.0.0, chora-compose>=0.1.0
- **Architecture:** Layered architecture with cryptographic verification
  - Storage Layer (SHA-256 content-addressable)
  - Crypto Layer (Ed25519 signatures)
  - Registry Layer (Multi-client support)
  - MCP Server (4 tools, 2 resources)
  - Diff Engine (Semantic change classification)

### Critical Context
Load immediately when starting a session:
1. [AGENTS.md](AGENTS.md) - Project structure and conventions
2. [src/mcp_orchestrator/mcp/server.py](src/mcp_orchestrator/mcp/server.py) - MCP server implementation
3. Current wave plan from [project-docs/WAVE_1X_PLAN.md](project-docs/WAVE_1X_PLAN.md)
4. If resuming: Check `.chora/memory/sessions/` for checkpoint

### Common Patterns in This Project
- **MCP tools:** 4 tools defined in `src/mcp_orchestrator/mcp/server.py`
  - `get_config` - Retrieve signed configurations
  - `check_for_updates` - Diff detection and recommendations
  - `add_server_to_config` - Add MCP server to draft config
  - `remove_server_from_config` - Remove MCP server from draft config
- **Storage:** Content-addressable with `src/mcp_orchestrator/storage/cas.py`
- **Crypto:** Ed25519 signing in `src/mcp_orchestrator/crypto/signing.py`
- **Registry:** Multi-client support in `src/mcp_orchestrator/registry/`
- **Testing:** pytest with comprehensive fixtures in `tests/conftest.py`

---

## Domain-Specific Context Management

### Essential Context (0-10k tokens)
When working on specific features, load:
1. **Active MCP tool** you're modifying (from `src/mcp_orchestrator/mcp/server.py`)
2. **Relevant layer** (storage/crypto/registry/diff)
3. **Current wave plan** section from `project-docs/WAVE_1X_PLAN.md`
4. **Related tests** from `tests/`

### Extended Context (10-50k tokens)
For broader understanding:
1. All 4 MCP tools (`src/mcp_orchestrator/mcp/server.py`)
2. Storage layer (`src/mcp_orchestrator/storage/`)
3. Crypto layer (`src/mcp_orchestrator/crypto/`)
4. Registry layer (`src/mcp_orchestrator/registry/`)
5. Full test suite (`tests/`)
6. User documentation (`user-docs/`)

### Phase 3 Context (50k+ tokens)
For comprehensive refactoring or architecture changes:
1. All source code (`src/mcp_orchestrator/`)
2. All tests (`tests/`)
3. All documentation (`dev-docs/`, `user-docs/`, `project-docs/`)
4. Wave plans and roadmap
5. Example configurations

---

## Project-Specific Patterns

### MCP Tool Implementation
```python
# mcp-orchestration pattern for MCP tools
from fastmcp import FastMCP
from mcp_orchestrator.telemetry import get_emitter

mcp = FastMCP("mcp-orchestration")

@mcp.tool()
async def tool_name(param: str) -> dict:
    """Tool description.

    Args:
        param: Description

    Returns:
        Result dictionary with status and data
    """
    emitter = get_emitter()
    try:
        # Implementation
        result = {"status": "success", "data": {}}
        emitter.emit("tool.success", tool="tool_name", param=param)
        return result
    except Exception as e:
        emitter.emit("tool.error", tool="tool_name", error=str(e))
        raise
```

### Content-Addressable Storage Pattern
```python
from mcp_orchestrator.storage.cas import ContentAddressableStorage
from pathlib import Path

storage = ContentAddressableStorage(Path("var/storage"))

# Store artifact (returns SHA-256 hash)
content_hash = storage.store("artifact-content")

# Retrieve by hash
content = storage.retrieve(content_hash)
```

### Cryptographic Signing Pattern
```python
from mcp_orchestrator.crypto.signing import Signer
from pathlib import Path

# Load or generate keypair
signer = Signer(Path("var/keys/signing_key"))

# Sign artifact
signature = signer.sign(artifact_hash.encode())

# Verify signature
is_valid = signer.verify(artifact_hash.encode(), signature, signer.public_key)
```

### Telemetry Pattern
```python
from mcp_orchestrator.telemetry import get_emitter

emitter = get_emitter()

# Emit events for tracking
emitter.emit("config.retrieved",
             client="claude-desktop",
             hash=artifact_hash,
             cached=True)
```

---

## Testing Patterns for This Project

### Test Structure
```python
# tests/test_mcp_tools.py
import pytest
from mcp_orchestrator.mcp.server import mcp

def test_get_config_success(sample_artifact, storage):
    """Test get_config with valid hash."""
    result = mcp.call_tool("get_config", {
        "client": "claude-desktop",
        "artifact_hash": sample_artifact.hash
    })
    assert result["status"] == "success"
    assert "config" in result["data"]
```

### Fixtures (from tests/conftest.py)
```python
@pytest.fixture
def storage():
    """Content-addressable storage for testing."""
    # Provides isolated storage for each test

@pytest.fixture
def signer():
    """Ed25519 signer for testing."""
    # Provides test keypair

@pytest.fixture
def sample_artifact():
    """Sample signed artifact for testing."""
    # Provides complete signed artifact
```

---

## Development Workflow for This Project

Follow chora-base workflows with mcp-orchestration adaptations:

### DDD (Documentation-Driven Design)
1. Document feature in `dev-docs/design/`
2. Specify MCP tool interface (input/output schemas)
3. List error conditions and edge cases
4. Document cryptographic requirements
5. **Project-specific:** Include Claude Desktop/Cursor config examples

### BDD (Behavior-Driven Development)
1. Write Gherkin scenarios in `project-docs/capabilities/behaviors/`
2. Implement as pytest tests in `tests/`
3. **Project-specific:** Test via MCP Inspector with real Claude Desktop
4. Verify cryptographic signatures in test scenarios

### TDD (Test-Driven Development)
1. Write failing test for new functionality
2. Implement minimal code to pass
3. Refactor for quality
4. **Project-specific:** Always test signature verification

---

## Wave-Based Development

mcp-orchestration follows wave-based capability evolution. Always check current wave:

### Current Wave (Wave 1.5)
Check [project-docs/WAVE_1X_PLAN.md](project-docs/WAVE_1X_PLAN.md) for:
- Current features in development
- Committed scope
- Testing requirements
- Documentation expectations

### Wave Planning
- **Wave 1.0 (v0.1.0):** Read-only orchestration (DONE)
- **Wave 1.1 (v0.1.1):** Server catalog and discovery (DONE)
- **Wave 1.2 (v0.1.2):** Draft config builder (DONE)
- **Wave 1.3 (v0.1.3):** User documentation (DONE)
- **Wave 1.4 (v0.1.4):** Config publishing (DONE)
- **Wave 1.5 (v0.1.5):** Config deployment (IN PROGRESS)

### Future Waves
See [dev-docs/vision/](dev-docs/vision/) for exploratory features:
- **Wave 2:** Governance (policy engine, approval workflows)
- **Wave 3:** Intelligence (smart validation, analytics)
- **Wave 4:** Ecosystem (multi-tenant SaaS, marketplace)

**Important:** Don't build future features now. Design extension points.

---

## Memory System Integration

### Event Log Usage
```bash
# Query MCP tool invocations
mcp-orchestration-memory query --type tool.invoked --since 24h

# Find configuration errors
mcp-orchestration-memory query --type config.error --since 7d

# Track signature verification failures
mcp-orchestration-memory query --type signature.failed --since 30d
```

### Knowledge Graph
```bash
# Search for cryptographic patterns
mcp-orchestration-memory knowledge search --tag cryptography

# Store learned patterns about client compatibility
echo "Claude Desktop requires 'mcpServers' key, Cursor uses 'mcp_servers'" | \
  mcp-orchestration-memory knowledge create "Client Config Formats" \
  --tag registry --tag compatibility
```

---

## Common Tasks with Claude

### Add New MCP Tool
```markdown
"Implement new MCP tool: [name]

Specification:
- Purpose: [what it does]
- Input schema: [Pydantic model or dict spec]
- Output schema: [return type]
- Storage interaction: [read/write CAS]
- Crypto requirements: [signing/verification needs]

Follow pattern in src/mcp_orchestrator/mcp/server.py
Include comprehensive tests in tests/
Add to README tool list
Emit telemetry events
Update user-docs/how-to/ guide"
```

### Debug Tool Failure
```markdown
"Debug MCP tool failure:

Tool: [name]
Error: [from logs/Claude Desktop console]
Input: [what was sent]

Context:
- src/mcp_orchestrator/mcp/server.py:[line]
- Recent changes: $(git log --oneline -5 server.py)
- Telemetry: var/telemetry/events.jsonl (last 10 lines)

Reproduce via MCP Inspector:
[steps]"
```

### Add Server to Catalog
```markdown
"Add new MCP server to catalog:

Server: [name]
Repository: [github url]
Package: [npm/pypi package if available]
Category: [filesystem/web/database/etc]

Steps:
1. Add entry to src/mcp_orchestrator/servers/catalog.json
2. Include installation instructions
3. Specify required environment variables
4. Add test case to tests/test_server_catalog.py
5. Update user-docs/reference/server-catalog.md"
```

---

## Project Metrics

Track Claude effectiveness for mcp-orchestration development:

```python
from mcp_orchestrator.utils.claude_metrics import ClaudeROICalculator

calculator = ClaudeROICalculator(developer_hourly_rate=100)

# Track session for MCP tool development
calculator.add_session(
    task_type="mcp_tool",
    duration_minutes=25,
    iterations=2,
    first_pass_success=True,
    test_coverage_delta=5.2
)

# Generate report
report = calculator.generate_report()
print(report)
```

---

## Resources

### Project-Specific
- **MCP Protocol:** https://modelcontextprotocol.io
- **FastMCP Docs:** https://github.com/jlowin/fastmcp
- **Ed25519 (RFC 8032):** https://datatracker.ietf.org/doc/html/rfc8032
- **Content-Addressable Storage:** https://en.wikipedia.org/wiki/Content-addressable_storage

### Chora-Base Patterns
- [claude/](claude/) - Claude pattern library
  - [CONTEXT_MANAGEMENT.md](claude/CONTEXT_MANAGEMENT.md) - Progressive loading
  - [CHECKPOINT_PATTERNS.md](claude/CHECKPOINT_PATTERNS.md) - Session recovery
  - [METRICS_TRACKING.md](claude/METRICS_TRACKING.md) - ROI tracking
  - [FRAMEWORK_TEMPLATES.md](claude/FRAMEWORK_TEMPLATES.md) - Request templates

### Nested CLAUDE.md Files

**Development:**
- [dev-docs/CLAUDE.md](dev-docs/CLAUDE.md) - Contributing and development patterns
  - [dev-docs/vision/CLAUDE.md](dev-docs/vision/CLAUDE.md) - Strategic vision planning
  - [dev-docs/research/CLAUDE.md](dev-docs/research/CLAUDE.md) - Research and investigation

**Testing & Deployment:**
- [tests/CLAUDE.md](tests/CLAUDE.md) - Test generation patterns for MCP tools
- [docker/CLAUDE.md](docker/CLAUDE.md) - Docker assistance for MCP server deployment
- [scripts/CLAUDE.md](scripts/CLAUDE.md) - Automation patterns for build/release

**Memory & Tracking:**
- [.chora/memory/CLAUDE.md](.chora/memory/CLAUDE.md) - Memory integration for wave tracking

---

## Claude Advantages for This Project

### 200k Context Window
- Load entire codebase for refactoring (all `src/mcp_orchestrator/`)
- Review all tests simultaneously for comprehensive test planning
- Cross-reference user docs with implementation for consistency

### Multi-Tool Orchestration
- **Parallel reads:** Load multiple source files simultaneously
- **Parallel testing:** Run pytest while checking git status
- **Batch operations:** Create multiple test files in one message

### Checkpoint Recovery
Save session state to `.chora/memory/sessions/` with:
- Current wave and feature in development
- Files modified in session
- Test results and coverage delta
- Next steps for continuation

### Progressive Context Loading
1. **Phase 1 (20-40s):** Current wave plan + active file
2. **Phase 2 (if needed):** Related layers + tests
3. **Phase 3 (if needed):** Full codebase + all docs

---

**Built with [chora-base v3.3.0](https://github.com/liminalcommons/chora-base)** - Claude-optimized Python project template
