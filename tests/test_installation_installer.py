"""Tests for server installer.

BDD tests for executing package installations.

Wave 2.2/3.0 - Automatic Server Installation
"""

import subprocess
from unittest.mock import MagicMock, patch

import pytest
from mcp_orchestrator.servers.models import PackageManager

# Import will fail until we implement the module - that's expected in BDD
pytest.importorskip(
    "mcp_orchestrator.installation", reason="Module not yet implemented"
)


class TestServerInstaller:
    """Test server installation execution."""

    @patch("subprocess.run")
    def test_install_npm_package_success(self, mock_run: MagicMock) -> None:
        """Should successfully install npm package."""
        from mcp_orchestrator.installation.installer import ServerInstaller
        from mcp_orchestrator.installation.models import InstallationStatus

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="+ @modelcontextprotocol/server-filesystem@2025.8.21\n",
            stderr="",
        )

        installer = ServerInstaller(dry_run=False)
        result = installer.install(
            package_manager=PackageManager.NPM,
            package_name="@modelcontextprotocol/server-filesystem",
            server_id="filesystem",
        )

        assert result.status == InstallationStatus.INSTALLED
        assert result.server_id == "filesystem"
        assert result.package_manager == PackageManager.NPM
        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_install_pip_package_success(self, mock_run: MagicMock) -> None:
        """Should successfully install pip package."""
        from mcp_orchestrator.installation.installer import ServerInstaller
        from mcp_orchestrator.installation.models import InstallationStatus

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Successfully installed lightrag-mcp-0.1.0\n",
            stderr="",
        )

        installer = ServerInstaller(dry_run=False)
        result = installer.install(
            package_manager=PackageManager.PIP,
            package_name="lightrag-mcp",
            server_id="lightrag-mcp",
        )

        assert result.status == InstallationStatus.INSTALLED
        assert result.server_id == "lightrag-mcp"
        mock_run.assert_called_once()

        # Verify pip command was called correctly
        call_args = mock_run.call_args[0][0]
        assert "pip" in call_args
        assert "install" in call_args
        assert "lightrag-mcp" in call_args

    @patch("subprocess.run")
    def test_install_failure_package_not_found(self, mock_run: MagicMock) -> None:
        """Should handle package not found error."""
        from mcp_orchestrator.installation.installer import ServerInstaller
        from mcp_orchestrator.installation.models import InstallationStatus

        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=["npm", "install", "-g", "nonexistent-package"],
            stderr="npm ERR! 404 Not Found",
        )

        installer = ServerInstaller(dry_run=False)
        result = installer.install(
            package_manager=PackageManager.NPM,
            package_name="nonexistent-package",
            server_id="nonexistent",
        )

        assert result.status == InstallationStatus.ERROR
        assert "404" in result.error_message or "failed" in result.error_message.lower()

    @patch("subprocess.run")
    def test_install_timeout_error(self, mock_run: MagicMock) -> None:
        """Should handle installation timeout."""
        from mcp_orchestrator.installation.installer import ServerInstaller
        from mcp_orchestrator.installation.models import InstallationStatus

        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd=["pip", "install", "slow-package"], timeout=300
        )

        installer = ServerInstaller(dry_run=False)
        result = installer.install(
            package_manager=PackageManager.PIP,
            package_name="slow-package",
            server_id="slow",
            timeout=300,
        )

        assert result.status == InstallationStatus.ERROR
        assert "timed out" in result.error_message.lower()

    @patch("subprocess.run")
    def test_install_network_error(self, mock_run: MagicMock) -> None:
        """Should handle network errors gracefully."""
        from mcp_orchestrator.installation.installer import ServerInstaller
        from mcp_orchestrator.installation.models import InstallationStatus

        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=["npm", "install", "-g", "package"],
            stderr="npm ERR! network request failed",
        )

        installer = ServerInstaller(dry_run=False)
        result = installer.install(
            package_manager=PackageManager.NPM, package_name="package", server_id="test"
        )

        assert result.status == InstallationStatus.ERROR
        assert (
            "network" in result.error_message.lower()
            or "failed" in result.error_message.lower()
        )


class TestServerInstallerDryRun:
    """Test dry-run mode for safe simulation."""

    def test_dry_run_mode_does_not_execute(self) -> None:
        """Dry run should not execute actual installation."""
        from mcp_orchestrator.installation.installer import ServerInstaller
        from mcp_orchestrator.installation.models import InstallationStatus

        installer = ServerInstaller(dry_run=True)
        result = installer.install(
            package_manager=PackageManager.NPM,
            package_name="test-package",
            server_id="test",
        )

        # Should return success but indicate dry run
        assert result.status == InstallationStatus.INSTALLED
        assert "Dry run" in result.error_message
        assert result.installation_command is not None

    def test_dry_run_generates_correct_command(self) -> None:
        """Dry run should show what command would be executed."""
        from mcp_orchestrator.installation.installer import ServerInstaller

        installer = ServerInstaller(dry_run=True)
        result = installer.install(
            package_manager=PackageManager.PIP,
            package_name="lightrag-mcp",
            server_id="lightrag",
        )

        assert "pip install lightrag-mcp" in result.installation_command


class TestServerInstallerCustomTimeout:
    """Test custom timeout configuration."""

    @patch("subprocess.run")
    def test_custom_timeout_respected(self, mock_run: MagicMock) -> None:
        """Should respect custom timeout value."""
        from mcp_orchestrator.installation.installer import ServerInstaller

        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        installer = ServerInstaller(dry_run=False)
        installer.install(
            package_manager=PackageManager.NPM,
            package_name="test-package",
            server_id="test",
            timeout=600,  # 10 minutes
        )

        # Check that subprocess.run was called with correct timeout
        call_kwargs = mock_run.call_args[1]
        assert call_kwargs["timeout"] == 600


class TestServerInstallerPackageManagerSupport:
    """Test support for different package managers."""

    @patch("subprocess.run")
    def test_install_with_pipx(self, mock_run: MagicMock) -> None:
        """Should install using pipx correctly."""
        from mcp_orchestrator.installation.installer import ServerInstaller
        from mcp_orchestrator.installation.models import InstallationStatus

        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        installer = ServerInstaller(dry_run=False)
        result = installer.install(
            package_manager=PackageManager.PIPX,
            package_name="lightrag-mcp",
            server_id="lightrag",
        )

        assert result.status == InstallationStatus.INSTALLED

        # Verify pipx command
        call_args = mock_run.call_args[0][0]
        assert "pipx" in call_args
        assert "install" in call_args

    @patch("subprocess.run")
    def test_install_with_uvx(self, mock_run: MagicMock) -> None:
        """Should install using uvx correctly."""
        from mcp_orchestrator.installation.installer import ServerInstaller
        from mcp_orchestrator.installation.models import InstallationStatus

        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        installer = ServerInstaller(dry_run=False)
        result = installer.install(
            package_manager=PackageManager.UVX,
            package_name="lightrag-mcp",
            server_id="lightrag",
        )

        assert result.status == InstallationStatus.INSTALLED

        # Verify uvx command (uvx just runs the package directly)
        call_args = mock_run.call_args[0][0]
        assert "uvx" in call_args
        assert "lightrag-mcp" in call_args

    def test_install_unsupported_package_manager(self) -> None:
        """Should reject unsupported package managers."""
        from mcp_orchestrator.installation.installer import ServerInstaller
        from mcp_orchestrator.installation.models import InstallationStatus

        installer = ServerInstaller(dry_run=False)
        result = installer.install(
            package_manager=PackageManager.CUSTOM, package_name="test", server_id="test"
        )

        assert result.status == InstallationStatus.ERROR
        assert (
            "Unsupported" in result.error_message
            or "not supported" in result.error_message.lower()
        )


class TestServerInstallerCommandGeneration:
    """Test installation command generation."""

    @patch("subprocess.run")
    def test_npm_global_install_command(self, mock_run: MagicMock) -> None:
        """Should generate npm -g install command."""
        from mcp_orchestrator.installation.installer import ServerInstaller

        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        installer = ServerInstaller(dry_run=False)
        installer.install(
            package_manager=PackageManager.NPM,
            package_name="@modelcontextprotocol/server-filesystem",
            server_id="filesystem",
        )

        call_args = mock_run.call_args[0][0]
        assert call_args == [
            "npm",
            "install",
            "-g",
            "@modelcontextprotocol/server-filesystem",
        ]

    @patch("subprocess.run")
    def test_installation_command_in_result(self, mock_run: MagicMock) -> None:
        """Should include installation command in result."""
        from mcp_orchestrator.installation.installer import ServerInstaller

        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        installer = ServerInstaller(dry_run=False)
        result = installer.install(
            package_manager=PackageManager.PIP,
            package_name="lightrag-mcp",
            server_id="lightrag",
        )

        assert result.installation_command is not None
        assert "pip install lightrag-mcp" in result.installation_command


class TestServerInstallerErrorHandling:
    """Test error handling and edge cases."""

    @patch("subprocess.run")
    def test_install_with_permission_error(self, mock_run: MagicMock) -> None:
        """Should handle permission denied errors."""
        from mcp_orchestrator.installation.installer import ServerInstaller
        from mcp_orchestrator.installation.models import InstallationStatus

        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=["npm", "install", "-g", "package"],
            stderr="npm ERR! EACCES: permission denied",
        )

        installer = ServerInstaller(dry_run=False)
        result = installer.install(
            package_manager=PackageManager.NPM, package_name="package", server_id="test"
        )

        assert result.status == InstallationStatus.ERROR
        assert (
            "permission" in result.error_message.lower()
            or "EACCES" in result.error_message
        )

    @patch("subprocess.run")
    def test_install_with_disk_space_error(self, mock_run: MagicMock) -> None:
        """Should handle disk space errors."""
        from mcp_orchestrator.installation.installer import ServerInstaller
        from mcp_orchestrator.installation.models import InstallationStatus

        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=["pip", "install", "package"],
            stderr="OSError: [Errno 28] No space left on device",
        )

        installer = ServerInstaller(dry_run=False)
        result = installer.install(
            package_manager=PackageManager.PIP, package_name="package", server_id="test"
        )

        assert result.status == InstallationStatus.ERROR
        assert (
            "space" in result.error_message.lower()
            or "No space" in result.error_message
        )
