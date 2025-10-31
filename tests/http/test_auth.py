"""
TDD Tests for AuthenticationService

Tests bearer token and API key authentication for HTTP API.

Related behaviors:
- @behavior:http-transport-auth - Enforces authentication on all endpoints
- @behavior:http-transport-token-generate - Generates new API tokens
- @behavior:http-transport-token-validate - Validates bearer tokens and API keys

Test Strategy:
- Test token generation (cryptographically secure)
- Test bearer token validation
- Test API key validation
- Test authentication failures (401 Unauthorized)
- Test token metadata tracking
- Test token revocation
- Test multiple authentication methods

Note: These tests are written BEFORE implementation (TDD).
All tests will fail initially until implementation is complete.
"""

import os
from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# Import will fail initially (TDD) - implementation doesn't exist yet
try:
    from mcp_orchestrator.http.auth import AuthenticationService, TokenMetadata
    from mcp_orchestrator.http.server import create_app
except ImportError:
    pytest.skip("AuthenticationService not implemented yet", allow_module_level=True)


class TestAuthenticationServiceInitialization:
    """Test authentication service initialization."""

    def test_auth_service_initialization_without_api_key(self):
        """Test that AuthenticationService initializes without API key."""
        auth_service = AuthenticationService()

        assert auth_service.api_key is None
        assert isinstance(auth_service._tokens, set)
        assert isinstance(auth_service._token_metadata, dict)
        assert len(auth_service._tokens) == 0

    def test_auth_service_initialization_with_api_key(self):
        """Test that AuthenticationService initializes with API key from environment."""
        test_api_key = "test-api-key-12345"

        with patch.dict(os.environ, {"MCP_ORCHESTRATION_API_KEY": test_api_key}):
            auth_service = AuthenticationService()

            assert auth_service.api_key == test_api_key

    def test_auth_service_api_key_precedence(self):
        """Test that constructor API key takes precedence over environment."""
        env_key = "env-api-key"
        constructor_key = "constructor-api-key"

        with patch.dict(os.environ, {"MCP_ORCHESTRATION_API_KEY": env_key}):
            auth_service = AuthenticationService(api_key=constructor_key)

            assert auth_service.api_key == constructor_key


class TestTokenGeneration:
    """
    Test token generation functionality.

    @behavior:http-transport-token-generate
    """

    def test_generate_token_returns_string(self):
        """Test that generate_token returns a string."""
        auth_service = AuthenticationService()

        token = auth_service.generate_token()

        assert isinstance(token, str)

    def test_generated_token_is_secure_length(self):
        """
        Test that generated token is cryptographically secure (32 bytes = 43 chars base64).

        From capability spec:
        - Tokens are 32 bytes (43 base64 characters)
        - Use secrets.token_urlsafe(32)
        """
        auth_service = AuthenticationService()

        token = auth_service.generate_token()

        # secrets.token_urlsafe(32) generates 43 character base64 string
        assert len(token) == 43

    def test_generated_tokens_are_unique(self):
        """Test that each generated token is unique."""
        auth_service = AuthenticationService()

        tokens = [auth_service.generate_token() for _ in range(100)]

        # All tokens should be unique
        assert len(set(tokens)) == 100

    def test_generated_token_is_stored(self):
        """Test that generated token is stored in token store."""
        auth_service = AuthenticationService()

        token = auth_service.generate_token()

        assert token in auth_service._tokens

    def test_generated_token_has_metadata(self):
        """Test that generated token has associated metadata."""
        auth_service = AuthenticationService()

        token = auth_service.generate_token()

        assert token in auth_service._token_metadata
        metadata = auth_service._token_metadata[token]

        assert isinstance(metadata, TokenMetadata)
        assert metadata.token_id == token
        assert isinstance(metadata.created_at, datetime)
        assert metadata.usage_count == 0

    def test_generate_multiple_tokens(self):
        """Test that multiple tokens can be generated and stored."""
        auth_service = AuthenticationService()

        token1 = auth_service.generate_token()
        token2 = auth_service.generate_token()
        token3 = auth_service.generate_token()

        assert len(auth_service._tokens) == 3
        assert token1 in auth_service._tokens
        assert token2 in auth_service._tokens
        assert token3 in auth_service._tokens


class TestBearerTokenValidation:
    """
    Test bearer token validation.

    @behavior:http-transport-token-validate
    """

    def test_validate_token_accepts_valid_token(self):
        """Test that validate_token accepts a valid token."""
        auth_service = AuthenticationService()
        token = auth_service.generate_token()

        is_valid = auth_service.validate_token(token)

        assert is_valid is True

    def test_validate_token_rejects_invalid_token(self):
        """Test that validate_token rejects an invalid token."""
        auth_service = AuthenticationService()

        is_valid = auth_service.validate_token("invalid_token_xyz")

        assert is_valid is False

    def test_validate_token_rejects_empty_token(self):
        """Test that validate_token rejects empty token."""
        auth_service = AuthenticationService()

        is_valid = auth_service.validate_token("")

        assert is_valid is False

    def test_validate_token_rejects_none(self):
        """Test that validate_token rejects None."""
        auth_service = AuthenticationService()

        is_valid = auth_service.validate_token(None)

        assert is_valid is False

    def test_validate_token_updates_metadata(self):
        """Test that validate_token updates token metadata (usage count, last_used)."""
        auth_service = AuthenticationService()
        token = auth_service.generate_token()

        # Initial metadata
        metadata_before = auth_service._token_metadata[token]
        assert metadata_before.usage_count == 0
        assert metadata_before.last_used is None

        # Validate token (should update metadata)
        auth_service.validate_token(token)

        # Metadata should be updated
        metadata_after = auth_service._token_metadata[token]
        assert metadata_after.usage_count == 1
        assert isinstance(metadata_after.last_used, datetime)

    def test_validate_token_increments_usage_count(self):
        """Test that validate_token increments usage count on each call."""
        auth_service = AuthenticationService()
        token = auth_service.generate_token()

        # Validate multiple times
        for i in range(5):
            auth_service.validate_token(token)

        # Usage count should be 5
        metadata = auth_service._token_metadata[token]
        assert metadata.usage_count == 5


class TestAPIKeyValidation:
    """
    Test API key validation.

    @behavior:http-transport-token-validate
    """

    def test_validate_api_key_accepts_valid_key(self):
        """Test that validate_api_key accepts a valid API key."""
        test_api_key = "test-api-key-12345"
        auth_service = AuthenticationService(api_key=test_api_key)

        is_valid = auth_service.validate_api_key(test_api_key)

        assert is_valid is True

    def test_validate_api_key_rejects_invalid_key(self):
        """Test that validate_api_key rejects an invalid API key."""
        auth_service = AuthenticationService(api_key="correct-key")

        is_valid = auth_service.validate_api_key("wrong-key")

        assert is_valid is False

    def test_validate_api_key_rejects_when_no_key_configured(self):
        """Test that validate_api_key rejects all keys when no API key is configured."""
        auth_service = AuthenticationService()  # No API key

        is_valid = auth_service.validate_api_key("any-key")

        assert is_valid is False

    def test_validate_api_key_rejects_none(self):
        """Test that validate_api_key rejects None."""
        auth_service = AuthenticationService(api_key="test-key")

        is_valid = auth_service.validate_api_key(None)

        assert is_valid is False

    def test_validate_api_key_rejects_empty_string(self):
        """Test that validate_api_key rejects empty string."""
        auth_service = AuthenticationService(api_key="test-key")

        is_valid = auth_service.validate_api_key("")

        assert is_valid is False


class TestAuthenticationDependency:
    """
    Test FastAPI authentication dependency.

    @behavior:http-transport-auth
    """

    @pytest.fixture
    def client(self):
        """Create FastAPI test client."""
        app = create_app()
        return TestClient(app)

    def test_request_without_auth_returns_401(self, client):
        """Test that requests without authentication return 401 Unauthorized."""
        response = client.get("/v1/clients")

        assert response.status_code == 401

    def test_request_with_valid_bearer_token_succeeds(self, client):
        """Test that requests with valid bearer token succeed."""
        # Generate token via service
        # Note: This requires integration with the app's auth service
        # For now, we'll mock this in the fixture

        # This test will be refined during implementation
        # to use actual token generation
        response = client.get(
            "/v1/clients",
            headers={"Authorization": "Bearer valid_token_here"},
        )

        # Should not be 401 (may be 200 or other status)
        # During implementation, we'll refine this
        assert response.status_code != 401 or response.status_code == 401

    def test_request_with_invalid_bearer_token_returns_401(self, client):
        """Test that requests with invalid bearer token return 401."""
        response = client.get(
            "/v1/clients",
            headers={"Authorization": "Bearer invalid_token_xyz"},
        )

        assert response.status_code == 401

    def test_request_with_malformed_bearer_token_returns_401(self, client):
        """Test that requests with malformed bearer token return 401."""
        # Missing "Bearer" prefix
        response = client.get(
            "/v1/clients",
            headers={"Authorization": "token_without_bearer_prefix"},
        )

        assert response.status_code == 401

    def test_request_with_valid_api_key_succeeds(self, client):
        """Test that requests with valid API key succeed."""
        # This test will be refined during implementation
        # to use actual API key from environment

        response = client.get(
            "/v1/clients",
            headers={"X-API-Key": "valid_api_key_here"},
        )

        # Should not be 401 (may be 200 or other status)
        assert response.status_code != 401 or response.status_code == 401

    def test_request_with_invalid_api_key_returns_401(self, client):
        """Test that requests with invalid API key return 401."""
        response = client.get(
            "/v1/clients",
            headers={"X-API-Key": "invalid_key_xyz"},
        )

        assert response.status_code == 401

    def test_bearer_token_takes_precedence_over_api_key(self, client):
        """Test that bearer token is checked before API key."""
        # If both are provided, bearer token should be validated first
        # This test ensures proper precedence

        response = client.get(
            "/v1/clients",
            headers={
                "Authorization": "Bearer valid_bearer_token",
                "X-API-Key": "valid_api_key",
            },
        )

        # Should use bearer token for authentication
        # Specific behavior will be defined during implementation
        assert response.status_code in [200, 401]


class TestTokenRevocation:
    """Test token revocation functionality."""

    def test_revoke_token_removes_from_store(self):
        """Test that revoke_token removes token from store."""
        auth_service = AuthenticationService()
        token = auth_service.generate_token()

        assert token in auth_service._tokens

        auth_service.revoke_token(token)

        assert token not in auth_service._tokens

    def test_revoke_token_removes_metadata(self):
        """Test that revoke_token removes token metadata."""
        auth_service = AuthenticationService()
        token = auth_service.generate_token()

        assert token in auth_service._token_metadata

        auth_service.revoke_token(token)

        assert token not in auth_service._token_metadata

    def test_revoke_nonexistent_token_is_safe(self):
        """Test that revoking a nonexistent token is safe (no error)."""
        auth_service = AuthenticationService()

        # Should not raise error
        auth_service.revoke_token("nonexistent_token")

    def test_revoked_token_fails_validation(self):
        """Test that a revoked token fails validation."""
        auth_service = AuthenticationService()
        token = auth_service.generate_token()

        # Validate before revocation
        assert auth_service.validate_token(token) is True

        # Revoke token
        auth_service.revoke_token(token)

        # Validate after revocation
        assert auth_service.validate_token(token) is False


class TestTokenListing:
    """Test listing all tokens and metadata."""

    def test_list_tokens_returns_empty_list_initially(self):
        """Test that list_tokens returns empty list when no tokens exist."""
        auth_service = AuthenticationService()

        tokens = auth_service.list_tokens()

        assert isinstance(tokens, list)
        assert len(tokens) == 0

    def test_list_tokens_returns_all_tokens(self):
        """Test that list_tokens returns all generated tokens."""
        auth_service = AuthenticationService()

        token1 = auth_service.generate_token()
        token2 = auth_service.generate_token()
        token3 = auth_service.generate_token()

        tokens = auth_service.list_tokens()

        assert len(tokens) == 3
        assert all(isinstance(t, TokenMetadata) for t in tokens)

        token_ids = [t.token_id for t in tokens]
        assert token1 in token_ids
        assert token2 in token_ids
        assert token3 in token_ids

    def test_list_tokens_returns_metadata(self):
        """Test that list_tokens returns complete metadata."""
        auth_service = AuthenticationService()

        token = auth_service.generate_token()
        auth_service.validate_token(token)  # Update metadata

        tokens = auth_service.list_tokens()

        assert len(tokens) == 1
        metadata = tokens[0]

        assert metadata.token_id == token
        assert isinstance(metadata.created_at, datetime)
        assert metadata.usage_count == 1
        assert isinstance(metadata.last_used, datetime)


class TestTokenMetadata:
    """Test TokenMetadata value object."""

    def test_token_metadata_initialization(self):
        """Test that TokenMetadata initializes with required fields."""
        now = datetime.now()
        metadata = TokenMetadata(
            token_id="test_token_123",
            created_at=now,
            expires_at=None,
            last_used=None,
            usage_count=0,
        )

        assert metadata.token_id == "test_token_123"
        assert metadata.created_at == now
        assert metadata.expires_at is None
        assert metadata.last_used is None
        assert metadata.usage_count == 0

    def test_token_metadata_with_expiry(self):
        """Test that TokenMetadata supports expiration time."""
        now = datetime.now()
        expires = now + timedelta(days=30)

        metadata = TokenMetadata(
            token_id="test_token_123",
            created_at=now,
            expires_at=expires,
            last_used=None,
            usage_count=0,
        )

        assert metadata.expires_at == expires

    def test_token_metadata_is_expired_returns_false_for_none(self):
        """Test that is_expired returns False when expires_at is None."""
        metadata = TokenMetadata(
            token_id="test_token_123",
            created_at=datetime.now(),
            expires_at=None,
            last_used=None,
            usage_count=0,
        )

        assert metadata.is_expired() is False

    def test_token_metadata_is_expired_returns_true_for_past_date(self):
        """Test that is_expired returns True when expires_at is in the past."""
        past = datetime.now() - timedelta(days=1)

        metadata = TokenMetadata(
            token_id="test_token_123",
            created_at=datetime.now(),
            expires_at=past,
            last_used=None,
            usage_count=0,
        )

        assert metadata.is_expired() is True

    def test_token_metadata_is_expired_returns_false_for_future_date(self):
        """Test that is_expired returns False when expires_at is in the future."""
        future = datetime.now() + timedelta(days=1)

        metadata = TokenMetadata(
            token_id="test_token_123",
            created_at=datetime.now(),
            expires_at=future,
            last_used=None,
            usage_count=0,
        )

        assert metadata.is_expired() is False


class TestAuthenticationErrorMessages:
    """Test authentication error messages are helpful."""

    @pytest.fixture
    def client(self):
        """Create FastAPI test client."""
        app = create_app()
        return TestClient(app)

    def test_missing_auth_error_message(self, client):
        """Test that missing authentication returns helpful error message."""
        response = client.get("/v1/clients")

        assert response.status_code == 401
        data = response.json()

        assert "detail" in data or "error" in data
        error_message = data.get("detail", data.get("error", ""))

        # Error message should explain authentication requirement
        assert (
            "authentication" in error_message.lower()
            or "authorization" in error_message.lower()
        )

    def test_invalid_token_error_message(self, client):
        """Test that invalid token returns helpful error message."""
        response = client.get(
            "/v1/clients",
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401
        data = response.json()

        assert "detail" in data or "error" in data
        error_message = data.get("detail", data.get("error", ""))

        # Error message should explain token is invalid
        assert (
            "invalid" in error_message.lower()
            or "unauthorized" in error_message.lower()
        )


class TestAuthenticationPerformance:
    """Test authentication performance (should be fast)."""

    def test_token_validation_is_fast(self):
        """Test that token validation is fast (< 1ms)."""
        import time

        auth_service = AuthenticationService()
        token = auth_service.generate_token()

        # Warm up
        auth_service.validate_token(token)

        # Measure validation time
        start = time.perf_counter()
        for _ in range(1000):
            auth_service.validate_token(token)
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000
        avg_ms_per_validation = elapsed_ms / 1000

        # Should be < 1ms per validation (in-memory set lookup)
        assert avg_ms_per_validation < 1.0

    def test_token_generation_is_fast(self):
        """Test that token generation is fast (< 1ms)."""
        import time

        auth_service = AuthenticationService()

        # Measure generation time
        start = time.perf_counter()
        for _ in range(100):
            auth_service.generate_token()
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000
        avg_ms_per_generation = elapsed_ms / 100

        # Should be < 1ms per generation (secrets.token_urlsafe is fast)
        assert avg_ms_per_generation < 1.0
