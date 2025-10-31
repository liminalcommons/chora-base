# Automatic Server Installation - Progress Summary

**Created:** 2025-10-25
**Status:** BDD Phase Complete, Ready for TDD Implementation
**Following Process:** DDD → BDD → TDD (as per [dev-docs/AGENTS.md](../AGENTS.md))

---

## What We've Accomplished

### ✅ Step 1: DDD (Documentation-Driven Design) - COMPLETE

**Created:** [automatic-server-installation.md](./automatic-server-installation.md)

**Documented:**
- Problem statement and solution overview
- Complete architecture design
- Data models (PackageManager enum, extended ServerDefinition, InstallationResult)
- Three implementation modules:
  - `package_manager.py` - Detection and command generation
  - `validator.py` - Installation status checking
  - `installer.py` - Package installation execution
- Three new MCP tools:
  - `check_server_installation(server_id)` - Check installation status
  - `install_server(server_id, confirm=True, package_manager=None)` - Install with confirmation
  - `list_installed_servers()` - List all servers and status
- Security considerations (user confirmation, timeout, error handling)
- Testing strategy
- Usage examples (conversational and CLI)

### ✅ Step 2: BDD (Behavior-Driven Development) - COMPLETE

**Created 4 test files** defining expected behavior:

#### 1. [test_installation_package_manager.py](../../tests/test_installation_package_manager.py)
- ✅ PackageManager enum values
- ✅ Package manager detection (npm, pip, pipx, uvx)
- ✅ Installation command generation for each package manager
- ✅ Error handling for unsupported package managers
- ✅ Integration workflow tests

**Test Count:** ~15 tests

#### 2. [test_installation_validator.py](../../tests/test_installation_validator.py)
- ✅ Check installation status (installed/not installed/unknown)
- ✅ Extract version information
- ✅ Handle multiple version flags (--version, -V, etc.)
- ✅ Timeout handling when getting versions
- ✅ Batch validation of multiple servers
- ✅ Edge cases (symlinks, empty commands)

**Test Count:** ~12 tests

#### 3. [test_installation_installer.py](../../tests/test_installation_installer.py)
- ✅ Successful npm package installation
- ✅ Successful pip/pipx/uvx installation
- ✅ Package not found errors
- ✅ Network errors
- ✅ Timeout errors
- ✅ Permission errors
- ✅ Disk space errors
- ✅ Dry-run mode (safe simulation)
- ✅ Custom timeout configuration
- ✅ Installation command generation

**Test Count:** ~18 tests

#### 4. [test_installation_mcp_tools.py](../../tests/test_installation_mcp_tools.py)
- ✅ `check_server_installation` tool behavior
  - Installed servers
  - Not installed servers (npm and pip)
  - Installation command suggestions
  - Error handling
- ✅ `install_server` tool behavior
  - Already installed check
  - Confirmation requirement (safety)
  - Successful installation
  - Installation failures
  - Custom package manager override
- ✅ `list_installed_servers` tool behavior
  - Mixed installation status
  - Version information
  - Empty registry handling
- ✅ Complete workflow integration tests
  - check → install → verify
  - list → install → list
- ✅ Error handling across all tools

**Test Count:** ~20 tests

**Total BDD Tests:** ~65 comprehensive behavioral tests

---

## What These Tests Define

The BDD tests define the complete expected behavior:

### User-Facing Behavior

1. **Checking installation status:**
   ```python
   result = await check_server_installation("filesystem")
   # Returns: status, version, location, installation_command
   ```

2. **Installing a server:**
   ```python
   # Requires confirmation by default (safety)
   result = await install_server("brave-search")
   # Returns: confirmation_required

   # Install with confirmation bypassed
   result = await install_server("brave-search", confirm=False)
   # Returns: installed or error
   ```

3. **Listing all servers:**
   ```python
   result = await list_installed_servers()
   # Returns: servers list, installed_count, not_installed_count
   ```

### Technical Behavior

1. **Package manager detection:**
   - Detects npm, pip, pipx, uvx availability
   - Generates correct install commands for each

2. **Installation validation:**
   - Checks PATH for binaries
   - Extracts version information
   - Handles edge cases gracefully

3. **Installation execution:**
   - Executes package manager commands
   - Handles all error types (network, permission, timeout, etc.)
   - Supports dry-run mode for safety
   - Respects custom timeouts

### Safety & Security

1. **User confirmation required** by default
2. **Timeout protection** (5 minutes default)
3. **Error handling** for all failure modes
4. **Dry-run mode** for testing without execution

---

## Next Steps: TDD Implementation

Now that behavior is defined, we implement code to make tests pass:

### Step 3.1: Extend ServerDefinition Model
```python
# Add to src/mcp_orchestrator/servers/models.py
class PackageManager(str, Enum):
    NPM = "npm"
    PIP = "pip"
    PIPX = "pipx"
    UVX = "uvx"
    CUSTOM = "custom"
    NONE = "none"

# Add fields to ServerDefinition:
pypi_package: str | None = None
package_manager: PackageManager = PackageManager.NONE
install_command: str | None = None
```

### Step 3.2: Create Installation Module Structure
```
src/mcp_orchestrator/installation/
├── __init__.py
├── models.py          # InstallationResult, InstallationStatus, PackageInfo
├── package_manager.py # PackageManagerDetector
├── validator.py       # InstallationValidator
└── installer.py       # ServerInstaller
```

### Step 3.3: Implement Each Module
Following TDD:
1. Run tests (they fail - expected)
2. Implement minimal code to pass one test
3. Refactor for quality
4. Repeat for next test

### Step 3.4: Implement MCP Tools
Add three tools to `src/mcp_orchestrator/mcp/server.py`:
- `check_server_installation()`
- `install_server()`
- `list_installed_servers()`

### Step 3.5: Add PyPI Servers to Registry
Add 3-5 Python MCP servers to `src/mcp_orchestrator/servers/defaults.py`:
- `lightrag-mcp` (confirmed exists)
- Search PyPI for other `*-mcp` packages

---

## Testing the Implementation

Once implemented, run tests:

```bash
# Run all installation tests
pytest tests/test_installation_*.py -v

# Run with coverage
pytest tests/test_installation_*.py --cov=src/mcp_orchestrator/installation --cov-report=term-missing

# Expected result: All 65 tests pass
```

---

## Documentation (After Implementation)

### User Documentation to Create

1. **user-docs/how-to/install-mcp-servers.md**
   - How to check installation status
   - How to install servers via Claude
   - How to install via CLI
   - Troubleshooting installation issues

2. **user-docs/explanation/package-managers.md**
   - What package managers are supported
   - npm vs pip vs pipx vs uvx
   - When to use which

3. **Update existing docs:**
   - [add-server-to-config.md](../../user-docs/how-to/add-server-to-config.md) - Add installation checking
   - [complete-workflow.md](../../user-docs/how-to/complete-workflow.md) - Add installation steps
   - [README.md](../../README.md) - Add installation features to features list

### Developer Documentation

1. **Update [src/mcp_orchestrator/installation/AGENTS.md](../../src/mcp_orchestrator/installation/AGENTS.md)**
   - Module architecture
   - How to extend with new package managers
   - Testing guidelines

---

## Wave Placement

**Recommended:** Wave 2.2 or 3.0

**Rationale:**
- Not critical for Wave 2.0-2.1 (HTTP transport priority)
- Adds significant UX value
- Well-scoped feature with clear boundaries
- Can be developed independently

**Dependencies:**
- None (standalone feature)
- Enhances existing server registry functionality

**Estimated Timeline:**
- TDD Implementation: 3-4 days
- Documentation: 1 day
- **Total:** 4-5 days

---

## Success Criteria

### Implementation Complete When:
- ✅ All 65 BDD tests pass
- ✅ Test coverage ≥85% for installation module
- ✅ All MCP tools working in Claude Desktop
- ✅ User documentation complete
- ✅ CHANGELOG.md updated

### Feature Complete When:
- ✅ Users can check installation status via Claude
- ✅ Users can install servers via Claude (with confirmation)
- ✅ Users can list installed servers
- ✅ Both npm and PyPI packages supported
- ✅ Installation errors handled gracefully

---

## Files Created

### Design Documents
- ✅ [automatic-server-installation.md](./automatic-server-installation.md) - Complete design
- ✅ [automatic-server-installation-progress.md](./automatic-server-installation-progress.md) - This file

### Test Files
- ✅ [test_installation_package_manager.py](../../tests/test_installation_package_manager.py)
- ✅ [test_installation_validator.py](../../tests/test_installation_validator.py)
- ✅ [test_installation_installer.py](../../tests/test_installation_installer.py)
- ✅ [test_installation_mcp_tools.py](../../tests/test_installation_mcp_tools.py)

**Total Lines of Test Code:** ~850 lines

---

## Process Followed

We strictly followed the **DDD → BDD → TDD** process as documented in [dev-docs/AGENTS.md](../AGENTS.md):

1. ✅ **DDD (Documentation-Driven Design)**
   - Wrote complete design document before any code
   - Defined all interfaces, data models, error conditions
   - Documented usage examples and workflows

2. ✅ **BDD (Behavior-Driven Development)**
   - Wrote behavioral tests defining expected behavior
   - Tests are executable specifications
   - Cover happy paths, error cases, edge cases

3. ⏳ **TDD (Test-Driven Development)** - Next
   - Implement code to make tests pass
   - Refactor for quality
   - Documentation follows implementation

This ensures:
- Clear requirements before coding
- Testable specifications
- Documentation stays current
- Reduced rework

---

## Questions Answered

**Original Question:** "Would it be possible to have mcp-orchestration find and install specified MCP servers (npm and PyPI)?"

**Answer:** **Yes, absolutely!**

**What we've done:**
1. ✅ Designed complete solution
2. ✅ Defined all expected behaviors via tests
3. ⏳ Ready to implement (TDD phase)

**What users will be able to do:**
- Ask Claude: "Is filesystem server installed?"
- Ask Claude: "Install the lightrag server"
- Ask Claude: "What servers are installed?"
- Get automatic installation with safety confirmation
- Support for both npm (Node.js) and PyPI (Python) packages

**Safety measures:**
- User confirmation required by default
- Dry-run mode available
- Timeout protection
- Comprehensive error handling

---

**Status:** Ready to proceed with TDD implementation when approved.

**Next Action:** Implement Step 3.1 (PackageManager enum) and run first tests.
