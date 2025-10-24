"""Server registry for managing MCP server definitions.

This module provides the ServerRegistry class which manages a catalog of
known MCP servers and provides lookup/search functionality.
"""

from typing import Any

from mcp_orchestrator.servers.models import ServerDefinition, TransportType


class ServerNotFoundError(Exception):
    """Raised when a server is not found in the registry."""

    pass


class ServerRegistry:
    """Registry of known MCP servers.

    The registry maintains a catalog of server definitions and provides
    methods for discovery, lookup, and search.
    """

    def __init__(self, servers: list[ServerDefinition] | None = None) -> None:
        """Initialize registry with server definitions.

        Args:
            servers: List of ServerDefinition objects (defaults to empty list)
        """
        self._servers: dict[str, ServerDefinition] = {}
        if servers:
            for server in servers:
                self.register(server)

    def register(self, server: ServerDefinition) -> None:
        """Register a server definition.

        Args:
            server: ServerDefinition to register

        Raises:
            ValueError: If server_id already registered
        """
        if server.server_id in self._servers:
            raise ValueError(
                f"Server '{server.server_id}' is already registered. "
                "Use update() to modify existing servers."
            )
        self._servers[server.server_id] = server

    def update(self, server: ServerDefinition) -> None:
        """Update an existing server definition.

        Args:
            server: ServerDefinition with updated data

        Raises:
            ServerNotFoundError: If server_id not found
        """
        if server.server_id not in self._servers:
            raise ServerNotFoundError(
                f"Server '{server.server_id}' not found. Use register() to add new servers."
            )
        self._servers[server.server_id] = server

    def unregister(self, server_id: str) -> None:
        """Remove a server from the registry.

        Args:
            server_id: Server identifier to remove

        Raises:
            ServerNotFoundError: If server_id not found
        """
        if server_id not in self._servers:
            raise ServerNotFoundError(f"Server '{server_id}' not found")
        del self._servers[server_id]

    def get(self, server_id: str) -> ServerDefinition:
        """Get a server definition by ID.

        Args:
            server_id: Server identifier

        Returns:
            ServerDefinition object

        Raises:
            ServerNotFoundError: If server_id not found
        """
        if server_id not in self._servers:
            available = list(self._servers.keys())
            raise ServerNotFoundError(
                f"Server '{server_id}' not found. Available servers: {available}"
            )
        return self._servers[server_id]

    def has(self, server_id: str) -> bool:
        """Check if a server exists in the registry.

        Args:
            server_id: Server identifier

        Returns:
            True if server exists, False otherwise
        """
        return server_id in self._servers

    def list_all(self) -> list[ServerDefinition]:
        """List all registered servers.

        Returns:
            List of all ServerDefinition objects (sorted by server_id)
        """
        return sorted(self._servers.values(), key=lambda s: s.server_id)

    def list_by_transport(self, transport: TransportType) -> list[ServerDefinition]:
        """List servers filtered by transport type.

        Args:
            transport: Transport type to filter by

        Returns:
            List of ServerDefinition objects matching transport type
        """
        return [s for s in self.list_all() if s.transport == transport]

    def search(self, query: str) -> list[ServerDefinition]:
        """Search servers by query string.

        Searches in server_id, display_name, description, and tags.

        Args:
            query: Search query (case-insensitive)

        Returns:
            List of matching ServerDefinition objects
        """
        query_lower = query.lower()
        results = []

        for server in self.list_all():
            # Search in server_id, display_name, description
            if (
                query_lower in server.server_id.lower()
                or query_lower in server.display_name.lower()
                or query_lower in server.description.lower()
            ):
                results.append(server)
                continue

            # Search in tags
            if any(query_lower in tag.lower() for tag in server.tags):
                results.append(server)
                continue

        return results

    def get_transport_counts(self) -> dict[str, int]:
        """Get count of servers by transport type.

        Returns:
            Dictionary mapping transport type to count
        """
        counts: dict[str, int] = {
            TransportType.STDIO.value: 0,
            TransportType.HTTP.value: 0,
            TransportType.SSE.value: 0,
        }

        for server in self._servers.values():
            # Handle both enum and string values (Pydantic may serialize to string)
            transport_val = server.transport.value if isinstance(server.transport, TransportType) else server.transport
            counts[transport_val] += 1

        return counts

    def server_ids(self) -> list[str]:
        """Get list of all server IDs.

        Returns:
            Sorted list of server IDs
        """
        return sorted(self._servers.keys())

    def count(self) -> int:
        """Get total number of registered servers.

        Returns:
            Count of servers
        """
        return len(self._servers)

    def to_dict(self) -> dict[str, Any]:
        """Export registry as dictionary.

        Returns:
            Dictionary with server_id -> ServerDefinition dict mapping
        """
        return {
            server_id: server.model_dump()
            for server_id, server in self._servers.items()
        }


# Global registry instance (will be initialized with defaults)
_default_registry: ServerRegistry | None = None


def get_default_registry() -> ServerRegistry:
    """Get the default server registry with built-in servers.

    Returns:
        ServerRegistry instance with default servers loaded

    Note:
        This is a singleton - the same instance is returned on subsequent calls.
    """
    global _default_registry

    if _default_registry is None:
        # Import here to avoid circular dependency
        from mcp_orchestrator.servers.defaults import get_default_servers

        _default_registry = ServerRegistry(servers=get_default_servers())

    return _default_registry
