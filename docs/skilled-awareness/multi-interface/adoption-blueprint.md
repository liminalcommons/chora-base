# SAP-043: Multi-Interface Capability Servers - Adoption Blueprint

**SAP ID**: SAP-043
**Version**: 1.0.0
**Last Updated**: 2025-11-12
**Estimated Time**: 1-4 weeks depending on tier

---

## Overview

This blueprint provides step-by-step instructions for implementing multi-interface capability servers following SAP-043 patterns. It covers three adoption tiers (Essential, Recommended, Advanced) with detailed phases, quality gates, and validation checkpoints.

**Outcome**: Capability server with 4 interfaces (Native API, CLI, REST, MCP) sharing a single core implementation, passing consistency tests, ready for production deployment.

---

## Prerequisites

### Knowledge Requirements

**Essential**:
- Python 3.9+ proficiency
- Object-oriented programming (classes, inheritance, exceptions)
- Data structures (dict, list, dataclass)
- Function signatures and type hints
- pytest basics

**Recommended**:
- Click (CLI framework)
- FastAPI (REST API framework)
- FastMCP (MCP protocol library)
- Pydantic (data validation)
- Async programming (optional, for I/O-bound operations)

**Resources**:
- **SAP-042** (InterfaceDesign): Read first for foundational principles
- **SAP-014** (mcp-server-development): For MCP interface patterns
- **SAP-004** (testing-framework): For pytest patterns

### Tool Requirements

**Development Tools**:
```bash
# Python 3.9+
python --version  # Should be >=3.9

# Package manager
pip install --upgrade pip
# or
curl -LsSf https://astral.sh/uv/install.sh | sh

# Virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows
```

**Dependencies**:
```toml
# pyproject.toml
[project]
name = "capability-server"
dependencies = [
    "click>=8.0",       # CLI
    "fastapi>=0.100",   # REST API
    "uvicorn>=0.20",    # ASGI server (for FastAPI)
    "fastmcp>=0.2.0",   # MCP
    "pydantic>=2.0",    # Data validation
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-mock>=3.12",
    "pytest-asyncio>=0.21",
    "mypy>=1.8",
    "ruff>=0.2",
]
```

### Environment Setup

```bash
# Install dependencies
pip install -e ".[dev]"

# Verify installations
python -c "import click; print(f'Click: {click.__version__}')"
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"
python -c "import fastmcp; print(f'FastMCP: {fastmcp.__version__}')"

# Run tests (should have 0 tests initially)
pytest tests/
```

---

## Essential Tier (Weeks 1-2)

**Goal**: Implement core + 4 adapters with consistency tests

**Estimated Time**: 1-2 weeks (40-80 hours)

**Outcome**: All 4 interfaces operational, passing consistency tests, documented

---

### Phase 1: Domain Modeling (Day 1-2, 8-16 hours)

**Goal**: Define domain models, exceptions, and core structure

#### Step 1.1: Create Directory Structure

```bash
mkdir -p capability-server/{core,api,tests}
touch capability-server/core/{__init__.py,service.py,models.py,exceptions.py,validators.py}
touch capability-server/api/{__init__.py,native.py,cli.py,http.py,mcp.py}
touch capability-server/tests/{__init__.py,test_core.py,test_cli.py,test_http.py,test_mcp.py,test_consistency.py}
```

**Result**:
```
capability-server/
├── core/
│   ├── __init__.py
│   ├── service.py          # Main service class
│   ├── models.py           # Domain models (dataclasses)
│   ├── exceptions.py       # Domain exceptions
│   └── validators.py       # Validation logic
├── api/
│   ├── __init__.py
│   ├── native.py           # Native Python API
│   ├── cli.py              # CLI adapter (Click)
│   ├── http.py             # REST API adapter (FastAPI)
│   └── mcp.py              # MCP adapter (FastMCP)
├── tests/
│   ├── __init__.py
│   ├── test_core.py        # Core logic tests
│   ├── test_cli.py         # CLI adapter tests
│   ├── test_http.py        # REST API tests
│   ├── test_mcp.py         # MCP tool tests
│   └── test_consistency.py # Cross-interface consistency tests
├── pyproject.toml
└── README.md
```

#### Step 1.2: Define Domain Models

**File**: `core/models.py`

```python
"""Domain models (immutable, interface-agnostic)."""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass(frozen=True)
class Deployment:
    """Deployment domain model."""
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

    @classmethod
    def from_dict(cls, data: dict) -> "Deployment":
        """Create from dict (for persistence layer)."""
        return cls(
            env_id=data["env_id"],
            service=data["service"],
            replicas=data["replicas"],
            deployment_id=data.get("deployment_id", ""),
            status=data.get("status", "pending"),
            created_at=datetime.fromisoformat(data["created_at"]),
            tags=data.get("tags", []),
        )

# Add other domain models as needed (Environment, etc.)
```

**Validation**: Run `python -c "from core.models import Deployment; print(Deployment('prod', 'web', 3))"`

#### Step 1.3: Define Domain Exceptions

**File**: `core/exceptions.py`

```python
"""Domain exceptions (interface-agnostic)."""
from typing import Optional, Dict, Any

class DomainException(Exception):
    """Base exception for all domain errors."""
    def __init__(self, message: str, **context):
        self.message = message
        self.context = context
        super().__init__(message)

class ValidationError(DomainException):
    """Input validation failed."""
    def __init__(self, message: str, field: Optional[str] = None, **context):
        super().__init__(message, field=field, **context)
        self.field = field

class NotFoundError(DomainException):
    """Requested resource not found."""
    def __init__(self, resource_type: str, resource_id: str, **context):
        message = f"{resource_type} not found: {resource_id}"
        super().__init__(message, resource_type=resource_type, resource_id=resource_id, **context)

class ConflictError(DomainException):
    """Resource already exists or conflicts with existing state."""
    def __init__(self, message: str, existing_id: Optional[str] = None, **context):
        super().__init__(message, existing_id=existing_id, **context)

class OperationError(DomainException):
    """Operation failed (e.g., deployment failed)."""
    pass

class AuthorizationError(DomainException):
    """User not authorized to perform operation."""
    def __init__(self, operation: str, resource: str, **context):
        message = f"Not authorized to {operation} {resource}"
        super().__init__(message, operation=operation, resource=resource, **context)
```

**Validation**: Run `python -c "from core.exceptions import ValidationError; raise ValidationError('test', field='replicas')"`

#### Step 1.4: Implement Validators

**File**: `core/validators.py`

```python
"""Validation logic (pure functions)."""
import re
from typing import Any
from .exceptions import ValidationError

def validate_service_name(service: str) -> None:
    """Validate service name format.

    Args:
        service: Service name to validate

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

    Args:
        replicas: Replica count to validate

    Raises:
        ValidationError: If replicas is invalid
    """
    if not isinstance(replicas, int):
        raise ValidationError(
            f"replicas must be integer, got {type(replicas).__name__}",
            field="replicas"
        )

    if replicas < 1:
        raise ValidationError("replicas must be >= 1", field="replicas")

    if replicas > 100:
        raise ValidationError(
            "replicas must be <= 100 (contact support for higher limits)",
            field="replicas"
        )

def validate_env_id(env_id: str) -> None:
    """Validate environment ID format.

    Args:
        env_id: Environment ID to validate

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

**Validation**: Run pytest:
```python
# tests/test_core.py (add validators tests)
from core.validators import validate_replicas
from core.exceptions import ValidationError
import pytest

def test_validate_replicas_success():
    validate_replicas(1)  # Should not raise
    validate_replicas(50)  # Should not raise

def test_validate_replicas_too_low():
    with pytest.raises(ValidationError) as exc_info:
        validate_replicas(0)
    assert "replicas must be >= 1" in exc_info.value.message

def test_validate_replicas_not_integer():
    with pytest.raises(ValidationError) as exc_info:
        validate_replicas("3")
    assert "must be integer" in exc_info.value.message
```

Run: `pytest tests/test_core.py -v`

**Quality Gate 1**: ✅ Domain models, exceptions, and validators implemented and tested

---

### Phase 2: Core Implementation (Day 3-5, 16-24 hours)

**Goal**: Implement core service with all operations

#### Step 2.1: Implement Core Service

**File**: `core/service.py`

```python
"""Core service (interface-agnostic business logic)."""
from typing import List, Dict, Any, Optional
import uuid
from .models import Deployment
from .exceptions import ValidationError, NotFoundError, ConflictError, OperationError
from .validators import validate_service_name, validate_replicas, validate_env_id

class OrchestratorService:
    """Orchestrator capability service (interface-agnostic)."""

    def __init__(self):
        """Initialize service."""
        # In-memory storage (replace with DB in production)
        self._deployments: Dict[str, Deployment] = {}
        self._environments = {"prod", "staging", "dev"}  # Mock environments

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
            ConflictError: If service already deployed in environment
            OperationError: If deployment creation fails
        """
        # Validate environment exists
        validate_env_id(env_id)
        if env_id not in self._environments:
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

        validate_service_name(service)
        validate_replicas(replicas)

        # Check for conflicts
        existing_key = f"{env_id}/{service}"
        if existing_key in self._deployments:
            raise ConflictError(
                f"Service '{service}' already deployed in environment '{env_id}'",
                existing_id=existing_key
            )

        # Create deployment
        deployment_id = f"deploy-{uuid.uuid4().hex[:8]}"
        deployment = Deployment(
            env_id=env_id,
            service=service,
            replicas=replicas,
            deployment_id=deployment_id,
            status="pending",
            tags=tags,
        )

        # Persist deployment
        self._deployments[deployment_id] = deployment
        self._deployments[existing_key] = deployment  # Also store by env/service

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
            status: Filter by status
            service: Filter by service name

        Returns:
            List of matching deployments
        """
        deployments = [
            d for d in self._deployments.values()
            if d.deployment_id.startswith("deploy-")  # Skip env/service keys
        ]

        if env_id:
            deployments = [d for d in deployments if d.env_id == env_id]
        if status:
            deployments = [d for d in deployments if d.status == status]
        if service:
            deployments = [d for d in deployments if d.service == service]

        return deployments

    def get_deployment(self, deployment_id: str) -> Deployment:
        """Get deployment by ID.

        Args:
            deployment_id: Deployment identifier

        Returns:
            Deployment object

        Raises:
            NotFoundError: If deployment doesn't exist
        """
        deployment = self._deployments.get(deployment_id)
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

        # Remove from storage
        del self._deployments[deployment_id]
        env_service_key = f"{deployment.env_id}/{deployment.service}"
        if env_service_key in self._deployments:
            del self._deployments[env_service_key]
```

#### Step 2.2: Test Core Service

**File**: `tests/test_core.py`

```python
"""Core service tests."""
import pytest
from core.service import OrchestratorService
from core.exceptions import ValidationError, NotFoundError, ConflictError

@pytest.fixture
def service():
    """Create service instance."""
    return OrchestratorService()

def test_create_deployment_success(service):
    """Test successful deployment creation."""
    deployment = service.create_deployment(
        env_id="prod",
        config={"service": "web", "replicas": 3, "tags": ["frontend"]}
    )

    assert deployment.env_id == "prod"
    assert deployment.service == "web"
    assert deployment.replicas == 3
    assert deployment.status == "pending"
    assert deployment.tags == ["frontend"]
    assert deployment.deployment_id.startswith("deploy-")

def test_create_deployment_validation_error(service):
    """Test validation error for invalid replicas."""
    with pytest.raises(ValidationError) as exc_info:
        service.create_deployment(
            env_id="prod",
            config={"service": "web", "replicas": 0}
        )

    assert "replicas must be >= 1" in exc_info.value.message
    assert exc_info.value.field == "replicas"

def test_create_deployment_not_found_error(service):
    """Test error for non-existent environment."""
    with pytest.raises(NotFoundError) as exc_info:
        service.create_deployment(
            env_id="nonexistent",
            config={"service": "web", "replicas": 3}
        )

    assert "Environment not found: nonexistent" in exc_info.value.message

def test_create_deployment_conflict_error(service):
    """Test conflict error for duplicate service."""
    service.create_deployment("prod", {"service": "web", "replicas": 3})

    with pytest.raises(ConflictError) as exc_info:
        service.create_deployment("prod", {"service": "web", "replicas": 5})

    assert "already deployed" in exc_info.value.message

def test_list_deployments(service):
    """Test listing deployments."""
    service.create_deployment("prod", {"service": "web", "replicas": 3})
    service.create_deployment("prod", {"service": "api", "replicas": 5})
    service.create_deployment("staging", {"service": "web", "replicas": 1})

    # All deployments
    all_deployments = service.list_deployments()
    assert len(all_deployments) == 3

    # Filter by environment
    prod_deployments = service.list_deployments(env_id="prod")
    assert len(prod_deployments) == 2

    # Filter by service
    web_deployments = service.list_deployments(service="web")
    assert len(web_deployments) == 2

def test_get_deployment(service):
    """Test getting deployment by ID."""
    deployment = service.create_deployment("prod", {"service": "web", "replicas": 3})
    retrieved = service.get_deployment(deployment.deployment_id)

    assert retrieved.deployment_id == deployment.deployment_id
    assert retrieved.service == "web"

def test_get_deployment_not_found(service):
    """Test error for non-existent deployment."""
    with pytest.raises(NotFoundError):
        service.get_deployment("nonexistent")

def test_delete_deployment(service):
    """Test deleting deployment."""
    deployment = service.create_deployment("prod", {"service": "web", "replicas": 3})
    service.delete_deployment(deployment.deployment_id)

    with pytest.raises(NotFoundError):
        service.get_deployment(deployment.deployment_id)
```

**Validation**: Run `pytest tests/test_core.py -v` (should pass all tests)

**Quality Gate 2**: ✅ Core service implemented and tested (85%+ coverage)

---

### Phase 3: Native API Adapter (Day 5, 2 hours)

**Goal**: Export core for programmatic use

#### Step 3.1: Implement Native API

**File**: `api/native.py` or `capability_server/__init__.py`

```python
"""Native Python API for Orchestrator capability server."""

# Re-export core classes for direct use
from core.service import OrchestratorService
from core.models import Deployment
from core.exceptions import (
    DomainException,
    ValidationError,
    NotFoundError,
    ConflictError,
    OperationError,
    AuthorizationError,
)

__all__ = [
    "OrchestratorService",
    "Deployment",
    "ValidationError",
    "NotFoundError",
    "ConflictError",
    "OperationError",
    "AuthorizationError",
]

__version__ = "1.0.0"
```

#### Step 3.2: Test Native API

**File**: `tests/test_native.py`

```python
"""Native API tests."""
from capability_server import OrchestratorService, Deployment, ValidationError

def test_native_api_usage():
    """Test using native API directly."""
    service = OrchestratorService()

    # Create deployment
    deployment = service.create_deployment(
        env_id="prod",
        config={"service": "web", "replicas": 3}
    )

    assert isinstance(deployment, Deployment)
    assert deployment.service == "web"
```

**Validation**: Run `pytest tests/test_native.py -v`

**Quality Gate 3**: ✅ Native API implemented and tested

---

### Phase 4: CLI Adapter (Day 6-7, 12-16 hours)

**Goal**: Implement Click-based CLI

See protocol-spec.md for complete CLI implementation. Key steps:

1. Implement CLI commands (`api/cli.py`)
2. Add error handling (translate core exceptions → CLI errors)
3. Add `--json` flag for machine-readable output
4. Add entry point to `pyproject.toml`
5. Test CLI commands

**Quality Gate 4**: ✅ CLI implemented, tested, and documented

---

### Phase 5: REST API Adapter (Day 8-9, 12-16 hours)

**Goal**: Implement FastAPI-based REST API

See protocol-spec.md for complete REST API implementation. Key steps:

1. Implement FastAPI app (`api/http.py`)
2. Add Pydantic models for request/response
3. Add exception handlers (translate core exceptions → HTTP errors)
4. Test endpoints
5. Generate OpenAPI docs

**Quality Gate 5**: ✅ REST API implemented, tested, OpenAPI spec available

---

### Phase 6: MCP Adapter (Day 10-11, 12-16 hours)

**Goal**: Implement FastMCP-based MCP interface

See protocol-spec.md for complete MCP implementation. Key steps:

1. Implement FastMCP server (`api/mcp.py`)
2. Add tools (operations)
3. Add resources (data sources)
4. Add prompts (AI interactions)
5. Configure MCP client (Claude Desktop)
6. Test tools

**Quality Gate 6**: ✅ MCP implemented, tested, integrated with Claude Desktop

---

### Phase 7: Consistency Tests (Day 12-13, 8-12 hours)

**Goal**: Verify all 4 interfaces produce identical results

**File**: `tests/test_consistency.py`

```python
"""Cross-interface consistency tests."""
import pytest
from core.service import OrchestratorService
from api.mcp import create_deployment_tool as mcp_create

def test_create_deployment_consistency():
    """Verify all interfaces produce same deployment."""
    # Core
    core_service = OrchestratorService()
    core_result = core_service.create_deployment(
        "prod",
        {"service": "web", "replicas": 3}
    )

    # MCP
    mcp_service = OrchestratorService()
    mcp_result = mcp_create(
        env_id="prod",
        service_name="web",
        replicas=3
    )

    # Assert consistency
    assert core_result.service == "web"
    assert core_result.replicas == 3
    assert mcp_result["deployment"]["service"] == "web"
    assert mcp_result["deployment"]["replicas"] == 3

def test_error_handling_consistency():
    """Verify all interfaces produce same error for invalid input."""
    # Core
    core_service = OrchestratorService()
    with pytest.raises(ValidationError) as core_exc:
        core_service.create_deployment("prod", {"service": "web", "replicas": 0})

    # MCP
    with pytest.raises(ValueError) as mcp_exc:
        mcp_create(env_id="prod", service_name="web", replicas=0)

    # Assert error messages are consistent
    assert "replicas must be >= 1" in core_exc.value.message
    assert "replicas must be >= 1" in str(mcp_exc.value)
```

**Validation**: Run `pytest tests/test_consistency.py -v`

**Quality Gate 7**: ✅ Consistency tests passing

---

### Phase 8: Documentation & Validation (Day 14, 4-8 hours)

**Goal**: Complete README, validate all interfaces

#### Step 8.1: Write README

**File**: `README.md`

```markdown
# Orchestrator Capability Server

Multi-interface deployment orchestration capability server.

## Interfaces

### 1. Native API (Python)

```python
from orchestrator import OrchestratorService

service = OrchestratorService()
deployment = service.create_deployment(
    env_id="prod",
    config={"service": "web", "replicas": 3}
)
print(f"Created: {deployment.deployment_id}")
```

### 2. CLI (Command Line)

```bash
orch create --env prod --service web --replicas 3
orch list --env prod
orch get deploy-abc123
orch delete deploy-abc123
```

### 3. REST API (HTTP)

```bash
curl -X POST http://localhost:8000/api/v1/environments/prod/deployments \
  -H "Content-Type: application/json" \
  -d '{"service": "web", "replicas": 3}'
```

### 4. MCP (AI Assistants)

Use with Claude Desktop:
- `orchestrator:create_deployment` - Create deployment
- `orchestrator:list_deployments` - List deployments
- `orchestrator:get_deployment` - Get deployment details
- `orchestrator:delete_deployment` - Delete deployment

## Installation

```bash
pip install -e .
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run CLI
orch --help

# Run REST API
uvicorn api.http:app --reload

# Run MCP server
python -m api.mcp
```

## Testing

```bash
# Core tests
pytest tests/test_core.py -v

# Interface tests
pytest tests/test_cli.py tests/test_http.py tests/test_mcp.py -v

# Consistency tests
pytest tests/test_consistency.py -v

# All tests
pytest tests/ -v --cov=core --cov=api
```

## Architecture

See [SAP-043](https://github.com/example/chora-base/docs/skilled-awareness/multi-interface/) for architectural patterns.

**Core + Adapters Pattern**:
- `core/` - Interface-agnostic business logic
- `api/` - Thin interface adapters (Native, CLI, REST, MCP)
- `tests/` - Unit tests + consistency tests
```

#### Step 8.2: Validate All Interfaces

**Checklist**:
- [ ] Core tests pass (85%+ coverage)
- [ ] CLI commands work (create, list, get, delete)
- [ ] REST API endpoints work (test with curl or Postman)
- [ ] MCP tools work (test with Claude Desktop)
- [ ] Consistency tests pass
- [ ] README complete with all 4 interface examples
- [ ] pyproject.toml has all dependencies
- [ ] Entry points configured (CLI, MCP)

**Quality Gate 8**: ✅ All interfaces validated, documentation complete

---

## Essential Tier Complete

**Estimated Time**: 1-2 weeks (40-80 hours)

**Deliverables**:
- ✅ Core module (interface-agnostic business logic)
- ✅ 4 interface adapters (Native, CLI, REST, MCP)
- ✅ Consistency tests (verify all interfaces produce identical results)
- ✅ Complete documentation (README with all 4 usage examples)
- ✅ 85%+ test coverage

**Validation**: Run full test suite:
```bash
pytest tests/ -v --cov=core --cov=api --cov-report=term-missing
```

---

## Recommended Tier (Weeks 3-4)

**Goal**: Production-ready with observability, versioning, backward compatibility

**Estimated Time**: +1 week (20-40 hours)

### Phase 9: Observability (Correlation IDs, Structured Logging)

**Add correlation ID propagation**:

```python
# core/context.py (new file)
import contextvars
import uuid

request_id_var = contextvars.ContextVar("request_id", default=None)

def get_request_id() -> str:
    """Get current request ID or generate new one."""
    request_id = request_id_var.get()
    if not request_id:
        request_id = str(uuid.uuid4())
        request_id_var.set(request_id)
    return request_id

def set_request_id(request_id: str) -> None:
    """Set request ID for current context."""
    request_id_var.set(request_id)
```

**Add structured logging**:

```python
# core/logging_config.py (new file)
import logging
import json
from .context import get_request_id

class JSONFormatter(logging.Formatter):
    """JSON log formatter with request_id."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": get_request_id(),
            "module": record.module,
            "function": record.funcName,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)
logging.getLogger().handlers[0].setFormatter(JSONFormatter())
```

**Update adapters to set request_id**:

```python
# api/http.py (add middleware)
from core.context import set_request_id

@app.middleware("http")
async def add_request_id(request, call_next):
    """Add X-Request-ID to all requests."""
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    set_request_id(request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

### Phase 10: Versioning Strategy

**REST API versioning**:
- URLs: `/api/v1/...`
- Document deprecation policy (6 months support for old versions)
- Add version negotiation

**MCP versioning**:
- Namespace tools: `orchestrator:v1:create_deployment`
- Provide backward compatibility layers

### Phase 11: Backward Compatibility Tests

**Add tests for API changes**:

```python
# tests/test_backward_compatibility.py
def test_old_client_still_works():
    """Verify old API version still supported."""
    # Test that v1 API works even after adding v2
    response = client.post("/api/v1/deployments", json={...})
    assert response.status_code == 201
```

---

## Advanced Tier (Weeks 5-8)

**Goal**: Ecosystem integration, SDK generation, gateway integration

**Estimated Time**: +2-4 weeks (40-80 hours)

### Phase 12: SDK Auto-Generation

**Generate Python client from OpenAPI**:

```bash
openapi-python-client generate --url http://localhost:8000/openapi.json
```

### Phase 13: Shell Autocompletion

**Add Click autocompletion**:

```python
# api/cli.py
import click

@cli.command()
@click.option("--env", type=click.Choice(["prod", "staging", "dev"]))
def create(...):
    pass

# Install autocompletion
# _ORCH_COMPLETE=bash_source orch > ~/.orch-complete.bash
# source ~/.orch-complete.bash
```

### Phase 14: Gateway Integration

**Register with API Gateway** (if available):
- Expose all interfaces via unified gateway
- Add service discovery
- Add authentication/authorization

---

## Quality Gates Summary

| Phase | Quality Gate | Validation |
|-------|-------------|------------|
| 1 | Domain models defined | Run: `python -c "from core.models import Deployment; print(Deployment('prod', 'web', 3))"` |
| 2 | Core service tested | Run: `pytest tests/test_core.py -v` (85%+ coverage) |
| 3 | Native API working | Run: `pytest tests/test_native.py -v` |
| 4 | CLI working | Run: `orch create --env prod --service web --replicas 3` |
| 5 | REST API working | Run: `curl http://localhost:8000/api/v1/deployments` |
| 6 | MCP working | Test with Claude Desktop |
| 7 | Consistency tests passing | Run: `pytest tests/test_consistency.py -v` |
| 8 | Documentation complete | Review README with all 4 interface examples |

---

## Migration Guide (Existing Projects)

**Scenario**: You have existing capability server with single interface, want to add multi-interface support.

### Step 1: Extract Core Logic

**Before** (business logic in interface):
```python
# api.py
@app.post("/deployments")
def create_deployment(request):
    if request.replicas < 1:  # ❌ Validation in interface
        return {"error": "Invalid replicas"}, 400
    # ❌ Business logic in interface
    deployment = Deployment(...)
    db.session.add(deployment)
    db.session.commit()
    return deployment.to_dict(), 201
```

**After** (business logic in core):
```python
# core/service.py
def create_deployment(self, env_id, config):
    if config["replicas"] < 1:  # ✅ Validation in core
        raise ValidationError("replicas must be >= 1")
    deployment = Deployment(...)
    repository.create(deployment)
    return deployment

# api/http.py
@app.post("/deployments")
def create_deployment_endpoint(env_id, request):
    try:
        deployment = service.create_deployment(env_id, request.dict())  # ✅ Thin adapter
        return deployment.to_dict(), 201
    except ValidationError as e:
        raise HTTPException(400, e.message)
```

### Step 2: Add Other Interfaces

Once core is extracted, add other interfaces using patterns from this blueprint.

### Step 3: Add Consistency Tests

Verify all interfaces produce identical results.

---

## Troubleshooting

### Issue 1: Adapters Getting Too Complex

**Symptom**: Adapter file >200 lines, complex logic

**Fix**: Move logic to core. Adapter should be <100 lines.

### Issue 2: Interfaces Producing Different Results

**Symptom**: Consistency tests failing

**Fix**: Ensure all adapters call core with same inputs. Check error handling.

### Issue 3: Core Has Interface Dependencies

**Symptom**: Core imports Flask, Click, FastMCP

**Fix**: Remove imports, use interface-agnostic types (dict, list, dataclass).

---

## Support

**Questions?**
- Read [protocol-spec.md](./protocol-spec.md) for implementation patterns
- Check [AGENTS.md](./AGENTS.md) for quick reference
- Review [ledger.md](./ledger.md) for adoption examples

---

**Version**: 1.0.0
**Last Updated**: 2025-11-12
**Feedback**: Submit to [ledger.md](./ledger.md)
