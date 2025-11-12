# SAP-043: Multi-Interface Capability Servers - Protocol Specification

**SAP ID**: SAP-043
**Version**: 1.0.0
**Last Updated**: 2025-11-12
**Compliance**: MCP 2024-11-05, OpenAPI 3.0, Click 8.x, FastMCP 0.2+

---

## Overview

This document provides the complete technical specification for implementing capability servers with four standardized interfaces: **Native API** (Python), **CLI** (Click), **REST** (FastAPI), and **MCP** (FastMCP). It defines the architecture, contracts, implementation patterns, and testing strategies required for consistent multi-interface capability servers.

**Scope**: Python-based capability servers following SAP-042 (InterfaceDesign) and SAP-043 (MultiInterface) patterns.

**Audience**: Developers implementing capability servers, AI agents generating code, architecture reviewers.

---

## Table of Contents

1. [Architecture Specification](#architecture-specification)
2. [Core Module Specification](#core-module-specification)
3. [Native API Specification](#native-api-specification)
4. [CLI Specification](#cli-specification)
5. [REST API Specification](#rest-api-specification)
6. [MCP Specification](#mcp-specification)
7. [Error Handling Specification](#error-handling-specification)
8. [Testing Specification](#testing-specification)
9. [Deployment Specification](#deployment-specification)
10. [Code Examples](#code-examples)

---

## Architecture Specification

### Directory Structure

```
capability-server/
├── core/                      # Core business logic (interface-agnostic)
│   ├── __init__.py
│   ├── service.py            # Main service class
│   ├── models.py             # Domain models (dataclasses)
│   ├── exceptions.py         # Domain exceptions
│   ├── repository.py         # Data access (if needed)
│   └── validators.py         # Validation logic
│
├── api/                       # Interface adapters
│   ├── __init__.py
│   ├── native.py             # Native Python API (re-exports core)
│   ├── cli.py                # CLI adapter (Click)
│   ├── http.py               # REST API adapter (FastAPI)
│   └── mcp.py                # MCP adapter (FastMCP)
│
├── tests/                     # Testing
│   ├── __init__.py
│   ├── test_core.py          # Core logic tests
│   ├── test_cli.py           # CLI adapter tests
│   ├── test_http.py          # REST API tests
│   ├── test_mcp.py           # MCP tool tests
│   └── test_consistency.py  # Cross-interface consistency tests
│
├── pyproject.toml            # Dependencies
├── README.md                 # Documentation
└── AGENTS.md                 # Agent guidance
```

### Layered Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    CLIENT APPLICATIONS                        │
│  (Python scripts, Shell, HTTP clients, AI assistants)         │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────┴─────────────────────────────────────┐
│                   INTERFACE ADAPTERS                          │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ ┌──────┐ │
│  │   Native    │  │     CLI     │  │  REST API   │ │  MCP │ │
│  │ (Python)    │  │   (Click)   │  │  (FastAPI)  │ │(Fast)│ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ └───┬──┘ │
│         │                │                │            │     │
│         └────────────────┴────────────────┴────────────┘     │
│                            │                                  │
└────────────────────────────┼──────────────────────────────────┘
                             │
┌────────────────────────────┴──────────────────────────────────┐
│                      CORE BUSINESS LOGIC                       │
│  (Interface-agnostic, no Flask/Click/FastMCP imports)          │
│                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Service    │  │    Models    │  │  Validators  │       │
│  │   Classes    │  │ (Dataclasses)│  │   (Pure)     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                                │
│  ┌──────────────┐  ┌──────────────┐                          │
│  │  Exceptions  │  │  Repository  │                          │
│  │   (Domain)   │  │  (Data)      │                          │
│  └──────────────┘  └──────────────┘                          │
└────────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┴──────────────────────────────────┐
│                     DATA LAYER                                 │
│  (Database, File System, External APIs)                        │
└────────────────────────────────────────────────────────────────┘
```

### Architectural Constraints

**Core Module Rules**:
1. ✅ MUST NOT import interface frameworks (Flask, FastAPI, Click, FastMCP)
2. ✅ MUST use only standard library + domain-specific deps (e.g., SQLAlchemy for DB)
3. ✅ MUST define domain exceptions (not HTTP exceptions, CLI exit codes, etc.)
4. ✅ MUST use interface-agnostic types (dict, list, dataclass, not Request/Response objects)
5. ✅ MUST be testable without any interface framework

**Interface Adapter Rules**:
1. ✅ MUST be thin (parse inputs, call core, format outputs)
2. ✅ MUST translate core exceptions to interface-specific errors
3. ✅ MUST NOT contain business logic (validation, computation, state management)
4. ✅ MUST call core for all operations
5. ✅ MUST handle interface-specific concerns only (CLI: colors, REST: status codes, MCP: JSON serialization)

---

## Core Module Specification

### Domain Models

**Pattern**: Use dataclasses for immutable domain objects.

```python
# core/models.py
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

@dataclass(frozen=True)
class Deployment:
    """Deployment domain model (immutable)."""
    env_id: str
    service: str
    replicas: int
    deployment_id: str = ""
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dict for interface adapters."""
        return {
            "deployment_id": self.deployment_id,
            "env_id": self.env_id,
            "service": self.service,
            "replicas": self.replicas,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags,
        }

@dataclass(frozen=True)
class Environment:
    """Environment domain model."""
    env_id: str
    name: str
    region: str
    created_at: datetime = field(default_factory=datetime.utcnow)
```

### Domain Exceptions

**Pattern**: Define domain-specific exceptions, not interface-specific.

```python
# core/exceptions.py

class DomainException(Exception):
    """Base exception for all domain errors."""
    def __init__(self, message: str, **kwargs):
        self.message = message
        self.context = kwargs
        super().__init__(message)

class ValidationError(DomainException):
    """Input validation failed."""
    def __init__(self, message: str, field: Optional[str] = None, **kwargs):
        super().__init__(message, field=field, **kwargs)
        self.field = field

class NotFoundError(DomainException):
    """Requested resource not found."""
    def __init__(self, resource_type: str, resource_id: str, **kwargs):
        message = f"{resource_type} not found: {resource_id}"
        super().__init__(message, resource_type=resource_type, resource_id=resource_id, **kwargs)

class ConflictError(DomainException):
    """Resource already exists or conflicts with existing state."""
    def __init__(self, message: str, existing_id: Optional[str] = None, **kwargs):
        super().__init__(message, existing_id=existing_id, **kwargs)

class OperationError(DomainException):
    """Operation failed (e.g., deployment failed, service unreachable)."""
    pass

class AuthorizationError(DomainException):
    """User not authorized to perform operation."""
    def __init__(self, operation: str, resource: str, **kwargs):
        message = f"Not authorized to {operation} {resource}"
        super().__init__(message, operation=operation, resource=resource, **kwargs)
```

### Service Layer

**Pattern**: Service class with all operations as methods.

```python
# core/service.py
from typing import List, Dict, Any, Optional
from .models import Deployment, Environment
from .exceptions import ValidationError, NotFoundError, ConflictError, OperationError
from .repository import DeploymentRepository, EnvironmentRepository
from .validators import validate_replicas, validate_service_name, validate_env_id

class OrchestratorService:
    """Orchestrator capability service (interface-agnostic)."""

    def __init__(
        self,
        deployment_repo: Optional[DeploymentRepository] = None,
        env_repo: Optional[EnvironmentRepository] = None,
    ):
        """Initialize service with repositories."""
        self.deployment_repo = deployment_repo or DeploymentRepository()
        self.env_repo = env_repo or EnvironmentRepository()

    def create_deployment(
        self,
        env_id: str,
        config: Dict[str, Any],
    ) -> Deployment:
        """Create deployment (core business logic).

        Args:
            env_id: Environment identifier
            config: Deployment configuration
                - service (str): Service name (required)
                - replicas (int): Replica count (required, >= 1)
                - tags (list[str]): Optional tags

        Returns:
            Created deployment object

        Raises:
            ValidationError: If config is invalid
            NotFoundError: If environment doesn't exist
            OperationError: If deployment creation fails
        """
        # Validate environment exists
        if not self.env_repo.exists(env_id):
            raise NotFoundError("Environment", env_id)

        # Validate required fields
        if "service" not in config:
            raise ValidationError("service is required", field="service")
        if "replicas" not in config:
            raise ValidationError("replicas is required", field="replicas")

        # Validate field values
        service = config["service"]
        replicas = config["replicas"]
        tags = config.get("tags", [])

        validate_service_name(service)  # Raises ValidationError if invalid
        validate_replicas(replicas)     # Raises ValidationError if invalid

        # Check for conflicts (duplicate service in env)
        if self.deployment_repo.exists_for_service(env_id, service):
            raise ConflictError(
                f"Service '{service}' already deployed in environment '{env_id}'",
                existing_id=f"{env_id}/{service}"
            )

        # Create deployment
        deployment = Deployment(
            env_id=env_id,
            service=service,
            replicas=replicas,
            deployment_id=f"deploy-{self._generate_id()}",
            status="pending",
            tags=tags,
        )

        # Persist deployment
        try:
            self.deployment_repo.create(deployment)
        except Exception as e:
            raise OperationError(f"Failed to create deployment: {e}")

        # Trigger deployment (async in production)
        try:
            self._trigger_deployment(deployment)
        except Exception as e:
            # Rollback deployment record
            self.deployment_repo.delete(deployment.deployment_id)
            raise OperationError(f"Failed to trigger deployment: {e}")

        return deployment

    def list_deployments(
        self,
        env_id: Optional[str] = None,
        status: Optional[str] = None,
        service: Optional[str] = None,
    ) -> List[Deployment]:
        """List deployments with optional filters.

        Args:
            env_id: Filter by environment
            status: Filter by status (pending, running, failed, completed)
            service: Filter by service name

        Returns:
            List of matching deployments
        """
        return self.deployment_repo.list(
            env_id=env_id,
            status=status,
            service=service,
        )

    def get_deployment(self, deployment_id: str) -> Deployment:
        """Get deployment by ID.

        Args:
            deployment_id: Deployment identifier

        Returns:
            Deployment object

        Raises:
            NotFoundError: If deployment doesn't exist
        """
        deployment = self.deployment_repo.get(deployment_id)
        if not deployment:
            raise NotFoundError("Deployment", deployment_id)
        return deployment

    def delete_deployment(self, deployment_id: str) -> None:
        """Delete deployment.

        Args:
            deployment_id: Deployment identifier

        Raises:
            NotFoundError: If deployment doesn't exist
            OperationError: If deletion fails
        """
        deployment = self.get_deployment(deployment_id)

        try:
            self._stop_deployment(deployment)
            self.deployment_repo.delete(deployment_id)
        except Exception as e:
            raise OperationError(f"Failed to delete deployment: {e}")

    # Private methods (implementation details)
    def _generate_id(self) -> str:
        """Generate unique ID."""
        import uuid
        return str(uuid.uuid4())[:8]

    def _trigger_deployment(self, deployment: Deployment) -> None:
        """Trigger deployment execution (stub for example)."""
        # In production: call container orchestrator, update status
        pass

    def _stop_deployment(self, deployment: Deployment) -> None:
        """Stop running deployment (stub for example)."""
        # In production: call container orchestrator to stop
        pass
```

### Validators

**Pattern**: Pure functions for validation logic.

```python
# core/validators.py
import re
from .exceptions import ValidationError

def validate_service_name(service: str) -> None:
    """Validate service name format.

    Raises:
        ValidationError: If service name is invalid
    """
    if not service or not service.strip():
        raise ValidationError("service cannot be empty", field="service")

    if not re.match(r'^[a-z][a-z0-9-]{0,62}$', service):
        raise ValidationError(
            "service must be lowercase alphanumeric with hyphens, 1-63 chars, start with letter",
            field="service"
        )

def validate_replicas(replicas: Any) -> None:
    """Validate replica count.

    Raises:
        ValidationError: If replicas is invalid
    """
    if not isinstance(replicas, int):
        raise ValidationError(
            f"replicas must be integer, got {type(replicas).__name__}",
            field="replicas"
        )

    if replicas < 1:
        raise ValidationError(
            "replicas must be >= 1",
            field="replicas"
        )

    if replicas > 100:
        raise ValidationError(
            "replicas must be <= 100 (contact support for higher limits)",
            field="replicas"
        )

def validate_env_id(env_id: str) -> None:
    """Validate environment ID format.

    Raises:
        ValidationError: If env_id is invalid
    """
    if not env_id or not env_id.strip():
        raise ValidationError("env_id cannot be empty", field="env_id")

    if not re.match(r'^[a-z][a-z0-9-]{0,31}$', env_id):
        raise ValidationError(
            "env_id must be lowercase alphanumeric with hyphens, 1-32 chars",
            field="env_id"
        )
```

---

## Native API Specification

### Export Pattern

**Goal**: Expose core directly for programmatic use.

```python
# api/native.py (or capability_server/__init__.py)
"""Native Python API for Orchestrator capability server."""

# Re-export core classes for direct use
from core.service import OrchestratorService
from core.models import Deployment, Environment
from core.exceptions import (
    DomainException,
    ValidationError,
    NotFoundError,
    ConflictError,
    OperationError,
    AuthorizationError,
)

# Convenience imports
from core.repository import DeploymentRepository, EnvironmentRepository

__all__ = [
    "OrchestratorService",
    "Deployment",
    "Environment",
    "ValidationError",
    "NotFoundError",
    "ConflictError",
    "OperationError",
    "AuthorizationError",
    "DeploymentRepository",
    "EnvironmentRepository",
]

__version__ = "1.0.0"
```

### Usage Example

```python
# User code
from orchestrator import OrchestratorService, ValidationError

service = OrchestratorService()

try:
    deployment = service.create_deployment(
        env_id="prod",
        config={"service": "web", "replicas": 3}
    )
    print(f"Created deployment: {deployment.deployment_id}")

except ValidationError as e:
    print(f"Validation error: {e.message}")
    if e.field:
        print(f"  Field: {e.field}")
```

---

## CLI Specification

### Implementation Pattern (Click)

```python
# api/cli.py
"""CLI adapter for Orchestrator capability server."""
import click
import sys
import json
from typing import Optional
from core.service import OrchestratorService
from core.exceptions import (
    ValidationError,
    NotFoundError,
    ConflictError,
    OperationError,
    DomainException,
)

# Initialize service (singleton for CLI session)
service = OrchestratorService()

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Orchestrator CLI - Manage deployments across environments."""
    pass

@cli.command(name="create")
@click.option("--env", required=True, help="Environment ID (e.g., prod, staging)")
@click.option("--service", required=True, help="Service name to deploy")
@click.option("--replicas", type=int, required=True, help="Number of replicas (>=1)")
@click.option("--tag", multiple=True, help="Tags (can be specified multiple times)")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def create_deployment(
    env: str,
    service: str,
    replicas: int,
    tag: tuple,
    output_json: bool,
):
    """Create new deployment."""
    try:
        # ✅ Thin adapter: parse CLI args → core call
        deployment = service.create_deployment(
            env_id=env,
            config={
                "service": service,
                "replicas": replicas,
                "tags": list(tag),
            }
        )

        # ✅ Format output for CLI
        if output_json:
            click.echo(json.dumps(deployment.to_dict(), indent=2))
        else:
            click.echo(f"✓ Deployment created: {deployment.deployment_id}")
            click.echo(f"  Environment: {deployment.env_id}")
            click.echo(f"  Service: {deployment.service}")
            click.echo(f"  Replicas: {deployment.replicas}")
            click.echo(f"  Status: {deployment.status}")
            if deployment.tags:
                click.echo(f"  Tags: {', '.join(deployment.tags)}")

    except ValidationError as e:
        # ✅ Translate core exception → CLI error
        click.echo(f"Error: {e.message}", err=True)
        if e.field:
            click.echo(f"  Field: {e.field}", err=True)
        sys.exit(1)

    except NotFoundError as e:
        click.echo(f"Error: {e.message}", err=True)
        sys.exit(1)

    except ConflictError as e:
        click.echo(f"Error: {e.message}", err=True)
        if e.context.get("existing_id"):
            click.echo(f"  Existing: {e.context['existing_id']}", err=True)
        sys.exit(1)

    except OperationError as e:
        click.echo(f"Error: {e.message}", err=True)
        sys.exit(1)

    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)

@cli.command(name="list")
@click.option("--env", help="Filter by environment")
@click.option("--status", help="Filter by status (pending, running, failed, completed)")
@click.option("--service", help="Filter by service name")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def list_deployments(
    env: Optional[str],
    status: Optional[str],
    service: Optional[str],
    output_json: bool,
):
    """List deployments."""
    try:
        deployments = service.list_deployments(
            env_id=env,
            status=status,
            service=service,
        )

        if output_json:
            click.echo(json.dumps([d.to_dict() for d in deployments], indent=2))
        else:
            if not deployments:
                click.echo("No deployments found.")
                return

            click.echo(f"Found {len(deployments)} deployment(s):\n")
            for d in deployments:
                click.echo(f"  [{d.deployment_id}] {d.service} ({d.env_id})")
                click.echo(f"    Replicas: {d.replicas}, Status: {d.status}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command(name="get")
@click.argument("deployment_id")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def get_deployment(deployment_id: str, output_json: bool):
    """Get deployment details."""
    try:
        deployment = service.get_deployment(deployment_id)

        if output_json:
            click.echo(json.dumps(deployment.to_dict(), indent=2))
        else:
            click.echo(f"Deployment: {deployment.deployment_id}")
            click.echo(f"  Environment: {deployment.env_id}")
            click.echo(f"  Service: {deployment.service}")
            click.echo(f"  Replicas: {deployment.replicas}")
            click.echo(f"  Status: {deployment.status}")
            click.echo(f"  Created: {deployment.created_at.isoformat()}")
            if deployment.tags:
                click.echo(f"  Tags: {', '.join(deployment.tags)}")

    except NotFoundError as e:
        click.echo(f"Error: {e.message}", err=True)
        sys.exit(1)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command(name="delete")
@click.argument("deployment_id")
@click.option("--yes", is_flag=True, help="Skip confirmation")
def delete_deployment(deployment_id: str, yes: bool):
    """Delete deployment."""
    try:
        # Get deployment first (to show what we're deleting)
        deployment = service.get_deployment(deployment_id)

        if not yes:
            click.confirm(
                f"Delete deployment {deployment.deployment_id} "
                f"({deployment.service} in {deployment.env_id})?",
                abort=True
            )

        service.delete_deployment(deployment_id)
        click.echo(f"✓ Deployment {deployment_id} deleted")

    except NotFoundError as e:
        click.echo(f"Error: {e.message}", err=True)
        sys.exit(1)

    except OperationError as e:
        click.echo(f"Error: {e.message}", err=True)
        sys.exit(1)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    cli()
```

### CLI Entry Point

```toml
# pyproject.toml
[project.scripts]
orch = "api.cli:cli"
```

### CLI Usage Examples

```bash
# Create deployment
orch create --env prod --service web --replicas 3 --tag frontend --tag v1.0

# List deployments
orch list --env prod --status running

# Get deployment details
orch get deploy-abc123

# Delete deployment
orch delete deploy-abc123 --yes

# JSON output (for scripting)
orch list --env prod --json | jq '.[] | select(.status=="running")'
```

---

## REST API Specification

### Implementation Pattern (FastAPI)

```python
# api/http.py
"""REST API adapter for Orchestrator capability server."""
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from core.service import OrchestratorService
from core.exceptions import (
    ValidationError,
    NotFoundError,
    ConflictError,
    OperationError,
    DomainException,
)

app = FastAPI(
    title="Orchestrator API",
    description="Deployment orchestration capability server",
    version="1.0.0",
)

# Initialize service
service = OrchestratorService()

# Request/Response Models (Pydantic)
class CreateDeploymentRequest(BaseModel):
    """Create deployment request."""
    service: str = Field(..., description="Service name", min_length=1, max_length=63)
    replicas: int = Field(..., description="Replica count", ge=1, le=100)
    tags: List[str] = Field(default_factory=list, description="Optional tags")

    @field_validator("service")
    @classmethod
    def validate_service(cls, v: str) -> str:
        """Validate service name format."""
        if not v.isidentifier() or not v.islower():
            raise ValueError("service must be lowercase alphanumeric")
        return v

class DeploymentResponse(BaseModel):
    """Deployment response."""
    deployment_id: str
    env_id: str
    service: str
    replicas: int
    status: str
    created_at: str
    tags: List[str]

class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    message: str
    field: Optional[str] = None
    context: dict = Field(default_factory=dict)

# Exception Handlers
@app.exception_handler(ValidationError)
def validation_error_handler(request, exc: ValidationError):
    """Translate core ValidationError → HTTP 400."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            error="VALIDATION_ERROR",
            message=exc.message,
            field=exc.field,
            context=exc.context,
        ).model_dump(),
    )

@app.exception_handler(NotFoundError)
def not_found_error_handler(request, exc: NotFoundError):
    """Translate core NotFoundError → HTTP 404."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponse(
            error="NOT_FOUND",
            message=exc.message,
            context=exc.context,
        ).model_dump(),
    )

@app.exception_handler(ConflictError)
def conflict_error_handler(request, exc: ConflictError):
    """Translate core ConflictError → HTTP 409."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=ErrorResponse(
            error="CONFLICT",
            message=exc.message,
            context=exc.context,
        ).model_dump(),
    )

@app.exception_handler(OperationError)
def operation_error_handler(request, exc: OperationError):
    """Translate core OperationError → HTTP 500."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="OPERATION_FAILED",
            message=exc.message,
            context=exc.context,
        ).model_dump(),
    )

# Endpoints
@app.post(
    "/api/v1/environments/{env_id}/deployments",
    response_model=DeploymentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["deployments"],
)
def create_deployment(env_id: str, request: CreateDeploymentRequest) -> DeploymentResponse:
    """Create deployment in environment.

    Args:
        env_id: Environment identifier
        request: Deployment configuration

    Returns:
        Created deployment

    Raises:
        400: Validation error
        404: Environment not found
        409: Service already deployed
        500: Operation failed
    """
    # ✅ Thin adapter: parse JSON → core call
    deployment = service.create_deployment(
        env_id=env_id,
        config=request.model_dump(),
    )

    # ✅ Format output as JSON response
    return DeploymentResponse(
        deployment_id=deployment.deployment_id,
        env_id=deployment.env_id,
        service=deployment.service,
        replicas=deployment.replicas,
        status=deployment.status,
        created_at=deployment.created_at.isoformat(),
        tags=deployment.tags,
    )

@app.get(
    "/api/v1/deployments",
    response_model=List[DeploymentResponse],
    tags=["deployments"],
)
def list_deployments(
    env_id: Optional[str] = None,
    status: Optional[str] = None,
    service: Optional[str] = None,
) -> List[DeploymentResponse]:
    """List deployments with optional filters.

    Args:
        env_id: Filter by environment
        status: Filter by status
        service: Filter by service name

    Returns:
        List of deployments
    """
    deployments = service.list_deployments(
        env_id=env_id,
        status=status,
        service=service,
    )

    return [
        DeploymentResponse(
            deployment_id=d.deployment_id,
            env_id=d.env_id,
            service=d.service,
            replicas=d.replicas,
            status=d.status,
            created_at=d.created_at.isoformat(),
            tags=d.tags,
        )
        for d in deployments
    ]

@app.get(
    "/api/v1/deployments/{deployment_id}",
    response_model=DeploymentResponse,
    tags=["deployments"],
)
def get_deployment(deployment_id: str) -> DeploymentResponse:
    """Get deployment by ID.

    Args:
        deployment_id: Deployment identifier

    Returns:
        Deployment details

    Raises:
        404: Deployment not found
    """
    deployment = service.get_deployment(deployment_id)

    return DeploymentResponse(
        deployment_id=deployment.deployment_id,
        env_id=deployment.env_id,
        service=deployment.service,
        replicas=deployment.replicas,
        status=deployment.status,
        created_at=deployment.created_at.isoformat(),
        tags=deployment.tags,
    )

@app.delete(
    "/api/v1/deployments/{deployment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["deployments"],
)
def delete_deployment(deployment_id: str) -> None:
    """Delete deployment.

    Args:
        deployment_id: Deployment identifier

    Raises:
        404: Deployment not found
        500: Operation failed
    """
    service.delete_deployment(deployment_id)
```

### OpenAPI Specification

FastAPI auto-generates OpenAPI spec at `/openapi.json`. Example excerpt:

```yaml
openapi: 3.0.0
info:
  title: Orchestrator API
  version: 1.0.0

paths:
  /api/v1/environments/{env_id}/deployments:
    post:
      summary: Create deployment
      parameters:
        - name: env_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateDeploymentRequest'
      responses:
        '201':
          description: Deployment created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DeploymentResponse'
        '400':
          description: Validation error
        '404':
          description: Environment not found
        '409':
          description: Service already deployed
        '500':
          description: Operation failed
```

### REST API Usage Examples

```bash
# Create deployment
curl -X POST http://localhost:8000/api/v1/environments/prod/deployments \
  -H "Content-Type: application/json" \
  -d '{
    "service": "web",
    "replicas": 3,
    "tags": ["frontend", "v1.0"]
  }'

# List deployments
curl http://localhost:8000/api/v1/deployments?env_id=prod&status=running

# Get deployment
curl http://localhost:8000/api/v1/deployments/deploy-abc123

# Delete deployment
curl -X DELETE http://localhost:8000/api/v1/deployments/deploy-abc123
```

---

## MCP Specification

### Implementation Pattern (FastMCP)

```python
# api/mcp.py
"""MCP adapter for Orchestrator capability server."""
from fastmcp import FastMCP
from typing import Optional
from core.service import OrchestratorService
from core.exceptions import (
    ValidationError,
    NotFoundError,
    ConflictError,
    OperationError,
)

# Initialize FastMCP server
mcp = FastMCP(
    "Orchestrator",
    version="1.0.0",
    description="Deployment orchestration capability server for AI assistants"
)

# Initialize service
service = OrchestratorService()

# MCP namespace (Chora MCP Conventions v1.0)
NAMESPACE = "orchestrator"

def make_tool_name(tool: str) -> str:
    """Create namespaced tool name: orchestrator:tool_name"""
    return f"{NAMESPACE}:{tool}"

def make_resource_uri(resource_type: str, resource_id: str) -> str:
    """Create namespaced resource URI: orchestrator://type/id"""
    return f"{NAMESPACE}://{resource_type}/{resource_id}"

# Tools
@mcp.tool(name=make_tool_name("create_deployment"))
def create_deployment_tool(
    env_id: str,
    service_name: str,
    replicas: int,
    tags: Optional[list[str]] = None,
) -> dict:
    """Create deployment in environment (MCP tool for AI assistants).

    Args:
        env_id: Environment identifier (e.g., "prod", "staging")
        service_name: Service to deploy (e.g., "web", "api")
        replicas: Number of replicas (must be >= 1)
        tags: Optional list of tags

    Returns:
        Deployment details including ID and status

    Raises:
        ValueError: If validation fails or environment not found
        RuntimeError: If deployment operation fails
    """
    try:
        # ✅ Thin adapter: parse MCP args → core call
        deployment = service.create_deployment(
            env_id=env_id,
            config={
                "service": service_name,
                "replicas": replicas,
                "tags": tags or [],
            }
        )

        # ✅ Format output for MCP (JSON-serializable)
        return {
            "status": "created",
            "deployment": {
                "id": deployment.deployment_id,
                "environment": deployment.env_id,
                "service": deployment.service,
                "replicas": deployment.replicas,
                "status": deployment.status,
                "created_at": deployment.created_at.isoformat(),
                "tags": deployment.tags,
            }
        }

    except ValidationError as e:
        # ✅ Translate core exception → MCP error (ValueError)
        error_msg = f"{e.message}"
        if e.field:
            error_msg += f" (field: {e.field})"
        raise ValueError(error_msg)

    except NotFoundError as e:
        raise ValueError(f"Resource not found: {e.message}")

    except ConflictError as e:
        raise ValueError(f"Conflict: {e.message}")

    except OperationError as e:
        raise RuntimeError(f"Operation failed: {e.message}")

@mcp.tool(name=make_tool_name("list_deployments"))
def list_deployments_tool(
    env_id: Optional[str] = None,
    status: Optional[str] = None,
    service: Optional[str] = None,
) -> dict:
    """List deployments with optional filters (MCP tool for AI assistants).

    Args:
        env_id: Filter by environment (optional)
        status: Filter by status (pending, running, failed, completed)
        service: Filter by service name (optional)

    Returns:
        List of matching deployments
    """
    deployments = service.list_deployments(
        env_id=env_id,
        status=status,
        service=service,
    )

    return {
        "count": len(deployments),
        "deployments": [
            {
                "id": d.deployment_id,
                "environment": d.env_id,
                "service": d.service,
                "replicas": d.replicas,
                "status": d.status,
                "created_at": d.created_at.isoformat(),
                "tags": d.tags,
            }
            for d in deployments
        ]
    }

@mcp.tool(name=make_tool_name("get_deployment"))
def get_deployment_tool(deployment_id: str) -> dict:
    """Get deployment details by ID (MCP tool for AI assistants).

    Args:
        deployment_id: Deployment identifier

    Returns:
        Deployment details

    Raises:
        ValueError: If deployment not found
    """
    try:
        deployment = service.get_deployment(deployment_id)

        return {
            "deployment": {
                "id": deployment.deployment_id,
                "environment": deployment.env_id,
                "service": deployment.service,
                "replicas": deployment.replicas,
                "status": deployment.status,
                "created_at": deployment.created_at.isoformat(),
                "tags": deployment.tags,
            }
        }

    except NotFoundError as e:
        raise ValueError(f"Deployment not found: {e.message}")

@mcp.tool(name=make_tool_name("delete_deployment"))
def delete_deployment_tool(deployment_id: str) -> dict:
    """Delete deployment (MCP tool for AI assistants).

    Args:
        deployment_id: Deployment identifier to delete

    Returns:
        Deletion confirmation

    Raises:
        ValueError: If deployment not found
        RuntimeError: If deletion fails
    """
    try:
        service.delete_deployment(deployment_id)

        return {
            "status": "deleted",
            "deployment_id": deployment_id,
        }

    except NotFoundError as e:
        raise ValueError(f"Deployment not found: {e.message}")

    except OperationError as e:
        raise RuntimeError(f"Failed to delete deployment: {e.message}")

# Resources
@mcp.resource(uri=make_resource_uri("deployments", "{deployment_id}"))
def get_deployment_resource(deployment_id: str) -> str:
    """Get deployment details as formatted text (MCP resource for AI assistants).

    Args:
        deployment_id: Deployment identifier (extracted from URI)

    Returns:
        Deployment details in markdown format

    Raises:
        ValueError: If deployment not found
    """
    try:
        deployment = service.get_deployment(deployment_id)

        return f"""# Deployment {deployment.deployment_id}

**Environment**: {deployment.env_id}
**Service**: {deployment.service}
**Replicas**: {deployment.replicas}
**Status**: {deployment.status}
**Created**: {deployment.created_at.isoformat()}
**Tags**: {', '.join(deployment.tags) if deployment.tags else 'None'}

## Operations

Use tools to manage this deployment:
- `orchestrator:delete_deployment` - Delete this deployment
"""

    except NotFoundError as e:
        raise ValueError(f"Deployment not found: {e.message}")

@mcp.resource(uri=make_resource_uri("docs", "quickstart.md"))
def get_quickstart_resource() -> str:
    """Get quickstart documentation (MCP resource for AI assistants)."""
    return """# Orchestrator Quickstart

## Creating Deployments

Use `orchestrator:create_deployment` tool:
- **env_id**: Environment (e.g., "prod", "staging")
- **service_name**: Service to deploy
- **replicas**: Number of replicas (>=1)
- **tags**: Optional tags

Example:
```
orchestrator:create_deployment(
    env_id="prod",
    service_name="web",
    replicas=3,
    tags=["frontend", "v1.0"]
)
```

## Listing Deployments

Use `orchestrator:list_deployments` tool with optional filters.

## Getting Deployment Details

Use `orchestrator:get_deployment` tool or read resource:
`orchestrator://deployments/{deployment_id}`
"""

# Prompts
@mcp.prompt(name="analyze_deployments")
def analyze_deployments_prompt(focus: str = "general") -> str:
    """Generate prompt for deployment analysis (MCP prompt for AI assistants).

    Args:
        focus: Analysis focus (general, capacity, failures)

    Returns:
        Analysis prompt
    """
    deployments = service.list_deployments()

    deployment_list = "\n".join([
        f"- [{d.deployment_id}] {d.service} in {d.env_id} "
        f"(Replicas: {d.replicas}, Status: {d.status})"
        for d in deployments
    ])

    if focus == "capacity":
        return f"""Analyze deployment capacity across environments:

{deployment_list}

Focus on:
1. Total replica count by environment
2. Service distribution (which services have most replicas)
3. Capacity recommendations (under/over-provisioned environments)
"""
    elif focus == "failures":
        failed = [d for d in deployments if d.status == "failed"]
        return f"""Analyze failed deployments:

{deployment_list}

Failed deployments: {len(failed)}

Focus on:
1. Common failure patterns
2. Affected services and environments
3. Remediation recommendations
"""
    else:
        return f"""Analyze deployment status across all environments:

{deployment_list}

Provide:
1. Overall health assessment
2. Environment-by-environment breakdown
3. Status distribution (pending, running, failed, completed)
4. Actionable recommendations
"""

# MCP Server Entry Point
if __name__ == "__main__":
    mcp.run()
```

### MCP Client Configuration

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "orchestrator": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/orchestrator",
        "run",
        "orchestrator-mcp"
      ]
    }
  }
}
```

**pyproject.toml**:

```toml
[project.scripts]
orchestrator-mcp = "api.mcp:mcp.run"
```

### MCP Usage Example

**Claude Desktop conversation**:

```
User: Create a deployment for the web service in production with 3 replicas

Claude: I'll create a deployment using the orchestrator tool.
[Calls orchestrator:create_deployment(env_id="prod", service_name="web", replicas=3)]

Result: Deployment created successfully!
- ID: deploy-abc123
- Environment: prod
- Service: web
- Replicas: 3
- Status: pending
```

---

## Error Handling Specification

### Error Mapping Table

| Core Exception | Native API | CLI | REST API | MCP | HTTP Status | Exit Code |
|----------------|------------|-----|----------|-----|-------------|-----------|
| `ValidationError` | Raise exception | stderr + exit 1 | 400 + JSON error | ValueError | 400 | 1 |
| `NotFoundError` | Raise exception | stderr + exit 1 | 404 + JSON error | ValueError | 404 | 1 |
| `ConflictError` | Raise exception | stderr + exit 1 | 409 + JSON error | ValueError | 409 | 1 |
| `OperationError` | Raise exception | stderr + exit 1 | 500 + JSON error | RuntimeError | 500 | 1 |
| `AuthorizationError` | Raise exception | stderr + exit 1 | 403 + JSON error | ValueError | 403 | 1 |
| Unexpected exception | Raise exception | stderr + exit 1 | 500 + generic error | RuntimeError | 500 | 1 |

### Error Response Formats

**CLI**:
```
Error: replicas must be >= 1
  Field: replicas
```

**REST API**:
```json
{
  "error": "VALIDATION_ERROR",
  "message": "replicas must be >= 1",
  "field": "replicas",
  "context": {}
}
```

**MCP**:
```json
{
  "error": {
    "code": -32602,
    "message": "replicas must be >= 1 (field: replicas)"
  }
}
```

---

## Testing Specification

### Core Tests

```python
# tests/test_core.py
import pytest
from core.service import OrchestratorService
from core.exceptions import ValidationError, NotFoundError, ConflictError

def test_create_deployment_success():
    """Test successful deployment creation."""
    service = OrchestratorService()
    deployment = service.create_deployment(
        env_id="test-env",
        config={"service": "web", "replicas": 3}
    )

    assert deployment.service == "web"
    assert deployment.replicas == 3
    assert deployment.status == "pending"

def test_create_deployment_validation_error():
    """Test validation error for invalid replicas."""
    service = OrchestratorService()

    with pytest.raises(ValidationError) as exc_info:
        service.create_deployment(
            env_id="test-env",
            config={"service": "web", "replicas": 0}
        )

    assert "replicas must be >= 1" in exc_info.value.message
    assert exc_info.value.field == "replicas"
```

### Consistency Tests

```python
# tests/test_consistency.py
import pytest
from core.service import OrchestratorService
from api.cli import create_deployment as cli_create
from api.http import create_deployment as http_create
from api.mcp import create_deployment_tool as mcp_create

def test_create_deployment_consistency():
    """Verify all 4 interfaces produce identical results."""
    config = {"service": "web", "replicas": 3}

    # Core
    core_result = OrchestratorService().create_deployment("test-env", config)

    # CLI (mocked Click context)
    # ... (mock Click, call cli_create)

    # REST (mocked FastAPI request)
    # ... (mock FastAPI, call http_create)

    # MCP
    mcp_result = mcp_create(
        env_id="test-env",
        service_name="web",
        replicas=3
    )

    # Assert all produce same deployment
    assert core_result.service == "web"
    assert core_result.replicas == 3
    assert mcp_result["deployment"]["service"] == "web"
    assert mcp_result["deployment"]["replicas"] == 3
```

---

## Deployment Specification

### Running All 4 Interfaces

**Native API**: Import in Python scripts
```python
from orchestrator import OrchestratorService
service = OrchestratorService()
```

**CLI**: Run as command
```bash
orch create --env prod --service web --replicas 3
```

**REST API**: Run with uvicorn
```bash
uvicorn api.http:app --host 0.0.0.0 --port 8000
```

**MCP**: Run with FastMCP
```bash
python -m api.mcp
```

**Docker** (all interfaces in one container):
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install -e .

# Expose REST API port
EXPOSE 8000

# Default: run REST API (can override CMD for CLI/MCP)
CMD ["uvicorn", "api.http:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Summary

SAP-043 provides:
- ✅ **Core + adapters** architecture for 4 interfaces
- ✅ **Complete code examples** for all interfaces
- ✅ **Error mapping** patterns
- ✅ **Consistency testing** patterns
- ✅ **Deployment** specifications

**Next**: Read [adoption-blueprint.md](./adoption-blueprint.md) for step-by-step implementation guide.
