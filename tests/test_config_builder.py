"""Tests for ConfigBuilder (Wave 1.2).

This module tests the ConfigBuilder class for managing draft configurations
and building MCP client config payloads.
"""

import tempfile
from pathlib import Path

import pytest

from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.building.builder import (
    ServerAlreadyAddedError,
    ServerNotInConfigError,
)
from mcp_orchestrator.servers import ServerRegistry
from mcp_orchestrator.servers.models import (
    ParameterDefinition,
    ServerDefinition,
    TransportType,
)


@pytest.fixture
def sample_registry():
    """Create a sample server registry for testing."""
    servers = [
        ServerDefinition(
            server_id="filesystem",
            display_name="Filesystem",
            description="File access",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@mcp/server-filesystem", "{path}"],
            parameters=[
                ParameterDefinition(
                    name="path", type="path", description="Root path", required=True
                )
            ],
        ),
        ServerDefinition(
            server_id="github",
            display_name="GitHub",
            description="GitHub integration",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@mcp/server-github"],
            required_env=["GITHUB_TOKEN"],
        ),
        ServerDefinition(
            server_id="n8n",
            display_name="n8n",
            description="n8n integration",
            transport=TransportType.HTTP,
            http_url="http://localhost:{port}/mcp",
            required_env=["N8N_API_KEY"],
            parameters=[
                ParameterDefinition(
                    name="port", type="int", description="Port", required=True
                )
            ],
        ),
    ]
    return ServerRegistry(servers)


class TestConfigBuilderBasics:
    """Tests for basic ConfigBuilder functionality."""

    def test_init(self, sample_registry):
        """Test builder initialization."""
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)

        assert builder.client_id == "claude-desktop"
        assert builder.profile_id == "default"
        assert builder.count() == 0
        assert builder.get_servers() == []

    def test_add_server_stdio(self, sample_registry):
        """Test adding a stdio server."""
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)

        builder.add_server("filesystem", params={"path": "/Users/me/Documents"})

        assert builder.count() == 1
        assert builder.has_server("filesystem")
        assert "filesystem" in builder.get_servers()

    def test_add_server_http(self, sample_registry):
        """Test adding an HTTP server (auto-wrapped with mcp-remote)."""
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)

        builder.add_server(
            "n8n", params={"port": 5679}, env_vars={"N8N_API_KEY": "secret"}
        )

        assert builder.count() == 1
        assert builder.has_server("n8n")

        # Build and verify mcp-remote wrapper
        payload = builder.build()
        assert "n8n" in payload["mcpServers"]
        assert payload["mcpServers"]["n8n"]["command"] == "npx"
        assert "@modelcontextprotocol/mcp-remote" in payload["mcpServers"]["n8n"]["args"]

    def test_add_server_with_custom_name(self, sample_registry):
        """Test adding a server with custom name."""
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)

        builder.add_server(
            "filesystem",
            params={"path": "/tmp"},
            server_name="filesystem-tmp",
        )

        assert builder.count() == 1
        assert builder.has_server("filesystem-tmp")
        assert not builder.has_server("filesystem")

    def test_add_multiple_servers(self, sample_registry):
        """Test adding multiple servers."""
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)

        builder.add_server("filesystem", params={"path": "/Users/me/Documents"})
        builder.add_server("github", env_vars={"GITHUB_TOKEN": "ghp_test"})

        assert builder.count() == 2
        assert builder.has_server("filesystem")
        assert builder.has_server("github")
        assert set(builder.get_servers()) == {"filesystem", "github"}

    def test_add_server_duplicate_name_fails(self, sample_registry):
        """Test that adding a server with duplicate name fails."""
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)

        builder.add_server("filesystem", params={"path": "/tmp"})

        with pytest.raises(
            ServerAlreadyAddedError, match="Server 'filesystem' already exists"
        ):
            builder.add_server("filesystem", params={"path": "/home"})

    def test_remove_server(self, sample_registry):
        """Test removing a server."""
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)

        builder.add_server("filesystem", params={"path": "/tmp"})
        assert builder.count() == 1

        builder.remove_server("filesystem")
        assert builder.count() == 0
        assert not builder.has_server("filesystem")

    def test_remove_nonexistent_server_fails(self, sample_registry):
        """Test that removing a nonexistent server fails."""
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)

        with pytest.raises(
            ServerNotInConfigError, match="Server 'nonexistent' not found"
        ):
            builder.remove_server("nonexistent")

    def test_clear(self, sample_registry):
        """Test clearing all servers."""
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)

        builder.add_server("filesystem", params={"path": "/tmp"})
        builder.add_server("github", env_vars={"GITHUB_TOKEN": "test"})
        assert builder.count() == 2

        builder.clear()
        assert builder.count() == 0
        assert builder.get_servers() == []


class TestConfigBuilderBuild:
    """Tests for building final mcpServers payloads."""

    def test_build_empty(self, sample_registry):
        """Test building empty config."""
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)

        payload = builder.build()

        assert payload == {"mcpServers": {}}

    def test_build_single_server(self, sample_registry):
        """Test building config with single server."""
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/Users/me/Documents"})

        payload = builder.build()

        assert "mcpServers" in payload
        assert "filesystem" in payload["mcpServers"]
        assert payload["mcpServers"]["filesystem"]["command"] == "npx"
        assert "/Users/me/Documents" in payload["mcpServers"]["filesystem"]["args"]

    def test_build_multiple_servers(self, sample_registry):
        """Test building config with multiple servers."""
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})
        builder.add_server("github", env_vars={"GITHUB_TOKEN": "test"})

        payload = builder.build()

        assert len(payload["mcpServers"]) == 2
        assert "filesystem" in payload["mcpServers"]
        assert "github" in payload["mcpServers"]

    def test_build_with_env_vars(self, sample_registry):
        """Test building config with environment variables."""
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("github", env_vars={"GITHUB_TOKEN": "ghp_test123"})

        payload = builder.build()

        assert payload["mcpServers"]["github"]["env"] == {"GITHUB_TOKEN": "ghp_test123"}

    def test_build_http_server_wrapped(self, sample_registry):
        """Test that HTTP servers are wrapped with mcp-remote in build."""
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server(
            "n8n", params={"port": 5679}, env_vars={"N8N_API_KEY": "secret"}
        )

        payload = builder.build()

        n8n_config = payload["mcpServers"]["n8n"]
        assert n8n_config["command"] == "npx"
        assert "-y" in n8n_config["args"]
        assert "@modelcontextprotocol/mcp-remote" in n8n_config["args"]
        assert "stdio" in n8n_config["args"]
        assert "http://localhost:5679/mcp" in n8n_config["args"]
        assert n8n_config["env"] == {"N8N_API_KEY": "secret"}


class TestConfigBuilderArtifact:
    """Tests for converting drafts to signed artifacts."""

    def test_to_artifact_basic(self, sample_registry, tmp_path):
        """Test converting draft to artifact."""
        # Create temporary keys
        from mcp_orchestrator.crypto import ArtifactSigner

        signer = ArtifactSigner.generate(key_id="test-2025")
        private_key_path = tmp_path / "test_signing.key"
        signer.save_private_key(str(private_key_path))

        # Build draft
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})

        # Convert to artifact
        artifact = builder.to_artifact(
            signing_key_id="test-2025",
            private_key_path=str(private_key_path),
            changelog="Added filesystem server",
        )

        # Verify artifact
        assert artifact.client_id == "claude-desktop"
        assert artifact.profile_id == "default"
        assert artifact.signing_key_id == "test-2025"
        assert artifact.payload == builder.build()
        assert artifact.metadata["changelog"] == "Added filesystem server"
        assert artifact.metadata["generator"] == "ConfigBuilder"
        assert artifact.metadata["server_count"] == 1
        assert len(artifact.signature) > 0  # Has signature

    def test_to_artifact_verifiable(self, sample_registry, tmp_path):
        """Test that generated artifact has valid signature."""
        # Create temporary keys
        from mcp_orchestrator.crypto import ArtifactSigner, verify_signature

        signer = ArtifactSigner.generate(key_id="test-2025")
        private_key_path = tmp_path / "test_signing.key"
        public_key_path = tmp_path / "test_signing.pub"
        signer.save_private_key(str(private_key_path))
        signer.save_public_key(str(public_key_path))

        # Build draft
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})

        # Convert to artifact
        artifact = builder.to_artifact(
            signing_key_id="test-2025",
            private_key_path=str(private_key_path),
        )

        # Verify signature
        is_valid = verify_signature(
            payload=artifact.payload,
            signature_b64=artifact.signature,
            public_key_path=str(public_key_path),
        )

        assert is_valid

    def test_to_artifact_content_addressable(self, sample_registry, tmp_path):
        """Test that artifact_id is SHA-256 hash of payload."""
        from mcp_orchestrator.crypto import ArtifactSigner
        from mcp_orchestrator.storage import ArtifactStore

        signer = ArtifactSigner.generate(key_id="test-2025")
        private_key_path = tmp_path / "test_signing.key"
        signer.save_private_key(str(private_key_path))

        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})

        artifact = builder.to_artifact(
            signing_key_id="test-2025",
            private_key_path=str(private_key_path),
        )

        # Verify artifact_id is SHA-256 of payload
        store = ArtifactStore()
        expected_id = store.compute_artifact_id(artifact.payload)
        assert artifact.artifact_id == expected_id


class TestConfigBuilderIntegration:
    """Integration tests using default registry."""

    def test_build_realistic_config(self):
        """Test building a realistic config with default registry."""
        from mcp_orchestrator.servers import get_default_registry

        registry = get_default_registry()
        builder = ConfigBuilder("claude-desktop", "default", registry)

        # Add several servers
        builder.add_server("filesystem", params={"path": "/Users/me/Documents"})
        builder.add_server("github", env_vars={"GITHUB_TOKEN": "ghp_test"})
        builder.add_server("memory")  # No params needed

        payload = builder.build()

        # Verify structure
        assert len(payload["mcpServers"]) == 3
        assert "filesystem" in payload["mcpServers"]
        assert "github" in payload["mcpServers"]
        assert "memory" in payload["mcpServers"]

        # Verify configs are valid
        for server_name, config in payload["mcpServers"].items():
            assert "command" in config
            assert "args" in config
            assert isinstance(config["args"], list)

    def test_add_remove_workflow(self):
        """Test realistic add/remove workflow."""
        from mcp_orchestrator.servers import get_default_registry

        registry = get_default_registry()
        builder = ConfigBuilder("claude-desktop", "dev", registry)

        # Build up config
        builder.add_server("filesystem", params={"path": "/tmp"})
        builder.add_server("memory")
        builder.add_server("github", env_vars={"GITHUB_TOKEN": "test"})
        assert builder.count() == 3

        # Remove one
        builder.remove_server("memory")
        assert builder.count() == 2
        assert not builder.has_server("memory")

        # Add another
        builder.add_server(
            "filesystem",
            params={"path": "/home"},
            server_name="filesystem-home",
        )
        assert builder.count() == 3

        # Verify final state
        servers = builder.get_servers()
        assert "filesystem" in servers
        assert "github" in servers
        assert "filesystem-home" in servers
        assert "memory" not in servers
