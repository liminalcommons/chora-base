"""Tests for validate_config tool (Wave 1.4).

This module tests the schema validation logic added in Wave 1.4 for
pre-publish configuration validation.
"""

from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.registry import (
    ClientCapabilities,
    ClientDefinition,
    ClientLimitations,
    ClientRegistry,
    ProfileDefinition,
)
from mcp_orchestrator.servers.models import (
    ParameterDefinition,
    ServerDefinition,
    TransportType,
)
from mcp_orchestrator.servers.registry import ServerRegistry


def validate_config_logic(builder, client_registry, client_id="claude-desktop"):
    """Simulate the validate_config tool logic for testing.

    This replicates the validation logic from the validate_config tool.
    """
    from datetime import datetime

    errors = []
    warnings = []

    # Validation 1: Check for empty config
    if builder.count() == 0:
        errors.append(
            {
                "code": "EMPTY_CONFIG",
                "message": "Configuration is empty. Add at least one server before publishing.",
                "severity": "error",
            }
        )

    # Validation 2: Check each server configuration
    payload = builder.build()
    if "mcpServers" in payload:
        servers = payload["mcpServers"]

        for server_name, server_config in servers.items():
            # Check required fields
            if "command" not in server_config:
                errors.append(
                    {
                        "code": "MISSING_COMMAND",
                        "message": f"Server '{server_name}' is missing required 'command' field.",
                        "severity": "error",
                        "server": server_name,
                    }
                )

            if "args" not in server_config:
                errors.append(
                    {
                        "code": "MISSING_ARGS",
                        "message": f"Server '{server_name}' is missing required 'args' field.",
                        "severity": "error",
                        "server": server_name,
                    }
                )

            # Check args is a list
            if "args" in server_config and not isinstance(server_config["args"], list):
                errors.append(
                    {
                        "code": "INVALID_ARGS_TYPE",
                        "message": f"Server '{server_name}' has invalid 'args' type (must be list).",
                        "severity": "error",
                        "server": server_name,
                    }
                )

            # Check env vars if present
            if "env" in server_config:
                env_vars = server_config["env"]
                if not isinstance(env_vars, dict):
                    errors.append(
                        {
                            "code": "INVALID_ENV_TYPE",
                            "message": f"Server '{server_name}' has invalid 'env' type (must be dict).",
                            "severity": "error",
                            "server": server_name,
                        }
                    )
                else:
                    # Check for empty env var values
                    for env_key, env_value in env_vars.items():
                        if not env_value or not str(env_value).strip():
                            warnings.append(
                                {
                                    "code": "EMPTY_ENV_VAR",
                                    "message": f"Server '{server_name}' has empty environment variable '{env_key}'.",
                                    "severity": "warning",
                                    "server": server_name,
                                }
                            )

    # Validation 3: Check client-specific limitations
    try:
        client_def = client_registry.get_client(client_id)

        # Check max servers
        max_servers = client_def.limitations.max_servers
        if max_servers and builder.count() > max_servers:
            errors.append(
                {
                    "code": "TOO_MANY_SERVERS",
                    "message": f"Configuration has {builder.count()} servers, but {client_id} supports max {max_servers}.",
                    "severity": "error",
                    "limit": max_servers,
                    "actual": builder.count(),
                }
            )

        # Check max env vars per server
        max_env_vars = client_def.limitations.max_env_vars_per_server
        if max_env_vars and "mcpServers" in payload:
            for server_name, server_config in payload["mcpServers"].items():
                if "env" in server_config:
                    env_count = len(server_config["env"])
                    if env_count > max_env_vars:
                        errors.append(
                            {
                                "code": "TOO_MANY_ENV_VARS",
                                "message": f"Server '{server_name}' has {env_count} env vars, but {client_id} supports max {max_env_vars}.",
                                "severity": "error",
                                "server": server_name,
                                "limit": max_env_vars,
                                "actual": env_count,
                            }
                        )

    except Exception:
        # Client not found - add warning but don't fail validation
        warnings.append(
            {
                "code": "UNKNOWN_CLIENT",
                "message": f"Client '{client_id}' not found in registry. Cannot validate client-specific limitations.",
                "severity": "warning",
            }
        )

    # Determine if valid
    valid = len(errors) == 0

    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "server_count": builder.count(),
        "validated_at": datetime.utcnow().isoformat() + "Z",
    }


class TestValidateConfigBasic:
    """Test basic validation scenarios."""

    def test_validate_empty_config(self):
        """Test validation fails for empty config."""
        # Create registries
        server_registry = ServerRegistry()
        client_registry = ClientRegistry()

        # Create empty builder
        builder = ConfigBuilder("claude-desktop", "default", server_registry)

        # Validate
        result = validate_config_logic(builder, client_registry)

        assert result["valid"] is False
        assert len(result["errors"]) == 1
        assert result["errors"][0]["code"] == "EMPTY_CONFIG"
        assert result["server_count"] == 0

    def test_validate_valid_config(self):
        """Test validation passes for valid config."""
        # Create server registry
        server_registry = ServerRegistry()
        server_registry.register(
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
            )
        )

        client_registry = ClientRegistry()

        # Create a valid config
        builder = ConfigBuilder("claude-desktop", "default", server_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})

        # Validate
        result = validate_config_logic(builder, client_registry)

        assert result["valid"] is True
        assert len(result["errors"]) == 0
        assert result["server_count"] == 1
        assert "validated_at" in result

    def test_validate_multiple_servers(self):
        """Test validation with multiple servers."""
        # Create server registry
        server_registry = ServerRegistry()
        server_registry.register(
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
            )
        )
        server_registry.register(
            ServerDefinition(
                server_id="github",
                display_name="GitHub",
                description="GitHub integration",
                transport=TransportType.STDIO,
                stdio_command="npx",
                stdio_args=["-y", "@mcp/server-github"],
                required_env=["GITHUB_TOKEN"],
            )
        )

        client_registry = ClientRegistry()

        # Create config with multiple servers
        builder = ConfigBuilder("claude-desktop", "default", server_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})
        builder.add_server("github", env_vars={"GITHUB_TOKEN": "ghp_test123"})

        # Validate
        result = validate_config_logic(builder, client_registry)

        assert result["valid"] is True
        assert len(result["errors"]) == 0
        assert result["server_count"] == 2


class TestValidateConfigStructure:
    """Test structural validation."""

    def test_missing_command_field(self):
        """Test validation catches missing command field."""
        server_registry = ServerRegistry()
        server_registry.register(
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
            )
        )

        client_registry = ClientRegistry()

        # Create builder and manually corrupt the config
        builder = ConfigBuilder("claude-desktop", "default", server_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})
        # Manually remove command field
        builder._servers["filesystem"].pop("command")

        # Validate
        result = validate_config_logic(builder, client_registry)

        assert result["valid"] is False
        assert any(e["code"] == "MISSING_COMMAND" for e in result["errors"])

    def test_missing_args_field(self):
        """Test validation catches missing args field."""
        server_registry = ServerRegistry()
        server_registry.register(
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
            )
        )

        client_registry = ClientRegistry()

        # Create builder and manually corrupt the config
        builder = ConfigBuilder("claude-desktop", "default", server_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})
        # Manually remove args field
        builder._servers["filesystem"].pop("args")

        # Validate
        result = validate_config_logic(builder, client_registry)

        assert result["valid"] is False
        assert any(e["code"] == "MISSING_ARGS" for e in result["errors"])

    def test_invalid_args_type(self):
        """Test validation catches invalid args type."""
        server_registry = ServerRegistry()
        server_registry.register(
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
            )
        )

        client_registry = ClientRegistry()

        # Create builder and manually corrupt the config
        builder = ConfigBuilder("claude-desktop", "default", server_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})
        # Set args to invalid type
        builder._servers["filesystem"]["args"] = "invalid-not-a-list"

        # Validate
        result = validate_config_logic(builder, client_registry)

        assert result["valid"] is False
        assert any(e["code"] == "INVALID_ARGS_TYPE" for e in result["errors"])

    def test_invalid_env_type(self):
        """Test validation catches invalid env type."""
        server_registry = ServerRegistry()
        server_registry.register(
            ServerDefinition(
                server_id="github",
                display_name="GitHub",
                description="GitHub integration",
                transport=TransportType.STDIO,
                stdio_command="npx",
                stdio_args=["-y", "@mcp/server-github"],
                required_env=["GITHUB_TOKEN"],
            )
        )

        client_registry = ClientRegistry()

        # Create builder and manually corrupt the config
        builder = ConfigBuilder("claude-desktop", "default", server_registry)
        builder.add_server("github", env_vars={"GITHUB_TOKEN": "test"})
        # Set env to invalid type
        builder._servers["github"]["env"] = ["invalid", "list"]

        # Validate
        result = validate_config_logic(builder, client_registry)

        assert result["valid"] is False
        assert any(e["code"] == "INVALID_ENV_TYPE" for e in result["errors"])


class TestValidateConfigWarnings:
    """Test warning scenarios."""

    def test_empty_env_var_warning(self):
        """Test warning for empty environment variable."""
        server_registry = ServerRegistry()
        server_registry.register(
            ServerDefinition(
                server_id="github",
                display_name="GitHub",
                description="GitHub integration",
                transport=TransportType.STDIO,
                stdio_command="npx",
                stdio_args=["-y", "@mcp/server-github"],
                required_env=["GITHUB_TOKEN"],
            )
        )

        client_registry = ClientRegistry()

        # Create builder with empty env var
        builder = ConfigBuilder("claude-desktop", "default", server_registry)
        builder.add_server("github", env_vars={"GITHUB_TOKEN": ""})

        # Validate
        result = validate_config_logic(builder, client_registry)

        # Should be valid (warnings don't fail validation)
        assert result["valid"] is True
        assert len(result["warnings"]) >= 1
        assert any(w["code"] == "EMPTY_ENV_VAR" for w in result["warnings"])

    def test_whitespace_only_env_var_warning(self):
        """Test warning for whitespace-only environment variable."""
        server_registry = ServerRegistry()
        server_registry.register(
            ServerDefinition(
                server_id="github",
                display_name="GitHub",
                description="GitHub integration",
                transport=TransportType.STDIO,
                stdio_command="npx",
                stdio_args=["-y", "@mcp/server-github"],
                required_env=["GITHUB_TOKEN"],
            )
        )

        client_registry = ClientRegistry()

        # Create builder with whitespace-only env var
        builder = ConfigBuilder("claude-desktop", "default", server_registry)
        builder.add_server("github", env_vars={"GITHUB_TOKEN": "   "})

        # Validate
        result = validate_config_logic(builder, client_registry)

        # Should be valid (warnings don't fail validation)
        assert result["valid"] is True
        assert any(w["code"] == "EMPTY_ENV_VAR" for w in result["warnings"])


class TestValidateConfigClientLimitations:
    """Test client-specific limitation validation."""

    def test_too_many_servers(self):
        """Test validation fails when exceeding max servers."""
        server_registry = ServerRegistry()
        server_registry.register(
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
            )
        )

        # Create client registry with limitation
        client_registry = ClientRegistry()
        client_registry.register(
            ClientDefinition(
                client_id="test-client",
                display_name="Test Client",
                platform="test",
                config_location="~/.test/config.json",
                config_format="mcp_v1",
                version_min="1.0.0",
                capabilities=ClientCapabilities(
                    environment_variables=True,
                    command_args=True,
                    working_directory=True,
                    multiple_servers=True,
                ),
                limitations=ClientLimitations(
                    max_servers=5,
                    max_env_vars_per_server=10,
                ),
                default_profiles=[
                    ProfileDefinition(
                        profile_id="default",
                        display_name="Default Profile",
                        description="Default test profile",
                    )
                ],
            )
        )

        # Create config with too many servers (limit is 5)
        builder = ConfigBuilder("test-client", "default", server_registry)
        for i in range(6):
            builder.add_server(
                "filesystem",
                params={"path": f"/tmp/{i}"},
                server_name=f"filesystem-{i}",
            )

        # Validate
        result = validate_config_logic(
            builder, client_registry, client_id="test-client"
        )

        assert result["valid"] is False
        assert any(e["code"] == "TOO_MANY_SERVERS" for e in result["errors"])
        error = next(e for e in result["errors"] if e["code"] == "TOO_MANY_SERVERS")
        assert error["limit"] == 5
        assert error["actual"] == 6

    def test_too_many_env_vars(self):
        """Test validation fails when exceeding max env vars per server."""
        server_registry = ServerRegistry()
        server_registry.register(
            ServerDefinition(
                server_id="github",
                display_name="GitHub",
                description="GitHub integration",
                transport=TransportType.STDIO,
                stdio_command="npx",
                stdio_args=["-y", "@mcp/server-github"],
                required_env=["GITHUB_TOKEN"],
            )
        )

        # Create client registry with limitation
        client_registry = ClientRegistry()
        client_registry.register(
            ClientDefinition(
                client_id="test-client",
                display_name="Test Client",
                platform="test",
                config_location="~/.test/config.json",
                config_format="mcp_v1",
                version_min="1.0.0",
                capabilities=ClientCapabilities(
                    environment_variables=True,
                    command_args=True,
                    working_directory=True,
                    multiple_servers=True,
                ),
                limitations=ClientLimitations(
                    max_servers=5,
                    max_env_vars_per_server=10,
                ),
                default_profiles=[
                    ProfileDefinition(
                        profile_id="default",
                        display_name="Default Profile",
                        description="Default test profile",
                    )
                ],
            )
        )

        # Create config with too many env vars (limit is 10)
        builder = ConfigBuilder("test-client", "default", server_registry)
        # Include required env var + 10 more = 11 total
        env_vars = {"GITHUB_TOKEN": "ghp_test"}
        env_vars.update({f"VAR_{i}": f"value_{i}" for i in range(10)})
        builder.add_server("github", env_vars=env_vars)

        # Validate
        result = validate_config_logic(
            builder, client_registry, client_id="test-client"
        )

        assert result["valid"] is False
        assert any(e["code"] == "TOO_MANY_ENV_VARS" for e in result["errors"])
        error = next(e for e in result["errors"] if e["code"] == "TOO_MANY_ENV_VARS")
        assert error["limit"] == 10
        assert error["actual"] == 11

    def test_unknown_client_warning(self):
        """Test warning for unknown client (can't validate limitations)."""
        server_registry = ServerRegistry()
        server_registry.register(
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
            )
        )

        client_registry = ClientRegistry()

        # Create config for unknown client
        builder = ConfigBuilder("unknown-client", "default", server_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})

        # Validate
        result = validate_config_logic(
            builder, client_registry, client_id="unknown-client"
        )

        # Should be valid (unknown client is just a warning)
        assert result["valid"] is True
        assert any(w["code"] == "UNKNOWN_CLIENT" for w in result["warnings"])
