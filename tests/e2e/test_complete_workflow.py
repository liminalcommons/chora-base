"""End-to-end test for complete config workflow.

This module tests the full workflow:
1. Browse servers
2. Add servers to draft
3. View draft
4. Publish config
5. Retrieve published config
"""

import pytest
from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.crypto import ArtifactSigner
from mcp_orchestrator.servers import get_default_registry
from mcp_orchestrator.storage import ArtifactStore


class TestCompleteWorkflow:
    """E2E tests for complete config management workflow."""

    @pytest.fixture
    def temp_store(self, tmp_path):
        """Create temporary artifact store."""
        store_path = tmp_path / ".mcp-orchestration"
        return ArtifactStore(base_path=str(store_path))

    @pytest.fixture
    def temp_keys(self, tmp_path):
        """Create temporary signing keys."""
        key_dir = tmp_path / "keys"
        key_dir.mkdir(parents=True, exist_ok=True)

        signer = ArtifactSigner.generate(key_id="test")
        private_key_path = key_dir / "signing.key"
        public_key_path = key_dir / "signing.pub"

        signer.save_private_key(str(private_key_path))
        signer.save_public_key(str(public_key_path))

        return {
            "private": str(private_key_path),
            "public": str(public_key_path),
        }

    def test_browse_add_publish_workflow(self, temp_store, temp_keys):
        """Test complete workflow: browse → add → publish → retrieve."""
        # Step 1: Browse available servers
        registry = get_default_registry()
        servers = registry.list_all()
        assert len(servers) >= 15  # Should have default catalog

        filesystem_server = registry.get("filesystem")
        assert filesystem_server.server_id == "filesystem"

        # Step 2: Create config and add servers
        builder = ConfigBuilder("claude-desktop", "default", registry)

        # Add filesystem server
        builder.add_server(
            "filesystem",
            params={"path": "/Users/test/Documents"},
        )

        # Add github server
        builder.add_server(
            "github",
            env_vars={"GITHUB_TOKEN": "ghp_test123"},
        )

        # Add memory server (no params)
        builder.add_server("memory")

        # Verify draft state
        assert builder.count() == 3
        assert set(builder.get_servers()) == {"filesystem", "github", "memory"}

        # Step 3: View draft
        draft = builder.build()
        assert "mcpServers" in draft
        assert len(draft["mcpServers"]) == 3
        assert "filesystem" in draft["mcpServers"]
        assert "github" in draft["mcpServers"]
        assert "memory" in draft["mcpServers"]

        # Verify filesystem has correct path
        assert "/Users/test/Documents" in draft["mcpServers"]["filesystem"]["args"]

        # Verify github has env vars
        assert draft["mcpServers"]["github"]["env"]["GITHUB_TOKEN"] == "ghp_test123"

        # Step 4: Publish config as signed artifact
        artifact = builder.to_artifact(
            signing_key_id="test",
            private_key_path=temp_keys["private"],
            changelog="Initial config with 3 servers",
        )

        # Verify artifact properties
        assert artifact.client_id == "claude-desktop"
        assert artifact.profile_id == "default"
        assert artifact.signing_key_id == "test"
        assert len(artifact.artifact_id) == 64  # SHA-256 hash
        assert artifact.metadata["server_count"] == 3
        assert artifact.metadata["changelog"] == "Initial config with 3 servers"

        # Step 5: Store artifact
        temp_store.store(artifact)

        # Step 6: Retrieve published config
        retrieved = temp_store.get("claude-desktop", "default")
        assert retrieved.artifact_id == artifact.artifact_id
        assert retrieved.payload == artifact.payload

        # Verify signature
        from mcp_orchestrator.crypto import verify_signature

        is_valid = verify_signature(
            payload=retrieved.payload,
            signature_b64=retrieved.signature,
            public_key_path=temp_keys["public"],
        )
        assert is_valid

    def test_incremental_updates_workflow(self, temp_store, temp_keys):
        """Test incremental config updates."""
        registry = get_default_registry()

        # Initial config
        builder = ConfigBuilder("claude-desktop", "dev", registry)
        builder.add_server("filesystem", params={"path": "/tmp"})
        builder.add_server("memory")

        artifact_v1 = builder.to_artifact(
            signing_key_id="test",
            private_key_path=temp_keys["private"],
            changelog="v1: Added filesystem and memory",
        )
        temp_store.store(artifact_v1)

        # Update: Add github, remove memory
        builder.remove_server("memory")
        builder.add_server("github", env_vars={"GITHUB_TOKEN": "test"})

        artifact_v2 = builder.to_artifact(
            signing_key_id="test",
            private_key_path=temp_keys["private"],
            changelog="v2: Added github, removed memory",
        )
        temp_store.store(artifact_v2)

        # Retrieve latest
        latest = temp_store.get("claude-desktop", "dev")
        assert latest.artifact_id == artifact_v2.artifact_id
        assert latest.metadata["changelog"] == "v2: Added github, removed memory"

        # Verify content
        assert "filesystem" in latest.payload["mcpServers"]
        assert "github" in latest.payload["mcpServers"]
        assert "memory" not in latest.payload["mcpServers"]

    def test_http_server_auto_wrapping(self, temp_store, temp_keys):
        """Test that HTTP/SSE servers are automatically wrapped with mcp-remote."""
        registry = get_default_registry()
        builder = ConfigBuilder("claude-desktop", "default", registry)

        # Add n8n server (HTTP/SSE)
        builder.add_server(
            "n8n",
            params={"port": 5679},
            env_vars={"N8N_API_KEY": "test_key"},
        )

        draft = builder.build()

        # Verify mcp-remote wrapper
        n8n_config = draft["mcpServers"]["n8n"]
        assert n8n_config["command"] == "npx"
        assert "@modelcontextprotocol/mcp-remote" in n8n_config["args"]
        assert "stdio" in n8n_config["args"]
        assert "http://localhost:5679/mcp/sse" in n8n_config["args"]
        assert n8n_config["env"]["N8N_API_KEY"] == "test_key"

        # Publish and verify wrapping persists
        artifact = builder.to_artifact(
            signing_key_id="test",
            private_key_path=temp_keys["private"],
        )

        assert "@modelcontextprotocol/mcp-remote" in str(artifact.payload)

    def test_multi_client_configs(self, temp_store, temp_keys):
        """Test managing configs for multiple clients."""
        registry = get_default_registry()

        # Claude Desktop config
        builder_claude = ConfigBuilder("claude-desktop", "default", registry)
        builder_claude.add_server("filesystem", params={"path": "/Users/claude/docs"})
        artifact_claude = builder_claude.to_artifact(
            signing_key_id="test",
            private_key_path=temp_keys["private"],
        )
        temp_store.store(artifact_claude)

        # Cursor config
        builder_cursor = ConfigBuilder("cursor", "default", registry)
        builder_cursor.add_server("github", env_vars={"GITHUB_TOKEN": "test"})
        artifact_cursor = builder_cursor.to_artifact(
            signing_key_id="test",
            private_key_path=temp_keys["private"],
        )
        temp_store.store(artifact_cursor)

        # Verify both stored
        claude_config = temp_store.get("claude-desktop", "default")
        cursor_config = temp_store.get("cursor", "default")

        assert claude_config.artifact_id == artifact_claude.artifact_id
        assert cursor_config.artifact_id == artifact_cursor.artifact_id
        assert "filesystem" in claude_config.payload["mcpServers"]
        assert "github" in cursor_config.payload["mcpServers"]
