"""Client family registry for MCP orchestration.

This module provides the registry of supported MCP client families and their
configurations, capabilities, and profiles.
"""

__all__ = ["ClientRegistry", "get_default_registry"]

from .clients import ClientRegistry, get_default_registry
