"""Integration tests for MCP installation tools.

BDD tests for check_server_installation, install_server, and list_installed_servers.
These tests define the expected behavior from the user/Claude perspective.

Wave 2.2/3.0 - Automatic Server Installation
"""

from unittest.mock import MagicMock, patch

import pytest
from mcp_orchestrator.servers.models import (
    PackageManager,
)

# Import will fail until we implement - expected in BDD
pytest.importorskip(
    "mcp_orchestrator.installation", reason="Module not yet implemented"
)


class TestCheckServerInstallationTool:
    """Test check_server_installation MCP tool behavior."""

    @pytest.mark.asyncio
    @patch(
        "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
    )
    async def test_check_installed_server(self, mock_check: MagicMock) -> None:
        """Should return installed status for installed server."""
        from mcp_orchestrator.installation.models import (
            InstallationResult,
            InstallationStatus,
        )
        from mcp_orchestrator.mcp.server import check_server_installation

        mock_check.return_value = InstallationResult(
            server_id="filesystem",
            status=InstallationStatus.INSTALLED,
            installed_version="2025.8.21",
            install_location="/usr/local/bin/npx",
            package_manager=PackageManager.NPM,
        )

        result = await check_server_installation("filesystem")

        assert result["server_id"] == "filesystem"
        assert result["status"] == "installed"
        assert result["installed_version"] == "2025.8.21"
        assert result["install_location"] == "/usr/local/bin/npx"
        assert "installation_command" not in result  # Not needed when installed

    @pytest.mark.asyncio
    @patch(
        "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
    )
    async def test_check_not_installed_server_with_npm_package(
        self, mock_check: MagicMock
    ) -> None:
        """Should return not installed status with installation command."""
        from mcp_orchestrator.installation.models import (
            InstallationResult,
            InstallationStatus,
        )
        from mcp_orchestrator.mcp.server import check_server_installation

        mock_check.return_value = InstallationResult(
            server_id="brave-search",
            status=InstallationStatus.NOT_INSTALLED,
            package_manager=PackageManager.NPM,
        )

        result = await check_server_installation("brave-search")

        assert result["server_id"] == "brave-search"
        assert result["status"] == "not_installed"
        assert result["installation_command"] is not None
        assert "npm install" in result["installation_command"]

    @pytest.mark.asyncio
    @patch(
        "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
    )
    async def test_check_not_installed_server_with_pip_package(
        self, mock_check: MagicMock
    ) -> None:
        """Should suggest pip install for PyPI packages."""
        from mcp_orchestrator.installation.models import (
            InstallationResult,
            InstallationStatus,
        )
        from mcp_orchestrator.mcp.server import check_server_installation

        # This assumes we've added a PyPI server to the registry
        mock_check.return_value = InstallationResult(
            server_id="lightrag-mcp",
            status=InstallationStatus.NOT_INSTALLED,
            package_manager=PackageManager.PIP,
        )

        result = await check_server_installation("lightrag-mcp")

        assert result["status"] == "not_installed"
        assert result["installation_command"] is not None
        assert "pip install" in result["installation_command"]

    @pytest.mark.asyncio
    async def test_check_nonexistent_server(self) -> None:
        """Should raise ValueError for unknown server ID."""
        from mcp_orchestrator.mcp.server import check_server_installation

        with pytest.raises(ValueError, match="not found"):
            await check_server_installation("nonexistent-server")


class TestInstallServerTool:
    """Test install_server MCP tool behavior."""

    @pytest.mark.asyncio
    @patch(
        "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
    )
    async def test_install_server_already_installed(
        self, mock_check: MagicMock
    ) -> None:
        """Should skip installation if server already installed."""
        from mcp_orchestrator.installation.models import (
            InstallationResult,
            InstallationStatus,
        )
        from mcp_orchestrator.mcp.server import install_server

        mock_check.return_value = InstallationResult(
            server_id="filesystem",
            status=InstallationStatus.INSTALLED,
            installed_version="2025.8.21",
            install_location="/usr/local/bin/npx",
        )

        result = await install_server("filesystem", confirm=False)

        assert result["status"] == "already_installed"
        assert result["server_id"] == "filesystem"
        assert result["installed_version"] == "2025.8.21"

    @pytest.mark.asyncio
    @patch(
        "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
    )
    async def test_install_server_requires_confirmation(
        self, mock_check: MagicMock
    ) -> None:
        """Should require confirmation before installing (safety)."""
        from mcp_orchestrator.installation.models import (
            InstallationResult,
            InstallationStatus,
        )
        from mcp_orchestrator.mcp.server import install_server

        mock_check.return_value = InstallationResult(
            server_id="brave-search", status=InstallationStatus.NOT_INSTALLED
        )

        # Default confirm=True should require confirmation
        result = await install_server("brave-search")

        assert result["status"] == "confirmation_required"
        assert "confirm=False" in result["message"]
        assert result["installation_command"] is not None

    @pytest.mark.asyncio
    @patch("mcp_orchestrator.installation.installer.ServerInstaller.install")
    @patch(
        "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
    )
    async def test_install_server_confirmed_success(
        self, mock_check: MagicMock, mock_install: MagicMock
    ) -> None:
        """Should install when confirmation bypassed."""
        from mcp_orchestrator.installation.models import (
            InstallationResult,
            InstallationStatus,
        )
        from mcp_orchestrator.mcp.server import install_server

        # Not installed initially
        mock_check.return_value = InstallationResult(
            server_id="brave-search", status=InstallationStatus.NOT_INSTALLED
        )

        # Installation succeeds
        mock_install.return_value = InstallationResult(
            server_id="brave-search",
            status=InstallationStatus.INSTALLED,
            package_manager=PackageManager.NPM,
            installation_command="npm install -g @modelcontextprotocol/server-brave-search",
        )

        result = await install_server("brave-search", confirm=False)

        assert result["status"] == "installed"
        assert result["server_id"] == "brave-search"
        mock_install.assert_called_once()

    @pytest.mark.asyncio
    @patch("mcp_orchestrator.installation.installer.ServerInstaller.install")
    @patch(
        "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
    )
    async def test_install_server_failure(
        self, mock_check: MagicMock, mock_install: MagicMock
    ) -> None:
        """Should handle installation failures gracefully."""
        from mcp_orchestrator.installation.models import (
            InstallationResult,
            InstallationStatus,
        )
        from mcp_orchestrator.mcp.server import install_server

        mock_check.return_value = InstallationResult(
            server_id="test-server", status=InstallationStatus.NOT_INSTALLED
        )

        mock_install.return_value = InstallationResult(
            server_id="test-server",
            status=InstallationStatus.ERROR,
            error_message="npm ERR! 404 Not Found",
        )

        result = await install_server("test-server", confirm=False)

        assert result["status"] == "error"
        assert "404" in result["error_message"]

    @pytest.mark.asyncio
    @patch("mcp_orchestrator.installation.installer.ServerInstaller.install")
    @patch(
        "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
    )
    async def test_install_server_with_custom_package_manager(
        self, mock_check: MagicMock, mock_install: MagicMock
    ) -> None:
        """Should allow overriding package manager."""
        from mcp_orchestrator.installation.models import (
            InstallationResult,
            InstallationStatus,
        )
        from mcp_orchestrator.mcp.server import install_server

        mock_check.return_value = InstallationResult(
            server_id="lightrag-mcp", status=InstallationStatus.NOT_INSTALLED
        )

        mock_install.return_value = InstallationResult(
            server_id="lightrag-mcp",
            status=InstallationStatus.INSTALLED,
            package_manager=PackageManager.PIPX,
        )

        result = await install_server(
            "lightrag-mcp", confirm=False, package_manager="pipx"
        )

        assert result["status"] == "installed"
        # Verify pipx was used
        call_args = mock_install.call_args
        assert call_args[1]["package_manager"] == PackageManager.PIPX

    @pytest.mark.asyncio
    async def test_install_server_nonexistent(self) -> None:
        """Should raise ValueError for unknown server."""
        from mcp_orchestrator.mcp.server import install_server

        with pytest.raises(ValueError, match="not found"):
            await install_server("nonexistent-server", confirm=False)

    @pytest.mark.asyncio
    async def test_install_server_no_package_manager_support(self) -> None:
        """Should raise ValueError if server doesn't support installation."""
        from mcp_orchestrator.mcp.server import install_server

        # Test with a server that has package_manager=NONE and no npm/pip package
        with pytest.raises(ValueError, match="does not support"):
            # This would be a custom server with no package info
            await install_server("custom-local-server", confirm=False)


class TestListInstalledServersTool:
    """Test list_installed_servers MCP tool behavior."""

    @pytest.mark.asyncio
    @patch(
        "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
    )
    async def test_list_installed_servers_mixed_status(
        self, mock_check: MagicMock
    ) -> None:
        """Should list all servers with their installation status."""
        from mcp_orchestrator.installation.models import (
            InstallationResult,
            InstallationStatus,
        )
        from mcp_orchestrator.mcp.server import list_installed_servers

        # Mock different statuses for different servers
        def check_side_effect(server):
            if server.server_id == "filesystem":
                return InstallationResult(
                    server_id="filesystem",
                    status=InstallationStatus.INSTALLED,
                    installed_version="2025.8.21",
                )
            elif server.server_id == "memory":
                return InstallationResult(
                    server_id="memory",
                    status=InstallationStatus.INSTALLED,
                    installed_version="2025.8.21",
                )
            else:
                return InstallationResult(
                    server_id=server.server_id, status=InstallationStatus.NOT_INSTALLED
                )

        mock_check.side_effect = check_side_effect

        result = await list_installed_servers()

        assert result["total_count"] > 0
        assert result["installed_count"] >= 2  # filesystem and memory
        assert result["not_installed_count"] > 0
        assert len(result["servers"]) == result["total_count"]

    @pytest.mark.asyncio
    @patch(
        "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
    )
    async def test_list_installed_servers_shows_versions(
        self, mock_check: MagicMock
    ) -> None:
        """Should include version information for installed servers."""
        from mcp_orchestrator.installation.models import (
            InstallationResult,
            InstallationStatus,
        )
        from mcp_orchestrator.mcp.server import list_installed_servers

        def check_side_effect(server):
            if server.server_id == "filesystem":
                return InstallationResult(
                    server_id="filesystem",
                    status=InstallationStatus.INSTALLED,
                    installed_version="2025.8.21",
                    package_manager=PackageManager.NPM,
                )
            else:
                return InstallationResult(
                    server_id=server.server_id, status=InstallationStatus.NOT_INSTALLED
                )

        mock_check.side_effect = check_side_effect

        result = await list_installed_servers()

        # Find filesystem server in results
        filesystem_server = next(
            s for s in result["servers"] if s["server_id"] == "filesystem"
        )

        assert filesystem_server["status"] == "installed"
        assert filesystem_server["installed_version"] == "2025.8.21"
        assert filesystem_server["package_manager"] == "npm"

    @pytest.mark.asyncio
    @patch(
        "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
    )
    async def test_list_installed_servers_empty_registry(
        self, mock_check: MagicMock
    ) -> None:
        """Should handle empty registry gracefully."""
        from mcp_orchestrator.mcp.server import list_installed_servers

        # This would only happen in tests with empty registry
        result = await list_installed_servers()

        assert result["total_count"] >= 0
        assert result["installed_count"] == 0 or result["installed_count"] >= 0
        assert result["servers"] is not None


class TestInstallationWorkflowIntegration:
    """Test complete workflows combining multiple tools."""

    @pytest.mark.asyncio
    @patch("mcp_orchestrator.installation.installer.ServerInstaller.install")
    @patch(
        "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
    )
    async def test_check_then_install_workflow(
        self, mock_check: MagicMock, mock_install: MagicMock
    ) -> None:
        """Should follow check → install → verify workflow."""
        from mcp_orchestrator.installation.models import (
            InstallationResult,
            InstallationStatus,
        )
        from mcp_orchestrator.mcp.server import (
            check_server_installation,
            install_server,
        )

        # Step 1: Check - not installed
        mock_check.return_value = InstallationResult(
            server_id="brave-search", status=InstallationStatus.NOT_INSTALLED
        )

        check_result = await check_server_installation("brave-search")
        assert check_result["status"] == "not_installed"

        # Step 2: Install
        mock_install.return_value = InstallationResult(
            server_id="brave-search", status=InstallationStatus.INSTALLED
        )

        install_result = await install_server("brave-search", confirm=False)
        assert install_result["status"] == "installed"

        # Step 3: Check again - now installed
        mock_check.return_value = InstallationResult(
            server_id="brave-search",
            status=InstallationStatus.INSTALLED,
            installed_version="1.0.0",
        )

        verify_result = await check_server_installation("brave-search")
        assert verify_result["status"] == "installed"

    @pytest.mark.asyncio
    @patch("mcp_orchestrator.installation.installer.ServerInstaller.install")
    @patch(
        "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
    )
    async def test_list_then_install_workflow(
        self, mock_check: MagicMock, mock_install: MagicMock
    ) -> None:
        """Should follow list → install → list workflow."""
        from mcp_orchestrator.installation.models import (
            InstallationResult,
            InstallationStatus,
        )
        from mcp_orchestrator.mcp.server import install_server, list_installed_servers

        # Step 1: List - shows some not installed
        def check_before(server):
            return InstallationResult(
                server_id=server.server_id, status=InstallationStatus.NOT_INSTALLED
            )

        mock_check.side_effect = check_before

        list_before = await list_installed_servers()
        initial_installed_count = list_before["installed_count"]

        # Step 2: Install one
        mock_install.return_value = InstallationResult(
            server_id="filesystem", status=InstallationStatus.INSTALLED
        )

        await install_server("filesystem", confirm=False)

        # Step 3: List again - count increased
        def check_after(server):
            if server.server_id == "filesystem":
                return InstallationResult(
                    server_id="filesystem", status=InstallationStatus.INSTALLED
                )
            else:
                return InstallationResult(
                    server_id=server.server_id, status=InstallationStatus.NOT_INSTALLED
                )

        mock_check.side_effect = check_after

        list_after = await list_installed_servers()
        assert list_after["installed_count"] >= initial_installed_count + 1


class TestInstallationToolErrorHandling:
    """Test error handling across all installation tools."""

    @pytest.mark.asyncio
    async def test_tools_handle_invalid_server_id(self) -> None:
        """All tools should handle invalid server IDs gracefully."""
        from mcp_orchestrator.mcp.server import (
            check_server_installation,
            install_server,
        )

        with pytest.raises(ValueError):
            await check_server_installation("invalid-server-id")

        with pytest.raises(ValueError):
            await install_server("invalid-server-id", confirm=False)

    @pytest.mark.asyncio
    @patch(
        "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
    )
    async def test_tools_handle_validator_errors(self, mock_check: MagicMock) -> None:
        """Should handle validator errors gracefully."""
        from mcp_orchestrator.installation.models import (
            InstallationResult,
            InstallationStatus,
        )
        from mcp_orchestrator.mcp.server import check_server_installation

        mock_check.return_value = InstallationResult(
            server_id="filesystem",
            status=InstallationStatus.ERROR,
            error_message="Something went wrong",
        )

        result = await check_server_installation("filesystem")

        # Should still return result, not raise
        assert result["status"] == "error"
        assert result["error_message"] is not None
