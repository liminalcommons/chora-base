"""MCP orchestration server implementation.

This module implements the Model Context Protocol server for MCP client
configuration orchestration and distribution.

Wave 1.0 (Foundation v0.1.0):
- 4 tools: list_clients, list_profiles, get_config, diff_config
- 2 resources: capabilities://server, capabilities://clients

Wave 1.1 (Server Registry v0.1.1):
- 2 tools: list_available_servers, describe_server
- 2 resources: server://registry, server://{server_id}

Wave 1.2 (Transport Abstraction + Config Generation v0.1.2):
- 3 tools: add_server_to_config, remove_server_from_config, publish_config
- 1 resource: config://{client_id}/{profile_id}/draft

Wave 1.3 (Claude Desktop Ergonomics v0.1.3):
- 3 tools: view_draft_config, clear_draft_config, initialize_keys
- Default parameters for common use cases
- Improved tool descriptions and cross-references

Wave 1.4 (Schema Validation v0.1.4):
- 1 tool: validate_config
- Comprehensive configuration validation before publishing
"""

import json
from typing import Any

from fastmcp import FastMCP

from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.deployment import DeploymentWorkflow, DeploymentError
from mcp_orchestrator.deployment.log import DeploymentLog
from mcp_orchestrator.diff import compare_configs
from mcp_orchestrator.publishing import PublishingWorkflow, ValidationError
from mcp_orchestrator.registry import get_default_registry
from mcp_orchestrator.servers import ServerRegistry, get_default_registry as get_server_registry
from mcp_orchestrator.servers.registry import ServerNotFoundError
from mcp_orchestrator.storage import ArtifactStore, StorageError

# Initialize MCP server
mcp = FastMCP("mcp-orchestration")

# Initialize global state (will be set on server startup)
_registry = get_default_registry()  # Client registry
_server_registry = get_server_registry()  # Server registry (Wave 1.1)
_store = ArtifactStore()  # Uses default ~/.mcp-orchestration path

# Wave 1.2: Draft config builders (keyed by "client_id/profile_id")
_builders: dict[str, ConfigBuilder] = {}

# Wave 1.5: Deployment support
_deployment_log = DeploymentLog(deployments_dir=str(_store.base_path / "deployments"))


# =============================================================================
# TOOLS (14 - Wave 1.0: 4, Wave 1.1: 2, Wave 1.2: 3, Wave 1.3: 3, Wave 1.4: 1)
# Note: Wave 1.3 includes parameter default changes to existing tools
# =============================================================================


@mcp.tool()
async def list_clients() -> dict[str, Any]:
    """List supported MCP client families.

    Returns information about all MCP client families supported by the
    orchestration system (e.g., Claude Desktop, Cursor).

    Performance: p95 < 200ms (NFR-4)

    Returns:
        Dictionary with:
        - clients: List of client objects with id, display_name, platform, etc.
        - count: Total number of clients
    """
    # Get clients from registry
    registry_clients = _registry.list_clients()

    # Build response with client metadata
    clients = []
    for client_def in registry_clients:
        # Get profile IDs from registry
        profile_ids = [p.profile_id for p in client_def.default_profiles]

        clients.append(
            {
                "client_id": client_def.client_id,
                "display_name": client_def.display_name,
                "platform": client_def.platform,
                "config_location": client_def.config_location,
                "available_profiles": profile_ids,
            }
        )

    return {
        "clients": clients,
        "count": len(clients),
    }


@mcp.tool()
async def list_profiles(client_id: str) -> dict[str, Any]:
    """List available configuration profiles for a client.

    Returns all profiles available for a given client family. Profiles represent
    different configuration sets (e.g., dev, staging, prod).

    Performance: p95 < 200ms (NFR-4)

    Args:
        client_id: Client family identifier (e.g., 'claude-desktop', 'cursor')

    Returns:
        Dictionary with:
        - client_id: Client family identifier
        - profiles: List of profile objects
        - count: Number of profiles

    Raises:
        ValueError: If client_id not found
    """
    # Validate client exists in registry
    if not _registry.has_client(client_id):
        available = _registry.client_ids()
        raise ValueError(
            f"Client '{client_id}' not found. Available: {available}"
        )

    # Get profile definitions from registry
    profile_defs = _registry.get_profiles(client_id)

    # Try to get stored profiles for artifact metadata
    try:
        stored_profile_ids = _store.list_profiles(client_id)
    except StorageError:
        # Client not in storage yet - use registry only
        stored_profile_ids = []

    profiles = []
    for profile_def in profile_defs:
        profile_data = {
            "profile_id": profile_def.profile_id,
            "display_name": profile_def.display_name,
            "description": profile_def.description,
        }

        # Add storage metadata if available
        if profile_def.profile_id in stored_profile_ids:
            try:
                metadata = _store.get_profile_metadata(
                    client_id, profile_def.profile_id
                )
                profile_data["latest_artifact_id"] = metadata.latest_artifact_id
                profile_data["updated_at"] = metadata.updated_at
            except StorageError:
                # Profile exists in storage list but metadata unavailable
                profile_data["latest_artifact_id"] = None
                profile_data["updated_at"] = None
        else:
            # Profile not yet in storage
            profile_data["latest_artifact_id"] = None
            profile_data["updated_at"] = None

        profiles.append(profile_data)

    return {
        "client_id": client_id,
        "profiles": profiles,
        "count": len(profiles),
    }


@mcp.tool()
async def get_config(
    client_id: str,
    profile_id: str = "default",
    artifact_id: str | None = None,
) -> dict[str, Any]:
    """Retrieve signed configuration artifact.

    Fetches the latest (or specified) configuration artifact for a client/profile
    combination. Returns a cryptographically signed artifact with content-addressable
    identifier.

    Performance: p95 < 300ms (NFR-3)

    Args:
        client_id: Client family identifier (e.g., 'claude-desktop')
        profile_id: Profile identifier (defaults to 'default')
        artifact_id: Optional specific artifact hash to retrieve

    Returns:
        Dictionary with:
        - artifact_id: SHA-256 hash of payload (content-addressable ID)
        - client_id: Client family identifier
        - profile_id: Profile identifier
        - created_at: ISO 8601 timestamp
        - payload: MCP client configuration (mcpServers structure)
        - signature: Base64-encoded Ed25519 signature
        - signing_key_id: Identifier for public key verification
        - metadata: Generator info

    Raises:
        ValueError: If client_id or profile_id not found, or artifact_id invalid
    """
    # Validate client exists
    if not _registry.has_client(client_id):
        available = _registry.client_ids()
        raise ValueError(
            f"Client '{client_id}' not found. Available: {available}"
        )

    # Retrieve artifact from storage
    try:
        if artifact_id:
            # Get specific artifact by ID
            artifact = _store.get_by_id(artifact_id)
        else:
            # Get latest artifact for client/profile
            artifact = _store.get(client_id, profile_id)

        # Convert ConfigArtifact to tool response format
        return {
            "artifact_id": artifact.artifact_id,
            "client_id": artifact.client_id,
            "profile_id": artifact.profile_id,
            "created_at": artifact.created_at,
            "payload": artifact.payload,
            "signature": artifact.signature,
            "signing_key_id": artifact.signing_key_id,
            "metadata": artifact.metadata,
        }

    except StorageError as e:
        # Convert storage errors to tool errors
        if "not found" in str(e).lower():
            if artifact_id:
                raise ValueError(f"Artifact '{artifact_id}' not found") from e
            else:
                raise ValueError(
                    f"No configuration found for {client_id}/{profile_id}. "
                    f"Run 'mcp-orchestration init-configs' to create initial configs."
                ) from e
        else:
            raise ValueError(f"Failed to retrieve configuration: {e}") from e


@mcp.tool()
async def diff_config(
    client_id: str,
    profile_id: str = "default",
    local_artifact_id: str | None = None,
    local_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compare configurations and detect updates.

    Compares a local configuration against the latest orchestrated version.
    Returns diff report showing additions, modifications, removals, and update
    availability.

    Performance: p95 < 200ms (NFR-4)

    Args:
        client_id: Client family identifier
        profile_id: Profile identifier (defaults to 'default')
        local_artifact_id: SHA-256 hash of local config (optional)
        local_payload: Local MCP configuration payload (alternative to local_artifact_id)

    Returns:
        Dictionary with:
        - status: 'up-to-date', 'outdated', 'diverged', or 'unknown'
        - local_artifact_id: Hash of local config
        - remote_artifact_id: Hash of latest orchestrated config
        - diff: Object with servers_added, servers_removed, servers_modified, servers_unchanged
        - summary: Counts of changes
        - recommendation: Human-readable action recommendation

    Raises:
        ValueError: If client_id not found or neither local_artifact_id nor local_payload provided
    """
    # Validate inputs
    if not local_artifact_id and not local_payload:
        raise ValueError("Must provide either local_artifact_id or local_payload")

    if not _registry.has_client(client_id):
        available = _registry.client_ids()
        raise ValueError(
            f"Client '{client_id}' not found. Available: {available}"
        )

    # Get local payload if only artifact_id provided
    if local_artifact_id and not local_payload:
        try:
            local_artifact = _store.get_by_id(local_artifact_id)
            local_payload = local_artifact.payload
        except StorageError:
            # Artifact not in storage - can't compare
            raise ValueError(
                f"Local artifact '{local_artifact_id}' not found in storage. "
                "Provide local_payload instead."
            )

    # Compute local artifact ID if not provided
    if not local_artifact_id and local_payload:
        local_artifact_id = _store.compute_artifact_id(local_payload)

    # Get remote configuration
    try:
        remote_artifact = _store.get(client_id, profile_id)
    except StorageError as e:
        raise ValueError(
            f"No remote configuration found for {client_id}/{profile_id}"
        ) from e

    # Compare configurations
    diff_result = compare_configs(local_payload, remote_artifact.payload)

    # Generate human-readable recommendation
    if diff_result.status == "up-to-date":
        recommendation = "Your configuration is current. No updates needed."
    elif diff_result.status == "outdated":
        recommendation = (
            f"Update available: {len(diff_result.servers_added)} new server(s), "
            f"{len(diff_result.servers_modified)} server(s) updated. "
            "Run 'get_config' to fetch latest."
        )
    elif diff_result.status == "diverged":
        recommendation = (
            f"Configuration diverged: Your local config has {len(diff_result.servers_removed)} "
            "server(s) not in remote. Review changes carefully before updating."
        )
    else:
        recommendation = "Unable to determine configuration status."

    return {
        "status": diff_result.status,
        "local_artifact_id": local_artifact_id,
        "remote_artifact_id": remote_artifact.artifact_id,
        "diff": {
            "servers_added": diff_result.servers_added,
            "servers_removed": diff_result.servers_removed,
            "servers_modified": diff_result.servers_modified,
            "servers_unchanged": diff_result.servers_unchanged,
        },
        "summary": {
            "total_changes": diff_result.total_changes,
            "added_count": len(diff_result.servers_added),
            "removed_count": len(diff_result.servers_removed),
            "modified_count": len(diff_result.servers_modified),
        },
        "recommendation": recommendation,
    }


# =============================================================================
# TOOLS - Wave 1.1 (Server Registry)
# =============================================================================


@mcp.tool()
async def list_available_servers(
    transport_filter: str | None = None, search_query: str | None = None
) -> dict[str, Any]:
    """List all MCP servers in the registry.

    Browse the catalog of available MCP servers that can be added to client
    configurations. Servers can be filtered by transport type or searched by keywords.

    Args:
        transport_filter: Optional filter by transport type ('stdio', 'http', 'sse')
        search_query: Optional search query (searches name, description, tags)

    Returns:
        Dictionary with:
        - servers: List of server objects with metadata
        - count: Total number of servers
        - transport_counts: Breakdown by transport type
        - available_transports: List of transport types
    """
    # Get servers based on filters
    if search_query:
        servers = _server_registry.search(search_query)
    elif transport_filter:
        from mcp_orchestrator.servers.models import TransportType

        try:
            transport = TransportType(transport_filter.lower())
            servers = _server_registry.list_by_transport(transport)
        except ValueError:
            raise ValueError(
                f"Invalid transport filter: '{transport_filter}'. "
                f"Valid options: stdio, http, sse"
            )
    else:
        servers = _server_registry.list_all()

    # Build response
    server_list = []
    for server in servers:
        server_list.append(
            {
                "server_id": server.server_id,
                "display_name": server.display_name,
                "description": server.description,
                "transport": _get_transport_value(server.transport),
                "npm_package": server.npm_package,
                "tags": server.tags,
                "has_parameters": len(server.parameters) > 0,
                "requires_env": server.required_env,
            }
        )

    return {
        "servers": server_list,
        "count": len(server_list),
        "transport_counts": _server_registry.get_transport_counts(),
        "available_transports": ["stdio", "http", "sse"],
    }


@mcp.tool()
async def describe_server(server_id: str) -> dict[str, Any]:
    """Get detailed information about a specific MCP server.

    Returns complete server definition including transport configuration,
    parameters, environment variables, and documentation links.

    Args:
        server_id: Server identifier (e.g., 'filesystem', 'n8n', 'brave-search')

    Returns:
        Dictionary with:
        - server_id, display_name, description
        - transport: Transport type and configuration
        - parameters: User-configurable parameters
        - env_vars: Required and optional environment variables
        - installation: NPM package and install command
        - documentation_url: Link to server documentation
        - usage_example: Example configuration snippet

    Raises:
        ValueError: If server_id not found in registry
    """
    try:
        server = _server_registry.get(server_id)
    except ServerNotFoundError as e:
        raise ValueError(str(e)) from e

    # Build transport info
    transport_value = _get_transport_value(server.transport)
    transport_info = {"type": transport_value}

    if transport_value == "stdio":
        transport_info["command"] = server.stdio_command
        transport_info["args"] = server.stdio_args
    else:  # http or sse
        transport_info["url"] = server.http_url
        transport_info["auth_type"] = server.http_auth_type
        transport_info["note"] = (
            "This server will be automatically wrapped with mcp-remote "
            "to provide stdio compatibility for clients."
        )

    # Build parameters info
    parameters_info = []
    for param in server.parameters:
        parameters_info.append(
            {
                "name": param.name,
                "type": param.type,
                "description": param.description,
                "required": param.required,
                "default": param.default,
                "example": param.example,
            }
        )

    # Build installation info
    installation_info = {}
    if server.npm_package:
        installation_info = {
            "npm_package": server.npm_package,
            "install_command": f"npm install -g {server.npm_package}",
            "note": "Can also be used via npx without installation",
        }

    # Build usage example
    usage_example = _generate_usage_example(server)

    return {
        "server_id": server.server_id,
        "display_name": server.display_name,
        "description": server.description,
        "transport": transport_info,
        "parameters": parameters_info,
        "env_vars": {
            "required": server.required_env,
            "optional": server.optional_env,
        },
        "installation": installation_info,
        "documentation_url": server.documentation_url,
        "tags": server.tags,
        "usage_example": usage_example,
    }


def _generate_usage_example(server) -> str:
    """Generate example configuration snippet for a server.

    Args:
        server: ServerDefinition

    Returns:
        JSON string with example mcpServers configuration
    """
    import json

    # Build example args with parameter placeholders
    transport_value = _get_transport_value(server.transport)
    if transport_value == "stdio":
        args = []
        for arg in server.stdio_args:
            # Replace parameter placeholders with example values
            example_arg = arg
            for param in server.parameters:
                placeholder = f"{{{param.name}}}"
                if placeholder in arg:
                    example_value = param.example or param.default or f"<{param.name}>"
                    example_arg = arg.replace(placeholder, str(example_value))
            args.append(example_arg)

        example = {
            server.server_id: {
                "command": server.stdio_command,
                "args": args,
            }
        }

        if server.required_env or server.optional_env:
            env_vars = {}
            for env_var in server.required_env:
                env_vars[env_var] = f"${{{env_var}}}"
            example[server.server_id]["env"] = env_vars

    else:  # http or sse
        # Show URL with parameter examples
        url = server.http_url
        for param in server.parameters:
            placeholder = f"{{{param.name}}}"
            example_value = param.example or param.default or f"<{param.name}>"
            url = url.replace(placeholder, str(example_value))

        example = {
            server.server_id: {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/mcp-remote", "stdio", url],
            }
        }

        if server.required_env:
            env_vars = {}
            for env_var in server.required_env:
                env_vars[env_var] = f"${{{env_var}}}"
            example[server.server_id]["env"] = env_vars

    return json.dumps({"mcpServers": example}, indent=2)


# =============================================================================
# TOOLS - Wave 1.2 (Config Building)
# =============================================================================


def _get_transport_value(transport: Any) -> str:
    """Safely get transport value (handles both enum and string).

    Pydantic's use_enum_values=True serializes enums to strings, so
    server.transport might be either TransportType enum or str.

    Args:
        transport: TransportType enum or string value

    Returns:
        String value of transport type
    """
    from mcp_orchestrator.servers.models import TransportType

    return transport.value if isinstance(transport, TransportType) else transport


def _get_builder(client_id: str, profile_id: str) -> ConfigBuilder:
    """Get or create a ConfigBuilder for client/profile.

    Args:
        client_id: Client family identifier
        profile_id: Profile identifier

    Returns:
        ConfigBuilder instance
    """
    key = f"{client_id}/{profile_id}"
    if key not in _builders:
        _builders[key] = ConfigBuilder(client_id, profile_id, _server_registry)
    return _builders[key]


@mcp.tool()
async def add_server_to_config(
    server_id: str,
    params: dict[str, Any] | str | None = None,
    env_vars: dict[str, str] | str | None = None,
    server_name: str | None = None,
    client_id: str = "claude-desktop",
    profile_id: str = "default",
) -> dict[str, Any]:
    """Add a server to the draft configuration.

    Adds an MCP server to the draft configuration for a client/profile.
    Automatically handles stdio vs HTTP/SSE transport (HTTP/SSE servers are
    wrapped with mcp-remote transparently).

    Note: When calling from Claude Desktop, params and env_vars can be passed
    as either dict objects or JSON strings - both formats work correctly.

    Args:
        server_id: Server identifier from registry (use list_available_servers)
        params: Parameter values (e.g., {"path": "/Users/me/Documents"})
        env_vars: Environment variables (e.g., {"GITHUB_TOKEN": "ghp_..."})
        server_name: Name to use in config (defaults to server_id)
        client_id: Client family identifier (defaults to 'claude-desktop')
        profile_id: Profile identifier (defaults to 'default')

    Returns:
        Dictionary with:
        - status: "added"
        - server_name: Name used in config
        - draft: Current draft configuration preview
        - server_count: Number of servers in draft

    Raises:
        ValueError: If server_id not found or parameters invalid

    Example:
        >>> result = await add_server_to_config(
        ...     server_id="filesystem",
        ...     params={"path": "/Users/me/Documents"}
        ... )
        >>> # Draft now contains filesystem server config for claude-desktop/default
    """
    try:
        # Get or create builder
        builder = _get_builder(client_id, profile_id)

        # Parse params if passed as JSON string (Claude Desktop serialization)
        if isinstance(params, str):
            import json
            params = json.loads(params)

        # Parse env_vars if passed as JSON string
        if isinstance(env_vars, str):
            import json
            env_vars = json.loads(env_vars)

        # Add server (will validate params and env_vars)
        builder.add_server(
            server_id=server_id,
            params=params,
            env_vars=env_vars,
            server_name=server_name,
        )

        # Return status with draft preview
        return {
            "status": "added",
            "server_name": server_name or server_id,
            "draft": builder.build(),
            "server_count": builder.count(),
        }

    except ServerNotFoundError as e:
        raise ValueError(f"Server not found: {e}")
    except Exception as e:
        raise ValueError(f"Failed to add server: {e}")


@mcp.tool()
async def remove_server_from_config(
    server_name: str,
    client_id: str = "claude-desktop",
    profile_id: str = "default",
) -> dict[str, Any]:
    """Remove a server from the draft configuration.

    Removes an MCP server from the draft configuration for a client/profile.

    Args:
        server_name: Name of server in config (use add_server_to_config result)
        client_id: Client family identifier (defaults to 'claude-desktop')
        profile_id: Profile identifier (defaults to 'default')

    Returns:
        Dictionary with:
        - status: "removed"
        - server_name: Name of removed server
        - draft: Updated draft configuration
        - server_count: Number of servers remaining in draft

    Raises:
        ValueError: If server_name not found in draft

    Example:
        >>> result = await remove_server_from_config(
        ...     server_name="filesystem"
        ... )
        >>> # Server removed from draft for claude-desktop/default
    """
    try:
        # Get builder (raises if doesn't exist)
        builder = _get_builder(client_id, profile_id)

        # Remove server
        from mcp_orchestrator.building.builder import ServerNotInConfigError

        try:
            builder.remove_server(server_name)
        except ServerNotInConfigError as e:
            raise ValueError(str(e))

        # Return status with updated draft
        return {
            "status": "removed",
            "server_name": server_name,
            "draft": builder.build(),
            "server_count": builder.count(),
        }

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to remove server: {e}")


@mcp.tool()
async def view_draft_config(
    client_id: str = "claude-desktop",
    profile_id: str = "default",
) -> dict[str, Any]:
    """View the current draft configuration without modifying it.

    Returns the current draft configuration for inspection. This is useful
    for checking what servers are configured before publishing.

    Args:
        client_id: Client family identifier (defaults to 'claude-desktop')
        profile_id: Profile identifier (defaults to 'default')

    Returns:
        Dictionary with:
        - draft: Current draft configuration
        - server_count: Number of servers in draft
        - servers: List of server names in draft

    Example:
        >>> result = await view_draft_config()
        >>> # Returns current draft for claude-desktop/default
    """
    try:
        # Check if draft exists
        key = f"{client_id}/{profile_id}"
        if key not in _builders:
            # Return empty draft
            return {
                "draft": {"mcpServers": {}},
                "server_count": 0,
                "servers": [],
            }

        builder = _builders[key]
        return {
            "draft": builder.build(),
            "server_count": builder.count(),
            "servers": builder.get_servers(),
        }

    except Exception as e:
        raise ValueError(f"Failed to view draft: {e}")


@mcp.tool()
async def clear_draft_config(
    client_id: str = "claude-desktop",
    profile_id: str = "default",
) -> dict[str, Any]:
    """Clear all servers from the draft configuration.

    Removes all servers from the draft, allowing you to start fresh.
    This does not affect any published configurations.

    Args:
        client_id: Client family identifier (defaults to 'claude-desktop')
        profile_id: Profile identifier (defaults to 'default')

    Returns:
        Dictionary with:
        - status: "cleared"
        - previous_count: Number of servers that were removed

    Example:
        >>> result = await clear_draft_config()
        >>> # Draft is now empty
    """
    try:
        # Check if draft exists
        key = f"{client_id}/{profile_id}"
        if key not in _builders:
            return {"status": "cleared", "previous_count": 0}

        builder = _builders[key]
        previous_count = builder.count()
        builder.clear()

        return {
            "status": "cleared",
            "previous_count": previous_count,
        }

    except Exception as e:
        raise ValueError(f"Failed to clear draft: {e}")


@mcp.tool()
async def publish_config(
    changelog: str | None = None,
    client_id: str = "claude-desktop",
    profile_id: str = "default",
) -> dict[str, Any]:
    """Publish draft configuration as signed artifact.

    Takes the current draft configuration for a client/profile and publishes
    it as a cryptographically signed, content-addressable artifact.

    This completes the workflow: browse → add → view → validate → publish

    The publishing workflow:
    1. Validates the draft configuration for errors
    2. Signs the configuration with your Ed25519 private key
    3. Stores it as a content-addressable artifact (SHA-256)
    4. Updates the profile index

    Note: Requires signing keys to be initialized. If keys don't exist, use
    the initialize_keys tool first.

    Args:
        changelog: Optional changelog describing the changes
        client_id: Client family identifier (defaults to 'claude-desktop')
        profile_id: Profile identifier (defaults to 'default')

    Returns:
        Dictionary with:
        - status: "published"
        - artifact_id: SHA-256 content address
        - client_id: Client family
        - profile_id: Profile
        - server_count: Number of servers in config
        - changelog: Changelog if provided
        - created_at: ISO 8601 timestamp

    Raises:
        ValueError: If draft is empty, validation fails, or publishing fails

    Example:
        >>> result = await publish_config(
        ...     changelog="Added filesystem and github servers"
        ... )
        >>> # Config is now validated, signed, and stored for claude-desktop/default
    """
    import logging

    logger = logging.getLogger(__name__)

    try:
        # Log start of publish operation
        logger.info(
            f"Starting publish_config for {client_id}/{profile_id} "
            f"(changelog: {changelog[:50] if changelog else 'None'})"
        )

        # Get builder (must exist with servers)
        builder = _get_builder(client_id, profile_id)
        logger.info(f"Got builder with {builder.count()} servers")

        # Get signing key paths
        from pathlib import Path

        home = Path.home()
        key_dir = home / ".mcp-orchestration" / "keys"
        private_key_path = key_dir / "signing.key"

        if not private_key_path.exists():
            logger.error(f"Signing key not found at {private_key_path}")
            raise ValueError(
                f"Signing key not found at {private_key_path}. "
                "Use the initialize_keys tool to generate keys."
            )

        logger.info(f"Found signing key at {private_key_path}")

        # Use PublishingWorkflow to validate → sign → store
        workflow = PublishingWorkflow(
            store=_store,
            client_registry=_registry,
        )

        logger.info("Created PublishingWorkflow, calling publish()...")

        # Call publish and log result
        try:
            result = workflow.publish(
                builder=builder,
                private_key_path=str(private_key_path),
                signing_key_id="default",
                changelog=changelog,
            )
            logger.info(f"Publish succeeded with artifact_id: {result.get('artifact_id', 'UNKNOWN')[:16]}...")

        except Exception as publish_error:
            logger.error(f"workflow.publish() raised exception: {type(publish_error).__name__}: {publish_error}")
            raise

        # Ensure result is JSON-serializable
        # Convert any datetime objects or other non-serializable types
        serializable_result = {
            "status": str(result.get("status", "published")),
            "artifact_id": str(result.get("artifact_id", "")),
            "client_id": str(result.get("client_id", client_id)),
            "profile_id": str(result.get("profile_id", profile_id)),
            "server_count": int(result.get("server_count", 0)),
            "created_at": str(result.get("created_at", "")),
        }

        if changelog:
            serializable_result["changelog"] = str(changelog)

        logger.info(f"Returning serializable result: {serializable_result}")
        return serializable_result

    except ValidationError as e:
        # Validation errors are user errors - provide helpful message
        logger.error(f"Validation failed: {e}")
        errors = e.validation_result.get("errors", [])
        error_msgs = [f"  - [{err['code']}] {err['message']}" for err in errors]
        raise ValueError(
            f"Configuration validation failed:\n" + "\n".join(error_msgs)
        )

    except ValueError as e:
        logger.error(f"ValueError in publish_config: {e}")
        raise

    except StorageError as e:
        # Storage-specific errors
        logger.error(f"Storage error during publish: {e}")
        raise ValueError(f"Failed to store configuration artifact: {e}")

    except Exception as e:
        # Catch-all for unexpected errors
        logger.error(f"Unexpected error in publish_config: {type(e).__name__}: {e}", exc_info=True)
        raise ValueError(f"Failed to publish config: {type(e).__name__}: {e}")


@mcp.tool()
async def initialize_keys(regenerate: bool = False) -> dict[str, Any]:
    """Initialize Ed25519 signing keys for cryptographic artifact signing.

    Generates a new Ed25519 key pair and stores them securely. The private key
    is saved with restricted permissions (0600). This is required before
    publishing configurations.

    Args:
        regenerate: If True, regenerate keys even if they already exist

    Returns:
        Dictionary with:
        - status: "initialized" or "already_exists"
        - key_dir: Directory where keys are stored
        - public_key_path: Path to public key file
        - message: Human-readable status message

    Example:
        >>> result = await initialize_keys()
        >>> # Keys generated and ready for use
    """
    try:
        from pathlib import Path

        from mcp_orchestrator.crypto import ArtifactSigner

        home = Path.home()
        key_dir = home / ".mcp-orchestration" / "keys"
        private_key_path = key_dir / "signing.key"
        public_key_path = key_dir / "signing.pub"

        # Check if keys already exist
        if private_key_path.exists() and not regenerate:
            return {
                "status": "already_exists",
                "key_dir": str(key_dir),
                "public_key_path": str(public_key_path),
                "message": "Signing keys already exist. Use regenerate=True to recreate them.",
            }

        # Ensure artifacts directory exists
        artifacts_dir = home / ".mcp-orchestration" / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        # Generate new keys
        signer = ArtifactSigner.generate()
        signer.save_private_key(str(private_key_path))
        signer.save_public_key(str(public_key_path))

        action = "regenerated" if regenerate else "initialized"
        return {
            "status": action,
            "key_dir": str(key_dir),
            "public_key_path": str(public_key_path),
            "message": f"Signing keys {action} successfully. You can now publish configurations.",
        }

    except Exception as e:
        raise ValueError(f"Failed to initialize keys: {e}")


# =============================================================================
# TOOLS - Wave 1.4 (Schema Validation)
# =============================================================================


@mcp.tool()
async def validate_config(
    client_id: str = "claude-desktop",
    profile_id: str = "default",
) -> dict[str, Any]:
    """Validate draft configuration before publishing.

    Performs comprehensive validation of the current draft configuration,
    checking for:
    - Empty configurations (at least one server required)
    - Server configuration structure (command, args)
    - Environment variable format
    - Client-specific limitations (max servers, max env vars)

    This is recommended before publishing to catch issues early.

    Args:
        client_id: Client family identifier (defaults to 'claude-desktop')
        profile_id: Profile identifier (defaults to 'default')

    Returns:
        Dictionary with:
        - valid: True if config is valid, False otherwise
        - errors: List of validation errors (empty if valid)
        - warnings: List of non-critical warnings
        - server_count: Number of servers in draft
        - validated_at: ISO 8601 timestamp of validation

    Example:
        >>> result = await validate_config()
        >>> if result["valid"]:
        ...     # Safe to publish
        ...     await publish_config()
        >>> else:
        ...     # Fix errors first
        ...     print(result["errors"])
    """
    from datetime import datetime

    try:
        # Get builder (may not exist yet)
        builder = _get_builder(client_id, profile_id)

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
            client_def = _registry.get_client(client_id)

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
            "client_id": client_id,
            "profile_id": profile_id,
            "validated_at": datetime.utcnow().isoformat() + "Z",
        }

    except Exception as e:
        # Unexpected error during validation
        return {
            "valid": False,
            "errors": [
                {
                    "code": "VALIDATION_ERROR",
                    "message": f"Validation failed with unexpected error: {str(e)}",
                    "severity": "error",
                }
            ],
            "warnings": [],
            "server_count": 0,
            "client_id": client_id,
            "profile_id": profile_id,
            "validated_at": datetime.utcnow().isoformat() + "Z",
        }


@mcp.tool()
async def deploy_config(
    client_id: str = "claude-desktop",
    profile_id: str = "default",
    artifact_id: str | None = None
) -> dict[str, Any]:
    """Deploy configuration to client.

    Automatically deploys a published configuration to the client's config location.
    This completes the full workflow: discover → add → validate → publish → deploy.

    The deployment workflow:
    1. Validates client exists in registry
    2. Fetches artifact (latest if not specified)
    3. Verifies cryptographic signature
    4. Writes config to client location
    5. Records deployment event

    Note: After deployment, restart the client application for changes to take effect.

    Args:
        client_id: Client family identifier (defaults to 'claude-desktop')
        profile_id: Profile identifier (defaults to 'default')
        artifact_id: Optional specific artifact to deploy (defaults to latest)

    Returns:
        Dictionary with:
        - status: "deployed"
        - config_path: Path where config was written
        - artifact_id: Deployed artifact ID
        - deployed_at: ISO 8601 timestamp

    Raises:
        ValueError: If client not found, artifact not found, or deployment fails

    Example:
        >>> # Deploy latest published config
        >>> result = await deploy_config()
        >>> print(f"Deployed to: {result['config_path']}")
        >>> # Restart client for changes to take effect

        >>> # Deploy specific version (rollback)
        >>> result = await deploy_config(artifact_id="abc123...")
    """
    try:
        # Create deployment workflow
        workflow = DeploymentWorkflow(
            store=_store,
            client_registry=_registry,
            deployment_log=_deployment_log
        )

        # Deploy configuration
        result = workflow.deploy(
            client_id=client_id,
            profile_id=profile_id,
            artifact_id=artifact_id
        )

        return result.model_dump()

    except DeploymentError as e:
        # Deployment-specific errors - provide helpful message
        error_code = e.details.get("code", "DEPLOYMENT_ERROR")
        raise ValueError(f"[{error_code}] {str(e)}")

    except ValueError:
        raise

    except Exception as e:
        raise ValueError(f"Failed to deploy config: {e}")


# =============================================================================
# RESOURCES (7 - Wave 1.0: 2, Wave 1.1: 2, Wave 1.2: 1, Wave 1.5: 2)
# =============================================================================


@mcp.resource("capabilities://server")
async def server_capabilities() -> str:
    """Expose server capabilities and features.

    Returns information about the orchestration server's capabilities, version,
    and supported features.

    Returns:
        JSON string with server metadata
    """
    capabilities = {
        "name": "mcp-orchestration",
        "version": "0.1.5",
        "wave": "Wave 1.5: Configuration Deployment",
        "capabilities": {
            "tools": [
                # Wave 1.0
                "list_clients",
                "list_profiles",
                "get_config",
                "diff_config",
                # Wave 1.1
                "list_available_servers",
                "describe_server",
                # Wave 1.2
                "add_server_to_config",
                "remove_server_from_config",
                "publish_config",
                # Wave 1.3
                "view_draft_config",
                "clear_draft_config",
                "initialize_keys",
                # Wave 1.4
                "validate_config",
                # Wave 1.5
                "deploy_config",
            ],
            "resources": [
                # Wave 1.0
                "capabilities://server",
                "capabilities://clients",
                # Wave 1.1
                "server://registry",
                "server://{server_id}",
                # Wave 1.2
                "config://{client_id}/{profile_id}/draft",
                # Wave 1.5
                "config://{client_id}/{profile_id}/latest",
                "config://{client_id}/{profile_id}/deployed",
            ],
            "prompts": [],
        },
        "features": {
            "content_addressing": True,
            "cryptographic_signing": True,
            "signature_algorithm": "Ed25519",
            "diff_reports": True,
            "profile_support": True,
            # Wave 1.1
            "server_registry": True,
            "server_discovery": True,
            # Wave 1.2
            "transport_abstraction": True,
            "config_building": True,
            "draft_management": True,
            "mcp_remote_wrapping": True,
            # Wave 1.3
            "default_parameters": True,
            "autonomous_key_initialization": True,
            "draft_inspection": True,
            # Wave 1.4
            "schema_validation": True,
            "pre_publish_validation": True,
            # Wave 1.5
            "automated_deployment": True,
            "deployment_logging": True,
            "configuration_drift_detection": True,
            "version_pinning": True,
            "atomic_deployment": True,
        },
        "endpoints": {
            "verification_key_url": "https://mcp-orchestration.example.com/keys/verification_key.pem"
        },
    }
    return json.dumps(capabilities, indent=2)


@mcp.resource("capabilities://clients")
async def client_capabilities() -> str:
    """Expose client family capability matrix.

    Returns detailed capability information for each supported client family,
    showing which features and configurations are supported per client.

    Returns:
        JSON string with client capability matrix
    """
    # Build capabilities from registry
    registry_clients = _registry.list_clients()

    client_list = []
    for client_def in registry_clients:
        client_list.append(
            {
                "client_id": client_def.client_id,
                "display_name": client_def.display_name,
                "version_min": client_def.version_min,
                "version_max": client_def.version_max,
                "config_format": client_def.config_format,
                "supports": {
                    "environment_variables": client_def.capabilities.environment_variables,
                    "command_args": client_def.capabilities.command_args,
                    "working_directory": client_def.capabilities.working_directory,
                    "multiple_servers": client_def.capabilities.multiple_servers,
                },
                "limitations": {
                    "max_servers": client_def.limitations.max_servers,
                    "max_env_vars_per_server": client_def.limitations.max_env_vars_per_server,
                },
            }
        )

    capabilities = {"clients": client_list}
    return json.dumps(capabilities, indent=2)


# =============================================================================
# RESOURCES - Wave 1.1 (Server Registry)
# =============================================================================


@mcp.resource("server://registry")
async def server_registry_resource() -> str:
    """Expose full server registry as JSON.

    Returns complete catalog of all available MCP servers with metadata,
    useful for clients that want to present a server browser UI.

    Returns:
        JSON string with server registry data
    """
    servers = _server_registry.list_all()

    registry_data = {
        "servers": [server.model_dump() for server in servers],
        "count": len(servers),
        "transport_counts": _server_registry.get_transport_counts(),
        "version": "0.1.1",
    }

    return json.dumps(registry_data, indent=2)


@mcp.resource("server://{server_id}")
async def server_definition_resource(server_id: str) -> str:
    """Expose detailed server definition as JSON.

    Returns complete server definition including transport config, parameters,
    environment variables, and documentation.

    Args:
        server_id: Server identifier

    Returns:
        JSON string with server definition

    Raises:
        ValueError: If server_id not found
    """
    try:
        server = _server_registry.get(server_id)
    except ServerNotFoundError as e:
        raise ValueError(str(e)) from e

    return json.dumps(server.model_dump(), indent=2)


# =============================================================================
# RESOURCES - Wave 1.2 (Config Building)
# =============================================================================


@mcp.resource("config://{client_id}/{profile_id}/draft")
async def draft_config_resource(client_id: str, profile_id: str) -> str:
    """Expose draft configuration as JSON resource.

    Returns the current draft configuration for a client/profile combination.
    The draft is an unsigned, work-in-progress configuration that can be
    validated and published.

    Args:
        client_id: Client family identifier
        profile_id: Profile identifier

    Returns:
        JSON string with draft configuration including:
        - payload: mcpServers structure
        - server_count: Number of servers in draft
        - servers: List of server names

    Example URI:
        config://claude-desktop/default/draft

    Note:
        If no draft exists yet for this client/profile, returns an empty config.
    """
    # Get or create builder (will be empty if new)
    builder = _get_builder(client_id, profile_id)

    # Return draft info
    draft_info = {
        "client_id": client_id,
        "profile_id": profile_id,
        "payload": builder.build(),
        "server_count": builder.count(),
        "servers": builder.get_servers(),
    }

    return json.dumps(draft_info, indent=2)


# =============================================================================
# RESOURCES - Wave 1.5 (Config Deployment)
# =============================================================================


@mcp.resource("config://{client_id}/{profile_id}/latest")
async def latest_config_resource(client_id: str, profile_id: str) -> str:
    """Expose latest published artifact as JSON resource.

    Returns the latest published configuration artifact for a client/profile.
    This is the most recent version that has been signed and published,
    regardless of whether it has been deployed yet.

    Args:
        client_id: Client family identifier
        profile_id: Profile identifier

    Returns:
        JSON string with artifact information including:
        - artifact_id: Content-addressed SHA-256 ID
        - client_id: Client this artifact is for
        - profile_id: Profile within client
        - payload: mcpServers configuration
        - metadata: Changelog and other metadata
        - signed_at: When artifact was published

    Example URI:
        config://claude-desktop/default/latest

    Raises:
        ValueError: If no published artifact exists for this client/profile

    Use Case:
        Query this resource to detect configuration drift:
        - Compare latest (this resource) vs deployed (deployed resource)
        - If IDs differ, configuration drift detected
        - Run deploy_config() to update deployed config
    """
    try:
        artifact = _store.get(client_id, profile_id)
    except Exception as e:
        raise ValueError(
            f"No published artifact found for {client_id}/{profile_id}. "
            f"Publish a configuration first using publish_config(). "
            f"Error: {e}"
        )

    # Return artifact info
    artifact_info = {
        "artifact_id": artifact.artifact_id,
        "client_id": artifact.client_id,
        "profile_id": artifact.profile_id,
        "payload": artifact.payload,
        "metadata": artifact.metadata,
        "signed_at": artifact.metadata.get("signed_at"),
        "server_count": len(artifact.payload.get("mcpServers", {})),
        "servers": list(artifact.payload.get("mcpServers", {}).keys()),
    }

    return json.dumps(artifact_info, indent=2)


@mcp.resource("config://{client_id}/{profile_id}/deployed")
async def deployed_config_resource(client_id: str, profile_id: str) -> str:
    """Expose currently deployed artifact as JSON resource.

    Returns the configuration artifact that is currently deployed to the
    client's config location on disk. This may differ from the latest
    published artifact if deployment hasn't been run yet.

    Args:
        client_id: Client family identifier
        profile_id: Profile identifier

    Returns:
        JSON string with deployment information including:
        - artifact_id: ID of deployed artifact
        - config_path: Where config was deployed
        - deployed_at: When deployment occurred
        - changelog: Changelog from deployed artifact
        - drift_detected: Whether deployed differs from latest

    Example URI:
        config://claude-desktop/default/deployed

    Raises:
        ValueError: If no deployment exists for this client/profile

    Use Case:
        Query this resource to:
        - Check what version is currently deployed
        - Detect configuration drift vs latest
        - View deployment history
    """
    deployed_artifact_id = _deployment_log.get_deployed_artifact(client_id, profile_id)

    if deployed_artifact_id is None:
        raise ValueError(
            f"No deployment found for {client_id}/{profile_id}. "
            f"Deploy a configuration first using deploy_config()."
        )

    # Get deployment details
    history = _deployment_log.get_deployment_history(client_id, profile_id, limit=1)
    if not history:
        raise ValueError(f"Deployment log entry not found for {client_id}/{profile_id}")

    deployment = history[0]

    # Check for drift (deployed vs latest)
    drift_detected = False
    latest_artifact_id = None
    try:
        latest_artifact = _store.get(client_id, profile_id)
        latest_artifact_id = latest_artifact.artifact_id
        drift_detected = (deployed_artifact_id != latest_artifact_id)
    except Exception:
        # No latest artifact - can't detect drift
        pass

    # Return deployment info
    deployment_info = {
        "artifact_id": deployed_artifact_id,
        "config_path": deployment.config_path,
        "deployed_at": deployment.deployed_at,
        "changelog": deployment.changelog,
        "drift_detected": drift_detected,
        "latest_artifact_id": latest_artifact_id,
    }

    return json.dumps(deployment_info, indent=2)


# =============================================================================
# TOOLS - Wave 2.2/3.0 (Automatic Server Installation)
# =============================================================================


@mcp.tool()
async def check_server_installation(server_id: str) -> dict[str, Any]:
    """Check if an MCP server is installed on the system.

    Checks installation status by looking for the server's command in the
    system PATH. Returns installation details including version and location.

    Args:
        server_id: Server identifier from registry (e.g., 'filesystem', 'lightrag-mcp')

    Returns:
        Dictionary with:
        - server_id: Server identifier
        - status: "installed", "not_installed", "unknown", or "error"
        - installed_version: Version string if installed
        - install_location: Path to installed binary
        - package_manager: Package manager used
        - installation_command: Suggested install command if not installed
        - error_message: Error details if status is "error"

    Raises:
        ValueError: If server_id not found in registry

    Example:
        >>> result = await check_server_installation("filesystem")
        >>> # Returns: {"status": "installed", "installed_version": "2025.8.21", ...}
    """
    from mcp_orchestrator.installation.validator import InstallationValidator

    # Get server from registry
    try:
        server = _server_registry.get(server_id)
    except ServerNotFoundError as e:
        raise ValueError(str(e)) from e

    # Check installation
    validator = InstallationValidator()
    result = validator.check_installation(server)

    # Build response
    response = result.model_dump()

    # Add installation command if not installed
    if result.status == "not_installed":
        if server.npm_package:
            response["installation_command"] = f"npm install -g {server.npm_package}"
        elif server.pypi_package:
            response["installation_command"] = f"pip install {server.pypi_package}"

    return response


@mcp.tool()
async def install_server(
    server_id: str,
    confirm: bool = True,
    package_manager: str | None = None
) -> dict[str, Any]:
    """Install an MCP server from npm or PyPI.

    **IMPORTANT:** This tool will execute system commands. User confirmation
    is required unless confirm=False is explicitly set.

    The installation workflow:
    1. Check if server is already installed
    2. Validate server exists in registry
    3. Request confirmation (if confirm=True)
    4. Execute installation via package manager
    5. Return installation result

    Args:
        server_id: Server identifier from registry
        confirm: Require user confirmation before installing (default: True)
        package_manager: Override package manager (npm, pip, pipx, uvx)

    Returns:
        Dictionary with:
        - server_id: Server identifier
        - status: "installed", "already_installed", "confirmation_required", or "error"
        - installed_version: Version if successful
        - installation_command: Command that was executed
        - error_message: Error details if failed
        - message: Human-readable message

    Raises:
        ValueError: If server_id not found or server doesn't support installation

    Example:
        >>> # Check what would be installed
        >>> result = await install_server("filesystem")
        >>> # Returns: {"status": "confirmation_required", ...}

        >>> # Actually install
        >>> result = await install_server("filesystem", confirm=False)
        >>> # Returns: {"status": "installed", ...}
    """
    from mcp_orchestrator.installation.installer import ServerInstaller
    from mcp_orchestrator.installation.validator import InstallationValidator
    from mcp_orchestrator.servers.models import PackageManager

    # Get server from registry
    try:
        server = _server_registry.get(server_id)
    except ServerNotFoundError as e:
        raise ValueError(str(e)) from e

    # Check if already installed
    validator = InstallationValidator()
    check_result = validator.check_installation(server)

    if check_result.status == "installed":
        return {
            "server_id": server_id,
            "status": "already_installed",
            "installed_version": check_result.installed_version,
            "install_location": check_result.install_location
        }

    # Determine package manager
    if package_manager:
        pm = PackageManager(package_manager)
    else:
        pm = server.package_manager

    # Get package name
    if pm == PackageManager.NPM and server.npm_package:
        package_name = server.npm_package
    elif pm in [PackageManager.PIP, PackageManager.PIPX, PackageManager.UVX] and server.pypi_package:
        package_name = server.pypi_package
    else:
        raise ValueError(
            f"Server '{server_id}' does not support package manager '{pm.value}'"
        )

    # Require confirmation in production
    if confirm:
        from mcp_orchestrator.installation.package_manager import PackageManagerDetector
        cmd = PackageManagerDetector.get_install_command(pm, package_name)
        return {
            "server_id": server_id,
            "status": "confirmation_required",
            "message": f"Ready to install {package_name} via {pm.value}. "
                      f"Call install_server(server_id='{server_id}', confirm=False) to proceed.",
            "installation_command": " ".join(cmd)
        }

    # Execute installation
    installer = ServerInstaller()
    result = installer.install(
        package_manager=pm,
        package_name=package_name,
        server_id=server_id
    )

    return result.model_dump()


@mcp.tool()
async def list_installed_servers() -> dict[str, Any]:
    """List all MCP servers and their installation status.

    Checks all servers in the registry and returns their installation status,
    including version information for installed servers.

    Returns:
        Dictionary with:
        - servers: List of server installation statuses
          - server_id: Server identifier
          - display_name: Human-readable name
          - status: Installation status
          - installed_version: Version if installed
          - package_manager: Package manager used
        - installed_count: Number of installed servers
        - not_installed_count: Number of not installed servers
        - total_count: Total servers in registry

    Example:
        >>> result = await list_installed_servers()
        >>> # Returns: {"installed_count": 3, "not_installed_count": 12, ...}
    """
    from mcp_orchestrator.installation.validator import InstallationValidator

    servers = _server_registry.list_all()
    validator = InstallationValidator()

    results = []
    installed_count = 0
    not_installed_count = 0

    for server in servers:
        check_result = validator.check_installation(server)

        if check_result.status == "installed":
            installed_count += 1
        elif check_result.status == "not_installed":
            not_installed_count += 1

        results.append({
            "server_id": server.server_id,
            "display_name": server.display_name,
            "status": check_result.status.value,
            "installed_version": check_result.installed_version,
            "package_manager": server.package_manager.value if server.package_manager else None
        })

    return {
        "servers": results,
        "installed_count": installed_count,
        "not_installed_count": not_installed_count,
        "total_count": len(servers)
    }


# =============================================================================
# ENTRY POINT
# =============================================================================


def main() -> None:
    """Run the MCP orchestration server."""
    mcp.run()


if __name__ == "__main__":
    main()
