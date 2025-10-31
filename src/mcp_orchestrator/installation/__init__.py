"""Installation module for automatic MCP server installation.

This module provides functionality for detecting, validating, and installing
MCP servers from npm and PyPI package registries.

Wave 2.2/3.0 - Automatic Server Installation

Components:
- models: InstallationResult, InstallationStatus, PackageInfo
- package_manager: Package manager detection and command generation
- validator: Installation status checking and version detection
- installer: Package installation execution with safety checks
"""

from mcp_orchestrator.installation.models import (
    InstallationResult,
    InstallationStatus,
    PackageInfo,
)

__all__ = [
    "InstallationResult",
    "InstallationStatus",
    "PackageInfo",
]
