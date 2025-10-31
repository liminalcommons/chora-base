"""
FastAPI HTTP server for MCP orchestration.

Exposes all 10 MCP tools via HTTP REST API with authentication and CORS.
"""

from typing import Any

import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .auth import AuthenticationService, get_auth_service
from .endpoints import *


def create_app(auth_service: AuthenticationService | None = None) -> FastAPI:
    """
    Create FastAPI application with all endpoints and middleware.

    Args:
        auth_service: Optional authentication service. If None, uses global singleton.

    Returns:
        Configured FastAPI application
    """
    # Create FastAPI app
    app = FastAPI(
        title="MCP Orchestration HTTP API",
        version="0.2.0",
        description="Centralized MCP configuration orchestration via HTTP",
        docs_url="/docs",
        openapi_url="/openapi.json",
    )

    # Get auth service (use provided or global singleton)
    if auth_service is None:
        auth_service = get_auth_service()

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for flexibility
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods (GET, POST, DELETE, OPTIONS)
        allow_headers=["*"],  # Allow all headers
    )

    # Authentication dependency
    async def verify_auth(
        authorization: str | None = Header(None),
        x_api_key: str | None = Header(None),
    ) -> None:
        """
        Verify authentication (bearer token or API key).

        Raises:
            HTTPException: 401 if authentication fails
        """
        # Try bearer token first
        if authorization:
            # Extract token from "Bearer <token>"
            if authorization.startswith("Bearer "):
                token = authorization[7:]  # Remove "Bearer " prefix
                if auth_service.validate_token(token):
                    return  # Authenticated

        # Try API key
        if x_api_key:
            if auth_service.validate_api_key(x_api_key):
                return  # Authenticated

        # No valid authentication provided
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Provide bearer token (Authorization: Bearer <token>) or API key (X-API-Key: <key>)",
        )

    # Store auth service in app state for access in endpoints
    app.state.auth_service = auth_service

    # =============================================================================
    # CLIENT ENDPOINTS
    # =============================================================================

    @app.get(
        "/v1/clients",
        response_model=ClientsResponse,
        tags=["Clients"],
        summary="List all MCP clients",
    )
    async def list_clients(auth: None = Depends(verify_auth)):
        """List all discovered MCP clients (Claude Desktop, Cursor, etc.)."""
        return await list_clients_endpoint()

    @app.get(
        "/v1/clients/{client_id}/profiles",
        response_model=ProfilesResponse,
        tags=["Clients"],
        summary="List profiles for a client",
    )
    async def list_profiles(client_id: str, auth: None = Depends(verify_auth)):
        """List all profiles for a specific client."""
        return await list_profiles_endpoint(client_id)

    # =============================================================================
    # CONFIG ENDPOINTS
    # =============================================================================

    @app.get(
        "/v1/config/{client_id}/{profile}",
        response_model=dict[str, Any],
        tags=["Configuration"],
        summary="Get configuration",
    )
    async def get_config(
        client_id: str, profile: str, auth: None = Depends(verify_auth)
    ):
        """Get current configuration for a client/profile."""
        return await get_config_endpoint(client_id, profile)

    @app.post(
        "/v1/config/diff",
        response_model=DiffConfigResponse,
        tags=["Configuration"],
        summary="Compare two configurations",
    )
    async def diff_config(
        request: DiffConfigRequest, auth: None = Depends(verify_auth)
    ):
        """Compare two configurations and return differences."""
        return await diff_config_endpoint(request)

    # =============================================================================
    # DRAFT CONFIG ENDPOINTS
    # =============================================================================

    @app.post(
        "/v1/config/{client_id}/{profile}/draft/add",
        response_model=DraftAddResponse,
        tags=["Draft Configuration"],
        summary="Add server to draft",
    )
    async def draft_add(
        client_id: str,
        profile: str,
        request: DraftAddRequest,
        auth: None = Depends(verify_auth),
    ):
        """Add a server to draft configuration."""
        return await draft_add_endpoint(client_id, profile, request)

    @app.post(
        "/v1/config/{client_id}/{profile}/draft/remove",
        response_model=DraftRemoveResponse,
        tags=["Draft Configuration"],
        summary="Remove server from draft",
    )
    async def draft_remove(
        client_id: str,
        profile: str,
        request: DraftRemoveRequest,
        auth: None = Depends(verify_auth),
    ):
        """Remove a server from draft configuration."""
        return await draft_remove_endpoint(client_id, profile, request)

    @app.get(
        "/v1/config/{client_id}/{profile}/draft",
        response_model=dict[str, Any],
        tags=["Draft Configuration"],
        summary="View draft configuration",
    )
    async def draft_view(
        client_id: str, profile: str, auth: None = Depends(verify_auth)
    ):
        """View current draft configuration."""
        return await draft_view_endpoint(client_id, profile)

    @app.delete(
        "/v1/config/{client_id}/{profile}/draft",
        response_model=dict[str, Any],
        tags=["Draft Configuration"],
        summary="Clear draft configuration",
    )
    async def draft_clear(
        client_id: str, profile: str, auth: None = Depends(verify_auth)
    ):
        """Clear draft configuration."""
        return await draft_clear_endpoint(client_id, profile)

    # =============================================================================
    # CONFIG WORKFLOW ENDPOINTS
    # =============================================================================

    @app.post(
        "/v1/config/{client_id}/{profile}/validate",
        response_model=ValidateConfigResponse,
        tags=["Configuration Workflow"],
        summary="Validate configuration",
    )
    async def validate_config(
        client_id: str, profile: str, auth: None = Depends(verify_auth)
    ):
        """Validate draft configuration."""
        return await validate_config_endpoint(client_id, profile)

    @app.post(
        "/v1/config/{client_id}/{profile}/publish",
        response_model=PublishConfigResponse,
        tags=["Configuration Workflow"],
        summary="Publish configuration",
    )
    async def publish_config(
        client_id: str, profile: str, auth: None = Depends(verify_auth)
    ):
        """Publish draft configuration (sign and store artifact)."""
        return await publish_config_endpoint(client_id, profile)

    @app.post(
        "/v1/config/{client_id}/{profile}/deploy",
        response_model=DeployConfigResponse,
        tags=["Configuration Workflow"],
        summary="Deploy configuration",
    )
    async def deploy_config(
        client_id: str, profile: str, auth: None = Depends(verify_auth)
    ):
        """Deploy published configuration to client."""
        return await deploy_config_endpoint(client_id, profile)

    # =============================================================================
    # SERVER REGISTRY ENDPOINTS
    # =============================================================================

    @app.get(
        "/v1/servers",
        response_model=ServersResponse,
        tags=["Server Registry"],
        summary="List all available servers",
    )
    async def list_servers(auth: None = Depends(verify_auth)):
        """List all available MCP servers from registry."""
        return await list_servers_endpoint()

    @app.get(
        "/v1/servers/{server_id}",
        response_model=ServerDetailResponse,
        tags=["Server Registry"],
        summary="Get server details",
    )
    async def describe_server(server_id: str, auth: None = Depends(verify_auth)):
        """Get detailed information about a specific server."""
        return await describe_server_endpoint(server_id)

    # =============================================================================
    # KEY MANAGEMENT ENDPOINTS
    # =============================================================================

    @app.post(
        "/v1/keys/initialize",
        response_model=InitializeKeysResponse,
        tags=["Key Management"],
        summary="Initialize signing keys",
    )
    async def initialize_keys(auth: None = Depends(verify_auth)):
        """Initialize cryptographic signing keys."""
        return await initialize_keys_endpoint()

    # =============================================================================
    # ERROR HANDLERS
    # =============================================================================

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc: HTTPException):
        """Handle HTTP exceptions with consistent error format."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "error_type": type(exc).__name__},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request, exc: Exception):
        """Handle unexpected exceptions."""
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "error_type": type(exc).__name__,
            },
        )

    return app


class HTTPTransportServer:
    """
    HTTP transport server for MCP orchestration.

    Wraps FastAPI application with lifecycle management.
    """

    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8000,
        auth_service: AuthenticationService | None = None,
    ):
        """
        Initialize HTTP server.

        Args:
            host: Server bind address
            port: Server port
            auth_service: Optional authentication service
        """
        self.host = host
        self.port = port
        self.auth_service = auth_service or get_auth_service()
        self.app = create_app(self.auth_service)
        self.running = False
        self._server = None

    async def start(self) -> None:
        """
        Start HTTP server.

        Raises:
            RuntimeError: If server is already running
        """
        if self.running:
            raise RuntimeError("Server is already running")

        self.running = True

        # Note: For production, use uvicorn.Server with async run
        # For testing, FastAPI TestClient is used
        # This method is primarily for programmatic server control

    async def stop(self) -> None:
        """Stop HTTP server gracefully."""
        self.running = False
        # Cleanup logic would go here

    def health_check(self) -> dict[str, Any]:
        """
        Get server health status.

        Returns:
            Dict with status and running state
        """
        if self.running:
            return {"status": "healthy", "running": True}
        else:
            return {"status": "unhealthy", "running": False}

    def run(self, **uvicorn_kwargs) -> None:
        """
        Run server using uvicorn (blocking).

        Args:
            **uvicorn_kwargs: Additional arguments to pass to uvicorn.run
        """
        print(f"Starting HTTP server on http://{self.host}:{self.port}")
        print(f"API docs: http://{self.host}:{self.port}/docs")
        print(f"OpenAPI schema: http://{self.host}:{self.port}/openapi.json")

        self.running = True

        try:
            uvicorn.run(
                self.app,
                host=self.host,
                port=self.port,
                **uvicorn_kwargs,
            )
        finally:
            self.running = False
            print("Server shut down gracefully")
