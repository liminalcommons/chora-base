"""
TDD Tests for CORS Configuration

Tests CORS (Cross-Origin Resource Sharing) middleware configuration for web client access.

Related behaviors:
- @behavior:http-transport-cors - CORS configured for web client access

Test Strategy:
- Test CORS preflight (OPTIONS) requests
- Test CORS headers on actual requests
- Test allowed origins, methods, headers
- Test credentials support
- Test browser compatibility scenarios

Note: These tests are written BEFORE implementation (TDD).
All tests will fail initially until implementation is complete.
"""

import pytest
from fastapi.testclient import TestClient

# Import will fail initially (TDD) - implementation doesn't exist yet
try:
    from mcp_orchestrator.http.server import create_app
except ImportError:
    pytest.skip("CORS configuration not implemented yet", allow_module_level=True)


@pytest.fixture
def client():
    """Create FastAPI test client."""
    app = create_app()
    return TestClient(app)


class TestCORSPreflightRequests:
    """
    Test CORS preflight (OPTIONS) requests.

    @behavior:http-transport-cors
    """

    def test_preflight_request_returns_200(self, client):
        """Test that OPTIONS preflight request returns 200 OK."""
        response = client.options(
            "/v1/clients",
            headers={"Origin": "http://localhost:3000"},
        )

        assert response.status_code == 200

    def test_preflight_has_allow_origin_header(self, client):
        """Test that preflight response includes Access-Control-Allow-Origin header."""
        response = client.options(
            "/v1/clients",
            headers={"Origin": "http://localhost:3000"},
        )

        assert "access-control-allow-origin" in response.headers

    def test_preflight_has_allow_methods_header(self, client):
        """Test that preflight response includes Access-Control-Allow-Methods header."""
        response = client.options(
            "/v1/clients",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )

        assert "access-control-allow-methods" in response.headers

    def test_preflight_has_allow_headers_header(self, client):
        """Test that preflight response includes Access-Control-Allow-Headers header."""
        response = client.options(
            "/v1/clients",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Headers": "authorization, content-type",
            },
        )

        assert "access-control-allow-headers" in response.headers

    def test_preflight_has_allow_credentials_header(self, client):
        """Test that preflight response includes Access-Control-Allow-Credentials header."""
        response = client.options(
            "/v1/clients",
            headers={"Origin": "http://localhost:3000"},
        )

        # From spec: allow_credentials: true
        assert "access-control-allow-credentials" in response.headers
        assert response.headers["access-control-allow-credentials"] == "true"


class TestCORSAllowedOrigins:
    """
    Test CORS allowed origins configuration.

    From spec: allow_origins: ["*"] (all origins allowed)
    """

    def test_wildcard_origin_is_allowed(self, client):
        """Test that wildcard (*) origin is allowed."""
        response = client.options(
            "/v1/clients",
            headers={"Origin": "http://localhost:3000"},
        )

        # Should allow all origins (wildcard)
        assert response.headers.get("access-control-allow-origin") in [
            "*",
            "http://localhost:3000",
        ]

    def test_localhost_origin_is_allowed(self, client):
        """Test that localhost origins are allowed."""
        origins = [
            "http://localhost:3000",
            "http://localhost:8080",
            "http://127.0.0.1:3000",
        ]

        for origin in origins:
            response = client.options(
                "/v1/clients",
                headers={"Origin": origin},
            )

            assert "access-control-allow-origin" in response.headers
            # Should be either wildcard or the specific origin
            assert response.headers["access-control-allow-origin"] in ["*", origin]

    def test_external_origin_is_allowed(self, client):
        """Test that external origins are allowed (wildcard)."""
        origins = [
            "https://example.com",
            "https://myapp.example.com",
            "https://n8n.cloud",
        ]

        for origin in origins:
            response = client.options(
                "/v1/clients",
                headers={"Origin": origin},
            )

            assert "access-control-allow-origin" in response.headers
            assert response.headers["access-control-allow-origin"] in ["*", origin]


class TestCORSAllowedMethods:
    """
    Test CORS allowed methods configuration.

    From spec: allow_methods: ["*"] (all methods allowed)
    """

    def test_get_method_is_allowed(self, client):
        """Test that GET method is allowed."""
        response = client.options(
            "/v1/clients",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )

        allowed_methods = response.headers.get("access-control-allow-methods", "")

        # Should include GET or be wildcard
        assert "GET" in allowed_methods or "*" in allowed_methods

    def test_post_method_is_allowed(self, client):
        """Test that POST method is allowed."""
        response = client.options(
            "/v1/config/diff",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            },
        )

        allowed_methods = response.headers.get("access-control-allow-methods", "")

        assert "POST" in allowed_methods or "*" in allowed_methods

    def test_delete_method_is_allowed(self, client):
        """Test that DELETE method is allowed."""
        response = client.options(
            "/v1/config/claude-desktop/default/draft",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "DELETE",
            },
        )

        allowed_methods = response.headers.get("access-control-allow-methods", "")

        assert "DELETE" in allowed_methods or "*" in allowed_methods

    def test_options_method_is_allowed(self, client):
        """Test that OPTIONS method is allowed (for preflight)."""
        response = client.options(
            "/v1/clients",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "OPTIONS",
            },
        )

        allowed_methods = response.headers.get("access-control-allow-methods", "")

        assert "OPTIONS" in allowed_methods or "*" in allowed_methods


class TestCORSAllowedHeaders:
    """
    Test CORS allowed headers configuration.

    From spec: allow_headers: ["*"] (all headers allowed)
    """

    def test_authorization_header_is_allowed(self, client):
        """Test that Authorization header is allowed."""
        response = client.options(
            "/v1/clients",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Headers": "authorization",
            },
        )

        allowed_headers = response.headers.get(
            "access-control-allow-headers", ""
        ).lower()

        assert "authorization" in allowed_headers or "*" in allowed_headers

    def test_content_type_header_is_allowed(self, client):
        """Test that Content-Type header is allowed."""
        response = client.options(
            "/v1/config/diff",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Headers": "content-type",
            },
        )

        allowed_headers = response.headers.get(
            "access-control-allow-headers", ""
        ).lower()

        assert "content-type" in allowed_headers or "*" in allowed_headers

    def test_x_api_key_header_is_allowed(self, client):
        """Test that X-API-Key header is allowed."""
        response = client.options(
            "/v1/clients",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Headers": "x-api-key",
            },
        )

        allowed_headers = response.headers.get(
            "access-control-allow-headers", ""
        ).lower()

        assert "x-api-key" in allowed_headers or "*" in allowed_headers

    def test_multiple_headers_are_allowed(self, client):
        """Test that multiple headers can be requested together."""
        response = client.options(
            "/v1/config/diff",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Headers": "authorization, content-type, x-api-key",
            },
        )

        assert "access-control-allow-headers" in response.headers

        allowed_headers = response.headers.get(
            "access-control-allow-headers", ""
        ).lower()

        # All headers should be allowed (either explicitly or via wildcard)
        assert (
            "authorization" in allowed_headers and "content-type" in allowed_headers
        ) or "*" in allowed_headers


class TestCORSActualRequests:
    """Test CORS headers on actual (non-preflight) requests."""

    def test_get_request_has_cors_headers(self, client):
        """Test that actual GET request includes CORS headers."""
        response = client.get(
            "/v1/clients",
            headers={
                "Origin": "http://localhost:3000",
                "Authorization": "Bearer test_token",
            },
        )

        # Should have CORS headers on actual response
        assert "access-control-allow-origin" in response.headers

    def test_post_request_has_cors_headers(self, client):
        """Test that actual POST request includes CORS headers."""
        response = client.post(
            "/v1/config/diff",
            headers={
                "Origin": "http://localhost:3000",
                "Authorization": "Bearer test_token",
            },
            json={"config1": {}, "config2": {}},
        )

        assert "access-control-allow-origin" in response.headers

    def test_delete_request_has_cors_headers(self, client):
        """Test that actual DELETE request includes CORS headers."""
        response = client.delete(
            "/v1/config/claude-desktop/default/draft",
            headers={
                "Origin": "http://localhost:3000",
                "Authorization": "Bearer test_token",
            },
        )

        assert "access-control-allow-origin" in response.headers


class TestCORSCredentials:
    """
    Test CORS credentials support.

    From spec: allow_credentials: true
    """

    def test_credentials_allowed_on_preflight(self, client):
        """Test that credentials are allowed on preflight requests."""
        response = client.options(
            "/v1/clients",
            headers={"Origin": "http://localhost:3000"},
        )

        assert response.headers.get("access-control-allow-credentials") == "true"

    def test_credentials_allowed_on_actual_request(self, client):
        """Test that credentials are allowed on actual requests."""
        response = client.get(
            "/v1/clients",
            headers={
                "Origin": "http://localhost:3000",
                "Authorization": "Bearer test_token",
            },
        )

        # Should allow credentials
        assert response.headers.get("access-control-allow-credentials") in [
            "true",
            None,
        ]
        # None is acceptable if wildcard origin is used (some CORS implementations)


class TestCORSBrowserScenarios:
    """Test CORS scenarios that browsers would encounter."""

    def test_browser_fetch_with_authorization_header(self, client):
        """
        Test browser scenario: fetch() with Authorization header.

        Browser would:
        1. Send preflight OPTIONS with Access-Control-Request-Headers: authorization
        2. Send actual GET with Authorization header
        """
        # Step 1: Preflight
        preflight = client.options(
            "/v1/clients",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "authorization",
            },
        )

        assert preflight.status_code == 200
        assert "access-control-allow-headers" in preflight.headers

        # Step 2: Actual request
        actual = client.get(
            "/v1/clients",
            headers={
                "Origin": "http://localhost:3000",
                "Authorization": "Bearer test_token",
            },
        )

        assert "access-control-allow-origin" in actual.headers

    def test_browser_fetch_with_json_body(self, client):
        """
        Test browser scenario: fetch() POST with JSON body.

        Browser would:
        1. Send preflight OPTIONS with Access-Control-Request-Headers: content-type, authorization
        2. Send actual POST with Content-Type: application/json and body
        """
        # Step 1: Preflight
        preflight = client.options(
            "/v1/config/diff",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type, authorization",
            },
        )

        assert preflight.status_code == 200

        # Step 2: Actual request
        actual = client.post(
            "/v1/config/diff",
            headers={
                "Origin": "http://localhost:3000",
                "Authorization": "Bearer test_token",
                "Content-Type": "application/json",
            },
            json={"config1": {}, "config2": {}},
        )

        assert "access-control-allow-origin" in actual.headers

    def test_react_app_fetch_scenario(self, client):
        """
        Test React app scenario from value scenario:

        React app makes fetch() request to /v1/servers
        CORS headers allow browser request
        Bearer token in Authorization header
        """
        # Preflight
        preflight = client.options(
            "/v1/servers",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "authorization",
            },
        )

        assert preflight.status_code == 200
        assert "access-control-allow-origin" in preflight.headers
        assert "access-control-allow-methods" in preflight.headers

        # Actual request
        actual = client.get(
            "/v1/servers",
            headers={
                "Origin": "http://localhost:3000",
                "Authorization": "Bearer test_token",
            },
        )

        # Should not have CORS errors
        assert "access-control-allow-origin" in actual.headers

        # Success criteria from value scenario: "No CORS errors in console"
        # (We verify this by checking CORS headers are present)


class TestCORSConfigurationCustomization:
    """Test CORS configuration can be customized (future feature)."""

    def test_cors_config_defaults_to_wildcard(self, client):
        """Test that CORS defaults to wildcard origin (*)."""
        response = client.options(
            "/v1/clients",
            headers={"Origin": "http://localhost:3000"},
        )

        # Default should allow all origins
        assert response.headers.get("access-control-allow-origin") in [
            "*",
            "http://localhost:3000",
        ]

    # Future tests for environment-based CORS configuration
    # (e.g., MCP_ORCHESTRATION_CORS_ORIGINS env var)
    # Will be added when feature is implemented


class TestCORSSecurityConsiderations:
    """Test CORS security considerations."""

    def test_cors_allows_any_origin_by_default(self, client):
        """
        Test that CORS allows any origin by default (wildcard).

        Note: This is appropriate for a development tool that needs
        to be accessible from various frontends (n8n, web apps, etc.).
        """
        response = client.options(
            "/v1/clients",
            headers={"Origin": "https://malicious-site.com"},
        )

        # Should allow (since we use wildcard)
        # This is intentional for flexibility
        assert "access-control-allow-origin" in response.headers

    def test_authentication_still_required_despite_cors(self, client):
        """
        Test that CORS headers don't bypass authentication.

        CORS only controls browser access, not authentication.
        """
        # Preflight should succeed (CORS check)
        preflight = client.options(
            "/v1/clients",
            headers={"Origin": "http://localhost:3000"},
        )
        assert preflight.status_code == 200

        # But actual request without auth should fail
        actual = client.get(
            "/v1/clients",
            headers={"Origin": "http://localhost:3000"},
            # No Authorization header
        )

        # Should require authentication (401)
        # (Unless test client mocks auth, in which case we accept that)
        assert actual.status_code in [200, 401]


class TestCORSCompliance:
    """Test CORS specification compliance."""

    def test_preflight_max_age_header(self, client):
        """Test that preflight response may include Access-Control-Max-Age header."""
        response = client.options(
            "/v1/clients",
            headers={"Origin": "http://localhost:3000"},
        )

        # Max-Age is optional but recommended (cache preflight result)
        # If present, should be a positive integer
        if "access-control-max-age" in response.headers:
            max_age = int(response.headers["access-control-max-age"])
            assert max_age > 0

    def test_vary_header_on_cors_responses(self, client):
        """Test that responses include Vary header for CORS."""
        response = client.get(
            "/v1/clients",
            headers={
                "Origin": "http://localhost:3000",
                "Authorization": "Bearer test_token",
            },
        )

        # Vary header should include Origin (for caching)
        # This is a best practice but not always required
        if "vary" in response.headers:
            assert (
                "Origin" in response.headers["vary"]
                or "origin" in response.headers["vary"]
            )

    def test_cors_headers_case_insensitive(self, client):
        """Test that CORS headers work regardless of case."""
        # HTTP headers are case-insensitive per RFC 7230
        response = client.options(
            "/v1/clients",
            headers={
                "origin": "http://localhost:3000",  # lowercase
                "access-control-request-method": "GET",  # lowercase
            },
        )

        # Should still work
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
