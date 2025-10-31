"""Models for MCP server definitions.

This module defines the schema for MCP server metadata, including transport
configuration, parameters, and documentation.
"""

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class TransportType(str, Enum):
    """MCP server transport type."""

    STDIO = "stdio"
    HTTP = "http"
    SSE = "sse"  # Server-Sent Events (HTTP streaming)


class PackageManager(str, Enum):
    """Package manager for server installation.

    Wave 2.2/3.0 - Automatic Server Installation
    """

    NPM = "npm"
    PIP = "pip"
    PIPX = "pipx"
    UVX = "uvx"
    CUSTOM = "custom"
    NONE = "none"  # No package manager (local script, binary, etc.)


class ParameterDefinition(BaseModel):
    """Definition of a server configuration parameter."""

    name: str = Field(description="Parameter name")
    type: Literal["string", "int", "bool", "path"] = Field(
        description="Parameter data type"
    )
    description: str = Field(description="Human-readable description")
    required: bool = Field(default=False, description="Whether parameter is required")
    default: Any | None = Field(
        default=None, description="Default value if not provided"
    )
    example: str | None = Field(default=None, description="Example value")


class ServerDefinition(BaseModel):
    """Definition of an MCP server that can be registered.

    This model describes a server's metadata, transport configuration,
    and parameters. Servers can use stdio (local process) or HTTP/SSE
    (remote server) transports.

    For HTTP/SSE servers, the orchestrator will automatically wrap them
    with mcp-remote to provide stdio compatibility for clients.
    """

    server_id: str = Field(
        description="Unique server identifier (e.g., 'filesystem', 'n8n')"
    )
    display_name: str = Field(description="Human-readable server name")
    description: str = Field(description="Server purpose and capabilities")

    # Transport configuration
    transport: TransportType = Field(description="Transport type")

    # For stdio servers
    stdio_command: str | None = Field(
        default=None, description="Command to execute (e.g., 'npx', 'python')"
    )
    stdio_args: list[str] = Field(
        default_factory=list,
        description="Command-line arguments (may contain {param} placeholders)",
    )

    # For HTTP/SSE servers (will be wrapped with mcp-remote)
    http_url: str | None = Field(
        default=None,
        description="HTTP/SSE endpoint URL (may contain {param} placeholders)",
    )
    http_auth_type: Literal["none", "bearer", "oauth"] | None = Field(
        default=None, description="Authentication type for HTTP servers"
    )

    # Environment variables
    required_env: list[str] = Field(
        default_factory=list, description="Required environment variable names"
    )
    optional_env: list[str] = Field(
        default_factory=list, description="Optional environment variable names"
    )

    # Configuration parameters
    parameters: list[ParameterDefinition] = Field(
        default_factory=list, description="User-configurable parameters"
    )

    # Metadata
    documentation_url: str | None = Field(
        default=None, description="URL to server documentation"
    )
    npm_package: str | None = Field(
        default=None, description="NPM package name if installable via npm"
    )
    tags: list[str] = Field(
        default_factory=list, description="Tags for categorization (e.g., 'search', 'database')"
    )

    # Package installation (Wave 2.2/3.0)
    pypi_package: str | None = Field(
        default=None, description="PyPI package name if installable via pip/pipx/uvx"
    )
    package_manager: PackageManager = Field(
        default=PackageManager.NONE,
        description="Preferred package manager for installation"
    )
    install_command: str | None = Field(
        default=None,
        description="Custom installation command (if package_manager=CUSTOM)"
    )

    model_config = ConfigDict(use_enum_values=True)
