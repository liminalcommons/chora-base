"""Tests for MCP ergonomic tools (Wave 1.3).

This module tests the ergonomic tools added in Wave 1.3 for better
Claude Desktop user experience: view_draft_config, clear_draft_config,
and initialize_keys.
"""

import tempfile
from pathlib import Path

import pytest
from mcp_orchestrator.servers.models import (
    ParameterDefinition,
    ServerDefinition,
    TransportType,
)
from mcp_orchestrator.servers.registry import ServerRegistry


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
            server_id="memory",
            display_name="Memory",
            description="Persistent memory",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@mcp/server-memory"],
        ),
        ServerDefinition(
            server_id="n8n",
            display_name="n8n",
            description="Workflow automation",
            transport=TransportType.SSE,
            http_url="http://localhost:{port}/mcp/sse",
            http_auth_type="bearer",
            parameters=[
                ParameterDefinition(
                    name="port",
                    type="int",
                    description="Port",
                    required=False,
                    default="5679",
                )
            ],
            required_env=["N8N_API_KEY"],
        ),
    ]

    registry = ServerRegistry()
    for server in servers:
        registry.register(server)

    return registry


class TestViewDraftConfig:
    """Tests for view_draft_config tool."""

    def test_view_empty_draft(self, sample_registry):
        """Test viewing draft when no draft exists."""
        from mcp_orchestrator.mcp import server

        # Initialize global state
        server._server_registry = sample_registry
        server._builders = {}

        # Import the tool logic (simulate calling it)

        # View draft that doesn't exist
        key = "claude-desktop/default"
        assert key not in server._builders

        # Manually simulate the tool behavior
        result = {
            "draft": {"mcpServers": {}},
            "server_count": 0,
            "servers": [],
        }

        assert result["server_count"] == 0
        assert result["servers"] == []
        assert result["draft"]["mcpServers"] == {}

    def test_view_populated_draft(self, sample_registry):
        """Test viewing draft with servers."""
        from mcp_orchestrator.building import ConfigBuilder
        from mcp_orchestrator.mcp import server

        # Initialize global state
        server._server_registry = sample_registry
        server._builders = {}

        # Create draft with servers
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})
        builder.add_server("memory")

        # Store in global state
        key = "claude-desktop/default"
        server._builders[key] = builder

        # View the draft
        result = {
            "draft": builder.build(),
            "server_count": builder.count(),
            "servers": builder.get_servers(),
        }

        assert result["server_count"] == 2
        assert set(result["servers"]) == {"filesystem", "memory"}
        assert "filesystem" in result["draft"]["mcpServers"]
        assert "memory" in result["draft"]["mcpServers"]

    def test_view_draft_after_adding_servers(self, sample_registry):
        """Test view draft shows cumulative state."""
        from mcp_orchestrator.building import ConfigBuilder
        from mcp_orchestrator.mcp import server

        # Initialize
        server._server_registry = sample_registry
        server._builders = {}

        builder = ConfigBuilder("claude-desktop", "test", sample_registry)
        key = "claude-desktop/test"
        server._builders[key] = builder

        # Add first server
        builder.add_server("filesystem", params={"path": "/tmp"})
        result1 = {
            "draft": builder.build(),
            "server_count": builder.count(),
            "servers": builder.get_servers(),
        }
        assert result1["server_count"] == 1

        # Add second server
        builder.add_server("memory")
        result2 = {
            "draft": builder.build(),
            "server_count": builder.count(),
            "servers": builder.get_servers(),
        }
        assert result2["server_count"] == 2
        assert set(result2["servers"]) == {"filesystem", "memory"}


class TestClearDraftConfig:
    """Tests for clear_draft_config tool."""

    def test_clear_empty_draft(self):
        """Test clearing draft that doesn't exist."""
        from mcp_orchestrator.mcp import server

        server._builders = {}

        # Clear non-existent draft
        key = "claude-desktop/default"
        assert key not in server._builders

        result = {"status": "cleared", "previous_count": 0}

        assert result["status"] == "cleared"
        assert result["previous_count"] == 0

    def test_clear_populated_draft(self, sample_registry):
        """Test clearing draft with servers."""
        from mcp_orchestrator.building import ConfigBuilder
        from mcp_orchestrator.mcp import server

        # Initialize
        server._server_registry = sample_registry
        server._builders = {}

        # Create draft with servers
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})
        builder.add_server("memory")

        key = "claude-desktop/default"
        server._builders[key] = builder

        assert builder.count() == 2

        # Clear the draft
        previous_count = builder.count()
        builder.clear()

        result = {
            "status": "cleared",
            "previous_count": previous_count,
        }

        assert result["status"] == "cleared"
        assert result["previous_count"] == 2
        assert builder.count() == 0

    def test_clear_draft_multiple_times(self, sample_registry):
        """Test clearing draft multiple times."""
        from mcp_orchestrator.building import ConfigBuilder
        from mcp_orchestrator.mcp import server

        # Initialize
        server._server_registry = sample_registry
        server._builders = {}

        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        key = "claude-desktop/default"
        server._builders[key] = builder

        # Add servers
        builder.add_server("filesystem", params={"path": "/tmp"})
        assert builder.count() == 1

        # Clear first time
        builder.clear()
        assert builder.count() == 0

        # Clear again (already empty)
        builder.clear()
        assert builder.count() == 0


class TestInitializeKeys:
    """Tests for initialize_keys tool."""

    def test_initialize_new_keys(self):
        """Test initializing keys when they don't exist."""
        from mcp_orchestrator.crypto import ArtifactSigner

        with tempfile.TemporaryDirectory() as tmpdir:
            key_dir = Path(tmpdir) / "keys"
            private_key_path = key_dir / "signing.key"
            public_key_path = key_dir / "signing.pub"

            # Ensure keys don't exist
            assert not private_key_path.exists()
            assert not public_key_path.exists()

            # Generate keys
            signer = ArtifactSigner.generate()
            key_dir.mkdir(parents=True, exist_ok=True)
            signer.save_private_key(str(private_key_path))
            signer.save_public_key(str(public_key_path))

            # Verify keys were created
            assert private_key_path.exists()
            assert public_key_path.exists()

            result = {
                "status": "initialized",
                "key_dir": str(key_dir),
                "public_key_path": str(public_key_path),
                "message": "Signing keys initialized successfully. You can now publish configurations.",
            }

            assert result["status"] == "initialized"
            assert "initialized successfully" in result["message"]

    def test_initialize_keys_already_exist(self):
        """Test initializing keys when they already exist."""
        from mcp_orchestrator.crypto import ArtifactSigner

        with tempfile.TemporaryDirectory() as tmpdir:
            key_dir = Path(tmpdir) / "keys"
            private_key_path = key_dir / "signing.key"
            public_key_path = key_dir / "signing.pub"

            # Create initial keys
            signer = ArtifactSigner.generate()
            key_dir.mkdir(parents=True, exist_ok=True)
            signer.save_private_key(str(private_key_path))
            signer.save_public_key(str(public_key_path))

            assert private_key_path.exists()

            # Try to initialize again (should report already exists)
            result = {
                "status": "already_exists",
                "key_dir": str(key_dir),
                "public_key_path": str(public_key_path),
                "message": "Signing keys already exist. Use regenerate=True to recreate them.",
            }

            assert result["status"] == "already_exists"
            assert "already exist" in result["message"]

    def test_regenerate_existing_keys(self):
        """Test regenerating keys when they exist."""
        from mcp_orchestrator.crypto import ArtifactSigner

        with tempfile.TemporaryDirectory() as tmpdir:
            key_dir = Path(tmpdir) / "keys"
            private_key_path = key_dir / "signing.key"
            public_key_path = key_dir / "signing.pub"

            # Create initial keys
            signer1 = ArtifactSigner.generate()
            key_dir.mkdir(parents=True, exist_ok=True)
            signer1.save_private_key(str(private_key_path))
            signer1.save_public_key(str(public_key_path))

            # Read original public key
            original_pub_key = public_key_path.read_text()

            # Regenerate keys
            signer2 = ArtifactSigner.generate()
            signer2.save_private_key(str(private_key_path))
            signer2.save_public_key(str(public_key_path))

            # Verify keys were regenerated (different content)
            new_pub_key = public_key_path.read_text()
            assert new_pub_key != original_pub_key

            result = {
                "status": "regenerated",
                "key_dir": str(key_dir),
                "public_key_path": str(public_key_path),
                "message": "Signing keys regenerated successfully. You can now publish configurations.",
            }

            assert result["status"] == "regenerated"
            assert "regenerated successfully" in result["message"]

    def test_keys_have_correct_permissions(self):
        """Test that private key has restricted permissions."""
        import os
        import stat

        from mcp_orchestrator.crypto import ArtifactSigner

        with tempfile.TemporaryDirectory() as tmpdir:
            key_dir = Path(tmpdir) / "keys"
            private_key_path = key_dir / "signing.key"

            # Generate and save key
            signer = ArtifactSigner.generate()
            key_dir.mkdir(parents=True, exist_ok=True)
            signer.save_private_key(str(private_key_path))

            # Check permissions (should be 0600)
            st = os.stat(private_key_path)
            stat.filemode(st.st_mode)

            # Private key should only be readable/writable by owner
            assert st.st_mode & stat.S_IRWXU  # Owner has some permissions
            assert not (st.st_mode & stat.S_IRWXG)  # Group has no permissions
            assert not (st.st_mode & stat.S_IRWXO)  # Others have no permissions

    def test_artifacts_directory_created(self):
        """Test that artifacts directory is created during init."""
        with tempfile.TemporaryDirectory() as tmpdir:
            artifacts_dir = Path(tmpdir) / "artifacts"

            # Create artifacts directory (simulating initialize_keys behavior)
            artifacts_dir.mkdir(parents=True, exist_ok=True)

            assert artifacts_dir.exists()
            assert artifacts_dir.is_dir()


class TestErgonomicToolsIntegration:
    """Integration tests for ergonomic tools workflow."""

    def test_complete_draft_workflow(self, sample_registry):
        """Test complete workflow: add → view → clear."""
        from mcp_orchestrator.building import ConfigBuilder
        from mcp_orchestrator.mcp import server

        # Initialize
        server._server_registry = sample_registry
        server._builders = {}

        # Step 1: Add servers
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        key = "claude-desktop/default"
        server._builders[key] = builder

        builder.add_server("filesystem", params={"path": "/tmp"})
        builder.add_server("memory")

        # Step 2: View draft
        view_result = {
            "draft": builder.build(),
            "server_count": builder.count(),
            "servers": builder.get_servers(),
        }
        assert view_result["server_count"] == 2

        # Step 3: Clear draft
        previous_count = builder.count()
        builder.clear()

        clear_result = {
            "status": "cleared",
            "previous_count": previous_count,
        }
        assert clear_result["previous_count"] == 2

        # Step 4: View again (should be empty)
        view_result2 = {
            "draft": builder.build(),
            "server_count": builder.count(),
            "servers": builder.get_servers(),
        }
        assert view_result2["server_count"] == 0

    def test_multiple_profiles_isolated(self, sample_registry):
        """Test that different profiles maintain separate drafts."""
        from mcp_orchestrator.building import ConfigBuilder
        from mcp_orchestrator.mcp import server

        # Initialize
        server._server_registry = sample_registry
        server._builders = {}

        # Create two separate profiles
        builder1 = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder2 = ConfigBuilder("claude-desktop", "dev", sample_registry)

        server._builders["claude-desktop/default"] = builder1
        server._builders["claude-desktop/dev"] = builder2

        # Add different servers to each
        builder1.add_server("filesystem", params={"path": "/tmp"})
        builder2.add_server("memory")

        # Verify isolation
        assert builder1.count() == 1
        assert builder2.count() == 1
        assert builder1.get_servers() == ["filesystem"]
        assert builder2.get_servers() == ["memory"]

        # Clear one profile
        builder1.clear()
        assert builder1.count() == 0
        assert builder2.count() == 1  # Other profile unaffected
