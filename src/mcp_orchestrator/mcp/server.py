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
- 2 tools: add_server_to_config, remove_server_from_config
- 1 resource: config://{client_id}/{profile_id}/draft
"""

import json
from typing import Any

from fastmcp import FastMCP

from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.diff import compare_configs
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


# =============================================================================
# TOOLS (8 - Wave 1.0: 4, Wave 1.1: 2, Wave 1.2: 2)
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
                "transport": server.transport.value,
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
    transport_info = {"type": server.transport.value}

    if server.transport.value == "stdio":
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
    if server.transport.value == "stdio":
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
    client_id: str,
    profile_id: str,
    server_id: str,
    params: dict[str, Any] | None = None,
    env_vars: dict[str, str] | None = None,
    server_name: str | None = None,
) -> dict[str, Any]:
    """Add a server to the draft configuration.

    Adds an MCP server to the draft configuration for a client/profile.
    Automatically handles stdio vs HTTP/SSE transport (HTTP/SSE servers are
    wrapped with mcp-remote transparently).

    Args:
        client_id: Client family identifier (e.g., 'claude-desktop')
        profile_id: Profile identifier (e.g., 'default', 'dev')
        server_id: Server identifier from registry (use list_available_servers)
        params: Parameter values (e.g., {"path": "/Users/me/Documents"})
        env_vars: Environment variables (e.g., {"GITHUB_TOKEN": "ghp_..."})
        server_name: Name to use in config (defaults to server_id)

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
        ...     client_id="claude-desktop",
        ...     profile_id="default",
        ...     server_id="filesystem",
        ...     params={"path": "/Users/me/Documents"}
        ... )
        >>> # Draft now contains filesystem server config
    """
    try:
        # Get or create builder
        builder = _get_builder(client_id, profile_id)

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
    client_id: str, profile_id: str, server_name: str
) -> dict[str, Any]:
    """Remove a server from the draft configuration.

    Removes an MCP server from the draft configuration for a client/profile.

    Args:
        client_id: Client family identifier
        profile_id: Profile identifier
        server_name: Name of server in config (use add_server_to_config result)

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
        ...     client_id="claude-desktop",
        ...     profile_id="default",
        ...     server_name="filesystem"
        ... )
        >>> # Server removed from draft
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


# =============================================================================
# RESOURCES (5 - Wave 1.0: 2, Wave 1.1: 2, Wave 1.2: 1)
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
        "version": "0.1.1",
        "wave": "Wave 1.1: Server Registry",
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
            ],
            "resources": [
                # Wave 1.0
                "capabilities://server",
                "capabilities://clients",
                # Wave 1.1
                "server://registry",
                "server://{server_id}",
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
# ENTRY POINT
# =============================================================================


def main() -> None:
    """Run the MCP orchestration server."""
    mcp.run()


if __name__ == "__main__":
    main()
