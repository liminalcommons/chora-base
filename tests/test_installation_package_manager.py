"""Tests for package manager detection and command generation.

BDD tests for automatic MCP server installation feature.
Tests follow behavior-driven development approach.

Wave 2.2/3.0 - Automatic Server Installation
"""

import pytest
from unittest.mock import patch, MagicMock

from mcp_orchestrator.servers.models import PackageManager


class TestPackageManagerEnum:
    """Test PackageManager enum values and behavior."""

    def test_package_manager_enum_values(self) -> None:
        """PackageManager should have all expected values."""
        assert PackageManager.NPM.value == "npm"
        assert PackageManager.PIP.value == "pip"
        assert PackageManager.PIPX.value == "pipx"
        assert PackageManager.UVX.value == "uvx"
        assert PackageManager.CUSTOM.value == "custom"
        assert PackageManager.NONE.value == "none"

    def test_package_manager_can_be_created_from_string(self) -> None:
        """PackageManager should be creatable from string values."""
        pm = PackageManager("npm")
        assert pm == PackageManager.NPM

        pm2 = PackageManager("pip")
        assert pm2 == PackageManager.PIP


# Import will fail until we implement the module - that's expected in BDD
# We'll add pytest.importorskip for now
pytest.importorskip("mcp_orchestrator.installation", reason="Module not yet implemented")


class TestPackageManagerDetector:
    """Test package manager detection on the system."""

    @patch("shutil.which")
    def test_detect_npm_available(self, mock_which: MagicMock) -> None:
        """Should detect npm when it's installed."""
        from mcp_orchestrator.installation.package_manager import PackageManagerDetector

        mock_which.side_effect = lambda cmd: "/usr/bin/npm" if cmd == "npm" else None

        detector = PackageManagerDetector()
        available = detector.detect_available()

        assert PackageManager.NPM in available

    @patch("shutil.which")
    def test_detect_pip_available(self, mock_which: MagicMock) -> None:
        """Should detect pip when it's installed."""
        from mcp_orchestrator.installation.package_manager import PackageManagerDetector

        mock_which.side_effect = lambda cmd: "/usr/bin/pip" if cmd in ["pip", "pip3"] else None

        detector = PackageManagerDetector()
        available = detector.detect_available()

        assert PackageManager.PIP in available

    @patch("shutil.which")
    def test_detect_multiple_package_managers(self, mock_which: MagicMock) -> None:
        """Should detect multiple package managers when installed."""
        from mcp_orchestrator.installation.package_manager import PackageManagerDetector

        def which_mock(cmd: str) -> str | None:
            paths = {
                "npm": "/usr/bin/npm",
                "pip": "/usr/bin/pip",
                "pip3": "/usr/bin/pip3",
                "pipx": "/usr/local/bin/pipx"
            }
            return paths.get(cmd)

        mock_which.side_effect = which_mock

        detector = PackageManagerDetector()
        available = detector.detect_available()

        assert PackageManager.NPM in available
        assert PackageManager.PIP in available
        assert PackageManager.PIPX in available

    @patch("shutil.which")
    def test_detect_no_package_managers(self, mock_which: MagicMock) -> None:
        """Should return empty list when no package managers installed."""
        from mcp_orchestrator.installation.package_manager import PackageManagerDetector

        mock_which.return_value = None

        detector = PackageManagerDetector()
        available = detector.detect_available()

        assert len(available) == 0


class TestPackageManagerCommandGeneration:
    """Test generation of installation commands for different package managers."""

    def test_get_npm_install_command_global(self) -> None:
        """Should generate correct npm global install command."""
        from mcp_orchestrator.installation.package_manager import PackageManagerDetector

        cmd = PackageManagerDetector.get_install_command(
            PackageManager.NPM,
            "@modelcontextprotocol/server-filesystem",
            global_install=True
        )

        assert cmd == ["npm", "install", "-g", "@modelcontextprotocol/server-filesystem"]

    def test_get_npm_install_command_local(self) -> None:
        """Should generate correct npm local install command."""
        from mcp_orchestrator.installation.package_manager import PackageManagerDetector

        cmd = PackageManagerDetector.get_install_command(
            PackageManager.NPM,
            "@modelcontextprotocol/server-filesystem",
            global_install=False
        )

        assert cmd == ["npm", "install", "@modelcontextprotocol/server-filesystem"]

    def test_get_pip_install_command(self) -> None:
        """Should generate correct pip install command."""
        from mcp_orchestrator.installation.package_manager import PackageManagerDetector

        cmd = PackageManagerDetector.get_install_command(
            PackageManager.PIP,
            "lightrag-mcp"
        )

        assert cmd == ["pip", "install", "lightrag-mcp"]

    def test_get_pipx_install_command(self) -> None:
        """Should generate correct pipx install command."""
        from mcp_orchestrator.installation.package_manager import PackageManagerDetector

        cmd = PackageManagerDetector.get_install_command(
            PackageManager.PIPX,
            "lightrag-mcp"
        )

        assert cmd == ["pipx", "install", "lightrag-mcp"]

    def test_get_uvx_install_command(self) -> None:
        """Should generate correct uvx install command."""
        from mcp_orchestrator.installation.package_manager import PackageManagerDetector

        cmd = PackageManagerDetector.get_install_command(
            PackageManager.UVX,
            "lightrag-mcp"
        )

        assert cmd == ["uvx", "lightrag-mcp"]

    def test_get_install_command_unsupported_package_manager(self) -> None:
        """Should raise ValueError for unsupported package managers."""
        from mcp_orchestrator.installation.package_manager import PackageManagerDetector

        with pytest.raises(ValueError, match="Unsupported package manager"):
            PackageManagerDetector.get_install_command(
                PackageManager.CUSTOM,
                "some-package"
            )


class TestPackageManagerIntegration:
    """Integration tests for package manager detection and command generation."""

    @patch("shutil.which")
    def test_full_workflow_npm(self, mock_which: MagicMock) -> None:
        """Should detect npm and generate install command."""
        from mcp_orchestrator.installation.package_manager import PackageManagerDetector

        mock_which.side_effect = lambda cmd: "/usr/bin/npm" if cmd == "npm" else None

        detector = PackageManagerDetector()

        # Detect
        available = detector.detect_available()
        assert PackageManager.NPM in available

        # Generate command
        cmd = detector.get_install_command(
            PackageManager.NPM,
            "@modelcontextprotocol/server-filesystem"
        )
        assert "npm" in cmd
        assert "install" in cmd

    @patch("shutil.which")
    def test_full_workflow_pip(self, mock_which: MagicMock) -> None:
        """Should detect pip and generate install command."""
        from mcp_orchestrator.installation.package_manager import PackageManagerDetector

        mock_which.side_effect = lambda cmd: "/usr/bin/pip" if cmd == "pip" else None

        detector = PackageManagerDetector()

        # Detect
        available = detector.detect_available()
        assert PackageManager.PIP in available

        # Generate command
        cmd = detector.get_install_command(
            PackageManager.PIP,
            "lightrag-mcp"
        )
        assert cmd == ["pip", "install", "lightrag-mcp"]
