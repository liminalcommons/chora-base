"""Installation validation for MCP servers.

Wave 2.2/3.0 - Automatic Server Installation
"""

import shutil
import subprocess
from typing import Optional

from mcp_orchestrator.installation.models import (
    InstallationResult,
    InstallationStatus,
)
from mcp_orchestrator.servers.models import PackageManager, ServerDefinition


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

        # Handle empty command
        if not command_to_check or not command_to_check.strip():
            return InstallationResult(
                server_id=server.server_id,
                status=InstallationStatus.UNKNOWN,
                error_message="stdio_command is empty"
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
                    # Return first line of output
                    return result.stdout.strip().split("\n")[0]
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
            except Exception:
                # Catch any other errors and continue trying
                continue

        return None
