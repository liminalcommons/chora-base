"""
Authentication service for HTTP API.

Supports:
- Bearer token authentication
- API key authentication
- Token generation and management
"""

import os
import secrets
from datetime import datetime
from typing import Dict, List, Optional, Set

from pydantic import BaseModel


class TokenMetadata(BaseModel):
    """Metadata about an API token."""

    token_id: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    usage_count: int = 0

    def is_expired(self) -> bool:
        """Check if token is expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at


class AuthenticationService:
    """
    Validates bearer tokens and API keys for HTTP requests.

    Attributes:
        api_key: API key from environment (MCP_ORCHESTRATION_API_KEY)
        _tokens: In-memory token store (set of valid tokens)
        _token_metadata: Token creation time, expiry, usage stats
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize authentication service.

        Args:
            api_key: Static API key for authentication. If None, reads from
                    MCP_ORCHESTRATION_API_KEY environment variable.
        """
        # API key (optional, from env or constructor)
        if api_key is None:
            api_key = os.environ.get("MCP_ORCHESTRATION_API_KEY")
        self.api_key = api_key

        # Token store (in-memory for v0.2.0)
        self._tokens: Set[str] = set()
        self._token_metadata: Dict[str, TokenMetadata] = {}

    def generate_token(self) -> str:
        """
        Generate a new cryptographically secure bearer token.

        Returns:
            43-character URL-safe base64 token (32 bytes)

        Security:
            - Uses secrets.token_urlsafe (cryptographically secure)
            - 32 bytes = 43 base64 characters
            - Collision probability negligible
        """
        # Generate 32 bytes = 43 base64 characters
        token = secrets.token_urlsafe(32)

        # Store token
        self._tokens.add(token)

        # Create metadata
        metadata = TokenMetadata(
            token_id=token,
            created_at=datetime.now(),
            expires_at=None,  # No expiry in v0.2.0
            last_used=None,
            usage_count=0,
        )
        self._token_metadata[token] = metadata

        return token

    def validate_token(self, token: Optional[str]) -> bool:
        """
        Validate a bearer token.

        Args:
            token: Bearer token to validate

        Returns:
            True if token is valid, False otherwise

        Side effects:
            Updates token metadata (usage_count, last_used) if valid
        """
        if token is None or token == "":
            return False

        # Check if token exists in store
        if token not in self._tokens:
            return False

        # Check if token is expired
        if token in self._token_metadata:
            metadata = self._token_metadata[token]
            if metadata.is_expired():
                return False

            # Update metadata
            metadata.usage_count += 1
            metadata.last_used = datetime.now()

        return True

    def validate_api_key(self, api_key: Optional[str]) -> bool:
        """
        Validate an API key.

        Args:
            api_key: API key to validate (from X-API-Key header)

        Returns:
            True if API key matches configured key, False otherwise
        """
        if api_key is None or api_key == "":
            return False

        # No API key configured
        if self.api_key is None:
            return False

        # Compare API keys (constant time to prevent timing attacks)
        return secrets.compare_digest(api_key, self.api_key)

    def revoke_token(self, token: str) -> None:
        """
        Revoke a token (remove from store).

        Args:
            token: Token to revoke

        Safe to call with nonexistent token (no-op).
        """
        self._tokens.discard(token)  # discard doesn't raise if not present
        self._token_metadata.pop(token, None)

    def list_tokens(self) -> List[TokenMetadata]:
        """
        List all token metadata.

        Returns:
            List of TokenMetadata objects for all active tokens
        """
        return list(self._token_metadata.values())


# Global singleton instance for shared token store
# This allows CLI-generated tokens to be used by HTTP server
_global_auth_service: Optional[AuthenticationService] = None


def get_auth_service() -> AuthenticationService:
    """
    Get global authentication service instance.

    Returns:
        Singleton AuthenticationService instance
    """
    global _global_auth_service
    if _global_auth_service is None:
        _global_auth_service = AuthenticationService()
    return _global_auth_service
