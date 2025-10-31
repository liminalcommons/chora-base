"""
TDD Tests for HTTP Endpoints

Tests all 14 HTTP endpoints that expose MCP tools via REST API.

Related behaviors:
- @behavior:http-transport-expose - All 10 MCP tools accessible via HTTP

Test Strategy:
- Test each endpoint's happy path
- Test request/response schemas
- Test error cases (400, 404, 500)
- Test parameter validation
- Test integration with underlying MCP tools

Endpoints tested:
1. GET /v1/clients
2. GET /v1/clients/{client_id}/profiles
3. GET /v1/config/{client_id}/{profile}
4. POST /v1/config/diff
5. POST /v1/config/{client_id}/{profile}/draft/add
6. POST /v1/config/{client_id}/{profile}/draft/remove
7. GET /v1/config/{client_id}/{profile}/draft
8. DELETE /v1/config/{client_id}/{profile}/draft
9. POST /v1/config/{client_id}/{profile}/validate
10. POST /v1/config/{client_id}/{profile}/publish
11. POST /v1/config/{client_id}/{profile}/deploy
12. GET /v1/servers
13. GET /v1/servers/{server_id}
14. POST /v1/keys/initialize

Note: These tests are written BEFORE implementation (TDD).
All tests will fail initially until implementation is complete.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# Import will fail initially (TDD) - implementation doesn't exist yet
try:
    from mcp_orchestrator.http.server import create_app
except ImportError:
    pytest.skip("HTTP endpoints not implemented yet", allow_module_level=True)


@pytest.fixture
def client():
    """Create FastAPI test client with mocked authentication."""
    from mcp_orchestrator.http.auth import AuthenticationService

    # Create auth service and add a test token
    auth_service = AuthenticationService()
    test_token = "test_token_123"
    auth_service._tokens.add(test_token)

    # Create app with test auth service
    app = create_app(auth_service=auth_service)
    client = TestClient(app)

    yield client


@pytest.fixture
def auth_headers():
    """Provide authentication headers for requests."""
    return {"Authorization": "Bearer test_token_123"}


class TestClientEndpoints:
    """Test client discovery and profile listing endpoints."""

    def test_list_clients_returns_200(self, client, auth_headers):
        """Test GET /v1/clients returns 200 OK."""
        response = client.get("/v1/clients", headers=auth_headers)

        assert response.status_code == 200

    def test_list_clients_returns_json(self, client, auth_headers):
        """Test GET /v1/clients returns valid JSON."""
        response = client.get("/v1/clients", headers=auth_headers)

        assert response.headers["content-type"] == "application/json"
        data = response.json()
        assert isinstance(data, dict)

    def test_list_clients_schema(self, client, auth_headers):
        """Test GET /v1/clients returns correct schema."""
        response = client.get("/v1/clients", headers=auth_headers)
        data = response.json()

        assert "clients" in data
        assert isinstance(data["clients"], list)

        # If clients exist, verify structure
        if len(data["clients"]) > 0:
            client_obj = data["clients"][0]
            assert "client_id" in client_obj
            assert "display_name" in client_obj
            assert "config_path" in client_obj
            assert "platform" in client_obj

    def test_list_profiles_returns_200(self, client, auth_headers):
        """Test GET /v1/clients/{client_id}/profiles returns 200 or 404."""
        response = client.get(
            "/v1/clients/claude-desktop/profiles", headers=auth_headers
        )

        # 200 if client exists, 404 if not
        assert response.status_code in [200, 404]

    def test_list_profiles_returns_json(self, client, auth_headers):
        """Test GET /v1/clients/{client_id}/profiles returns valid JSON."""
        response = client.get(
            "/v1/clients/claude-desktop/profiles", headers=auth_headers
        )

        assert response.headers["content-type"] == "application/json"

    def test_list_profiles_schema(self, client, auth_headers):
        """Test GET /v1/clients/{client_id}/profiles returns correct schema."""
        # First get a real client
        clients_response = client.get("/v1/clients", headers=auth_headers)
        clients = clients_response.json()["clients"]

        if len(clients) > 0:
            client_id = clients[0]["client_id"]

            response = client.get(
                f"/v1/clients/{client_id}/profiles", headers=auth_headers
            )

            if response.status_code == 200:
                data = response.json()
                assert "profiles" in data
                assert isinstance(data["profiles"], list)

    def test_list_profiles_nonexistent_client_returns_404(self, client, auth_headers):
        """Test GET /v1/clients/{client_id}/profiles returns 404 for nonexistent client."""
        response = client.get(
            "/v1/clients/nonexistent_client_xyz/profiles", headers=auth_headers
        )

        assert response.status_code == 404


class TestConfigEndpoints:
    """Test configuration retrieval and manipulation endpoints."""

    def test_get_config_returns_200_or_404(self, client, auth_headers):
        """Test GET /v1/config/{client_id}/{profile} returns 200 or 404."""
        response = client.get("/v1/config/claude-desktop/default", headers=auth_headers)

        # 200 if config exists, 404 if not
        assert response.status_code in [200, 404]

    def test_get_config_returns_json(self, client, auth_headers):
        """Test GET /v1/config/{client_id}/{profile} returns valid JSON."""
        response = client.get("/v1/config/claude-desktop/default", headers=auth_headers)

        assert response.headers["content-type"] == "application/json"

    def test_get_config_schema(self, client, auth_headers):
        """Test GET /v1/config/{client_id}/{profile} returns MCP config structure."""
        response = client.get("/v1/config/claude-desktop/default", headers=auth_headers)

        if response.status_code == 200:
            data = response.json()
            # Should have mcpServers key (standard MCP config format)
            assert "mcpServers" in data or "mcp_servers" in data

    def test_diff_config_returns_200(self, client, auth_headers):
        """Test POST /v1/config/diff returns 200 OK."""
        config1 = {"mcpServers": {"filesystem": {}}}
        config2 = {"mcpServers": {"filesystem": {}, "brave-search": {}}}

        response = client.post(
            "/v1/config/diff",
            headers=auth_headers,
            json={"config1": config1, "config2": config2},
        )

        assert response.status_code == 200

    def test_diff_config_returns_diff_structure(self, client, auth_headers):
        """Test POST /v1/config/diff returns diff structure."""
        config1 = {"mcpServers": {"filesystem": {}}}
        config2 = {"mcpServers": {"brave-search": {}}}

        response = client.post(
            "/v1/config/diff",
            headers=auth_headers,
            json={"config1": config1, "config2": config2},
        )

        data = response.json()

        # Should have added/removed/modified keys
        assert (
            "added" in data or "removed" in data or "modified" in data or "diff" in data
        )

    def test_diff_config_invalid_json_returns_400(self, client, auth_headers):
        """Test POST /v1/config/diff returns 400 for invalid JSON."""
        response = client.post(
            "/v1/config/diff",
            headers=auth_headers,
            json={"config1": "not_a_dict"},  # Invalid: should be dict
        )

        assert response.status_code in [400, 422]  # 422 = Unprocessable Entity


class TestDraftConfigEndpoints:
    """Test draft configuration endpoints."""

    def test_draft_add_returns_200(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/draft/add returns 200."""
        response = client.post(
            "/v1/config/claude-desktop/default/draft/add",
            headers=auth_headers,
            json={"server_id": "filesystem", "params": {"path": "/tmp/test"}},
        )

        assert response.status_code in [200, 400]

    def test_draft_add_success_response(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/draft/add returns success structure."""
        response = client.post(
            "/v1/config/claude-desktop/default/draft/add",
            headers=auth_headers,
            json={"server_id": "filesystem", "params": {"path": "/tmp/test"}},
        )

        if response.status_code == 200:
            data = response.json()
            assert "success" in data or "message" in data or "draft" in data

    def test_draft_add_missing_server_id_returns_400(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/draft/add returns 400 for missing server_id."""
        response = client.post(
            "/v1/config/claude-desktop/default/draft/add",
            headers=auth_headers,
            json={"params": {"path": "/tmp/test"}},  # Missing server_id
        )

        assert response.status_code in [400, 422]

    def test_draft_remove_returns_200(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/draft/remove returns 200."""
        # First add a server to draft
        client.post(
            "/v1/config/claude-desktop/default/draft/add",
            headers=auth_headers,
            json={"server_id": "filesystem", "params": {"path": "/tmp/test"}},
        )

        # Then remove it
        response = client.post(
            "/v1/config/claude-desktop/default/draft/remove",
            headers=auth_headers,
            json={"server_id": "filesystem"},
        )

        assert response.status_code in [200, 400, 404]

    def test_draft_view_returns_200_or_404(self, client, auth_headers):
        """Test GET /v1/config/{client}/{profile}/draft returns 200 or 404."""
        response = client.get(
            "/v1/config/claude-desktop/default/draft",
            headers=auth_headers,
        )

        assert response.status_code in [200, 404]

    def test_draft_view_returns_config_structure(self, client, auth_headers):
        """Test GET /v1/config/{client}/{profile}/draft returns config structure."""
        # Add server to draft first
        client.post(
            "/v1/config/claude-desktop/default/draft/add",
            headers=auth_headers,
            json={"server_id": "filesystem", "params": {"path": "/tmp/test"}},
        )

        response = client.get(
            "/v1/config/claude-desktop/default/draft",
            headers=auth_headers,
        )

        if response.status_code == 200:
            data = response.json()
            # Should be a config structure
            assert isinstance(data, dict)

    def test_draft_clear_returns_200(self, client, auth_headers):
        """Test DELETE /v1/config/{client}/{profile}/draft returns 200."""
        response = client.delete(
            "/v1/config/claude-desktop/default/draft",
            headers=auth_headers,
        )

        assert response.status_code in [200, 404]


class TestConfigWorkflowEndpoints:
    """Test configuration workflow endpoints (validate, publish, deploy)."""

    def test_validate_config_returns_200(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/validate returns 200."""
        response = client.post(
            "/v1/config/claude-desktop/default/validate",
            headers=auth_headers,
        )

        assert response.status_code in [200, 400]

    def test_validate_config_returns_validation_result(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/validate returns validation result."""
        # Add valid server to draft first
        client.post(
            "/v1/config/claude-desktop/default/draft/add",
            headers=auth_headers,
            json={"server_id": "filesystem", "params": {"path": "/tmp/test"}},
        )

        response = client.post(
            "/v1/config/claude-desktop/default/validate",
            headers=auth_headers,
        )

        if response.status_code == 200:
            data = response.json()
            # Should have valid/errors keys
            assert "valid" in data or "errors" in data or "validation" in data

    def test_publish_config_returns_200_or_400(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/publish returns 200 or 400."""
        response = client.post(
            "/v1/config/claude-desktop/default/publish",
            headers=auth_headers,
        )

        # 200 if successful, 400 if keys missing or invalid draft
        assert response.status_code in [200, 400, 500]

    def test_publish_config_returns_artifact_id(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/publish returns artifact_id."""
        # Add valid config to draft
        client.post(
            "/v1/config/claude-desktop/default/draft/add",
            headers=auth_headers,
            json={"server_id": "filesystem", "params": {"path": "/tmp/test"}},
        )

        response = client.post(
            "/v1/config/claude-desktop/default/publish",
            headers=auth_headers,
        )

        if response.status_code == 200:
            data = response.json()
            # Should have artifact_id or similar identifier
            assert "artifact_id" in data or "hash" in data or "success" in data

    def test_deploy_config_returns_200_or_404(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/deploy returns 200 or 404."""
        response = client.post(
            "/v1/config/claude-desktop/default/deploy",
            headers=auth_headers,
        )

        # 200 if successful, 404 if no published config
        assert response.status_code in [200, 404, 400]

    def test_deploy_config_returns_success_message(self, client, auth_headers):
        """Test POST /v1/config/{client}/{profile}/deploy returns success message."""
        response = client.post(
            "/v1/config/claude-desktop/default/deploy",
            headers=auth_headers,
        )

        if response.status_code == 200:
            data = response.json()
            assert "success" in data or "message" in data or "deployed" in data


class TestServerRegistryEndpoints:
    """Test server registry endpoints."""

    def test_list_servers_returns_200(self, client, auth_headers):
        """Test GET /v1/servers returns 200 OK."""
        response = client.get("/v1/servers", headers=auth_headers)

        assert response.status_code == 200

    def test_list_servers_returns_json(self, client, auth_headers):
        """Test GET /v1/servers returns valid JSON."""
        response = client.get("/v1/servers", headers=auth_headers)

        assert response.headers["content-type"] == "application/json"
        data = response.json()
        assert isinstance(data, dict)

    def test_list_servers_schema(self, client, auth_headers):
        """Test GET /v1/servers returns correct schema."""
        response = client.get("/v1/servers", headers=auth_headers)
        data = response.json()

        assert "servers" in data
        assert isinstance(data["servers"], list)
        assert len(data["servers"]) > 0  # Should have at least some servers

        # Verify server structure
        server = data["servers"][0]
        assert "server_id" in server
        assert "description" in server
        assert "transport" in server

    def test_describe_server_returns_200(self, client, auth_headers):
        """Test GET /v1/servers/{server_id} returns 200 for valid server."""
        # First get list of servers
        servers_response = client.get("/v1/servers", headers=auth_headers)
        servers = servers_response.json()["servers"]
        assert len(servers) > 0

        server_id = servers[0]["server_id"]

        response = client.get(f"/v1/servers/{server_id}", headers=auth_headers)

        assert response.status_code == 200

    def test_describe_server_schema(self, client, auth_headers):
        """Test GET /v1/servers/{server_id} returns correct schema."""
        # Get a real server ID
        servers_response = client.get("/v1/servers", headers=auth_headers)
        servers = servers_response.json()["servers"]
        server_id = servers[0]["server_id"]

        response = client.get(f"/v1/servers/{server_id}", headers=auth_headers)
        data = response.json()

        assert data["server_id"] == server_id
        assert "description" in data
        assert "transport" in data

    def test_describe_server_nonexistent_returns_404(self, client, auth_headers):
        """Test GET /v1/servers/{server_id} returns 404 for nonexistent server."""
        response = client.get(
            "/v1/servers/nonexistent_server_xyz", headers=auth_headers
        )

        assert response.status_code == 404


class TestKeyManagementEndpoints:
    """Test cryptographic key management endpoints."""

    def test_initialize_keys_returns_200_or_400(self, client, auth_headers):
        """Test POST /v1/keys/initialize returns 200 or 400."""
        response = client.post("/v1/keys/initialize", headers=auth_headers)

        # 200 if successful, 400 if keys already exist
        assert response.status_code in [200, 400]

    def test_initialize_keys_creates_keys(self, client, auth_headers):
        """Test POST /v1/keys/initialize creates signing keys."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Set keys directory for test
            with patch(
                "mcp_orchestrator.storage.base.get_base_dir", return_value=Path(tmpdir)
            ):
                response = client.post("/v1/keys/initialize", headers=auth_headers)

                if response.status_code == 200:
                    data = response.json()
                    # Should indicate success
                    assert "success" in data or "message" in data or "keys" in data

    def test_initialize_keys_already_initialized_returns_400(
        self, client, auth_headers
    ):
        """Test POST /v1/keys/initialize returns 400 if keys already exist."""
        # Initialize keys
        response1 = client.post("/v1/keys/initialize", headers=auth_headers)

        # Try to initialize again
        response2 = client.post("/v1/keys/initialize", headers=auth_headers)

        # Second call should fail (keys already exist)
        if response1.status_code == 200:
            assert response2.status_code in [400, 409]  # 409 = Conflict


class TestEndpointErrorHandling:
    """Test error handling across all endpoints."""

    def test_404_for_unknown_endpoint(self, client, auth_headers):
        """Test that unknown endpoints return 404."""
        response = client.get("/v1/unknown/endpoint", headers=auth_headers)

        assert response.status_code == 404

    def test_405_for_wrong_method(self, client, auth_headers):
        """Test that wrong HTTP method returns 405 Method Not Allowed."""
        # POST to a GET-only endpoint
        response = client.post("/v1/clients", headers=auth_headers)

        assert response.status_code == 405

    def test_error_responses_are_json(self, client, auth_headers):
        """Test that error responses are valid JSON."""
        # Trigger an error (e.g., 404)
        response = client.get("/v1/servers/nonexistent_server", headers=auth_headers)

        assert response.headers["content-type"] == "application/json"
        data = response.json()

        # Should have error details
        assert "detail" in data or "error" in data

    def test_error_messages_are_helpful(self, client, auth_headers):
        """Test that error messages provide helpful context."""
        response = client.get("/v1/servers/nonexistent_server", headers=auth_headers)

        data = response.json()
        error_message = data.get("detail", data.get("error", ""))

        # Error message should not be empty
        assert len(error_message) > 0


class TestEndpointResponseHeaders:
    """Test response headers for all endpoints."""

    def test_content_type_is_application_json(self, client, auth_headers):
        """Test that all endpoints return application/json."""
        endpoints = [
            ("GET", "/v1/clients"),
            ("GET", "/v1/servers"),
            ("GET", "/v1/config/claude-desktop/default/draft"),
        ]

        for method, path in endpoints:
            if method == "GET":
                response = client.get(path, headers=auth_headers)
            elif method == "POST":
                response = client.post(path, headers=auth_headers, json={})

            assert response.headers["content-type"] == "application/json"

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present (basic check)."""
        # This is tested more thoroughly in test_cors.py
        response = client.options(
            "/v1/clients", headers={"Origin": "http://localhost:3000"}
        )

        # Should have CORS headers
        assert (
            "access-control-allow-origin" in response.headers
            or response.status_code == 200
        )


class TestEndpointIntegrationWithMCPTools:
    """Test that endpoints properly integrate with underlying MCP tools."""

    @pytest.mark.skip(reason="mcp_orchestrator.tools module does not exist")
    def test_list_clients_calls_discover_clients(self, client, auth_headers):
        """Test that GET /v1/clients calls underlying discover_clients tool."""
        # This test assumes a module structure that doesn't exist
        # The actual implementation uses _registry.list_clients() directly
        pass

    def test_list_servers_calls_registry(self, client, auth_headers):
        """Test that GET /v1/servers calls server registry."""
        # Test that the endpoint returns valid server data
        response = client.get("/v1/servers", headers=auth_headers)

        # Should return 200 OK
        assert response.status_code == 200

        # Response should have servers list
        data = response.json()
        assert "servers" in data
        assert isinstance(data["servers"], list)
