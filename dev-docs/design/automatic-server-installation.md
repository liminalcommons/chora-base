# Design: Automatic MCP Server Installation

**Status:** Draft
**Author:** Claude (with Victor Piper)
**Date:** 2025-10-25
**Target Wave:** 2.2 or 3.0
**Related:** [WAVE_1X_PLAN.md](../../project-docs/WAVE_1X_PLAN.md)

---

## Problem Statement

Currently, users must manually install MCP servers before they can be used:

1. **npm servers:** Run `npm install -g @modelcontextprotocol/server-filesystem`
2. **PyPI servers:** Run `pip install lightrag-mcp` or `uvx lightrag-mcp`
3. **Check installation:** Verify server is available in PATH

This creates friction in the user experience:
- Requires terminal access and package manager knowledge
- Interrupts conversational workflow in Claude Desktop
- Users may not know which package manager to use
- No validation that installation succeeded

**Goal:** Enable mcp-orchestration to automatically discover, validate, and install MCP servers from npm and PyPI registries.

---

## Solution Overview

### Architecture

```
┌─────────────────────────────────────────────────┐
│           User (via Claude or CLI)              │
└───────────────┬─────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────┐
│      MCP Tools (check/install/list)             │
│  - check_server_installation()                  │
│  - install_server()                             │
│  - list_installed_servers()                     │
└───────────────┬─────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────┐
│      Installation Module                        │
│  ├── package_manager.py (detect npm/pip/etc)    │
│  ├── installer.py (execute installs)            │
│  ├── validator.py (verify success)              │
│  └── models.py (result types)                   │
└───────────────┬─────────────────────────────────┘
                │
                ├──────────────────┬───────────────┤
                ▼                  ▼               ▼
     ┌─────────────────┐  ┌─────────────┐  ┌─────────────┐
     │  NPM Registry   │  │PyPI Registry│  │ Local Check │
     │  (API query)    │  │  (API query)│  │  (which/    │
     │                 │  │             │  │   whereis)  │
     └─────────────────┘  └─────────────┘  └─────────────┘
```

### Key Components

**1. Extended ServerDefinition Model**
- Add `pypi_package` field (str | None)
- Add `package_manager` field (PackageManager enum)
- Add `install_command` field (str | None) for custom installers

**2. Installation Module** (`src/mcp_orchestrator/installation/`)
- **PackageManager detection:** Auto-detect available package managers
- **Installer:** Execute installations with safety checks and user confirmation
- **Validator:** Verify installation success and get installed version
- **Models:** Typed installation results

**3. Registry Query Module** (`src/mcp_orchestrator/discovery/`)
- **NPM API client:** Query npm registry for package metadata
- **PyPI API client:** Query PyPI for package metadata
- **Models:** Package metadata types

**4. MCP Tools** (3 new)
- `check_server_installation(server_id)` - Check if server is installed
- `install_server(server_id, confirm=True)` - Install with user confirmation
- `list_installed_servers()` - List all installed MCP servers

---

## Detailed Design

### 1. Data Models

#### PackageManager Enum

```python
# src/mcp_orchestrator/servers/models.py

class PackageManager(str, Enum):
    """Package manager for server installation."""

    NPM = "npm"           # npm install -g
    PIP = "pip"           # pip install
    PIPX = "pipx"         # pipx install (isolated Python apps)
    UVX = "uvx"           # uvx (uv-based installer)
    CUSTOM = "custom"     # Custom install command
    NONE = "none"         # No installation (local script)
```

#### Extended ServerDefinition

```python
# src/mcp_orchestrator/servers/models.py

class ServerDefinition(BaseModel):
    # ... existing fields ...

    # Package installation (NEW)
    npm_package: str | None = Field(
        default=None,
        description="NPM package name if installable via npm"
    )
    pypi_package: str | None = Field(
        default=None,
        description="PyPI package name if installable via pip/pipx/uvx"
    )
    package_manager: PackageManager = Field(
        default=PackageManager.NONE,
        description="Preferred package manager for installation"
    )
    install_command: str | None = Field(
        default=None,
        description="Custom installation command (if package_manager=CUSTOM)"
    )
```

#### Installation Result Models

```python
# src/mcp_orchestrator/installation/models.py

class InstallationStatus(str, Enum):
    """Installation status."""
    INSTALLED = "installed"
    NOT_INSTALLED = "not_installed"
    UNKNOWN = "unknown"
    ERROR = "error"


class InstallationResult(BaseModel):
    """Result of installation check or install operation."""

    server_id: str
    status: InstallationStatus
    installed_version: str | None = None
    install_location: str | None = None
    package_manager: PackageManager | None = None
    error_message: str | None = None
    installation_command: str | None = None


class PackageInfo(BaseModel):
    """Package metadata from registry."""

    package_name: str
    latest_version: str
    description: str | None = None
    homepage: str | None = None
    repository: str | None = None
```

### 2. Installation Module

#### Package Manager Detection

```python
# src/mcp_orchestrator/installation/package_manager.py

from typing import List
import shutil
import subprocess

class PackageManagerDetector:
    """Detect available package managers on the system."""

    @staticmethod
    def detect_available() -> List[PackageManager]:
        """Detect which package managers are installed.

        Returns:
            List of available PackageManager enums
        """
        available = []

        # Check npm
        if shutil.which("npm"):
            available.append(PackageManager.NPM)

        # Check pip
        if shutil.which("pip") or shutil.which("pip3"):
            available.append(PackageManager.PIP)

        # Check pipx
        if shutil.which("pipx"):
            available.append(PackageManager.PIPX)

        # Check uvx
        if shutil.which("uvx"):
            available.append(PackageManager.UVX)

        return available

    @staticmethod
    def get_install_command(
        package_manager: PackageManager,
        package_name: str,
        global_install: bool = True
    ) -> List[str]:
        """Get installation command for package manager.

        Args:
            package_manager: Which package manager to use
            package_name: Name of package to install
            global_install: Whether to install globally (npm only)

        Returns:
            List of command arguments
        """
        if package_manager == PackageManager.NPM:
            cmd = ["npm", "install"]
            if global_install:
                cmd.append("-g")
            cmd.append(package_name)
            return cmd

        elif package_manager == PackageManager.PIP:
            return ["pip", "install", package_name]

        elif package_manager == PackageManager.PIPX:
            return ["pipx", "install", package_name]

        elif package_manager == PackageManager.UVX:
            return ["uvx", package_name]

        else:
            raise ValueError(f"Unsupported package manager: {package_manager}")
```

#### Installer

```python
# src/mcp_orchestrator/installation/installer.py

import subprocess
from pathlib import Path
from typing import Optional

from mcp_orchestrator.installation.models import (
    InstallationResult,
    InstallationStatus
)
from mcp_orchestrator.installation.package_manager import PackageManagerDetector
from mcp_orchestrator.servers.models import PackageManager


class ServerInstaller:
    """Install MCP servers via package managers."""

    def __init__(self, dry_run: bool = False):
        """Initialize installer.

        Args:
            dry_run: If True, don't actually install, just simulate
        """
        self.dry_run = dry_run
        self.detector = PackageManagerDetector()

    def install(
        self,
        package_manager: PackageManager,
        package_name: str,
        server_id: str,
        timeout: int = 300  # 5 minutes
    ) -> InstallationResult:
        """Install a server package.

        Args:
            package_manager: Which package manager to use
            package_name: Package name to install
            server_id: Server identifier for result tracking
            timeout: Installation timeout in seconds

        Returns:
            InstallationResult with status and details
        """
        # Get install command
        try:
            cmd = self.detector.get_install_command(
                package_manager,
                package_name
            )
        except ValueError as e:
            return InstallationResult(
                server_id=server_id,
                status=InstallationStatus.ERROR,
                error_message=str(e)
            )

        # Dry run mode
        if self.dry_run:
            return InstallationResult(
                server_id=server_id,
                status=InstallationStatus.INSTALLED,
                installation_command=" ".join(cmd),
                error_message="Dry run - installation not executed"
            )

        # Execute installation
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True
            )

            return InstallationResult(
                server_id=server_id,
                status=InstallationStatus.INSTALLED,
                package_manager=package_manager,
                installation_command=" ".join(cmd)
            )

        except subprocess.CalledProcessError as e:
            return InstallationResult(
                server_id=server_id,
                status=InstallationStatus.ERROR,
                error_message=f"Installation failed: {e.stderr}",
                installation_command=" ".join(cmd)
            )

        except subprocess.TimeoutExpired:
            return InstallationResult(
                server_id=server_id,
                status=InstallationStatus.ERROR,
                error_message=f"Installation timed out after {timeout}s",
                installation_command=" ".join(cmd)
            )
```

#### Validator

```python
# src/mcp_orchestrator/installation/validator.py

import shutil
import subprocess
from typing import Optional

from mcp_orchestrator.installation.models import (
    InstallationResult,
    InstallationStatus
)
from mcp_orchestrator.servers.models import ServerDefinition, PackageManager


class InstallationValidator:
    """Validate server installation status."""

    def check_installation(
        self,
        server: ServerDefinition
    ) -> InstallationResult:
        """Check if a server is installed.

        Args:
            server: ServerDefinition to check

        Returns:
            InstallationResult with current status
        """
        # Extract command to check
        if server.stdio_command:
            command_to_check = server.stdio_command
        else:
            return InstallationResult(
                server_id=server.server_id,
                status=InstallationStatus.UNKNOWN,
                error_message="No stdio_command defined"
            )

        # Check if command exists in PATH
        location = shutil.which(command_to_check)

        if location:
            # Try to get version
            version = self._get_version(command_to_check, server.package_manager)

            return InstallationResult(
                server_id=server.server_id,
                status=InstallationStatus.INSTALLED,
                install_location=location,
                installed_version=version,
                package_manager=server.package_manager
            )
        else:
            return InstallationResult(
                server_id=server.server_id,
                status=InstallationStatus.NOT_INSTALLED,
                package_manager=server.package_manager
            )

    def _get_version(
        self,
        command: str,
        package_manager: PackageManager
    ) -> Optional[str]:
        """Try to get installed version.

        Args:
            command: Command to check
            package_manager: Package manager used

        Returns:
            Version string if available, None otherwise
        """
        # Try common version flags
        for flag in ["--version", "-v", "-V", "version"]:
            try:
                result = subprocess.run(
                    [command, flag],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return result.stdout.strip().split("\n")[0]
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue

        return None
```

### 3. MCP Tools

#### Tool: check_server_installation

```python
# src/mcp_orchestrator/mcp/server.py

@mcp.tool()
async def check_server_installation(server_id: str) -> dict[str, Any]:
    """Check if an MCP server is installed on the system.

    Args:
        server_id: Server identifier from registry

    Returns:
        Dictionary with:
        - server_id: Server identifier
        - status: "installed", "not_installed", or "unknown"
        - installed_version: Version string if installed
        - install_location: Path to installed binary
        - package_manager: Package manager used
        - installation_command: Suggested install command if not installed

    Raises:
        ValueError: If server_id not found in registry
    """
    # Get server from registry
    try:
        server = _server_registry.get(server_id)
    except ServerNotFoundError as e:
        raise ValueError(str(e)) from e

    # Check installation
    validator = InstallationValidator()
    result = validator.check_installation(server)

    # Build response
    response = result.model_dump()

    # Add installation command if not installed
    if result.status == InstallationStatus.NOT_INSTALLED:
        if server.npm_package:
            response["installation_command"] = f"npm install -g {server.npm_package}"
        elif server.pypi_package:
            response["installation_command"] = f"pip install {server.pypi_package}"

    return response
```

#### Tool: install_server

```python
@mcp.tool()
async def install_server(
    server_id: str,
    confirm: bool = True,
    package_manager: str | None = None
) -> dict[str, Any]:
    """Install an MCP server from npm or PyPI.

    **IMPORTANT:** This tool will execute system commands. User confirmation
    is required unless confirm=False is explicitly set.

    Args:
        server_id: Server identifier from registry
        confirm: Require user confirmation before installing (default: True)
        package_manager: Override package manager (npm, pip, pipx, uvx)

    Returns:
        Dictionary with:
        - server_id: Server identifier
        - status: "installed", "error", "confirmation_required"
        - installed_version: Version if successful
        - error_message: Error details if failed
        - installation_command: Command that was executed

    Raises:
        ValueError: If server_id not found or installation fails
    """
    # Get server from registry
    try:
        server = _server_registry.get(server_id)
    except ServerNotFoundError as e:
        raise ValueError(str(e)) from e

    # Check if already installed
    validator = InstallationValidator()
    check_result = validator.check_installation(server)

    if check_result.status == InstallationStatus.INSTALLED:
        return {
            "server_id": server_id,
            "status": "already_installed",
            "installed_version": check_result.installed_version,
            "install_location": check_result.install_location
        }

    # Determine package manager
    if package_manager:
        pm = PackageManager(package_manager)
    else:
        pm = server.package_manager

    # Get package name
    if pm == PackageManager.NPM and server.npm_package:
        package_name = server.npm_package
    elif pm in [PackageManager.PIP, PackageManager.PIPX, PackageManager.UVX] and server.pypi_package:
        package_name = server.pypi_package
    else:
        raise ValueError(
            f"Server '{server_id}' does not support package manager '{pm}'"
        )

    # Require confirmation in production
    if confirm:
        return {
            "server_id": server_id,
            "status": "confirmation_required",
            "message": f"Ready to install {package_name} via {pm.value}. "
                      f"Call install_server(server_id='{server_id}', confirm=False) to proceed.",
            "installation_command": PackageManagerDetector.get_install_command(pm, package_name)
        }

    # Execute installation
    installer = ServerInstaller()
    result = installer.install(
        package_manager=pm,
        package_name=package_name,
        server_id=server_id
    )

    return result.model_dump()
```

#### Tool: list_installed_servers

```python
@mcp.tool()
async def list_installed_servers() -> dict[str, Any]:
    """List all MCP servers and their installation status.

    Returns:
        Dictionary with:
        - servers: List of server installation statuses
        - installed_count: Number of installed servers
        - not_installed_count: Number of not installed servers
        - total_count: Total servers in registry
    """
    servers = _server_registry.list_all()
    validator = InstallationValidator()

    results = []
    installed_count = 0
    not_installed_count = 0

    for server in servers:
        check_result = validator.check_installation(server)

        if check_result.status == InstallationStatus.INSTALLED:
            installed_count += 1
        elif check_result.status == InstallationStatus.NOT_INSTALLED:
            not_installed_count += 1

        results.append({
            "server_id": server.server_id,
            "display_name": server.display_name,
            "status": check_result.status,
            "installed_version": check_result.installed_version,
            "package_manager": server.package_manager.value if server.package_manager else None
        })

    return {
        "servers": results,
        "installed_count": installed_count,
        "not_installed_count": not_installed_count,
        "total_count": len(servers)
    }
```

---

## Usage Examples

### Conversational (via Claude Desktop)

**Check installation:**
```
User: "Is the filesystem server installed?"

Claude: [Calls check_server_installation("filesystem")]

"✓ Yes, filesystem server is installed
  Version: 2025.8.21
  Location: /opt/homebrew/bin/npx
  Package manager: npm"
```

**Install server:**
```
User: "Install the lightrag server"

Claude: [Calls install_server("lightrag-mcp")]

"I can install lightrag-mcp for you via pip.

Installation command: pip install lightrag-mcp

Shall I proceed? (This will execute system commands)"

User: "Yes"

Claude: [Calls install_server("lightrag-mcp", confirm=False)]

"✓ Successfully installed lightrag-mcp
  Package manager: pip

Would you like me to add it to your configuration?"
```

**List installed:**
```
User: "What servers are installed?"

Claude: [Calls list_installed_servers()]

"You have 3 out of 15 servers installed:

✓ Installed (3):
  - filesystem (npm) - v2025.8.21
  - memory (npm) - v2025.8.21
  - lightrag-mcp (pip) - v0.1.0

✗ Not installed (12):
  - brave-search, github, postgres, ...

Would you like to install any of these?"
```

### CLI

```bash
# Check installation
mcp-orchestration-check-installation filesystem
# Output: ✓ Installed - @modelcontextprotocol/server-filesystem@2025.8.21

# Install server
mcp-orchestration-install-server lightrag-mcp
# Output: Installing lightrag-mcp via pip... ✓ Done

# List installed
mcp-orchestration-list-installed
# Output: (formatted table of servers)
```

---

## Security Considerations

### Safety Measures

1. **User confirmation required** by default
2. **Package source validation** - Only npm/PyPI allowed
3. **Command sanitization** - No arbitrary shell injection
4. **Timeout limits** - 5 minutes max per installation
5. **Error handling** - Safe failures, no partial installs

### Sandboxing

For Python packages, consider using virtual environments:
- `pipx` - Installs in isolated venvs automatically
- `uvx` - Modern alternative with better isolation

### Audit Trail

Log all installation attempts:
```python
emit_event("server.installation_requested",
           server_id=server_id,
           package_name=package_name,
           package_manager=pm.value)

emit_event("server.installation_completed",
           server_id=server_id,
           status=result.status,
           version=result.installed_version)
```

---

## Testing Strategy

### Unit Tests

```python
# tests/unit/test_installation/test_package_manager.py
def test_detect_available_package_managers():
    """Should detect npm, pip, etc. on system."""

def test_get_install_command_npm():
    """Should generate correct npm install command."""

def test_get_install_command_pip():
    """Should generate correct pip install command."""


# tests/unit/test_installation/test_validator.py
def test_check_installation_installed():
    """Should detect installed server."""

def test_check_installation_not_installed():
    """Should detect missing server."""

def test_get_version():
    """Should extract version from command output."""


# tests/unit/test_installation/test_installer.py
def test_install_success(monkeypatch):
    """Should successfully install via subprocess."""

def test_install_failure(monkeypatch):
    """Should handle installation errors gracefully."""

def test_install_timeout(monkeypatch):
    """Should timeout long installations."""

def test_dry_run_mode():
    """Should simulate installation without executing."""
```

### Integration Tests

```python
# tests/integration/test_installation_workflow.py

def test_check_then_install_workflow(test_registry):
    """Should check installation, then install if missing."""
    # 1. Check status
    result = check_server_installation("test-server")
    assert result["status"] == "not_installed"

    # 2. Install
    install_result = install_server("test-server", confirm=False)
    assert install_result["status"] == "installed"

    # 3. Check again
    result2 = check_server_installation("test-server")
    assert result2["status"] == "installed"


def test_list_installed_after_installs(test_registry):
    """Should show correct counts after installations."""
    # Install some servers
    install_server("server-a", confirm=False)
    install_server("server-b", confirm=False)

    # List
    result = list_installed_servers()
    assert result["installed_count"] >= 2
```

### E2E Tests

```python
# tests/e2e/test_installation_e2e.py

@pytest.mark.e2e
def test_full_installation_workflow():
    """Test complete workflow via MCP tools."""
    # Use MCP Inspector or test client
    # Test conversational flow
```

---

## Migration Path

### Phase 1: Add Models (Non-breaking)
- Add `PackageManager` enum
- Add optional fields to `ServerDefinition`
- Default values ensure backward compatibility

### Phase 2: Add Installation Module
- New module, no impact on existing code
- Can be tested independently

### Phase 3: Add MCP Tools
- New tools, don't modify existing ones
- Opt-in usage

### Phase 4: Integration
- Update `describe_server` to show installation status
- Update `add_server_to_config` to check installation
- Still backward compatible

---

## Future Enhancements

### Wave 3.x+

1. **Registry sync** - Auto-update server catalog from npm/PyPI
2. **Version management** - Install specific versions, update servers
3. **Dependency resolution** - Handle server dependencies
4. **Uninstall tool** - Remove installed servers
5. **Virtual environments** - Isolated Python server installs
6. **Installation templates** - Pre-configured server bundles
7. **Offline mode** - Cache packages for offline install

---

## Open Questions

1. **Should we support global vs. local installs?**
   - npm: `-g` vs local `node_modules`
   - pip: system vs `--user` vs venv
   - **Recommendation:** Start with global installs, add local in Wave 3.x

2. **How to handle version conflicts?**
   - What if user already has different version installed?
   - **Recommendation:** Detect existing, warn user, don't force upgrade

3. **Should we auto-install on `add_server_to_config`?**
   - Pro: Seamless UX
   - Con: Unexpected system changes
   - **Recommendation:** Offer to install, require confirmation

4. **How to handle failed installations?**
   - Retry? Rollback? Report to user?
   - **Recommendation:** Report error with actionable guidance

---

## Success Metrics

1. **Installation success rate** - >95% of installations succeed
2. **User satisfaction** - Reduce "installation failed" support issues
3. **Adoption** - >50% of users use auto-install feature
4. **Coverage** - Support >80% of popular MCP servers

---

## References

- [Wave 1.X Plan](../../project-docs/WAVE_1X_PLAN.md)
- [Server Registry AGENTS.md](../../src/mcp_orchestrator/servers/AGENTS.md)
- [MCP Server Catalog (defaults.py)](../../src/mcp_orchestrator/servers/defaults.py)
- [npm Registry API](https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md)
- [PyPI JSON API](https://warehouse.pypa.io/api-reference/json.html)
- [lightrag-mcp on PyPI](https://pypi.org/project/lightrag-mcp/)

---

**Status:** Ready for review and BDD implementation
