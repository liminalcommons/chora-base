"""MCP server registry and definitions.

This module provides a registry of known MCP servers that can be added to
client configurations. It handles server discovery, metadata, and transport
abstraction (stdio vs HTTP/SSE).

Wave 1.1 (v0.1.1):
- Server definition models
- Server registry with lookup
- Default catalog of common servers
"""

from mcp_orchestrator.servers.models import (
    PackageManager,
    ParameterDefinition,
    ServerDefinition,
    TransportType,
)
from mcp_orchestrator.servers.registry import ServerRegistry, get_default_registry

__all__ = [
    "TransportType",
    "PackageManager",
    "ParameterDefinition",
    "ServerDefinition",
    "ServerRegistry",
    "get_default_registry",
]
