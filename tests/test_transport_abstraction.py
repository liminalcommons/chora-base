"""Tests for transport abstraction (Wave 1.2).

This module tests the ServerRegistry.to_client_config() method which
performs transport abstraction for stdio and HTTP/SSE servers.
"""

import pytest
from mcp_orchestrator.servers.models import (
    ParameterDefinition,
    ServerDefinition,
    TransportType,
)
from mcp_orchestrator.servers.registry import ServerNotFoundError, ServerRegistry


class TestStdioTransportAbstraction:
    """Tests for stdio server config generation."""

    def test_stdio_server_basic(self):
        """Test basic stdio server without parameters."""
        server = ServerDefinition(
            server_id="simple",
            display_name="Simple Server",
            description="A simple server",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@example/server"],
        )

        registry = ServerRegistry([server])
        config = registry.to_client_config("simple")

        assert config == {
            "command": "npx",
            "args": ["-y", "@example/server"],
        }

    def test_stdio_server_with_parameter_substitution(self):
        """Test stdio server with parameter placeholder substitution."""
        server = ServerDefinition(
            server_id="filesystem",
            display_name="Filesystem",
            description="Filesystem access",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@mcp/server-filesystem", "{path}"],
            parameters=[
                ParameterDefinition(
                    name="path",
                    type="path",
                    description="Root path",
                    required=True,
                    example="/tmp",
                )
            ],
        )

        registry = ServerRegistry([server])
        config = registry.to_client_config(
            "filesystem", params={"path": "/Users/me/Documents"}
        )

        assert config == {
            "command": "npx",
            "args": ["-y", "@mcp/server-filesystem", "/Users/me/Documents"],
        }

    def test_stdio_server_with_env_vars(self):
        """Test stdio server with environment variables."""
        server = ServerDefinition(
            server_id="github",
            display_name="GitHub",
            description="GitHub integration",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@mcp/server-github"],
            required_env=["GITHUB_TOKEN"],
        )

        registry = ServerRegistry([server])
        config = registry.to_client_config(
            "github", env_vars={"GITHUB_TOKEN": "ghp_test123"}
        )

        assert config == {
            "command": "npx",
            "args": ["-y", "@mcp/server-github"],
            "env": {"GITHUB_TOKEN": "ghp_test123"},
        }

    def test_stdio_server_with_multiple_params(self):
        """Test stdio server with multiple parameter substitutions."""
        server = ServerDefinition(
            server_id="multi-param",
            display_name="Multi Param Server",
            description="Server with multiple params",
            transport=TransportType.STDIO,
            stdio_command="python",
            stdio_args=["server.py", "--host", "{host}", "--port", "{port}"],
            parameters=[
                ParameterDefinition(
                    name="host", type="string", description="Host", required=True
                ),
                ParameterDefinition(
                    name="port", type="int", description="Port", required=True
                ),
            ],
        )

        registry = ServerRegistry([server])
        config = registry.to_client_config(
            "multi-param", params={"host": "localhost", "port": 8080}
        )

        assert config == {
            "command": "python",
            "args": ["server.py", "--host", "localhost", "--port", "8080"],
        }

    def test_stdio_server_missing_required_param(self):
        """Test error when required parameter is missing."""
        server = ServerDefinition(
            server_id="filesystem",
            display_name="Filesystem",
            description="Filesystem access",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@mcp/server-filesystem", "{path}"],
            parameters=[
                ParameterDefinition(
                    name="path",
                    type="path",
                    description="Root path",
                    required=True,
                )
            ],
        )

        registry = ServerRegistry([server])

        with pytest.raises(ValueError, match="Missing required parameters.*path"):
            registry.to_client_config("filesystem")  # No params provided

    def test_stdio_server_missing_required_env(self):
        """Test error when required environment variable is missing."""
        server = ServerDefinition(
            server_id="github",
            display_name="GitHub",
            description="GitHub integration",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@mcp/server-github"],
            required_env=["GITHUB_TOKEN"],
        )

        registry = ServerRegistry([server])

        with pytest.raises(
            ValueError, match="Missing required environment.*GITHUB_TOKEN"
        ):
            registry.to_client_config("github")  # No env_vars provided


class TestHTTPSSETransportAbstraction:
    """Tests for HTTP/SSE server config generation (mcp-remote wrapping)."""

    def test_http_server_basic(self):
        """Test basic HTTP server wrapped with mcp-remote."""
        server = ServerDefinition(
            server_id="n8n",
            display_name="n8n",
            description="n8n integration",
            transport=TransportType.HTTP,
            http_url="http://localhost:5679/mcp",
        )

        registry = ServerRegistry([server])
        config = registry.to_client_config("n8n")

        # Should be wrapped with mcp-remote
        assert config == {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/mcp-remote",
                "stdio",
                "http://localhost:5679/mcp",
            ],
        }

    def test_sse_server_basic(self):
        """Test basic SSE server wrapped with mcp-remote."""
        server = ServerDefinition(
            server_id="sse-server",
            display_name="SSE Server",
            description="SSE integration",
            transport=TransportType.SSE,
            http_url="http://localhost:3000/sse",
        )

        registry = ServerRegistry([server])
        config = registry.to_client_config("sse-server")

        # Should be wrapped with mcp-remote
        assert config == {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/mcp-remote",
                "stdio",
                "http://localhost:3000/sse",
            ],
        }

    def test_http_server_with_parameter_substitution(self):
        """Test HTTP server with URL parameter substitution."""
        server = ServerDefinition(
            server_id="n8n",
            display_name="n8n",
            description="n8n integration",
            transport=TransportType.HTTP,
            http_url="http://localhost:{port}/mcp",
            parameters=[
                ParameterDefinition(
                    name="port",
                    type="int",
                    description="Port number",
                    required=True,
                )
            ],
        )

        registry = ServerRegistry([server])
        config = registry.to_client_config("n8n", params={"port": 5679})

        assert config == {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/mcp-remote",
                "stdio",
                "http://localhost:5679/mcp",
            ],
        }

    def test_http_server_with_env_vars(self):
        """Test HTTP server with environment variables."""
        server = ServerDefinition(
            server_id="api-server",
            display_name="API Server",
            description="Custom API",
            transport=TransportType.HTTP,
            http_url="http://api.example.com/mcp",
            required_env=["API_KEY"],
        )

        registry = ServerRegistry([server])
        config = registry.to_client_config(
            "api-server", env_vars={"API_KEY": "secret123"}
        )

        # mcp-remote wrapper + env vars
        assert config == {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/mcp-remote",
                "stdio",
                "http://api.example.com/mcp",
            ],
            "env": {"API_KEY": "secret123"},
        }

    def test_http_server_with_multiple_url_params(self):
        """Test HTTP server with multiple URL parameters."""
        server = ServerDefinition(
            server_id="custom-api",
            display_name="Custom API",
            description="Configurable API",
            transport=TransportType.HTTP,
            http_url="http://{host}:{port}/api/v{version}",
            parameters=[
                ParameterDefinition(
                    name="host", type="string", description="Host", required=True
                ),
                ParameterDefinition(
                    name="port", type="int", description="Port", required=True
                ),
                ParameterDefinition(
                    name="version", type="int", description="Version", required=True
                ),
            ],
        )

        registry = ServerRegistry([server])
        config = registry.to_client_config(
            "custom-api",
            params={"host": "api.example.com", "port": 443, "version": 2},
        )

        assert config == {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/mcp-remote",
                "stdio",
                "http://api.example.com:443/api/v2",
            ],
        }


class TestTransportAbstractionErrors:
    """Tests for error handling in transport abstraction."""

    def test_server_not_found(self):
        """Test error when server_id doesn't exist."""
        registry = ServerRegistry()

        with pytest.raises(ServerNotFoundError, match="Server 'nonexistent' not found"):
            registry.to_client_config("nonexistent")

    def test_unsupported_transport_type(self):
        """Test error for unsupported transport types."""
        # This test verifies the safety of the transport type check
        # In practice, Pydantic validation would prevent this, but we test the fallback

        server = ServerDefinition(
            server_id="test",
            display_name="Test",
            description="Test",
            transport=TransportType.STDIO,  # We'll manually change this
            stdio_command="test",
            stdio_args=[],
        )

        registry = ServerRegistry([server])

        # Manually set an invalid transport (simulating data corruption)
        server.transport = "invalid"  # type: ignore

        with pytest.raises(ValueError, match="Unsupported transport type"):
            registry.to_client_config("test")


class TestTransportAbstractionIntegration:
    """Integration tests using default registry servers."""

    def test_filesystem_server_from_defaults(self):
        """Test filesystem server from default catalog."""
        from mcp_orchestrator.servers import get_default_registry

        registry = get_default_registry()

        config = registry.to_client_config(
            "filesystem", params={"path": "/Users/test/Documents"}
        )

        assert config["command"] == "npx"
        assert "-y" in config["args"]
        assert "@modelcontextprotocol/server-filesystem" in config["args"]
        assert "/Users/test/Documents" in config["args"]

    def test_github_server_from_defaults(self):
        """Test GitHub server from default catalog."""
        from mcp_orchestrator.servers import get_default_registry

        registry = get_default_registry()

        config = registry.to_client_config(
            "github", env_vars={"GITHUB_TOKEN": "ghp_test"}
        )

        assert config["command"] == "npx"
        assert config["env"] == {"GITHUB_TOKEN": "ghp_test"}

    def test_n8n_server_wrapped_from_defaults(self):
        """Test n8n server is wrapped with mcp-remote."""
        from mcp_orchestrator.servers import get_default_registry

        registry = get_default_registry()

        config = registry.to_client_config(
            "n8n", params={"port": 5679}, env_vars={"N8N_API_KEY": "test"}
        )

        # Should be wrapped with mcp-remote
        assert config["command"] == "npx"
        assert "@modelcontextprotocol/mcp-remote" in config["args"]
        assert "stdio" in config["args"]
        assert any("5679" in str(arg) for arg in config["args"])
        assert config["env"] == {"N8N_API_KEY": "test"}
