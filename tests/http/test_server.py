"""
TDD Tests for HTTPTransportServer

Tests the HTTP server lifecycle, endpoint exposure, and backward compatibility.

Related behaviors:
- @behavior:http-transport-expose - All 10 MCP tools accessible via HTTP
- @behavior:http-transport-lifecycle - Start/stop server gracefully
- @behavior:http-transport-backward-compat - stdio continues to work

Test Strategy:
- Test server initialization
- Test server start/stop lifecycle
- Test endpoint routing (all 14 endpoints)
- Test OpenAPI schema generation
- Test health checks
- Test graceful shutdown
- Test backward compatibility (stdio unaffected)

Note: These tests are written BEFORE implementation (TDD).
All tests will fail initially until implementation is complete.
"""

import subprocess
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

# Import will fail initially (TDD) - implementation doesn't exist yet
try:
    from mcp_orchestrator.http.server import HTTPTransportServer, create_app
except ImportError:
    pytest.skip("HTTPTransportServer not implemented yet", allow_module_level=True)


class TestHTTPTransportServerInitialization:
    """Test server initialization and configuration."""

    def test_server_initialization_with_defaults(self):
        """
        Test that HTTPTransportServer initializes with default values.

        Expected defaults:
        - host: "0.0.0.0"
        - port: 8000
        - auth_service: not None
        - running: False
        """
        server = HTTPTransportServer()

        assert server.host == "0.0.0.0"
        assert server.port == 8000
        assert server.auth_service is not None
        assert server.running is False
        assert server.app is not None

    def test_server_initialization_with_custom_host_port(self):
        """
        Test that HTTPTransportServer accepts custom host and port.
        """
        server = HTTPTransportServer(host="127.0.0.1", port=9000)

        assert server.host == "127.0.0.1"
        assert server.port == 9000

    def test_server_initialization_with_custom_auth_service(self):
        """
        Test that HTTPTransportServer accepts custom authentication service.
        """
        mock_auth = MagicMock()
        server = HTTPTransportServer(auth_service=mock_auth)

        assert server.auth_service is mock_auth

    def test_fastapi_app_configuration(self):
        """
        Test that FastAPI app is configured correctly.

        Expected configuration:
        - title: "MCP Orchestration HTTP API"
        - version: "0.2.0"
        - docs_url: "/docs"
        - openapi_url: "/openapi.json"
        """
        server = HTTPTransportServer()

        assert server.app.title == "MCP Orchestration HTTP API"
        assert server.app.version == "0.2.0"
        assert server.app.docs_url == "/docs"
        assert server.app.openapi_url == "/openapi.json"


class TestHTTPTransportServerLifecycle:
    """Test server start, stop, and lifecycle management."""

    @pytest.mark.asyncio
    async def test_server_start(self):
        """
        Test that server starts and binds to host:port.

        @behavior:http-transport-lifecycle
        """
        server = HTTPTransportServer(host="127.0.0.1", port=8001)

        # Start server (async)
        await server.start()

        assert server.running is True

        # Cleanup
        await server.stop()

    @pytest.mark.asyncio
    async def test_server_stop_gracefully(self):
        """
        Test that server stops gracefully.

        @behavior:http-transport-lifecycle
        """
        server = HTTPTransportServer(host="127.0.0.1", port=8002)

        await server.start()
        assert server.running is True

        await server.stop()
        assert server.running is False

    @pytest.mark.asyncio
    async def test_server_start_already_running(self):
        """
        Test that starting an already-running server raises error.
        """
        server = HTTPTransportServer(host="127.0.0.1", port=8003)

        await server.start()

        with pytest.raises(RuntimeError, match="already running"):
            await server.start()

        await server.stop()

    @pytest.mark.asyncio
    async def test_server_stop_not_running(self):
        """
        Test that stopping a non-running server is safe (no-op).
        """
        server = HTTPTransportServer()

        # Should not raise error
        await server.stop()
        assert server.running is False

    def test_health_check_when_running(self):
        """
        Test that health check returns healthy status when server is running.
        """
        server = HTTPTransportServer()
        server.running = True

        health = server.health_check()

        assert health["status"] == "healthy"
        assert health["running"] is True

    def test_health_check_when_not_running(self):
        """
        Test that health check returns unhealthy status when server is stopped.
        """
        server = HTTPTransportServer()
        server.running = False

        health = server.health_check()

        assert health["status"] == "unhealthy"
        assert health["running"] is False


class TestHTTPEndpointExposure:
    """
    Test that all 10 MCP tools are exposed via HTTP endpoints.

    @behavior:http-transport-expose
    """

    @pytest.fixture
    def client(self):
        """Create FastAPI test client."""
        app = create_app()
        return TestClient(app)

    @pytest.fixture
    def auth_headers(self):
        """Mock authentication headers."""
        return {"Authorization": "Bearer test_token_123"}

    # Client endpoints
    def test_list_clients_endpoint_exists(self, client, auth_headers):
        """Test GET /v1/clients endpoint exists and returns 200."""
        response = client.get("/v1/clients", headers=auth_headers)
        assert response.status_code == 200

    def test_list_profiles_endpoint_exists(self, client, auth_headers):
        """Test GET /v1/clients/{client_id}/profiles endpoint exists."""
        response = client.get(
            "/v1/clients/claude-desktop/profiles", headers=auth_headers
        )
        assert response.status_code in [200, 404]  # 404 if client doesn't exist

    # Config endpoints
    def test_get_config_endpoint_exists(self, client, auth_headers):
        """Test GET /v1/config/{client_id}/{profile} endpoint exists."""
        response = client.get("/v1/config/claude-desktop/default", headers=auth_headers)
        assert response.status_code in [200, 404]

    def test_diff_config_endpoint_exists(self, client, auth_headers):
        """Test POST /v1/config/diff endpoint exists."""
        response = client.post(
            "/v1/config/diff",
            headers=auth_headers,
            json={"config1": {}, "config2": {}},
        )
        assert response.status_code in [200, 400]

    def test_draft_add_endpoint_exists(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/draft/add endpoint exists."""
        response = client.post(
            "/v1/config/claude-desktop/default/draft/add",
            headers=auth_headers,
            json={"server_id": "filesystem", "params": {}},
        )
        assert response.status_code in [200, 400]

    def test_draft_remove_endpoint_exists(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/draft/remove endpoint exists."""
        response = client.post(
            "/v1/config/claude-desktop/default/draft/remove",
            headers=auth_headers,
            json={"server_id": "filesystem"},
        )
        assert response.status_code in [200, 400]

    def test_draft_view_endpoint_exists(self, client, auth_headers):
        """Test GET /v1/config/{client}/{profile}/draft endpoint exists."""
        response = client.get(
            "/v1/config/claude-desktop/default/draft",
            headers=auth_headers,
        )
        assert response.status_code in [200, 404]

    def test_draft_clear_endpoint_exists(self, client, auth_headers):
        """Test DELETE /v1/config/{client}/{profile}/draft endpoint exists."""
        response = client.delete(
            "/v1/config/claude-desktop/default/draft",
            headers=auth_headers,
        )
        assert response.status_code in [200, 404]

    def test_validate_config_endpoint_exists(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/validate endpoint exists."""
        response = client.post(
            "/v1/config/claude-desktop/default/validate",
            headers=auth_headers,
        )
        assert response.status_code in [200, 400]

    def test_publish_config_endpoint_exists(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/publish endpoint exists."""
        response = client.post(
            "/v1/config/claude-desktop/default/publish",
            headers=auth_headers,
        )
        assert response.status_code in [200, 400]

    def test_deploy_config_endpoint_exists(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/deploy endpoint exists."""
        response = client.post(
            "/v1/config/claude-desktop/default/deploy",
            headers=auth_headers,
        )
        assert response.status_code in [200, 400, 404]

    # Server registry endpoints
    def test_list_servers_endpoint_exists(self, client, auth_headers):
        """Test GET /v1/servers endpoint exists."""
        response = client.get("/v1/servers", headers=auth_headers)
        assert response.status_code == 200

    def test_describe_server_endpoint_exists(self, client, auth_headers):
        """Test GET /v1/servers/{server_id} endpoint exists."""
        response = client.get("/v1/servers/filesystem", headers=auth_headers)
        assert response.status_code in [200, 404]

    # Key management endpoints
    def test_initialize_keys_endpoint_exists(self, client, auth_headers):
        """Test POST /v1/keys/initialize endpoint exists."""
        response = client.post("/v1/keys/initialize", headers=auth_headers)
        assert response.status_code in [200, 400]


class TestOpenAPISchema:
    """Test OpenAPI schema generation."""

    @pytest.fixture
    def client(self):
        """Create FastAPI test client."""
        app = create_app()
        return TestClient(app)

    def test_openapi_json_endpoint(self, client):
        """Test GET /openapi.json returns valid OpenAPI schema."""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        schema = response.json()

        assert "openapi" in schema
        assert schema["openapi"].startswith("3.")
        assert "info" in schema
        assert schema["info"]["title"] == "MCP Orchestration HTTP API"
        assert schema["info"]["version"] == "0.2.0"

    def test_openapi_schema_has_all_endpoints(self, client):
        """Test that OpenAPI schema documents all 14 endpoints."""
        response = client.get("/openapi.json")
        schema = response.json()

        paths = schema["paths"]

        # Verify all endpoints are documented
        expected_paths = [
            "/v1/clients",
            "/v1/clients/{client_id}/profiles",
            "/v1/config/{client_id}/{profile}",
            "/v1/config/diff",
            "/v1/config/{client_id}/{profile}/draft/add",
            "/v1/config/{client_id}/{profile}/draft/remove",
            "/v1/config/{client_id}/{profile}/draft",
            "/v1/config/{client_id}/{profile}/validate",
            "/v1/config/{client_id}/{profile}/publish",
            "/v1/config/{client_id}/{profile}/deploy",
            "/v1/servers",
            "/v1/servers/{server_id}",
            "/v1/keys/initialize",
        ]

        for path in expected_paths:
            assert path in paths, f"Expected path {path} in OpenAPI schema"

    def test_swagger_ui_accessible(self, client):
        """Test that Swagger UI is accessible at /docs."""
        response = client.get("/docs")

        assert response.status_code == 200
        assert "swagger" in response.text.lower()


class TestBackwardCompatibility:
    """
    Test that stdio transport continues to work (no breaking changes).

    @behavior:http-transport-backward-compat
    """

    def test_stdio_list_clients_works(self):
        """Test that mcp-orchestration-discover still works via stdio."""
        result = subprocess.run(
            ["mcp-orchestration-discover"],
            capture_output=True,
            text=True,
            check=False,
        )

        # stdio should work regardless of HTTP server status
        assert result.returncode == 0

    def test_stdio_list_servers_works(self):
        """Test that mcp-orchestration-list-servers still works via stdio."""
        result = subprocess.run(
            ["mcp-orchestration-list-servers"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0

    def test_http_server_does_not_interfere_with_stdio(self):
        """
        Test that starting HTTP server does not break stdio commands.

        This is critical for backward compatibility during migration.
        """
        # First verify stdio works
        result_before = subprocess.run(
            ["mcp-orchestration-discover"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result_before.returncode == 0

        # Start HTTP server (in background)
        # Note: This is a simplified test - full E2E test in test_http_transport.py
        # Here we just verify no import errors or conflicts

        try:
            from mcp_orchestrator.http.server import HTTPTransportServer

            server = HTTPTransportServer()
            # Don't actually start (would block), just verify it can be imported
            assert server is not None
        except ImportError:
            pytest.skip("HTTP server not implemented yet")

        # Verify stdio still works
        result_after = subprocess.run(
            ["mcp-orchestration-discover"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result_after.returncode == 0
        assert result_after.stdout == result_before.stdout


class TestServerIntegration:
    """Integration tests for HTTP server with real MCP tools."""

    @pytest.fixture
    def client(self):
        """Create FastAPI test client."""
        app = create_app()
        return TestClient(app)

    @pytest.fixture
    def auth_headers(self):
        """Mock authentication headers."""
        return {"Authorization": "Bearer test_token_123"}

    def test_list_clients_returns_valid_json(self, client, auth_headers):
        """Test that /v1/clients returns valid JSON structure."""
        response = client.get("/v1/clients", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        assert "clients" in data
        assert isinstance(data["clients"], list)

        # If clients exist, verify structure
        if len(data["clients"]) > 0:
            client_obj = data["clients"][0]
            assert "client_id" in client_obj
            assert "display_name" in client_obj
            assert "config_path" in client_obj

    def test_list_servers_returns_valid_json(self, client, auth_headers):
        """Test that /v1/servers returns valid JSON structure."""
        response = client.get("/v1/servers", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        assert "servers" in data
        assert isinstance(data["servers"], list)

        # Should have at least some servers in registry
        assert len(data["servers"]) > 0

        # Verify server structure
        server = data["servers"][0]
        assert "server_id" in server
        assert "description" in server
        assert "transport" in server

    def test_get_server_details_returns_valid_json(self, client, auth_headers):
        """Test that /v1/servers/{server_id} returns valid JSON structure."""
        # First get list of servers
        response = client.get("/v1/servers", headers=auth_headers)
        servers = response.json()["servers"]
        assert len(servers) > 0

        server_id = servers[0]["server_id"]

        # Get server details
        response = client.get(f"/v1/servers/{server_id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        assert data["server_id"] == server_id
        assert "description" in data
        assert "transport" in data

    def test_error_handling_returns_valid_json(self, client, auth_headers):
        """Test that errors are returned as valid JSON."""
        # Try to get non-existent server
        response = client.get(
            "/v1/servers/nonexistent_server_xyz", headers=auth_headers
        )

        # Should return 404 or 400
        assert response.status_code in [404, 400]

        # Error should be JSON
        data = response.json()
        assert "detail" in data or "error" in data


class TestCORSMiddleware:
    """Test CORS configuration (tested more thoroughly in test_cors.py)."""

    @pytest.fixture
    def client(self):
        """Create FastAPI test client."""
        app = create_app()
        return TestClient(app)

    def test_cors_middleware_is_configured(self, client):
        """Test that CORS middleware is present."""
        # Make OPTIONS request (CORS preflight)
        response = client.options(
            "/v1/clients",
            headers={"Origin": "http://localhost:3000"},
        )

        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
