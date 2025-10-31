"""Server installer for executing package installations.

Wave 2.2/3.0 - Automatic Server Installation
"""

import subprocess

from mcp_orchestrator.installation.models import (
    InstallationResult,
    InstallationStatus,
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
        timeout: int = 300,  # 5 minutes
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
            cmd = self.detector.get_install_command(package_manager, package_name)
        except ValueError as e:
            return InstallationResult(
                server_id=server_id,
                status=InstallationStatus.ERROR,
                error_message=str(e),
            )

        # Convert command list to string for display
        cmd_string = " ".join(cmd)

        # Dry run mode
        if self.dry_run:
            return InstallationResult(
                server_id=server_id,
                status=InstallationStatus.INSTALLED,
                installation_command=cmd_string,
                error_message="Dry run - installation not executed",
            )

        # Execute installation
        try:
            subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout, check=True
            )

            return InstallationResult(
                server_id=server_id,
                status=InstallationStatus.INSTALLED,
                package_manager=package_manager,
                installation_command=cmd_string,
            )

        except subprocess.CalledProcessError as e:
            # Installation failed
            error_msg = (
                f"Installation failed: {e.stderr}"
                if e.stderr
                else "Installation failed"
            )
            return InstallationResult(
                server_id=server_id,
                status=InstallationStatus.ERROR,
                error_message=error_msg,
                installation_command=cmd_string,
            )

        except subprocess.TimeoutExpired:
            return InstallationResult(
                server_id=server_id,
                status=InstallationStatus.ERROR,
                error_message=f"Installation timed out after {timeout}s",
                installation_command=cmd_string,
            )
