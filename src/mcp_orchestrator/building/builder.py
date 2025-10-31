"""Configuration builder for constructing MCP client configs.

This module provides the ConfigBuilder class which manages draft configurations
and generates final mcpServers payloads.
"""

from datetime import datetime
from typing import Any

from mcp_orchestrator.servers import ServerRegistry, get_default_registry
from mcp_orchestrator.storage import ConfigArtifact


class ServerAlreadyAddedError(Exception):
    """Raised when trying to add a server that already exists in the config."""

    pass


class ServerNotInConfigError(Exception):
    """Raised when trying to remove a server that doesn't exist in the config."""

    pass


class ConfigBuilder:
    """Builder for constructing MCP client configurations.

    This class manages a draft configuration state and provides methods to:
    - Add servers from the registry
    - Remove servers from the config
    - Build final mcpServers payload
    - Convert to signed ConfigArtifact

    Example:
        >>> builder = ConfigBuilder("claude-desktop", "default")
        >>> builder.add_server(
        ...     "filesystem",
        ...     params={"path": "/Users/me/Documents"}
        ... )
        >>> builder.add_server(
        ...     "github",
        ...     env_vars={"GITHUB_TOKEN": "ghp_..."}
        ... )
        >>> payload = builder.build()
        >>> # payload = {
        ...     "mcpServers": {
        ...         "filesystem": {
        ...             "command": "npx",
        ...             "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/Documents"]
        ...         },
        ...         "github": {
        ...             "command": "npx",
        ...             "args": ["-y", "@modelcontextprotocol/server-github"],
        ...             "env": {"GITHUB_TOKEN": "ghp_..."}
        ...         }
        ...     }
        ... }
    """

    def __init__(
        self,
        client_id: str,
        profile_id: str,
        server_registry: ServerRegistry | None = None,
    ) -> None:
        """Initialize config builder.

        Args:
            client_id: Client family identifier (e.g., "claude-desktop")
            profile_id: Profile identifier (e.g., "default", "dev")
            server_registry: ServerRegistry instance (defaults to global registry)
        """
        self.client_id = client_id
        self.profile_id = profile_id
        self._registry = server_registry or get_default_registry()
        self._servers: dict[str, dict[str, Any]] = {}  # server_name -> config

    def add_server(
        self,
        server_id: str,
        params: dict[str, Any] | None = None,
        env_vars: dict[str, str] | None = None,
        server_name: str | None = None,
    ) -> None:
        """Add a server to the draft configuration.

        Args:
            server_id: Server identifier from registry
            params: Parameter values for server
            env_vars: Environment variables
            server_name: Name to use in config (defaults to server_id)

        Raises:
            ServerNotFoundError: If server_id not found in registry
            ValueError: If required parameters missing
            ServerAlreadyAddedError: If server_name already in config
        """
        # Use server_id as server_name if not provided
        server_name = server_name or server_id

        # Check if server already added
        if server_name in self._servers:
            raise ServerAlreadyAddedError(
                f"Server '{server_name}' already exists in config. "
                "Use a different server_name or remove it first."
            )

        # Generate config from registry (with transport abstraction)
        config = self._registry.to_client_config(
            server_id=server_id,
            params=params,
            env_vars=env_vars,
            server_name=server_name,
        )

        # Add to draft
        self._servers[server_name] = config

    def remove_server(self, server_name: str) -> None:
        """Remove a server from the draft configuration.

        Args:
            server_name: Name of server in config

        Raises:
            ServerNotInConfigError: If server_name not in config
        """
        if server_name not in self._servers:
            raise ServerNotInConfigError(
                f"Server '{server_name}' not found in config. "
                f"Available servers: {sorted(self._servers.keys())}"
            )

        del self._servers[server_name]

    def get_servers(self) -> list[str]:
        """Get list of server names in current draft.

        Returns:
            Sorted list of server names
        """
        return sorted(self._servers.keys())

    def has_server(self, server_name: str) -> bool:
        """Check if a server exists in the draft.

        Args:
            server_name: Name of server to check

        Returns:
            True if server exists, False otherwise
        """
        return server_name in self._servers

    def count(self) -> int:
        """Get number of servers in draft.

        Returns:
            Count of servers
        """
        return len(self._servers)

    def clear(self) -> None:
        """Remove all servers from the draft."""
        self._servers.clear()

    def build(self) -> dict[str, Any]:
        """Build the final mcpServers payload.

        Returns:
            Dictionary with mcpServers structure ready for MCP client

        Example:
            >>> builder.build()
            {
                "mcpServers": {
                    "filesystem": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
                    }
                }
            }
        """
        return {"mcpServers": dict(self._servers)}

    def to_artifact(
        self,
        signing_key_id: str,
        private_key_path: str,
        changelog: str | None = None,
    ) -> ConfigArtifact:
        """Convert draft to signed ConfigArtifact.

        Args:
            signing_key_id: Key identifier for signature
            private_key_path: Path to Ed25519 private key
            changelog: Optional changelog message

        Returns:
            Signed ConfigArtifact ready for storage

        Example:
            >>> artifact = builder.to_artifact(
            ...     signing_key_id="prod-2025",
            ...     private_key_path="~/.mcp-orchestration/keys/signing.key",
            ...     changelog="Added filesystem and github servers"
            ... )
        """
        # Build payload
        payload = self.build()

        # Sign payload
        from mcp_orchestrator.crypto import ArtifactSigner

        signer = ArtifactSigner.from_file(private_key_path, key_id=signing_key_id)
        signature_b64 = signer.sign(payload)

        # Compute artifact ID
        from mcp_orchestrator.storage import ArtifactStore

        store = ArtifactStore()
        artifact_id = store.compute_artifact_id(payload)

        # Create metadata
        metadata: dict[str, Any] = {
            "generator": "ConfigBuilder",
            "server_count": self.count(),
        }
        if changelog:
            metadata["changelog"] = changelog

        # Create artifact
        artifact = ConfigArtifact(
            artifact_id=artifact_id,
            client_id=self.client_id,
            profile_id=self.profile_id,
            created_at=datetime.utcnow().isoformat() + "Z",
            payload=payload,
            signature=signature_b64,
            signing_key_id=signing_key_id,
            metadata=metadata,
        )

        return artifact
