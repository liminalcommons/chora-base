"""
Pydantic models for HTTP API request/response schemas.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# Client models
class Client(BaseModel):
    """MCP client information."""

    client_id: str = Field(..., description="Unique client identifier (e.g., 'claude-desktop')")
    display_name: str = Field(..., description="Human-readable client name")
    config_path: str = Field(..., description="Path to client's MCP configuration file")
    platform: str = Field(..., description="Operating system platform")


class ClientsResponse(BaseModel):
    """Response for GET /v1/clients."""

    clients: List[Client] = Field(..., description="List of discovered MCP clients")


class ProfilesResponse(BaseModel):
    """Response for GET /v1/clients/{client_id}/profiles."""

    profiles: List[str] = Field(..., description="List of profile names for the client")


# Config models
class ConfigResponse(BaseModel):
    """Response for GET /v1/config/{client_id}/{profile}."""

    # Config is a dict with arbitrary structure (MCP config format)
    # We use model_config to allow arbitrary types
    model_config = {"extra": "allow"}


class DiffConfigRequest(BaseModel):
    """Request for POST /v1/config/diff."""

    config1: Dict[str, Any] = Field(..., description="First configuration to compare")
    config2: Dict[str, Any] = Field(..., description="Second configuration to compare")


class DiffConfigResponse(BaseModel):
    """Response for POST /v1/config/diff."""

    added: List[str] = Field(default_factory=list, description="Server IDs added in config2")
    removed: List[str] = Field(default_factory=list, description="Server IDs removed from config1")
    modified: List[str] = Field(default_factory=list, description="Server IDs with modified parameters")
    diff: Optional[str] = Field(None, description="Human-readable diff summary")


# Draft config models
class DraftAddRequest(BaseModel):
    """Request for POST /v1/config/{client_id}/{profile}/draft/add."""

    server_id: str = Field(..., description="Server ID to add to draft configuration")
    params: Dict[str, Any] = Field(default_factory=dict, description="Server-specific parameters")


class DraftAddResponse(BaseModel):
    """Response for POST /v1/config/{client_id}/{profile}/draft/add."""

    success: bool = Field(..., description="Whether the operation succeeded")
    message: Optional[str] = Field(None, description="Success or error message")
    draft: Optional[Dict[str, Any]] = Field(None, description="Current draft configuration")


class DraftRemoveRequest(BaseModel):
    """Request for POST /v1/config/{client_id}/{profile}/draft/remove."""

    server_id: str = Field(..., description="Server ID to remove from draft configuration")


class DraftRemoveResponse(BaseModel):
    """Response for POST /v1/config/{client_id}/{profile}/draft/remove."""

    success: bool = Field(..., description="Whether the operation succeeded")
    message: Optional[str] = Field(None, description="Success or error message")


# Validation models
class ValidateConfigResponse(BaseModel):
    """Response for POST /v1/config/{client_id}/{profile}/validate."""

    valid: bool = Field(..., description="Whether the configuration is valid")
    errors: List[str] = Field(default_factory=list, description="Validation errors (if any)")


# Publish models
class PublishConfigResponse(BaseModel):
    """Response for POST /v1/config/{client_id}/{profile}/publish."""

    success: bool = Field(..., description="Whether publishing succeeded")
    artifact_id: Optional[str] = Field(None, description="SHA-256 hash of published artifact")
    message: Optional[str] = Field(None, description="Success or error message")


# Deploy models
class DeployConfigResponse(BaseModel):
    """Response for POST /v1/config/{client_id}/{profile}/deploy."""

    success: bool = Field(..., description="Whether deployment succeeded")
    message: Optional[str] = Field(None, description="Success or error message")
    deployed: Optional[str] = Field(None, description="Path where config was deployed")


# Server registry models
class Server(BaseModel):
    """MCP server information."""

    server_id: str = Field(..., description="Unique server identifier")
    description: str = Field(..., description="Human-readable server description")
    transport: str = Field(..., description="Transport type (stdio, sse, etc.)")
    npm_package: Optional[str] = Field(None, description="NPM package name (if applicable)")
    command: Optional[str] = Field(None, description="Command to run the server")
    args: Optional[List[str]] = Field(None, description="Command arguments")
    env: Optional[Dict[str, str]] = Field(None, description="Environment variables")


class ServersResponse(BaseModel):
    """Response for GET /v1/servers."""

    servers: List[Server] = Field(..., description="List of available MCP servers")


class ServerDetailResponse(BaseModel):
    """Response for GET /v1/servers/{server_id}."""

    server_id: str = Field(..., description="Unique server identifier")
    description: str = Field(..., description="Human-readable server description")
    transport: str = Field(..., description="Transport type")
    npm_package: Optional[str] = Field(None, description="NPM package name")
    command: Optional[str] = Field(None, description="Command to run the server")
    args: Optional[List[str]] = Field(None, description="Command arguments")
    env: Optional[Dict[str, str]] = Field(None, description="Environment variables")
    # Additional metadata
    model_config = {"extra": "allow"}


# Key management models
class InitializeKeysResponse(BaseModel):
    """Response for POST /v1/keys/initialize."""

    success: bool = Field(..., description="Whether key initialization succeeded")
    message: str = Field(..., description="Success or error message")
    keys: Optional[Dict[str, str]] = Field(None, description="Paths to generated keys")


# Error models
class ErrorResponse(BaseModel):
    """Standard error response."""

    detail: str = Field(..., description="Error message")
    error_type: Optional[str] = Field(None, description="Type of error")
