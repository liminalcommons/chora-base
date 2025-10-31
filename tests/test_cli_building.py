"""Tests for CLI building commands (Wave 1.2, 1.4, 1.5).

This module tests the Click CLI commands for:
- add_server: Add server to draft config
- remove_server: Remove server from draft config
- publish_config: Publish and sign configuration
- deploy_config: Deploy configuration to client location

Testing patterns:
- Use CliRunner for command invocation
- Test both JSON and text output formats
- Test success and error paths
- Mock file system operations where needed
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner
from mcp_orchestrator.cli_building import (
    add_server,
    deploy_config,
    publish_config,
    remove_server,
)
from mcp_orchestrator.crypto import ArtifactSigner
from mcp_orchestrator.deployment import DeploymentError, DeploymentResult
from mcp_orchestrator.publishing import ValidationError
from mcp_orchestrator.servers.models import (
    ParameterDefinition,
    ServerDefinition,
    TransportType,
)
from mcp_orchestrator.servers.registry import ServerRegistry


@pytest.fixture
def cli_runner():
    """Create Click test runner."""
    return CliRunner()


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
            stdio_args=["-y", "@modelcontextprotocol/server-filesystem", "{path}"],
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
            stdio_args=["-y", "@modelcontextprotocol/server-github"],
            required_env=["GITHUB_TOKEN"],
        ),
    ]
    return ServerRegistry(servers)


@pytest.fixture
def temp_keys():
    """Create temporary key directory with test keys."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create .mcp-orchestration/keys structure like the real home dir
        home_dir = Path(tmpdir)
        mcp_dir = home_dir / ".mcp-orchestration"
        key_dir = mcp_dir / "keys"
        key_dir.mkdir(parents=True)

        private_key_path = key_dir / "signing.key"
        public_key_path = key_dir / "signing.pub"

        # Generate test keys
        signer = ArtifactSigner.generate(key_id="default")
        signer.save_private_key(str(private_key_path))
        signer.save_public_key(str(public_key_path))

        yield {
            "home_dir": home_dir,
            "mcp_dir": mcp_dir,
            "key_dir": key_dir,
            "private_key_path": private_key_path,
            "public_key_path": public_key_path,
        }


@pytest.fixture
def sample_config_file(tmp_path):
    """Create a sample config file for testing."""
    config = {
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
                "env": {},
            }
        }
    }

    config_file = tmp_path / "test-config.json"
    config_file.write_text(json.dumps(config, indent=2))

    return config_file


class TestAddServerCommand:
    """Tests for add_server CLI command."""

    def test_add_server_success_text_output(self, cli_runner, sample_registry):
        """Test add_server with text output format."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            result = cli_runner.invoke(
                add_server,
                [
                    "filesystem",
                    "--client",
                    "claude-desktop",
                    "--profile",
                    "default",
                    "--param",
                    "path=/Users/me/Documents",
                    "--format",
                    "text",
                ],
            )

        assert result.exit_code == 0
        assert "Added server 'filesystem' to draft config" in result.output
        assert "Client: claude-desktop" in result.output
        assert "Profile: default" in result.output
        assert "Servers in draft: 1" in result.output
        assert "Draft configuration:" in result.output

    def test_add_server_success_json_output(self, cli_runner, sample_registry):
        """Test add_server with JSON output format."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            result = cli_runner.invoke(
                add_server,
                [
                    "filesystem",
                    "--client",
                    "claude-desktop",
                    "--profile",
                    "default",
                    "--param",
                    "path=/tmp",
                    "--format",
                    "json",
                ],
            )

        assert result.exit_code == 0

        output = json.loads(result.output)
        assert output["status"] == "added"
        assert output["server_name"] == "filesystem"
        assert output["client_id"] == "claude-desktop"
        assert output["profile_id"] == "default"
        assert output["server_count"] == 1
        assert "draft" in output
        assert "mcpServers" in output["draft"]

    def test_add_server_with_custom_name(self, cli_runner, sample_registry):
        """Test add_server with custom server name."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            result = cli_runner.invoke(
                add_server,
                [
                    "filesystem",
                    "--client",
                    "claude-desktop",
                    "--profile",
                    "dev",
                    "--param",
                    "path=/tmp",
                    "--name",
                    "filesystem-tmp",
                    "--format",
                    "json",
                ],
            )

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["server_name"] == "filesystem-tmp"

    def test_add_server_with_multiple_params(self, cli_runner, sample_registry):
        """Test add_server with multiple parameters."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            result = cli_runner.invoke(
                add_server,
                [
                    "filesystem",
                    "--client",
                    "claude-desktop",
                    "--profile",
                    "default",
                    "--param",
                    "path=/tmp",
                    "--param",
                    "readonly=true",
                    "--format",
                    "json",
                ],
            )

        assert result.exit_code == 0

    def test_add_server_with_env_vars(self, cli_runner, sample_registry):
        """Test add_server with environment variables."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            result = cli_runner.invoke(
                add_server,
                [
                    "github",
                    "--client",
                    "claude-desktop",
                    "--profile",
                    "default",
                    "--env",
                    "GITHUB_TOKEN=ghp_test123",
                    "--format",
                    "json",
                ],
            )

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["server_name"] == "github"

    def test_add_server_with_multiple_env_vars(self, cli_runner, sample_registry):
        """Test add_server with multiple environment variables."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            result = cli_runner.invoke(
                add_server,
                [
                    "github",
                    "--client",
                    "claude-desktop",
                    "--profile",
                    "default",
                    "--env",
                    "GITHUB_TOKEN=ghp_test123",
                    "--env",
                    "GITHUB_ORG=myorg",
                    "--format",
                    "json",
                ],
            )

        assert result.exit_code == 0

    def test_add_server_invalid_param_format(self, cli_runner, sample_registry):
        """Test add_server with invalid parameter format (missing =)."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            result = cli_runner.invoke(
                add_server,
                [
                    "filesystem",
                    "--client",
                    "claude-desktop",
                    "--profile",
                    "default",
                    "--param",
                    "invalid-param-format",
                ],
            )

        assert result.exit_code == 1
        assert "Invalid parameter format 'invalid-param-format'" in result.output
        assert "Use key=value" in result.output

    def test_add_server_invalid_env_format(self, cli_runner, sample_registry):
        """Test add_server with invalid env format (missing =)."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            result = cli_runner.invoke(
                add_server,
                [
                    "github",
                    "--client",
                    "claude-desktop",
                    "--profile",
                    "default",
                    "--env",
                    "INVALID_ENV_FORMAT",
                ],
            )

        assert result.exit_code == 1
        assert "Invalid env format 'INVALID_ENV_FORMAT'" in result.output
        assert "Use KEY=VALUE" in result.output

    def test_add_server_exception_handling(self, cli_runner, sample_registry):
        """Test add_server handles exceptions gracefully."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            with patch("mcp_orchestrator.cli_building.ConfigBuilder") as mock_builder:
                mock_builder.side_effect = Exception("Test error")

                result = cli_runner.invoke(
                    add_server,
                    [
                        "filesystem",
                        "--client",
                        "claude-desktop",
                        "--profile",
                        "default",
                        "--param",
                        "path=/tmp",
                    ],
                )

        assert result.exit_code == 1
        assert "Error: Test error" in result.output

    def test_add_server_missing_required_option(self, cli_runner):
        """Test add_server with missing required --client option."""
        result = cli_runner.invoke(add_server, ["filesystem", "--profile", "default"])

        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()


class TestRemoveServerCommand:
    """Tests for remove_server CLI command."""

    def test_remove_server_shows_limitation_warning(self, cli_runner, sample_registry):
        """Test remove_server shows CLI limitation warning."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            result = cli_runner.invoke(
                remove_server,
                ["filesystem", "--client", "claude-desktop", "--profile", "default"],
            )

        # Command will fail because draft is empty, but should show warnings first
        assert "CLI drafts are not persisted" in result.output
        assert "Use MCP tools for stateful drafts" in result.output

    def test_remove_server_text_output(self, cli_runner, sample_registry):
        """Test remove_server with text output format."""
        # Mock builder to have a server to remove
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            with patch(
                "mcp_orchestrator.cli_building.ConfigBuilder"
            ) as mock_builder_class:
                mock_builder = Mock()
                mock_builder.count.return_value = 0
                mock_builder.build.return_value = {"mcpServers": {}}
                mock_builder_class.return_value = mock_builder

                result = cli_runner.invoke(
                    remove_server,
                    [
                        "filesystem",
                        "--client",
                        "claude-desktop",
                        "--profile",
                        "default",
                        "--format",
                        "text",
                    ],
                )

        # Should show limitation warnings
        assert "CLI drafts are not persisted" in result.output

    def test_remove_server_json_output(self, cli_runner, sample_registry):
        """Test remove_server with JSON output format."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            with patch(
                "mcp_orchestrator.cli_building.ConfigBuilder"
            ) as mock_builder_class:
                mock_builder = Mock()
                mock_builder.count.return_value = 0
                mock_builder.build.return_value = {"mcpServers": {}}
                mock_builder_class.return_value = mock_builder

                result = cli_runner.invoke(
                    remove_server,
                    [
                        "filesystem",
                        "--client",
                        "claude-desktop",
                        "--profile",
                        "default",
                        "--format",
                        "json",
                    ],
                )

        # Check for warning in stderr
        assert "CLI drafts are not persisted" in result.output

    def test_remove_server_exception_handling(self, cli_runner, sample_registry):
        """Test remove_server handles exceptions gracefully."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            with patch(
                "mcp_orchestrator.cli_building.ConfigBuilder"
            ) as mock_builder_class:
                mock_builder = Mock()
                mock_builder.remove_server.side_effect = Exception("Server not found")
                mock_builder_class.return_value = mock_builder

                result = cli_runner.invoke(
                    remove_server,
                    [
                        "filesystem",
                        "--client",
                        "claude-desktop",
                        "--profile",
                        "default",
                    ],
                )

        assert result.exit_code == 1
        assert "Error: Server not found" in result.output

    def test_remove_server_missing_required_options(self, cli_runner):
        """Test remove_server with missing required options."""
        result = cli_runner.invoke(remove_server, ["filesystem"])

        assert result.exit_code != 0


class TestPublishConfigCommand:
    """Tests for publish_config CLI command."""

    def test_publish_config_success_text_output(
        self, cli_runner, sample_config_file, temp_keys, sample_registry
    ):
        """Test publish_config with text output format."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            with patch("mcp_orchestrator.cli_building.get_client_registry"):
                with patch(
                    "mcp_orchestrator.cli_building.Path.home",
                    return_value=temp_keys["home_dir"],
                ):
                    with patch(
                        "mcp_orchestrator.cli_building.PublishingWorkflow"
                    ) as mock_workflow_class:
                        mock_workflow = Mock()
                        mock_workflow.publish.return_value = {
                            "artifact_id": "abc123def456" * 4,
                            "client_id": "claude-desktop",
                            "profile_id": "default",
                            "server_count": 1,
                        }
                        mock_workflow_class.return_value = mock_workflow

                        result = cli_runner.invoke(
                            publish_config,
                            [
                                "--client",
                                "claude-desktop",
                                "--profile",
                                "default",
                                "--file",
                                str(sample_config_file),
                                "--changelog",
                                "Test publish",
                                "--format",
                                "text",
                            ],
                        )

        assert result.exit_code == 0
        assert "Configuration validated successfully" in result.output
        assert "Configuration signed with Ed25519" in result.output
        assert "Artifact stored:" in result.output
        assert "Published successfully!" in result.output
        assert "Artifact ID:" in result.output
        assert "Server count: 1" in result.output
        assert "Changelog: Test publish" in result.output

    def test_publish_config_success_json_output(
        self, cli_runner, sample_config_file, temp_keys, sample_registry
    ):
        """Test publish_config with JSON output format."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            with patch("mcp_orchestrator.cli_building.get_client_registry"):
                with patch(
                    "mcp_orchestrator.cli_building.Path.home",
                    return_value=temp_keys["home_dir"],
                ):
                    with patch(
                        "mcp_orchestrator.cli_building.PublishingWorkflow"
                    ) as mock_workflow_class:
                        mock_workflow = Mock()
                        result_data = {
                            "artifact_id": "abc123",
                            "client_id": "claude-desktop",
                            "profile_id": "default",
                            "server_count": 1,
                        }
                        mock_workflow.publish.return_value = result_data
                        mock_workflow_class.return_value = mock_workflow

                        result = cli_runner.invoke(
                            publish_config,
                            [
                                "--client",
                                "claude-desktop",
                                "--profile",
                                "default",
                                "--file",
                                str(sample_config_file),
                                "--format",
                                "json",
                            ],
                        )

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["artifact_id"] == "abc123"
        assert output["client_id"] == "claude-desktop"
        assert output["server_count"] == 1

    def test_publish_config_missing_mcpServers_key(
        self, cli_runner, tmp_path, temp_keys
    ):
        """Test publish_config with config missing 'mcpServers' key."""
        bad_config = tmp_path / "bad-config.json"
        bad_config.write_text(json.dumps({"servers": {}}))

        with patch(
            "mcp_orchestrator.cli_building.Path.home",
            return_value=temp_keys["home_dir"],
        ):
            result = cli_runner.invoke(
                publish_config,
                [
                    "--client",
                    "claude-desktop",
                    "--profile",
                    "default",
                    "--file",
                    str(bad_config),
                ],
            )

        assert result.exit_code == 1
        assert "Configuration file missing 'mcpServers' key" in result.output

    def test_publish_config_empty_servers(self, cli_runner, tmp_path, temp_keys):
        """Test publish_config with empty servers list."""
        empty_config = tmp_path / "empty-config.json"
        empty_config.write_text(json.dumps({"mcpServers": {}}))

        with patch(
            "mcp_orchestrator.cli_building.Path.home",
            return_value=temp_keys["home_dir"],
        ):
            result = cli_runner.invoke(
                publish_config,
                [
                    "--client",
                    "claude-desktop",
                    "--profile",
                    "default",
                    "--file",
                    str(empty_config),
                ],
            )

        assert result.exit_code == 1
        assert "Configuration has no servers" in result.output

    def test_publish_config_missing_signing_key(
        self, cli_runner, sample_config_file, tmp_path
    ):
        """Test publish_config when signing key doesn't exist."""
        fake_home = tmp_path / "fake-home"
        fake_home.mkdir()

        with patch("mcp_orchestrator.cli_building.Path.home", return_value=fake_home):
            result = cli_runner.invoke(
                publish_config,
                [
                    "--client",
                    "claude-desktop",
                    "--profile",
                    "default",
                    "--file",
                    str(sample_config_file),
                ],
            )

        assert result.exit_code == 1
        assert "Signing key not found" in result.output
        assert "mcp-orchestration-init-keys" in result.output

    def test_publish_config_validation_error(
        self, cli_runner, sample_config_file, temp_keys, sample_registry
    ):
        """Test publish_config with validation errors."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            with patch("mcp_orchestrator.cli_building.get_client_registry"):
                with patch(
                    "mcp_orchestrator.cli_building.Path.home",
                    return_value=temp_keys["home_dir"],
                ):
                    with patch(
                        "mcp_orchestrator.cli_building.PublishingWorkflow"
                    ) as mock_workflow_class:
                        mock_workflow = Mock()

                        # Create ValidationError with validation_result
                        validation_result = {
                            "errors": [
                                {
                                    "code": "INVALID_COMMAND",
                                    "message": "Command not found",
                                },
                                {
                                    "code": "MISSING_ENV",
                                    "message": "Required env var missing",
                                },
                            ]
                        }
                        error = ValidationError(validation_result)
                        mock_workflow.publish.side_effect = error
                        mock_workflow_class.return_value = mock_workflow

                        result = cli_runner.invoke(
                            publish_config,
                            [
                                "--client",
                                "claude-desktop",
                                "--profile",
                                "default",
                                "--file",
                                str(sample_config_file),
                            ],
                        )

        assert result.exit_code == 1
        assert "Configuration validation failed" in result.output
        assert "[INVALID_COMMAND] Command not found" in result.output
        assert "[MISSING_ENV] Required env var missing" in result.output

    def test_publish_config_file_not_found(self, cli_runner, temp_keys):
        """Test publish_config with non-existent config file."""
        result = cli_runner.invoke(
            publish_config,
            [
                "--client",
                "claude-desktop",
                "--profile",
                "default",
                "--file",
                "/nonexistent/config.json",
            ],
        )

        # Click validates file existence, so this should fail during argument parsing
        assert result.exit_code != 0

    def test_publish_config_invalid_json(self, cli_runner, tmp_path, temp_keys):
        """Test publish_config with invalid JSON file."""
        bad_json = tmp_path / "bad.json"
        bad_json.write_text("{ invalid json }")

        with patch(
            "mcp_orchestrator.cli_building.Path.home",
            return_value=temp_keys["home_dir"],
        ):
            result = cli_runner.invoke(
                publish_config,
                [
                    "--client",
                    "claude-desktop",
                    "--profile",
                    "default",
                    "--file",
                    str(bad_json),
                ],
            )

        assert result.exit_code == 1
        assert "Invalid JSON in configuration file" in result.output

    def test_publish_config_general_exception(
        self, cli_runner, sample_config_file, temp_keys, sample_registry
    ):
        """Test publish_config handles general exceptions."""
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            with patch("mcp_orchestrator.cli_building.get_client_registry"):
                with patch(
                    "mcp_orchestrator.cli_building.Path.home",
                    return_value=temp_keys["home_dir"],
                ):
                    with patch(
                        "mcp_orchestrator.cli_building.PublishingWorkflow"
                    ) as mock_workflow_class:
                        mock_workflow_class.side_effect = Exception("Unexpected error")

                        result = cli_runner.invoke(
                            publish_config,
                            [
                                "--client",
                                "claude-desktop",
                                "--profile",
                                "default",
                                "--file",
                                str(sample_config_file),
                            ],
                        )

        assert result.exit_code == 1
        assert "Error: Unexpected error" in result.output


class TestDeployConfigCommand:
    """Tests for deploy_config CLI command."""

    def test_deploy_config_success_text_output(self, cli_runner, temp_keys):
        """Test deploy_config with text output format."""
        with patch("mcp_orchestrator.cli_building.get_client_registry"):
            with patch(
                "mcp_orchestrator.cli_building.Path.home",
                return_value=temp_keys["home_dir"],
            ):
                with patch(
                    "mcp_orchestrator.cli_building.DeploymentWorkflow"
                ) as mock_workflow_class:
                    mock_workflow = Mock()

                    result_obj = DeploymentResult(
                        status="deployed",
                        artifact_id="abc123def456",
                        config_path="/path/to/config.json",
                        deployed_at="2025-10-31T12:00:00Z",
                    )
                    mock_workflow.deploy.return_value = result_obj
                    mock_workflow_class.return_value = mock_workflow

                    result = cli_runner.invoke(
                        deploy_config,
                        [
                            "--client",
                            "claude-desktop",
                            "--profile",
                            "default",
                            "--format",
                            "text",
                        ],
                    )

        assert result.exit_code == 0
        assert "Configuration deployed successfully!" in result.output
        assert "Artifact ID: abc123def456" in result.output
        assert "Config path: /path/to/config.json" in result.output
        assert "Deployed at: 2025-10-31T12:00:00Z" in result.output
        assert "Restart the client application" in result.output
        assert "killall Claude" in result.output

    def test_deploy_config_success_json_output(self, cli_runner, temp_keys):
        """Test deploy_config with JSON output format."""
        with patch("mcp_orchestrator.cli_building.get_client_registry"):
            with patch(
                "mcp_orchestrator.cli_building.Path.home",
                return_value=temp_keys["home_dir"],
            ):
                with patch(
                    "mcp_orchestrator.cli_building.DeploymentWorkflow"
                ) as mock_workflow_class:
                    mock_workflow = Mock()

                    result_obj = DeploymentResult(
                        status="deployed",
                        artifact_id="abc123",
                        config_path="/path/to/config.json",
                        deployed_at="2025-10-31T12:00:00Z",
                    )
                    mock_workflow.deploy.return_value = result_obj
                    mock_workflow_class.return_value = mock_workflow

                    result = cli_runner.invoke(
                        deploy_config,
                        [
                            "--client",
                            "claude-desktop",
                            "--profile",
                            "default",
                            "--format",
                            "json",
                        ],
                    )

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["artifact_id"] == "abc123"
        assert output["config_path"] == "/path/to/config.json"
        assert output["status"] == "deployed"

    def test_deploy_config_with_artifact_id(self, cli_runner, temp_keys):
        """Test deploy_config with specific artifact ID (rollback scenario)."""
        with patch("mcp_orchestrator.cli_building.get_client_registry"):
            with patch(
                "mcp_orchestrator.cli_building.Path.home",
                return_value=temp_keys["home_dir"],
            ):
                with patch(
                    "mcp_orchestrator.cli_building.DeploymentWorkflow"
                ) as mock_workflow_class:
                    mock_workflow = Mock()

                    result_obj = DeploymentResult(
                        status="deployed",
                        artifact_id="old123",
                        config_path="/path/to/config.json",
                        deployed_at="2025-10-31T12:00:00Z",
                    )
                    mock_workflow.deploy.return_value = result_obj
                    mock_workflow_class.return_value = mock_workflow

                    result = cli_runner.invoke(
                        deploy_config,
                        [
                            "--client",
                            "claude-desktop",
                            "--profile",
                            "default",
                            "--artifact-id",
                            "old123",
                        ],
                    )

        assert result.exit_code == 0
        mock_workflow.deploy.assert_called_once_with(
            client_id="claude-desktop", profile_id="default", artifact_id="old123"
        )

    def test_deploy_config_cursor_restart_instructions(self, cli_runner, temp_keys):
        """Test deploy_config shows Cursor-specific restart instructions."""
        with patch("mcp_orchestrator.cli_building.get_client_registry"):
            with patch(
                "mcp_orchestrator.cli_building.Path.home",
                return_value=temp_keys["home_dir"],
            ):
                with patch(
                    "mcp_orchestrator.cli_building.DeploymentWorkflow"
                ) as mock_workflow_class:
                    mock_workflow = Mock()

                    result_obj = DeploymentResult(
                        status="deployed",
                        artifact_id="abc123",
                        config_path="/path/to/config.json",
                        deployed_at="2025-10-31T12:00:00Z",
                    )
                    mock_workflow.deploy.return_value = result_obj
                    mock_workflow_class.return_value = mock_workflow

                    result = cli_runner.invoke(
                        deploy_config, ["--client", "cursor", "--profile", "default"]
                    )

        assert result.exit_code == 0
        assert "Reload window in Cursor" in result.output

    def test_deploy_config_missing_public_key(self, cli_runner, tmp_path):
        """Test deploy_config when public key doesn't exist."""
        fake_home = tmp_path / "fake-home"
        fake_home.mkdir()

        with patch("mcp_orchestrator.cli_building.get_client_registry"):
            with patch(
                "mcp_orchestrator.cli_building.Path.home", return_value=fake_home
            ):
                result = cli_runner.invoke(
                    deploy_config,
                    ["--client", "claude-desktop", "--profile", "default"],
                )

        assert result.exit_code == 1
        assert "Public key not found" in result.output
        assert "mcp-orchestration-init-keys" in result.output

    def test_deploy_config_client_not_found_error(self, cli_runner, temp_keys):
        """Test deploy_config with CLIENT_NOT_FOUND error."""
        with patch(
            "mcp_orchestrator.cli_building.get_client_registry"
        ) as mock_registry_func:
            with patch(
                "mcp_orchestrator.cli_building.Path.home",
                return_value=temp_keys["home_dir"],
            ):
                with patch(
                    "mcp_orchestrator.cli_building.DeploymentWorkflow"
                ) as mock_workflow_class:
                    mock_workflow = Mock()

                    # Create error with message attribute for CLI compatibility
                    error = DeploymentError(
                        "Client not found", {"code": "CLIENT_NOT_FOUND"}
                    )
                    error.message = "Client not found"  # Add message attribute
                    mock_workflow.deploy.side_effect = error
                    mock_workflow_class.return_value = mock_workflow

                    # Mock client registry for listing
                    mock_registry = Mock()
                    mock_client = Mock()
                    mock_client.client_id = "claude-desktop"
                    mock_registry.list_clients.return_value = [mock_client]
                    mock_registry_func.return_value = mock_registry

                    result = cli_runner.invoke(
                        deploy_config,
                        ["--client", "invalid-client", "--profile", "default"],
                    )

        assert result.exit_code == 1
        assert "Deployment failed: [CLIENT_NOT_FOUND]" in result.output
        assert "Client not found" in result.output

    def test_deploy_config_artifact_not_found_error(self, cli_runner, temp_keys):
        """Test deploy_config with ARTIFACT_NOT_FOUND error."""
        with patch("mcp_orchestrator.cli_building.get_client_registry"):
            with patch(
                "mcp_orchestrator.cli_building.Path.home",
                return_value=temp_keys["home_dir"],
            ):
                with patch(
                    "mcp_orchestrator.cli_building.DeploymentWorkflow"
                ) as mock_workflow_class:
                    mock_workflow = Mock()

                    error = DeploymentError(
                        "Artifact not found", {"code": "ARTIFACT_NOT_FOUND"}
                    )
                    error.message = "Artifact not found"  # Add message attribute
                    mock_workflow.deploy.side_effect = error
                    mock_workflow_class.return_value = mock_workflow

                    result = cli_runner.invoke(
                        deploy_config,
                        ["--client", "claude-desktop", "--profile", "default"],
                    )

        assert result.exit_code == 1
        assert "Deployment failed: [ARTIFACT_NOT_FOUND]" in result.output
        assert "No published artifact found" in result.output
        assert "mcp-orchestration-publish-config" in result.output

    def test_deploy_config_signature_invalid_error(self, cli_runner, temp_keys):
        """Test deploy_config with SIGNATURE_INVALID error."""
        with patch("mcp_orchestrator.cli_building.get_client_registry"):
            with patch(
                "mcp_orchestrator.cli_building.Path.home",
                return_value=temp_keys["home_dir"],
            ):
                with patch(
                    "mcp_orchestrator.cli_building.DeploymentWorkflow"
                ) as mock_workflow_class:
                    mock_workflow = Mock()

                    error = DeploymentError(
                        "Signature invalid", {"code": "SIGNATURE_INVALID"}
                    )
                    error.message = "Signature invalid"  # Add message attribute
                    mock_workflow.deploy.side_effect = error
                    mock_workflow_class.return_value = mock_workflow

                    result = cli_runner.invoke(
                        deploy_config,
                        ["--client", "claude-desktop", "--profile", "default"],
                    )

        assert result.exit_code == 1
        assert "Deployment failed: [SIGNATURE_INVALID]" in result.output
        assert "artifact's signature is invalid" in result.output
        assert "Corrupted storage" in result.output
        assert "Tampering" in result.output
        assert "Wrong public key" in result.output

    def test_deploy_config_write_failed_error(self, cli_runner, temp_keys):
        """Test deploy_config with WRITE_FAILED error."""
        with patch("mcp_orchestrator.cli_building.get_client_registry"):
            with patch(
                "mcp_orchestrator.cli_building.Path.home",
                return_value=temp_keys["home_dir"],
            ):
                with patch(
                    "mcp_orchestrator.cli_building.DeploymentWorkflow"
                ) as mock_workflow_class:
                    mock_workflow = Mock()

                    error = DeploymentError("Write failed", {"code": "WRITE_FAILED"})
                    error.message = "Write failed"  # Add message attribute
                    mock_workflow.deploy.side_effect = error
                    mock_workflow_class.return_value = mock_workflow

                    result = cli_runner.invoke(
                        deploy_config,
                        ["--client", "claude-desktop", "--profile", "default"],
                    )

        assert result.exit_code == 1
        assert "Deployment failed: [WRITE_FAILED]" in result.output
        assert "Failed to write config file" in result.output
        assert "File permissions" in result.output
        assert "Parent directory exists" in result.output
        assert "Disk space available" in result.output

    def test_deploy_config_unknown_deployment_error(self, cli_runner, temp_keys):
        """Test deploy_config with unknown DeploymentError code."""
        with patch("mcp_orchestrator.cli_building.get_client_registry"):
            with patch(
                "mcp_orchestrator.cli_building.Path.home",
                return_value=temp_keys["home_dir"],
            ):
                with patch(
                    "mcp_orchestrator.cli_building.DeploymentWorkflow"
                ) as mock_workflow_class:
                    mock_workflow = Mock()

                    error = DeploymentError("Unknown error", {"code": "UNKNOWN_ERROR"})
                    mock_workflow.deploy.side_effect = error
                    mock_workflow_class.return_value = mock_workflow

                    result = cli_runner.invoke(
                        deploy_config,
                        ["--client", "claude-desktop", "--profile", "default"],
                    )

        assert result.exit_code == 1
        assert "Deployment failed: [UNKNOWN_ERROR]" in result.output

    def test_deploy_config_general_exception(self, cli_runner, temp_keys):
        """Test deploy_config handles general exceptions."""
        with patch("mcp_orchestrator.cli_building.get_client_registry"):
            with patch(
                "mcp_orchestrator.cli_building.Path.home",
                return_value=temp_keys["home_dir"],
            ):
                with patch(
                    "mcp_orchestrator.cli_building.DeploymentWorkflow"
                ) as mock_workflow_class:
                    mock_workflow_class.side_effect = Exception(
                        "Unexpected deployment error"
                    )

                    result = cli_runner.invoke(
                        deploy_config,
                        ["--client", "claude-desktop", "--profile", "default"],
                    )

        assert result.exit_code == 1
        assert "Error: Unexpected deployment error" in result.output


class TestCLIIntegration:
    """Integration tests for CLI commands working together."""

    def test_add_server_then_publish_workflow(
        self, cli_runner, sample_registry, temp_keys, tmp_path
    ):
        """Test workflow: add server → save to file → publish config."""
        # Step 1: Add server to get draft config
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            result = cli_runner.invoke(
                add_server,
                [
                    "filesystem",
                    "--client",
                    "claude-desktop",
                    "--profile",
                    "default",
                    "--param",
                    "path=/tmp",
                    "--format",
                    "json",
                ],
            )

        assert result.exit_code == 0
        draft = json.loads(result.output)["draft"]

        # Step 2: Save draft to file
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(draft, indent=2))

        # Step 3: Publish the config
        with patch(
            "mcp_orchestrator.cli_building.get_default_registry",
            return_value=sample_registry,
        ):
            with patch("mcp_orchestrator.cli_building.get_client_registry"):
                with patch(
                    "mcp_orchestrator.cli_building.Path.home",
                    return_value=temp_keys["home_dir"],
                ):
                    with patch(
                        "mcp_orchestrator.cli_building.PublishingWorkflow"
                    ) as mock_workflow_class:
                        mock_workflow = Mock()
                        mock_workflow.publish.return_value = {
                            "artifact_id": "abc123",
                            "client_id": "claude-desktop",
                            "profile_id": "default",
                            "server_count": 1,
                        }
                        mock_workflow_class.return_value = mock_workflow

                        result = cli_runner.invoke(
                            publish_config,
                            [
                                "--client",
                                "claude-desktop",
                                "--profile",
                                "default",
                                "--file",
                                str(config_file),
                            ],
                        )

        assert result.exit_code == 0
        assert "Published successfully!" in result.output

    def test_command_help_output(self, cli_runner):
        """Test that all commands provide --help output."""
        commands = [add_server, remove_server, publish_config, deploy_config]

        for cmd in commands:
            result = cli_runner.invoke(cmd, ["--help"])
            assert result.exit_code == 0
            assert "Usage:" in result.output or "Options:" in result.output
