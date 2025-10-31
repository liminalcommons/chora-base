"""Data models for installation operations.

Wave 2.2/3.0 - Automatic Server Installation
"""

from enum import Enum

from pydantic import BaseModel, Field

from mcp_orchestrator.servers.models import PackageManager


class InstallationStatus(str, Enum):
    """Installation status for an MCP server."""

    INSTALLED = "installed"
    NOT_INSTALLED = "not_installed"
    UNKNOWN = "unknown"
    ERROR = "error"


class InstallationResult(BaseModel):
    """Result of installation check or install operation."""

    server_id: str = Field(description="Server identifier")
    status: InstallationStatus = Field(description="Installation status")
    installed_version: str | None = Field(
        default=None, description="Installed version if available"
    )
    install_location: str | None = Field(
        default=None, description="Path to installed binary/command"
    )
    package_manager: PackageManager | None = Field(
        default=None, description="Package manager used or available"
    )
    error_message: str | None = Field(
        default=None, description="Error message if status is ERROR"
    )
    installation_command: str | None = Field(
        default=None, description="Installation command that was or should be executed"
    )


class PackageInfo(BaseModel):
    """Package metadata from registry (npm or PyPI)."""

    package_name: str = Field(description="Package name")
    latest_version: str = Field(description="Latest available version")
    description: str | None = Field(default=None, description="Package description")
    homepage: str | None = Field(default=None, description="Package homepage URL")
    repository: str | None = Field(default=None, description="Source repository URL")
