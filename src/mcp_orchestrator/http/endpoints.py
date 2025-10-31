"""
HTTP endpoint handlers for MCP orchestration API.

Maps HTTP endpoints to underlying MCP tools.
"""

import json
from typing import Any

from fastapi import HTTPException

# Import MCP tools from the MCP server module
# These are async functions that implement the actual MCP tool logic
from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.crypto.signing import SigningError
from mcp_orchestrator.deployment import DeploymentError, DeploymentWorkflow
from mcp_orchestrator.deployment.log import DeploymentLog
from mcp_orchestrator.diff import compare_configs
from mcp_orchestrator.publishing import PublishingWorkflow, ValidationError
from mcp_orchestrator.registry import get_default_registry
from mcp_orchestrator.servers import get_default_registry as get_server_registry
from mcp_orchestrator.servers.registry import ServerNotFoundError
from mcp_orchestrator.storage import ArtifactStore, StorageError

from .models import *

# Global state (matching MCP server pattern)
_registry = get_default_registry()  # Client registry
_server_registry = get_server_registry()  # Server registry
_store = ArtifactStore()  # Artifact storage
_builders: dict[str, ConfigBuilder] = {}  # Draft config builders
_deployment_log = DeploymentLog(deployments_dir=str(_store.base_path / "deployments"))


# =============================================================================
# CLIENT ENDPOINTS
# =============================================================================


async def list_clients_endpoint() -> ClientsResponse:
    """
    GET /v1/clients

    List all discovered MCP clients.
    """
    # Get clients from registry
    registry_clients = _registry.list_clients()

    # Build response with client metadata
    clients = []
    for client_def in registry_clients:
        # Get profile IDs from registry
        [p.profile_id for p in client_def.default_profiles]

        clients.append(
            Client(
                client_id=client_def.client_id,
                display_name=client_def.display_name,
                config_path=client_def.config_location,
                platform=client_def.platform,
            )
        )

    return ClientsResponse(clients=clients)


async def list_profiles_endpoint(client_id: str) -> ProfilesResponse:
    """
    GET /v1/clients/{client_id}/profiles

    List all profiles for a specific client.
    """
    try:
        client_def = _registry.get_client(client_id)
        if client_def is None:
            raise HTTPException(
                status_code=404, detail=f"Client '{client_id}' not found"
            )
        profile_ids = [p.profile_id for p in client_def.default_profiles]
        return ProfilesResponse(profiles=profile_ids)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Client '{client_id}' not found")


# =============================================================================
# CONFIG ENDPOINTS
# =============================================================================


async def get_config_endpoint(client_id: str, profile: str) -> dict[str, Any]:
    """
    GET /v1/config/{client_id}/{profile}

    Get current configuration for a client/profile.
    """
    # Get builder key
    builder_key = f"{client_id}/{profile}"

    # Check if there's a draft config
    if builder_key in _builders:
        # Return draft config
        builder = _builders[builder_key]
        config = builder.build()
        return config

    # Otherwise, try to get deployed config
    try:
        deployment = _deployment_log.get_latest_deployment(client_id, profile)
        if deployment and deployment.status == "completed":
            # Load config from deployed path
            import pathlib

            config_path = pathlib.Path(deployment.deployed_path)
            if config_path.exists():
                config = json.loads(config_path.read_text())
                return config
    except Exception:
        pass

    # No config found
    raise HTTPException(
        status_code=404, detail=f"No configuration found for {client_id}/{profile}"
    )


async def diff_config_endpoint(request: DiffConfigRequest) -> DiffConfigResponse:
    """
    POST /v1/config/diff

    Compare two configurations and return differences.
    """
    try:
        diff_result = compare_configs(request.config1, request.config2)

        # Parse diff result (DiffResult object with servers_added/removed/modified fields)
        # Extract modified server IDs from servers_modified list
        modified = [
            m["server_id"] if isinstance(m, dict) else m.get("server_id", "unknown")
            for m in diff_result.servers_modified
        ]

        return DiffConfigResponse(
            added=diff_result.servers_added,
            removed=diff_result.servers_removed,
            modified=modified,
            diff=f"{diff_result.status}: {diff_result.total_changes} changes",
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to compare configs: {str(e)}"
        )


# =============================================================================
# DRAFT CONFIG ENDPOINTS
# =============================================================================


async def draft_add_endpoint(
    client_id: str, profile: str, request: DraftAddRequest
) -> DraftAddResponse:
    """
    POST /v1/config/{client_id}/{profile}/draft/add

    Add a server to draft configuration.
    """
    builder_key = f"{client_id}/{profile}"

    # Get or create builder
    if builder_key not in _builders:
        _builders[builder_key] = ConfigBuilder(client_id=client_id, profile_id=profile)

    builder = _builders[builder_key]

    try:
        # Get server from registry
        server = _server_registry.get(request.server_id)

        # Add server to draft
        builder.add_server(server, **request.params)

        # Build draft config
        draft_config = builder.build()

        return DraftAddResponse(
            success=True,
            message=f"Added {request.server_id} to draft configuration",
            draft=draft_config,
        )
    except ServerNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Server '{request.server_id}' not found"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to add server: {str(e)}")


async def draft_remove_endpoint(
    client_id: str, profile: str, request: DraftRemoveRequest
) -> DraftRemoveResponse:
    """
    POST /v1/config/{client_id}/{profile}/draft/remove

    Remove a server from draft configuration.
    """
    builder_key = f"{client_id}/{profile}"

    if builder_key not in _builders:
        raise HTTPException(status_code=404, detail="No draft configuration found")

    builder = _builders[builder_key]

    try:
        builder.remove_server(request.server_id)

        return DraftRemoveResponse(
            success=True,
            message=f"Removed {request.server_id} from draft configuration",
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to remove server: {str(e)}"
        )


async def draft_view_endpoint(client_id: str, profile: str) -> dict[str, Any]:
    """
    GET /v1/config/{client_id}/{profile}/draft

    View current draft configuration.
    """
    builder_key = f"{client_id}/{profile}"

    if builder_key not in _builders:
        raise HTTPException(status_code=404, detail="No draft configuration found")

    builder = _builders[builder_key]
    draft_config = builder.build()

    return draft_config


async def draft_clear_endpoint(client_id: str, profile: str) -> dict[str, Any]:
    """
    DELETE /v1/config/{client_id}/{profile}/draft

    Clear draft configuration.
    """
    builder_key = f"{client_id}/{profile}"

    if builder_key in _builders:
        del _builders[builder_key]

    return {"success": True, "message": "Draft configuration cleared"}


# =============================================================================
# CONFIG WORKFLOW ENDPOINTS
# =============================================================================


async def validate_config_endpoint(
    client_id: str, profile: str
) -> ValidateConfigResponse:
    """
    POST /v1/config/{client_id}/{profile}/validate

    Validate draft configuration.
    """
    builder_key = f"{client_id}/{profile}"

    if builder_key not in _builders:
        raise HTTPException(status_code=404, detail="No draft configuration found")

    builder = _builders[builder_key]

    try:
        # Validate configuration
        # The builder automatically validates, so if build() succeeds, it's valid
        builder.build()

        # Additional validation logic can be added here
        errors = []

        return ValidateConfigResponse(valid=True, errors=errors)
    except Exception as e:
        return ValidateConfigResponse(valid=False, errors=[str(e)])


async def publish_config_endpoint(
    client_id: str, profile: str
) -> PublishConfigResponse:
    """
    POST /v1/config/{client_id}/{profile}/publish

    Publish draft configuration (sign and store artifact).
    """
    builder_key = f"{client_id}/{profile}"

    if builder_key not in _builders:
        raise HTTPException(status_code=404, detail="No draft configuration found")

    builder = _builders[builder_key]

    try:
        # Create publishing workflow (needs client_registry)
        workflow = PublishingWorkflow(store=_store, client_registry=_registry)

        # Publish configuration
        # This signs the config and stores it as an artifact
        artifact_id = workflow.publish(
            builder=builder,
            private_key_path=str(_store.base_path / "keys" / "signing.key"),
            signing_key_id="default",
        )

        return PublishConfigResponse(
            success=True,
            artifact_id=artifact_id,
            message="Configuration published successfully",
        )
    except (ValidationError, SigningError, StorageError) as e:
        # Return detailed error
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError:
        raise HTTPException(
            status_code=400,
            detail="Signing keys not found. Run initialize_keys first.",
        )


async def deploy_config_endpoint(client_id: str, profile: str) -> DeployConfigResponse:
    """
    POST /v1/config/{client_id}/{profile}/deploy

    Deploy published configuration to client.
    """
    try:
        # Create deployment workflow
        workflow = DeploymentWorkflow(
            store=_store,
            deployment_log=_deployment_log,
        )

        # Deploy latest published config
        result = workflow.deploy(client_id=client_id, profile_id=profile)

        return DeployConfigResponse(
            success=True,
            message="Configuration deployed successfully",
            deployed=result.get("deployed_path"),
        )
    except DeploymentError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # No published config found
        raise HTTPException(
            status_code=404, detail=f"No published configuration found: {str(e)}"
        )


# =============================================================================
# SERVER REGISTRY ENDPOINTS
# =============================================================================


async def list_servers_endpoint() -> ServersResponse:
    """
    GET /v1/servers

    List all available MCP servers from registry.
    """
    servers_data = _server_registry.list_all()  # Returns list[ServerDefinition]

    servers = []
    for server_def in servers_data:
        # Convert ServerDefinition (Pydantic model) to Server response model
        servers.append(
            Server(
                server_id=server_def.server_id,
                description=server_def.description,
                transport=server_def.transport.value
                if hasattr(server_def.transport, "value")
                else str(server_def.transport),
                npm_package=server_def.npm_package
                if hasattr(server_def, "npm_package")
                else None,
                command=server_def.command if hasattr(server_def, "command") else None,
                args=server_def.args if hasattr(server_def, "args") else None,
                env=server_def.env if hasattr(server_def, "env") else None,
            )
        )

    return ServersResponse(servers=servers)


async def describe_server_endpoint(server_id: str) -> ServerDetailResponse:
    """
    GET /v1/servers/{server_id}

    Get detailed information about a specific server.
    """
    try:
        server_def = _server_registry.get(server_id)  # Returns ServerDefinition

        # Convert ServerDefinition to ServerDetailResponse
        return ServerDetailResponse(
            server_id=server_def.server_id,
            description=server_def.description,
            transport=server_def.transport.value
            if hasattr(server_def.transport, "value")
            else str(server_def.transport),
            npm_package=server_def.npm_package
            if hasattr(server_def, "npm_package")
            else None,
            command=server_def.command if hasattr(server_def, "command") else None,
            args=server_def.args if hasattr(server_def, "args") else None,
            env=server_def.env if hasattr(server_def, "env") else None,
        )
    except ServerNotFoundError:
        raise HTTPException(status_code=404, detail=f"Server '{server_id}' not found")


# =============================================================================
# KEY MANAGEMENT ENDPOINTS
# =============================================================================


async def initialize_keys_endpoint() -> InitializeKeysResponse:
    """
    POST /v1/keys/initialize

    Initialize cryptographic signing keys.
    """
    try:
        from mcp_orchestrator.crypto.signing import SigningService

        # Initialize signing service
        signing_service = SigningService(keys_dir=str(_store.base_path / "keys"))

        # Check if keys already exist
        if signing_service.has_keys():
            raise HTTPException(
                status_code=400, detail="Signing keys already initialized"
            )

        # Generate keys
        key_paths = signing_service.generate_keypair()

        return InitializeKeysResponse(
            success=True,
            message="Signing keys initialized successfully",
            keys={
                "private_key": str(key_paths["private_key"]),
                "public_key": str(key_paths["public_key"]),
            },
        )
    except FileExistsError:
        raise HTTPException(status_code=400, detail="Signing keys already exist")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to initialize keys: {str(e)}"
        )
