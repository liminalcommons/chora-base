"""Package manager detection and command generation.

Wave 2.2/3.0 - Automatic Server Installation
"""

import shutil
from typing import List

from mcp_orchestrator.servers.models import PackageManager


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

        # Check pip (try both pip and pip3)
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

        Raises:
            ValueError: If package_manager is unsupported
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
