"""Tests for MCP server registry functionality.

Wave 1.1 (v0.1.1):
- Test ServerDefinition model
- Test ServerRegistry operations
- Test server search and filtering
- Test default catalog loading
"""

import pytest

from mcp_orchestrator.servers import (
    ParameterDefinition,
    ServerDefinition,
    ServerRegistry,
    TransportType,
    get_default_registry,
)
from mcp_orchestrator.servers.registry import ServerNotFoundError


class TestServerDefinition:
    """Tests for ServerDefinition model."""

    def test_stdio_server_creation(self) -> None:
        """Test creating a stdio server definition."""
        server = ServerDefinition(
            server_id="test-server",
            display_name="Test Server",
            description="A test server",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "test-package"],
            tags=["test"],
        )

        assert server.server_id == "test-server"
        assert server.transport == TransportType.STDIO
        assert server.stdio_command == "npx"
        assert len(server.stdio_args) == 2

    def test_http_server_creation(self) -> None:
        """Test creating an HTTP server definition."""
        server = ServerDefinition(
            server_id="http-server",
            display_name="HTTP Server",
            description="An HTTP server",
            transport=TransportType.HTTP,
            http_url="http://localhost:8080/mcp",
            http_auth_type="bearer",
            required_env=["API_KEY"],
        )

        assert server.server_id == "http-server"
        assert server.transport == TransportType.HTTP
        assert server.http_url == "http://localhost:8080/mcp"
        assert server.http_auth_type == "bearer"
        assert "API_KEY" in server.required_env

    def test_server_with_parameters(self) -> None:
        """Test server with configuration parameters."""
        param = ParameterDefinition(
            name="path",
            type="path",
            description="Directory path",
            required=True,
            example="/tmp",
        )

        server = ServerDefinition(
            server_id="test",
            display_name="Test",
            description="Test",
            transport=TransportType.STDIO,
            stdio_command="test",
            parameters=[param],
        )

        assert len(server.parameters) == 1
        assert server.parameters[0].name == "path"
        assert server.parameters[0].required is True


class TestServerRegistry:
    """Tests for ServerRegistry class."""

    def test_empty_registry(self) -> None:
        """Test creating an empty registry."""
        registry = ServerRegistry()
        assert registry.count() == 0
        assert len(registry.list_all()) == 0

    def test_register_server(self) -> None:
        """Test registering a server."""
        registry = ServerRegistry()
        server = ServerDefinition(
            server_id="test",
            display_name="Test",
            description="Test",
            transport=TransportType.STDIO,
            stdio_command="test",
        )

        registry.register(server)

        assert registry.count() == 1
        assert registry.has("test")
        assert registry.get("test").server_id == "test"

    def test_register_duplicate_fails(self) -> None:
        """Test that registering duplicate server_id fails."""
        registry = ServerRegistry()
        server = ServerDefinition(
            server_id="test",
            display_name="Test",
            description="Test",
            transport=TransportType.STDIO,
            stdio_command="test",
        )

        registry.register(server)

        with pytest.raises(ValueError, match="already registered"):
            registry.register(server)

    def test_update_server(self) -> None:
        """Test updating an existing server."""
        registry = ServerRegistry()
        server = ServerDefinition(
            server_id="test",
            display_name="Test",
            description="Original",
            transport=TransportType.STDIO,
            stdio_command="test",
        )

        registry.register(server)

        updated = ServerDefinition(
            server_id="test",
            display_name="Test Updated",
            description="Updated",
            transport=TransportType.STDIO,
            stdio_command="test",
        )

        registry.update(updated)

        assert registry.get("test").display_name == "Test Updated"
        assert registry.get("test").description == "Updated"

    def test_update_nonexistent_fails(self) -> None:
        """Test that updating nonexistent server fails."""
        registry = ServerRegistry()
        server = ServerDefinition(
            server_id="test",
            display_name="Test",
            description="Test",
            transport=TransportType.STDIO,
            stdio_command="test",
        )

        with pytest.raises(ServerNotFoundError, match="not found"):
            registry.update(server)

    def test_unregister_server(self) -> None:
        """Test unregistering a server."""
        registry = ServerRegistry()
        server = ServerDefinition(
            server_id="test",
            display_name="Test",
            description="Test",
            transport=TransportType.STDIO,
            stdio_command="test",
        )

        registry.register(server)
        assert registry.count() == 1

        registry.unregister("test")
        assert registry.count() == 0
        assert not registry.has("test")

    def test_unregister_nonexistent_fails(self) -> None:
        """Test that unregistering nonexistent server fails."""
        registry = ServerRegistry()

        with pytest.raises(ServerNotFoundError, match="not found"):
            registry.unregister("nonexistent")

    def test_get_nonexistent_fails(self) -> None:
        """Test that getting nonexistent server fails."""
        registry = ServerRegistry()

        with pytest.raises(ServerNotFoundError, match="not found"):
            registry.get("nonexistent")

    def test_list_by_transport(self) -> None:
        """Test filtering servers by transport type."""
        registry = ServerRegistry()

        stdio_server = ServerDefinition(
            server_id="stdio",
            display_name="Stdio Server",
            description="Test",
            transport=TransportType.STDIO,
            stdio_command="test",
        )

        http_server = ServerDefinition(
            server_id="http",
            display_name="HTTP Server",
            description="Test",
            transport=TransportType.HTTP,
            http_url="http://localhost:8080",
        )

        registry.register(stdio_server)
        registry.register(http_server)

        stdio_servers = registry.list_by_transport(TransportType.STDIO)
        assert len(stdio_servers) == 1
        assert stdio_servers[0].server_id == "stdio"

        http_servers = registry.list_by_transport(TransportType.HTTP)
        assert len(http_servers) == 1
        assert http_servers[0].server_id == "http"

    def test_search_by_name(self) -> None:
        """Test searching servers by name."""
        registry = ServerRegistry()

        server1 = ServerDefinition(
            server_id="filesystem",
            display_name="Filesystem Access",
            description="File operations",
            transport=TransportType.STDIO,
            stdio_command="test",
        )

        server2 = ServerDefinition(
            server_id="database",
            display_name="Database Access",
            description="Database operations",
            transport=TransportType.STDIO,
            stdio_command="test",
        )

        registry.register(server1)
        registry.register(server2)

        results = registry.search("filesystem")
        assert len(results) == 1
        assert results[0].server_id == "filesystem"

        results = registry.search("access")
        assert len(results) == 2

    def test_search_by_description(self) -> None:
        """Test searching servers by description."""
        registry = ServerRegistry()

        server = ServerDefinition(
            server_id="test",
            display_name="Test",
            description="Search for web content",
            transport=TransportType.STDIO,
            stdio_command="test",
        )

        registry.register(server)

        results = registry.search("web")
        assert len(results) == 1

    def test_search_by_tags(self) -> None:
        """Test searching servers by tags."""
        registry = ServerRegistry()

        server1 = ServerDefinition(
            server_id="postgres",
            display_name="PostgreSQL",
            description="Database",
            transport=TransportType.STDIO,
            stdio_command="test",
            tags=["database", "sql", "relational"],
        )

        server2 = ServerDefinition(
            server_id="mongo",
            display_name="MongoDB",
            description="Database",
            transport=TransportType.STDIO,
            stdio_command="test",
            tags=["database", "document"],
        )

        registry.register(server1)
        registry.register(server2)

        results = registry.search("relational")
        assert len(results) == 1
        assert results[0].server_id == "postgres"

        results = registry.search("database")
        assert len(results) == 2

    def test_get_transport_counts(self) -> None:
        """Test getting transport type counts."""
        registry = ServerRegistry()

        for i in range(3):
            registry.register(
                ServerDefinition(
                    server_id=f"stdio-{i}",
                    display_name="Stdio",
                    description="Test",
                    transport=TransportType.STDIO,
                    stdio_command="test",
                )
            )

        for i in range(2):
            registry.register(
                ServerDefinition(
                    server_id=f"http-{i}",
                    display_name="HTTP",
                    description="Test",
                    transport=TransportType.HTTP,
                    http_url="http://localhost",
                )
            )

        counts = registry.get_transport_counts()
        assert counts["stdio"] == 3
        assert counts["http"] == 2
        assert counts["sse"] == 0

    def test_server_ids(self) -> None:
        """Test getting list of server IDs."""
        registry = ServerRegistry()

        server_ids = ["alpha", "beta", "gamma"]
        for server_id in server_ids:
            registry.register(
                ServerDefinition(
                    server_id=server_id,
                    display_name=server_id.title(),
                    description="Test",
                    transport=TransportType.STDIO,
                    stdio_command="test",
                )
            )

        ids = registry.server_ids()
        assert len(ids) == 3
        assert ids == sorted(server_ids)  # Should be sorted

    def test_to_dict(self) -> None:
        """Test exporting registry as dictionary."""
        registry = ServerRegistry()

        server = ServerDefinition(
            server_id="test",
            display_name="Test",
            description="Test",
            transport=TransportType.STDIO,
            stdio_command="npx",
        )

        registry.register(server)

        data = registry.to_dict()
        assert "test" in data
        assert data["test"]["server_id"] == "test"
        assert data["test"]["display_name"] == "Test"


class TestDefaultRegistry:
    """Tests for default server catalog."""

    def test_default_registry_loads(self) -> None:
        """Test that default registry loads successfully."""
        registry = get_default_registry()

        assert registry.count() > 0
        assert registry.count() >= 10  # Should have at least 10 servers

    def test_default_registry_has_stdio_servers(self) -> None:
        """Test that default registry includes stdio servers."""
        registry = get_default_registry()

        stdio_servers = registry.list_by_transport(TransportType.STDIO)
        assert len(stdio_servers) > 0

        # Check for common servers
        assert registry.has("filesystem")
        assert registry.has("brave-search")

    def test_default_registry_has_http_servers(self) -> None:
        """Test that default registry includes HTTP/SSE servers."""
        registry = get_default_registry()

        http_servers = registry.list_by_transport(TransportType.HTTP)
        sse_servers = registry.list_by_transport(TransportType.SSE)

        # Should have at least one HTTP or SSE server
        assert len(http_servers) + len(sse_servers) > 0

    def test_filesystem_server_details(self) -> None:
        """Test filesystem server definition details."""
        registry = get_default_registry()

        filesystem = registry.get("filesystem")

        assert filesystem.server_id == "filesystem"
        assert filesystem.transport == TransportType.STDIO
        assert filesystem.stdio_command == "npx"
        assert filesystem.npm_package == "@modelcontextprotocol/server-filesystem"
        assert len(filesystem.parameters) > 0
        assert filesystem.parameters[0].name == "path"

    def test_brave_search_server_details(self) -> None:
        """Test brave-search server definition details."""
        registry = get_default_registry()

        brave = registry.get("brave-search")

        assert brave.server_id == "brave-search"
        assert brave.transport == TransportType.STDIO
        assert "BRAVE_API_KEY" in brave.required_env
        assert "search" in brave.tags or "web" in brave.tags

    def test_default_registry_singleton(self) -> None:
        """Test that get_default_registry returns same instance."""
        registry1 = get_default_registry()
        registry2 = get_default_registry()

        assert registry1 is registry2  # Same object
