"""Tests for installation validation.

BDD tests for checking if MCP servers are installed on the system.

Wave 2.2/3.0 - Automatic Server Installation
"""

from unittest.mock import MagicMock, patch

import pytest
from mcp_orchestrator.installation.models import InstallationStatus
from mcp_orchestrator.servers.models import (
    PackageManager,
    ServerDefinition,
    TransportType,
)

# Import will fail until we implement the module - that's expected in BDD
pytest.importorskip(
    "mcp_orchestrator.installation", reason="Module not yet implemented"
)


class TestInstallationValidator:
    """Test validation of server installation status."""

    @patch("shutil.which")
    def test_check_installation_installed(self, mock_which: MagicMock) -> None:
        """Should detect when a server is installed."""
        from mcp_orchestrator.installation.models import InstallationStatus
        from mcp_orchestrator.installation.validator import InstallationValidator

        mock_which.return_value = "/usr/local/bin/npx"

        server = ServerDefinition(
            server_id="filesystem",
            display_name="Filesystem",
            description="File access",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-filesystem"],
            package_manager=PackageManager.NPM,
            npm_package="@modelcontextprotocol/server-filesystem",
        )

        validator = InstallationValidator()
        result = validator.check_installation(server)

        assert result.status == InstallationStatus.INSTALLED
        assert result.server_id == "filesystem"
        assert result.install_location == "/usr/local/bin/npx"

    @patch("shutil.which")
    def test_check_installation_not_installed(self, mock_which: MagicMock) -> None:
        """Should detect when a server is not installed."""
        from mcp_orchestrator.installation.models import InstallationStatus
        from mcp_orchestrator.installation.validator import InstallationValidator

        mock_which.return_value = None

        server = ServerDefinition(
            server_id="custom-server",
            display_name="Custom Server",
            description="Custom",
            transport=TransportType.STDIO,
            stdio_command="custom-binary",
            package_manager=PackageManager.NONE,
        )

        validator = InstallationValidator()
        result = validator.check_installation(server)

        assert result.status == InstallationStatus.NOT_INSTALLED
        assert result.server_id == "custom-server"
        assert result.install_location is None

    @patch("shutil.which")
    def test_check_installation_unknown_no_command(self, mock_which: MagicMock) -> None:
        """Should return unknown status when server has no stdio_command."""
        from mcp_orchestrator.installation.models import InstallationStatus
        from mcp_orchestrator.installation.validator import InstallationValidator

        server = ServerDefinition(
            server_id="http-server",
            display_name="HTTP Server",
            description="HTTP based",
            transport=TransportType.HTTP,
            http_url="http://localhost:8080",
            package_manager=PackageManager.NONE,
        )

        validator = InstallationValidator()
        result = validator.check_installation(server)

        assert result.status == InstallationStatus.UNKNOWN
        assert "No stdio_command" in result.error_message

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_check_installation_with_version(
        self, mock_run: MagicMock, mock_which: MagicMock
    ) -> None:
        """Should extract version information when available."""
        from mcp_orchestrator.installation.models import InstallationStatus
        from mcp_orchestrator.installation.validator import InstallationValidator

        mock_which.return_value = "/usr/local/bin/npm"
        mock_run.return_value = MagicMock(returncode=0, stdout="npm version 9.8.1\n")

        server = ServerDefinition(
            server_id="test",
            display_name="Test",
            description="Test",
            transport=TransportType.STDIO,
            stdio_command="npm",
            package_manager=PackageManager.NPM,
        )

        validator = InstallationValidator()
        result = validator.check_installation(server)

        assert result.status == InstallationStatus.INSTALLED
        assert result.installed_version is not None
        assert (
            "9.8.1" in result.installed_version
            or "npm version" in result.installed_version
        )

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_get_version_multiple_flags(
        self, mock_run: MagicMock, mock_which: MagicMock
    ) -> None:
        """Should try multiple version flags to extract version."""
        from mcp_orchestrator.installation.validator import InstallationValidator

        mock_which.return_value = "/usr/bin/python"

        # First flag fails, second succeeds
        mock_run.side_effect = [
            MagicMock(returncode=1, stdout=""),  # --version fails
            MagicMock(returncode=0, stdout="Python 3.12.0\n"),  # -V succeeds
        ]

        server = ServerDefinition(
            server_id="python-server",
            display_name="Python Server",
            description="Python",
            transport=TransportType.STDIO,
            stdio_command="python",
            package_manager=PackageManager.PIP,
        )

        validator = InstallationValidator()
        result = validator.check_installation(server)

        # Should have tried multiple flags and found version
        assert mock_run.call_count >= 1
        assert result.installed_version is not None

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_get_version_timeout_handling(
        self, mock_run: MagicMock, mock_which: MagicMock
    ) -> None:
        """Should handle timeout when getting version gracefully."""
        import subprocess

        from mcp_orchestrator.installation.validator import InstallationValidator

        mock_which.return_value = "/usr/bin/slow-command"
        mock_run.side_effect = subprocess.TimeoutExpired("cmd", 5)

        server = ServerDefinition(
            server_id="slow-server",
            display_name="Slow Server",
            description="Slow",
            transport=TransportType.STDIO,
            stdio_command="slow-command",
            package_manager=PackageManager.NONE,
        )

        validator = InstallationValidator()
        result = validator.check_installation(server)

        # Should still report as installed, just without version
        assert result.status == InstallationStatus.INSTALLED
        assert result.installed_version is None


class TestInstallationValidatorBatchOperations:
    """Test batch validation of multiple servers."""

    @patch("shutil.which")
    def test_check_multiple_servers(self, mock_which: MagicMock) -> None:
        """Should correctly check installation status of multiple servers."""
        from mcp_orchestrator.installation.models import InstallationStatus
        from mcp_orchestrator.installation.validator import InstallationValidator

        # npm is installed, python is not
        def which_mock(cmd: str) -> str | None:
            if cmd == "npx":
                return "/usr/local/bin/npx"
            elif cmd == "npm":
                return "/usr/local/bin/npm"
            else:
                return None

        mock_which.side_effect = which_mock

        servers = [
            ServerDefinition(
                server_id="filesystem",
                display_name="Filesystem",
                description="File access",
                transport=TransportType.STDIO,
                stdio_command="npx",
                package_manager=PackageManager.NPM,
            ),
            ServerDefinition(
                server_id="python-server",
                display_name="Python Server",
                description="Python",
                transport=TransportType.STDIO,
                stdio_command="python-custom",
                package_manager=PackageManager.PIP,
            ),
        ]

        validator = InstallationValidator()
        results = [validator.check_installation(server) for server in servers]

        assert results[0].status == InstallationStatus.INSTALLED
        assert results[1].status == InstallationStatus.NOT_INSTALLED


class TestInstallationValidatorEdgeCases:
    """Test edge cases and error conditions."""

    @patch("shutil.which")
    def test_check_installation_with_symlink(self, mock_which: MagicMock) -> None:
        """Should handle symlinked binaries correctly."""
        from mcp_orchestrator.installation.models import InstallationStatus
        from mcp_orchestrator.installation.validator import InstallationValidator

        # Symlink path
        mock_which.return_value = "/usr/local/bin/node -> /opt/node/bin/node"

        server = ServerDefinition(
            server_id="node-server",
            display_name="Node Server",
            description="Node",
            transport=TransportType.STDIO,
            stdio_command="node",
            package_manager=PackageManager.NPM,
        )

        validator = InstallationValidator()
        result = validator.check_installation(server)

        assert result.status == InstallationStatus.INSTALLED

    @patch("shutil.which")
    def test_check_installation_empty_command(self, mock_which: MagicMock) -> None:
        """Should handle empty stdio_command gracefully."""
        from mcp_orchestrator.installation.models import InstallationStatus
        from mcp_orchestrator.installation.validator import InstallationValidator

        server = ServerDefinition(
            server_id="empty-server",
            display_name="Empty Server",
            description="Empty",
            transport=TransportType.STDIO,
            stdio_command="",  # Empty string
            package_manager=PackageManager.NONE,
        )

        validator = InstallationValidator()
        result = validator.check_installation(server)

        # Should handle gracefully, not crash
        assert result.status in [
            InstallationStatus.UNKNOWN,
            InstallationStatus.NOT_INSTALLED,
        ]
