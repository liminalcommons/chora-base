"""Comprehensive tests for MCP server tools and resources.

This module tests all 14 MCP tools and 7 resources to increase coverage
from 15.15% to 60%+ for src/mcp_orchestrator/mcp/server.py.

Test Coverage:
- Wave 1.0: list_clients, list_profiles, get_config, diff_config
- Wave 1.1: list_available_servers, describe_server
- Wave 1.2: add_server_to_config, remove_server_from_config, publish_config
- Wave 1.3: view_draft_config, clear_draft_config, initialize_keys
- Wave 1.4: validate_config
- Wave 1.5: deploy_config
- Wave 2.2/3.0: check_server_installation, install_server, list_installed_servers
- Resources: Testing via dedicated resource test classes
"""

import json
from unittest.mock import Mock, patch

import pytest
from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.crypto import ArtifactSigner
from mcp_orchestrator.deployment.log import DeploymentLog
from mcp_orchestrator.mcp import server
from mcp_orchestrator.publishing import PublishingWorkflow
from mcp_orchestrator.registry import get_default_registry
from mcp_orchestrator.servers import ServerRegistry
from mcp_orchestrator.servers.models import (
    PackageManager,
    ParameterDefinition,
    ServerDefinition,
    TransportType,
)
from mcp_orchestrator.storage import ArtifactStore

# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def sample_server_registry():
    """Create sample server registry with test servers."""
    registry = ServerRegistry()

    # Add test servers
    registry.register(
        ServerDefinition(
            server_id="filesystem",
            display_name="Filesystem",
            description="File access server",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-filesystem", "{path}"],
            npm_package="@modelcontextprotocol/server-filesystem",
            package_manager=PackageManager.NPM,
            parameters=[
                ParameterDefinition(
                    name="path",
                    type="path",
                    description="Root path",
                    required=True,
                    example="/Users/me/Documents",
                )
            ],
            tags=["filesystem", "files"],
        )
    )

    registry.register(
        ServerDefinition(
            server_id="github",
            display_name="GitHub",
            description="GitHub integration",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-github"],
            npm_package="@modelcontextprotocol/server-github",
            package_manager=PackageManager.NPM,
            required_env=["GITHUB_TOKEN"],
            tags=["github", "git"],
        )
    )

    registry.register(
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
                    description="Port number",
                    required=False,
                    default="5679",
                    example="5679",
                )
            ],
            required_env=["N8N_API_KEY"],
            tags=["workflow", "automation"],
        )
    )

    return registry


@pytest.fixture
def setup_mcp_server(tmp_path, sample_server_registry):
    """Setup MCP server with temporary storage and registries."""
    # Initialize storage
    artifacts_dir = tmp_path / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # Initialize keys
    keys_dir = tmp_path / "keys"
    keys_dir.mkdir(parents=True, exist_ok=True)
    private_key_path = keys_dir / "signing.key"
    public_key_path = keys_dir / "signing.pub"

    signer = ArtifactSigner.generate(key_id="test")
    signer.save_private_key(str(private_key_path))
    signer.save_public_key(str(public_key_path))

    # Setup server global state
    server._store = ArtifactStore(base_path=tmp_path)
    server._registry = get_default_registry()
    server._server_registry = sample_server_registry
    server._builders = {}
    server._deployment_log = DeploymentLog(
        deployments_dir=str(tmp_path / "deployments")
    )

    yield {
        "tmp_path": tmp_path,
        "store": server._store,
        "registry": server._registry,
        "server_registry": sample_server_registry,
        "private_key_path": private_key_path,
        "public_key_path": public_key_path,
    }

    # Cleanup
    server._builders = {}


# =============================================================================
# WAVE 1.0 TOOLS: list_clients, list_profiles, get_config, diff_config
# =============================================================================


class TestListClients:
    """Tests for list_clients tool."""

    @pytest.mark.asyncio
    async def test_list_clients_returns_supported_clients(self, setup_mcp_server):
        """Test list_clients returns all supported client families."""
        # Call underlying function directly
        result = await server.list_clients.fn()

        assert "clients" in result
        assert "count" in result
        assert isinstance(result["clients"], list)
        assert result["count"] > 0

        # Verify client structure
        for client in result["clients"]:
            assert "client_id" in client
            assert "display_name" in client
            assert "platform" in client
            assert "config_location" in client
            assert "available_profiles" in client

    @pytest.mark.asyncio
    async def test_list_clients_includes_claude_desktop(self, setup_mcp_server):
        """Test list_clients includes claude-desktop client."""
        result = await server.list_clients.fn()

        client_ids = [c["client_id"] for c in result["clients"]]
        assert "claude-desktop" in client_ids


class TestListProfiles:
    """Tests for list_profiles tool."""

    @pytest.mark.asyncio
    async def test_list_profiles_for_valid_client(self, setup_mcp_server):
        """Test list_profiles returns profiles for valid client."""
        result = await server.list_profiles.fn(client_id="claude-desktop")

        assert "client_id" in result
        assert result["client_id"] == "claude-desktop"
        assert "profiles" in result
        assert "count" in result
        assert isinstance(result["profiles"], list)
        assert result["count"] > 0

        # Verify profile structure
        for profile in result["profiles"]:
            assert "profile_id" in profile
            assert "display_name" in profile
            assert "description" in profile

    @pytest.mark.asyncio
    async def test_list_profiles_invalid_client_raises_error(self, setup_mcp_server):
        """Test list_profiles raises ValueError for invalid client."""
        with pytest.raises(ValueError, match="Client 'nonexistent' not found"):
            await server.list_profiles.fn(client_id="nonexistent")

    @pytest.mark.asyncio
    async def test_list_profiles_includes_metadata_when_available(
        self, setup_mcp_server
    ):
        """Test list_profiles includes storage metadata when profile exists."""
        setup = setup_mcp_server

        # Publish a config first
        builder = ConfigBuilder("claude-desktop", "default", setup["server_registry"])
        builder.add_server("filesystem", params={"path": "/tmp"})

        workflow = PublishingWorkflow(
            store=setup["store"], client_registry=setup["registry"]
        )
        workflow.publish(
            builder=builder,
            private_key_path=str(setup["private_key_path"]),
            signing_key_id="test",
        )

        # Now list profiles - should include artifact metadata
        result = await server.list_profiles.fn(client_id="claude-desktop")

        default_profile = next(
            p for p in result["profiles"] if p["profile_id"] == "default"
        )
        assert "latest_artifact_id" in default_profile
        assert default_profile["latest_artifact_id"] is not None


class TestGetConfig:
    """Tests for get_config tool."""

    @pytest.mark.asyncio
    async def test_get_config_retrieves_latest_artifact(self, setup_mcp_server):
        """Test get_config retrieves latest configuration."""
        setup = setup_mcp_server

        # Publish a config
        builder = ConfigBuilder("claude-desktop", "default", setup["server_registry"])
        builder.add_server("filesystem", params={"path": "/tmp"})

        workflow = PublishingWorkflow(
            store=setup["store"], client_registry=setup["registry"]
        )
        result = workflow.publish(
            builder=builder,
            private_key_path=str(setup["private_key_path"]),
            signing_key_id="test",
        )

        artifact_id = result["artifact_id"]

        # Retrieve config
        config = await server.get_config.fn(
            client_id="claude-desktop", profile_id="default"
        )

        assert config["artifact_id"] == artifact_id
        assert config["client_id"] == "claude-desktop"
        assert config["profile_id"] == "default"
        assert "payload" in config
        assert "signature" in config
        assert "signing_key_id" in config

    @pytest.mark.asyncio
    async def test_get_config_invalid_client_raises_error(self, setup_mcp_server):
        """Test get_config raises ValueError for invalid client."""
        with pytest.raises(ValueError, match="Client 'nonexistent' not found"):
            await server.get_config.fn(client_id="nonexistent", profile_id="default")

    @pytest.mark.asyncio
    async def test_get_config_missing_artifact_raises_error(self, setup_mcp_server):
        """Test get_config raises ValueError when no artifact exists."""
        with pytest.raises(ValueError, match="No configuration found"):
            await server.get_config.fn(client_id="claude-desktop", profile_id="default")


class TestDiffConfig:
    """Tests for diff_config tool."""

    @pytest.mark.asyncio
    async def test_diff_config_detects_up_to_date(self, setup_mcp_server):
        """Test diff_config detects when local matches remote."""
        setup = setup_mcp_server

        # Publish a config
        builder = ConfigBuilder("claude-desktop", "default", setup["server_registry"])
        builder.add_server("filesystem", params={"path": "/tmp"})

        workflow = PublishingWorkflow(
            store=setup["store"], client_registry=setup["registry"]
        )
        workflow.publish(
            builder=builder,
            private_key_path=str(setup["private_key_path"]),
            signing_key_id="test",
        )

        # Diff against same config
        diff_result = await server.diff_config.fn(
            client_id="claude-desktop",
            profile_id="default",
            local_payload=builder.build(),
        )

        assert diff_result["status"] == "up-to-date"
        assert diff_result["diff"]["servers_added"] == []
        assert diff_result["diff"]["servers_removed"] == []
        assert diff_result["diff"]["servers_modified"] == []

    @pytest.mark.asyncio
    async def test_diff_config_requires_local_payload_or_id(self, setup_mcp_server):
        """Test diff_config raises error when neither payload nor ID provided."""
        with pytest.raises(
            ValueError, match="Must provide either local_artifact_id or local_payload"
        ):
            await server.diff_config.fn(
                client_id="claude-desktop", profile_id="default"
            )


# =============================================================================
# WAVE 1.1 TOOLS: list_available_servers, describe_server
# =============================================================================


class TestListAvailableServers:
    """Tests for list_available_servers tool."""

    @pytest.mark.asyncio
    async def test_list_all_servers(self, setup_mcp_server):
        """Test list_available_servers returns all servers."""
        result = await server.list_available_servers.fn()

        assert "servers" in result
        assert "count" in result
        assert "transport_counts" in result
        assert "available_transports" in result
        assert isinstance(result["servers"], list)
        assert result["count"] == len(result["servers"])

    @pytest.mark.asyncio
    async def test_filter_by_transport(self, setup_mcp_server):
        """Test list_available_servers filters by transport type."""
        result = await server.list_available_servers.fn(transport_filter="stdio")

        # All servers should be stdio
        for srv in result["servers"]:
            assert srv["transport"] == "stdio"

    @pytest.mark.asyncio
    async def test_filter_by_invalid_transport_raises_error(self, setup_mcp_server):
        """Test list_available_servers raises error for invalid transport."""
        with pytest.raises(ValueError, match="Invalid transport filter"):
            await server.list_available_servers.fn(transport_filter="invalid")

    @pytest.mark.asyncio
    async def test_search_servers(self, setup_mcp_server):
        """Test list_available_servers searches by query."""
        result = await server.list_available_servers.fn(search_query="filesystem")

        assert result["count"] > 0
        # Should include filesystem server
        server_ids = [s["server_id"] for s in result["servers"]]
        assert "filesystem" in server_ids


class TestDescribeServer:
    """Tests for describe_server tool."""

    @pytest.mark.asyncio
    async def test_describe_server_returns_full_definition(self, setup_mcp_server):
        """Test describe_server returns complete server definition."""
        result = await server.describe_server.fn(server_id="filesystem")

        assert result["server_id"] == "filesystem"
        assert "display_name" in result
        assert "description" in result
        assert "transport" in result
        assert "parameters" in result
        assert "env_vars" in result
        assert "installation" in result
        assert "usage_example" in result

    @pytest.mark.asyncio
    async def test_describe_server_stdio_transport_info(self, setup_mcp_server):
        """Test describe_server includes stdio transport details."""
        result = await server.describe_server.fn(server_id="filesystem")

        transport = result["transport"]
        assert transport["type"] == "stdio"
        assert "command" in transport
        assert "args" in transport

    @pytest.mark.asyncio
    async def test_describe_server_http_transport_info(self, setup_mcp_server):
        """Test describe_server includes HTTP/SSE transport details."""
        result = await server.describe_server.fn(server_id="n8n")

        transport = result["transport"]
        assert transport["type"] == "sse"
        assert "url" in transport
        assert "note" in transport
        assert "mcp-remote" in transport["note"]

    @pytest.mark.asyncio
    async def test_describe_server_invalid_id_raises_error(self, setup_mcp_server):
        """Test describe_server raises error for invalid server ID."""
        with pytest.raises(ValueError, match="not found"):
            await server.describe_server.fn(server_id="nonexistent")

    @pytest.mark.asyncio
    async def test_describe_server_usage_example_is_valid_json(self, setup_mcp_server):
        """Test describe_server usage example is valid JSON."""
        result = await server.describe_server.fn(server_id="filesystem")

        usage_example = result["usage_example"]
        # Should be valid JSON
        parsed = json.loads(usage_example)
        assert "mcpServers" in parsed


# =============================================================================
# WAVE 1.2 TOOLS: add_server_to_config, remove_server_from_config, publish_config
# =============================================================================


class TestAddServerToConfig:
    """Tests for add_server_to_config tool."""

    @pytest.mark.asyncio
    async def test_add_server_to_empty_draft(self, setup_mcp_server):
        """Test adding server to empty draft configuration."""
        result = await server.add_server_to_config.fn(
            server_id="filesystem",
            params={"path": "/tmp"},
            client_id="claude-desktop",
            profile_id="default",
        )

        assert result["status"] == "added"
        assert result["server_name"] == "filesystem"
        assert result["server_count"] == 1
        assert "draft" in result
        assert "filesystem" in result["draft"]["mcpServers"]

    @pytest.mark.asyncio
    async def test_add_server_with_custom_name(self, setup_mcp_server):
        """Test adding server with custom name."""
        result = await server.add_server_to_config.fn(
            server_id="filesystem",
            params={"path": "/tmp"},
            server_name="my-filesystem",
            client_id="claude-desktop",
            profile_id="default",
        )

        assert result["server_name"] == "my-filesystem"
        assert "my-filesystem" in result["draft"]["mcpServers"]

    @pytest.mark.asyncio
    async def test_add_server_with_env_vars(self, setup_mcp_server):
        """Test adding server with environment variables."""
        result = await server.add_server_to_config.fn(
            server_id="github",
            env_vars={"GITHUB_TOKEN": "test-token"},
            client_id="claude-desktop",
            profile_id="default",
        )

        assert result["status"] == "added"
        github_config = result["draft"]["mcpServers"]["github"]
        assert "env" in github_config
        assert github_config["env"]["GITHUB_TOKEN"] == "test-token"

    @pytest.mark.asyncio
    async def test_add_server_with_json_string_params(self, setup_mcp_server):
        """Test adding server with params as JSON string (Claude Desktop format)."""
        params_json = json.dumps({"path": "/tmp"})

        result = await server.add_server_to_config.fn(
            server_id="filesystem",
            params=params_json,
            client_id="claude-desktop",
            profile_id="default",
        )

        assert result["status"] == "added"
        assert result["server_count"] == 1

    @pytest.mark.asyncio
    async def test_add_server_invalid_id_raises_error(self, setup_mcp_server):
        """Test adding server with invalid ID raises error."""
        with pytest.raises(ValueError, match="Server not found"):
            await server.add_server_to_config.fn(
                server_id="nonexistent",
                client_id="claude-desktop",
                profile_id="default",
            )


class TestRemoveServerFromConfig:
    """Tests for remove_server_from_config tool."""

    @pytest.mark.asyncio
    async def test_remove_server_from_draft(self, setup_mcp_server):
        """Test removing server from draft configuration."""
        # Add servers first
        await server.add_server_to_config.fn(
            server_id="filesystem", params={"path": "/tmp"}
        )
        await server.add_server_to_config.fn(
            server_id="github", env_vars={"GITHUB_TOKEN": "test"}
        )

        # Remove one
        result = await server.remove_server_from_config.fn(
            server_name="filesystem", client_id="claude-desktop", profile_id="default"
        )

        assert result["status"] == "removed"
        assert result["server_name"] == "filesystem"
        assert result["server_count"] == 1
        assert "filesystem" not in result["draft"]["mcpServers"]
        assert "github" in result["draft"]["mcpServers"]

    @pytest.mark.asyncio
    async def test_remove_nonexistent_server_raises_error(self, setup_mcp_server):
        """Test removing non-existent server raises error."""
        with pytest.raises(ValueError):
            await server.remove_server_from_config.fn(
                server_name="nonexistent",
                client_id="claude-desktop",
                profile_id="default",
            )


# =============================================================================
# WAVE 1.3 TOOLS: view_draft_config, clear_draft_config, initialize_keys
# =============================================================================


class TestViewDraftConfig:
    """Tests for view_draft_config tool."""

    @pytest.mark.asyncio
    async def test_view_empty_draft(self, setup_mcp_server):
        """Test viewing draft when none exists."""
        result = await server.view_draft_config.fn(
            client_id="claude-desktop", profile_id="default"
        )

        assert result["server_count"] == 0
        assert result["servers"] == []
        assert result["draft"]["mcpServers"] == {}

    @pytest.mark.asyncio
    async def test_view_populated_draft(self, setup_mcp_server):
        """Test viewing draft with servers."""
        # Add servers
        await server.add_server_to_config.fn(
            server_id="filesystem", params={"path": "/tmp"}
        )
        await server.add_server_to_config.fn(
            server_id="github", env_vars={"GITHUB_TOKEN": "test"}
        )

        # View draft
        result = await server.view_draft_config.fn()

        assert result["server_count"] == 2
        assert set(result["servers"]) == {"filesystem", "github"}
        assert "filesystem" in result["draft"]["mcpServers"]
        assert "github" in result["draft"]["mcpServers"]


class TestClearDraftConfig:
    """Tests for clear_draft_config tool."""

    @pytest.mark.asyncio
    async def test_clear_empty_draft(self, setup_mcp_server):
        """Test clearing when no draft exists."""
        result = await server.clear_draft_config.fn()

        assert result["status"] == "cleared"
        assert result["previous_count"] == 0

    @pytest.mark.asyncio
    async def test_clear_populated_draft(self, setup_mcp_server):
        """Test clearing draft with servers."""
        # Add servers
        await server.add_server_to_config.fn(
            server_id="filesystem", params={"path": "/tmp"}
        )
        await server.add_server_to_config.fn(
            server_id="github", env_vars={"GITHUB_TOKEN": "test"}
        )

        # Clear
        result = await server.clear_draft_config.fn()

        assert result["status"] == "cleared"
        assert result["previous_count"] == 2

        # Verify cleared
        view_result = await server.view_draft_config.fn()
        assert view_result["server_count"] == 0


class TestInitializeKeys:
    """Tests for initialize_keys tool."""

    @pytest.mark.asyncio
    async def test_initialize_new_keys(self, tmp_path):
        """Test initializing keys when they don't exist."""
        # Use custom home to avoid interfering with real keys
        with patch("pathlib.Path.home", return_value=tmp_path):
            result = await server.initialize_keys.fn()

            assert result["status"] == "initialized"
            assert "key_dir" in result
            assert "public_key_path" in result

            # Verify keys were created
            key_dir = tmp_path / ".mcp-orchestration" / "keys"
            assert (key_dir / "signing.key").exists()
            assert (key_dir / "signing.pub").exists()

    @pytest.mark.asyncio
    async def test_initialize_keys_already_exist(self, tmp_path):
        """Test initializing when keys already exist."""
        with patch("pathlib.Path.home", return_value=tmp_path):
            # Initialize once
            result1 = await server.initialize_keys.fn()
            assert result1["status"] == "initialized"

            # Try again
            result2 = await server.initialize_keys.fn()
            assert result2["status"] == "already_exists"
            assert "already exist" in result2["message"]


# =============================================================================
# WAVE 1.4 TOOLS: validate_config
# =============================================================================


class TestValidateConfig:
    """Tests for validate_config tool."""

    @pytest.mark.asyncio
    async def test_validate_empty_config_fails(self, setup_mcp_server):
        """Test validating empty config returns errors."""
        result = await server.validate_config.fn()

        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert any(e["code"] == "EMPTY_CONFIG" for e in result["errors"])

    @pytest.mark.asyncio
    async def test_validate_valid_config_passes(self, setup_mcp_server):
        """Test validating valid config passes."""
        # Add valid server
        await server.add_server_to_config.fn(
            server_id="filesystem", params={"path": "/tmp"}
        )

        result = await server.validate_config.fn()

        assert result["valid"] is True
        assert len(result["errors"]) == 0
        assert result["server_count"] == 1

    @pytest.mark.asyncio
    async def test_validate_includes_timestamp(self, setup_mcp_server):
        """Test validation result includes timestamp."""
        result = await server.validate_config.fn()

        assert "validated_at" in result
        assert result["validated_at"].endswith("Z")  # ISO 8601 UTC


# =============================================================================
# WAVE 1.5 TOOLS: deploy_config
# =============================================================================


class TestDeployConfig:
    """Tests for deploy_config tool."""

    @pytest.mark.asyncio
    async def test_deploy_without_published_config_raises_error(self, setup_mcp_server):
        """Test deploy raises error when no published config exists."""
        with pytest.raises(ValueError):
            await server.deploy_config.fn(
                client_id="claude-desktop", profile_id="default"
            )


# =============================================================================
# WAVE 2.2/3.0 TOOLS: check_server_installation, install_server, list_installed_servers
# =============================================================================


class TestCheckServerInstallation:
    """Tests for check_server_installation tool."""

    @pytest.mark.asyncio
    async def test_check_installation_invalid_server_raises_error(
        self, setup_mcp_server
    ):
        """Test checking installation for invalid server raises error."""
        with pytest.raises(ValueError, match="not found"):
            await server.check_server_installation.fn(server_id="nonexistent")

    @pytest.mark.asyncio
    async def test_check_installation_returns_status(self, setup_mcp_server):
        """Test check_server_installation returns status."""
        result = await server.check_server_installation.fn(server_id="filesystem")

        assert "server_id" in result
        assert result["server_id"] == "filesystem"
        assert "status" in result
        assert result["status"] in ["installed", "not_installed", "unknown", "error"]


class TestInstallServer:
    """Tests for install_server tool."""

    @pytest.mark.asyncio
    async def test_install_server_requires_confirmation(self, setup_mcp_server):
        """Test install_server requires confirmation by default."""
        from mcp_orchestrator.installation.models import InstallationStatus

        with patch(
            "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
        ) as mock_check:
            mock_result = Mock()
            mock_result.status = InstallationStatus.NOT_INSTALLED
            mock_check.return_value = mock_result

            result = await server.install_server.fn(server_id="filesystem")

            assert result["status"] == "confirmation_required"
            assert "installation_command" in result

    @pytest.mark.asyncio
    async def test_install_server_invalid_id_raises_error(self, setup_mcp_server):
        """Test install_server raises error for invalid server ID."""
        with pytest.raises(ValueError):
            await server.install_server.fn(server_id="nonexistent")


class TestListInstalledServers:
    """Tests for list_installed_servers tool."""

    @pytest.mark.asyncio
    async def test_list_installed_servers_returns_all_servers(self, setup_mcp_server):
        """Test list_installed_servers returns all servers with status."""
        from mcp_orchestrator.installation.models import InstallationStatus

        with patch(
            "mcp_orchestrator.installation.validator.InstallationValidator.check_installation"
        ) as mock_check:
            # Mock some servers as installed, some not
            def check_side_effect(srv):
                mock_result = Mock()
                if srv.server_id == "filesystem":
                    mock_result.status = InstallationStatus.INSTALLED
                    mock_result.installed_version = "1.0.0"
                else:
                    mock_result.status = InstallationStatus.NOT_INSTALLED
                    mock_result.installed_version = None
                return mock_result

            mock_check.side_effect = check_side_effect

            result = await server.list_installed_servers.fn()

            assert "servers" in result
            assert "installed_count" in result
            assert "not_installed_count" in result
            assert "total_count" in result


# =============================================================================
# RESOURCES
# =============================================================================


class TestServerCapabilitiesResource:
    """Tests for server_capabilities resource."""

    @pytest.mark.asyncio
    async def test_server_capabilities_returns_json(self, setup_mcp_server):
        """Test server_capabilities returns valid JSON."""
        result = await server.server_capabilities.fn()

        # Should be JSON string
        assert isinstance(result, str)

        # Parse and validate
        capabilities = json.loads(result)
        assert "name" in capabilities
        assert capabilities["name"] == "mcp-orchestration"
        assert "version" in capabilities
        assert "capabilities" in capabilities
        assert "tools" in capabilities["capabilities"]
        assert "resources" in capabilities["capabilities"]
        assert "features" in capabilities

    @pytest.mark.asyncio
    async def test_server_capabilities_includes_all_tools(self, setup_mcp_server):
        """Test server_capabilities includes all 14+ tools."""
        result = await server.server_capabilities.fn()
        capabilities = json.loads(result)

        tools = capabilities["capabilities"]["tools"]

        # Wave 1.0 tools
        assert "list_clients" in tools
        assert "list_profiles" in tools
        assert "get_config" in tools
        assert "diff_config" in tools

        # Wave 1.1 tools
        assert "list_available_servers" in tools
        assert "describe_server" in tools

        # Wave 1.2 tools
        assert "add_server_to_config" in tools
        assert "remove_server_from_config" in tools
        assert "publish_config" in tools


class TestClientCapabilitiesResource:
    """Tests for client_capabilities resource."""

    @pytest.mark.asyncio
    async def test_client_capabilities_returns_json(self, setup_mcp_server):
        """Test client_capabilities returns valid JSON."""
        result = await server.client_capabilities.fn()

        assert isinstance(result, str)

        # Parse and validate
        capabilities = json.loads(result)
        assert "clients" in capabilities
        assert isinstance(capabilities["clients"], list)


class TestServerRegistryResource:
    """Tests for server_registry_resource."""

    @pytest.mark.asyncio
    async def test_server_registry_resource_returns_json(self, setup_mcp_server):
        """Test server_registry_resource returns valid JSON."""
        result = await server.server_registry_resource.fn()

        assert isinstance(result, str)

        registry_data = json.loads(result)
        assert "servers" in registry_data
        assert "count" in registry_data
        assert "transport_counts" in registry_data


class TestServerDefinitionResource:
    """Tests for server_definition_resource."""

    @pytest.mark.asyncio
    async def test_server_definition_resource_returns_json(self, setup_mcp_server):
        """Test server_definition_resource returns valid JSON."""
        result = await server.server_definition_resource.fn(server_id="filesystem")

        assert isinstance(result, str)

        definition = json.loads(result)
        assert "server_id" in definition
        assert definition["server_id"] == "filesystem"

    @pytest.mark.asyncio
    async def test_server_definition_invalid_id_raises_error(self, setup_mcp_server):
        """Test server_definition_resource raises error for invalid ID."""
        with pytest.raises(ValueError):
            await server.server_definition_resource.fn(server_id="nonexistent")


class TestDraftConfigResource:
    """Tests for draft_config_resource."""

    @pytest.mark.asyncio
    async def test_draft_config_resource_empty(self, setup_mcp_server):
        """Test draft_config_resource returns empty draft."""
        result = await server.draft_config_resource.fn(
            client_id="claude-desktop", profile_id="default"
        )

        assert isinstance(result, str)

        draft_info = json.loads(result)
        assert draft_info["client_id"] == "claude-desktop"
        assert draft_info["profile_id"] == "default"
        assert draft_info["server_count"] == 0

    @pytest.mark.asyncio
    async def test_draft_config_resource_with_servers(self, setup_mcp_server):
        """Test draft_config_resource returns populated draft."""
        # Add servers
        await server.add_server_to_config.fn(
            server_id="filesystem", params={"path": "/tmp"}
        )

        result = await server.draft_config_resource.fn(
            client_id="claude-desktop", profile_id="default"
        )

        draft_info = json.loads(result)
        assert draft_info["server_count"] == 1
        assert "filesystem" in draft_info["servers"]


class TestLatestConfigResource:
    """Tests for latest_config_resource."""

    @pytest.mark.asyncio
    async def test_latest_config_resource_no_artifact_raises_error(
        self, setup_mcp_server
    ):
        """Test latest_config_resource raises error when no artifact exists."""
        with pytest.raises(ValueError, match="No published artifact found"):
            await server.latest_config_resource.fn(
                client_id="claude-desktop", profile_id="default"
            )

    @pytest.mark.asyncio
    async def test_latest_config_resource_returns_published_artifact(
        self, setup_mcp_server
    ):
        """Test latest_config_resource returns latest published artifact."""
        setup = setup_mcp_server

        # Publish a config
        builder = ConfigBuilder("claude-desktop", "default", setup["server_registry"])
        builder.add_server("filesystem", params={"path": "/tmp"})

        workflow = PublishingWorkflow(
            store=setup["store"], client_registry=setup["registry"]
        )
        publish_result = workflow.publish(
            builder=builder,
            private_key_path=str(setup["private_key_path"]),
            signing_key_id="test",
        )

        # Get latest via resource
        result = await server.latest_config_resource.fn(
            client_id="claude-desktop", profile_id="default"
        )

        assert isinstance(result, str)

        artifact_info = json.loads(result)
        assert artifact_info["artifact_id"] == publish_result["artifact_id"]
        assert artifact_info["client_id"] == "claude-desktop"
        assert artifact_info["profile_id"] == "default"


class TestDeployedConfigResource:
    """Tests for deployed_config_resource."""

    @pytest.mark.asyncio
    async def test_deployed_config_resource_no_deployment_raises_error(
        self, setup_mcp_server
    ):
        """Test deployed_config_resource raises error when no deployment exists."""
        with pytest.raises(ValueError, match="No deployment found"):
            await server.deployed_config_resource.fn(
                client_id="claude-desktop", profile_id="default"
            )


# =============================================================================
# HELPER FUNCTIONS TESTS
# =============================================================================


class TestHelperFunctions:
    """Tests for helper functions in server.py."""

    def test_get_transport_value_with_enum(self, setup_mcp_server):
        """Test _get_transport_value handles TransportType enum."""
        transport_value = server._get_transport_value(TransportType.STDIO)
        assert transport_value == "stdio"

    def test_get_transport_value_with_string(self, setup_mcp_server):
        """Test _get_transport_value handles string value."""
        transport_value = server._get_transport_value("stdio")
        assert transport_value == "stdio"

    def test_get_builder_creates_new(self, setup_mcp_server):
        """Test _get_builder creates new builder if doesn't exist."""
        builder = server._get_builder("claude-desktop", "test-profile")

        assert builder is not None
        assert "claude-desktop/test-profile" in server._builders

    def test_get_builder_returns_existing(self, setup_mcp_server):
        """Test _get_builder returns existing builder."""
        builder1 = server._get_builder("claude-desktop", "default")
        builder2 = server._get_builder("claude-desktop", "default")

        assert builder1 is builder2

    def test_generate_usage_example_stdio(self, setup_mcp_server):
        """Test _generate_usage_example for stdio server."""
        srv = setup_mcp_server["server_registry"].get("filesystem")
        example = server._generate_usage_example(srv)

        # Should be valid JSON
        parsed = json.loads(example)
        assert "mcpServers" in parsed
        assert "filesystem" in parsed["mcpServers"]
        assert "command" in parsed["mcpServers"]["filesystem"]

    def test_generate_usage_example_http(self, setup_mcp_server):
        """Test _generate_usage_example for HTTP/SSE server."""
        srv = setup_mcp_server["server_registry"].get("n8n")
        example = server._generate_usage_example(srv)

        # Should include mcp-remote wrapper
        parsed = json.loads(example)
        assert "mcpServers" in parsed
        assert "n8n" in parsed["mcpServers"]
        config = parsed["mcpServers"]["n8n"]
        assert "mcp-remote" in str(config["args"]) or config["command"] == "npx"


# =============================================================================
# INTEGRATION TESTS
# =============================================================================


class TestMCPServerIntegration:
    """Integration tests for complete MCP server workflows."""

    @pytest.mark.asyncio
    async def test_complete_workflow_browse_add_validate_publish(
        self, setup_mcp_server
    ):
        """Test complete workflow from browsing to publishing."""

        # Step 1: Browse available servers
        servers = await server.list_available_servers.fn()
        assert servers["count"] > 0

        # Step 2: Describe a server
        description = await server.describe_server.fn(server_id="filesystem")
        assert description["server_id"] == "filesystem"

        # Step 3: Add server to draft
        add_result = await server.add_server_to_config.fn(
            server_id="filesystem", params={"path": "/tmp"}
        )
        assert add_result["status"] == "added"

        # Step 4: View draft
        draft = await server.view_draft_config.fn()
        assert draft["server_count"] == 1

        # Step 5: Validate
        validation = await server.validate_config.fn()
        assert validation["valid"] is True

        # Step 6: Publish
        publish_result = await server.publish_config.fn(changelog="Test config")
        assert publish_result["status"] == "published"

    @pytest.mark.asyncio
    async def test_draft_isolation_between_profiles(self, setup_mcp_server):
        """Test that different profiles maintain isolated drafts."""
        # Add server to default profile
        await server.add_server_to_config.fn(
            server_id="filesystem", params={"path": "/tmp"}, profile_id="default"
        )

        # Add different server to dev profile
        await server.add_server_to_config.fn(
            server_id="github", env_vars={"GITHUB_TOKEN": "test"}, profile_id="dev"
        )

        # Verify isolation
        default_draft = await server.view_draft_config.fn(profile_id="default")
        dev_draft = await server.view_draft_config.fn(profile_id="dev")

        assert default_draft["servers"] == ["filesystem"]
        assert dev_draft["servers"] == ["github"]

    @pytest.mark.asyncio
    async def test_error_handling_consistency(self, setup_mcp_server):
        """Test that all tools handle errors consistently."""
        # Invalid client ID
        with pytest.raises(ValueError):
            await server.list_profiles.fn(client_id="nonexistent")

        with pytest.raises(ValueError):
            await server.get_config.fn(client_id="nonexistent", profile_id="default")

        # Invalid server ID
        with pytest.raises(ValueError):
            await server.describe_server.fn(server_id="nonexistent")

        with pytest.raises(ValueError):
            await server.add_server_to_config.fn(server_id="nonexistent")
