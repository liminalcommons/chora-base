# SAP-042: Interface Design Patterns - Adoption Blueprint

**SAP ID**: SAP-042
**Estimated Adoption Time**:
- Essential: 1-2 weeks
- Recommended: 2-4 weeks
- Advanced: 4-8 weeks

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Tiered Adoption Overview](#tiered-adoption-overview)
3. [Essential Tier: Contract-First Basics](#essential-tier-contract-first-basics)
4. [Recommended Tier: Versioning & Observability](#recommended-tier-versioning--observability)
5. [Advanced Tier: Multi-Protocol & Optimization](#advanced-tier-multi-protocol--optimization)
6. [Validation & Quality Gates](#validation--quality-gates)
7. [Migration Guide (Existing Projects)](#migration-guide-existing-projects)

---

## Prerequisites

### Knowledge Requirements

- **Essential**:
  - Python 3.9+ (for core logic)
  - REST API concepts (HTTP methods, status codes)
  - CLI design basics (commands, flags)

- **Recommended**:
  - OpenAPI 3.x specification format
  - Distributed systems concepts (tracing, correlation IDs)
  - Testing frameworks (pytest, contract testing)

- **Advanced**:
  - gRPC and Protocol Buffers
  - Event-driven architecture
  - API gateway patterns (Envoy, Kong)

### Tool Requirements

```bash
# Essential
pip install flask click pyyaml openapi-spec-validator

# Recommended
pip install opentelemetry-api opentelemetry-sdk pytest-bdd

# Advanced
pip install grpcio grpcio-tools fastmcp
```

### Environment Setup

```bash
# 1. Create project structure
mkdir -p capability-server/{core,api,cli,tests}
cd capability-server

# 2. Initialize git
git init

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## Tiered Adoption Overview

### Essential Tier (1-2 weeks)

**Goal**: Establish contract-first design with REST API + CLI

**Deliverables**:
- [ ] OpenAPI 3.x specification (`openapi.yaml`)
- [ ] CLI specification (`cli-spec.md`)
- [ ] Core domain logic (interface-agnostic)
- [ ] REST API implementation (Flask/FastAPI)
- [ ] CLI implementation (Click)
- [ ] Error mapping table
- [ ] Basic documentation

**Time Estimate**: 40-60 hours

---

### Recommended Tier (2-4 weeks)

**Goal**: Add versioning, observability, and backward compatibility

**Deliverables**:
- [ ] API versioning (`/api/v1/`)
- [ ] Correlation ID propagation
- [ ] Structured logging (JSON format)
- [ ] Backward compatibility tests
- [ ] Interface consistency tests
- [ ] Deprecation strategy

**Time Estimate**: 60-80 hours (includes Essential)

---

### Advanced Tier (4-8 weeks)

**Goal**: Implement high-performance interfaces and optimizations

**Deliverables**:
- [ ] gRPC interface with proto definitions
- [ ] MCP integration via Gateway
- [ ] Auto-generated SDKs (Python, TypeScript)
- [ ] Shell autocompletion for CLI
- [ ] Hypermedia links (HATEOAS)
- [ ] API gateway integration (Envoy)

**Time Estimate**: 100-150 hours (includes Essential + Recommended)

---

## Essential Tier: Contract-First Basics

### Phase 1: Domain Modeling (Day 1)

#### Step 1.1: Identify Domain Concepts

**Brainstorm nouns and verbs** for your capability:

**Example** (Orchestrator capability):

**Nouns** (Resources):
- Environment
- Deployment
- ServiceInstance
- Configuration

**Verbs** (Operations):
- Create
- Update
- Delete
- List
- Scale
- Rollback

**Document in** `domain-glossary.md`:
```markdown
# Orchestrator Domain Glossary

## Concepts

### Environment
A logical grouping of deployments (e.g., prod, staging, dev).

### Deployment
An instance of a service running in an environment with specific configuration (replicas, image, etc.).

### Service Instance
A single running instance of a deployment (1 of N replicas).

## Operations

### Create
Initialize a new resource (environment or deployment).

### Scale
Adjust the number of replicas for a deployment.
```

#### Step 1.2: Define Aggregates and Boundaries

**Identify parent-child relationships**:
```
Environment (aggregate root)
└─ Deployment (child)
   └─ ServiceInstance (child of deployment)
```

**Result**: `POST /environments/{envId}/deployments` (deployment is child of environment)

#### Step 1.3: Establish Naming Conventions

**Decide on case and terminology**:
- **REST JSON**: `snake_case` for fields (`environment_id`, `created_at`)
- **REST URLs**: `kebab-case` for paths (`/service-instances`)
- **CLI**: `kebab-case` for commands and `--flags`
- **Code**: `snake_case` for Python (`def create_deployment`)

**Document in** `style-guide.md`

---

### Phase 2: Contract Definition (Day 2-3)

#### Step 2.1: Write OpenAPI Specification

**File**: `openapi.yaml`

Start with skeleton:
```yaml
openapi: 3.0.0
info:
  title: Orchestrator API
  version: 1.0.0
servers:
  - url: http://localhost:8080/api/v1
paths: {}
components:
  schemas: {}
```

**Add first endpoint**:
```yaml
paths:
  /environments/{envId}/deployments:
    post:
      summary: Create deployment
      operationId: createDeployment
      tags: [Deployments]
      parameters:
        - name: envId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DeploymentConfig'
      responses:
        '201':
          description: Deployment created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Deployment'
        '400':
          description: Invalid configuration
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

components:
  schemas:
    DeploymentConfig:
      type: object
      required: [service, replicas, image]
      properties:
        service:
          type: string
          pattern: '^[a-z0-9-]+$'
        replicas:
          type: integer
          minimum: 1
        image:
          type: string

    Deployment:
      type: object
      properties:
        id: {type: string}
        environment_id: {type: string}
        service: {type: string}
        replicas: {type: integer}
        status:
          type: string
          enum: [creating, running, failed]
        created_at:
          type: string
          format: date-time

    Error:
      type: object
      required: [error]
      properties:
        error:
          type: object
          required: [code, message]
          properties:
            code: {type: string}
            message: {type: string}
            field: {type: string}
```

**Validate spec**:
```bash
openapi-spec-validator openapi.yaml
```

#### Step 2.2: Write CLI Specification

**File**: `cli-spec.md`

```markdown
# Orchestrator CLI Specification

## Command: deployment create

**Usage**:
```bash
chora-orch deployment create [OPTIONS]
```

**Options**:
- `--env <env-id>` (required): Environment ID
- `--service <name>` (required): Service name
- `--replicas <count>` (required): Number of replicas (>= 1)
- `--image <image>` (required): Container image
- `--json` (optional): Output as JSON

**Examples**:
```bash
chora-orch deployment create --env prod --service webapp --replicas 3 --image nginx:latest
```

**Exit Codes**:
- 0: Success
- 1: Error (validation, not found, etc.)
- 2: Usage error (missing required option)

**Error Output** (stderr):
```
Error: Invalid deployment config: replicas must be >= 1 (field: replicas)
```
```

#### Step 2.3: Review Contracts

**Conduct design review**:
1. Share `openapi.yaml` and `cli-spec.md` with team
2. Check naming consistency (REST `replicas` = CLI `--replicas`)
3. Validate error responses are consistent
4. Confirm success criteria match use cases

**Approval Gate**: Contracts must be approved before implementation

---

### Phase 3: Core Implementation (Day 4-6)

#### Step 3.1: Define Core Exceptions

**File**: `core/exceptions.py`

```python
class CapabilityError(Exception):
    """Base exception for capability-specific errors"""
    def __init__(self, message: str, **context):
        super().__init__(message)
        self.message = message
        self.context = context


class ValidationError(CapabilityError):
    """Raised when input validation fails"""
    def __init__(self, message: str, field: str = None):
        super().__init__(message, field=field)
        self.field = field


class ResourceNotFoundError(CapabilityError):
    """Raised when resource doesn't exist"""
    def __init__(self, resource_type: str, resource_id: str):
        message = f"{resource_type} '{resource_id}' not found"
        super().__init__(message, resource_type=resource_type, resource_id=resource_id)
        self.resource_type = resource_type
        self.resource_id = resource_id


class AlreadyExistsError(CapabilityError):
    """Raised when resource already exists"""
    def __init__(self, resource_type: str, resource_id: str):
        message = f"{resource_type} '{resource_id}' already exists"
        super().__init__(message, resource_type=resource_type, resource_id=resource_id)
```

#### Step 3.2: Implement Core Logic

**File**: `core/orchestrator.py`

```python
from typing import Dict, Any
from core.exceptions import ValidationError, ResourceNotFoundError
from core.models import Deployment
import re


class OrchestratorService:
    """Core orchestrator logic (interface-agnostic)"""

    def __init__(self, deployment_repo, environment_repo):
        self.deployment_repo = deployment_repo
        self.environment_repo = environment_repo

    def create_deployment(self, env_id: str, config: Dict[str, Any]) -> Deployment:
        """
        Create a new deployment in an environment.

        Args:
            env_id: Environment ID
            config: Deployment configuration with keys:
                - service (str): Service name
                - replicas (int): Number of replicas
                - image (str): Container image

        Returns:
            Created Deployment object

        Raises:
            ValidationError: If configuration is invalid
            ResourceNotFoundError: If environment doesn't exist
        """
        # Validate environment exists
        environment = self.environment_repo.get_by_id(env_id)
        if not environment:
            raise ResourceNotFoundError("Environment", env_id)

        # Validate configuration
        self._validate_config(config)

        # Create deployment
        deployment = Deployment(
            environment_id=env_id,
            service=config["service"],
            replicas=config["replicas"],
            image=config["image"],
            status="creating"
        )

        # Persist
        deployment = self.deployment_repo.create(deployment)

        return deployment

    def _validate_config(self, config: Dict[str, Any]):
        """Validate deployment configuration"""
        # Check required fields
        required = ["service", "replicas", "image"]
        for field in required:
            if field not in config:
                raise ValidationError(f"Missing required field: {field}", field=field)

        # Validate replicas
        replicas = config["replicas"]
        if not isinstance(replicas, int) or replicas < 1:
            raise ValidationError("replicas must be >= 1", field="replicas")

        # Validate service name
        service = config["service"]
        if not re.match(r"^[a-z0-9-]+$", service):
            raise ValidationError(
                "service name must be alphanumeric and hyphens only",
                field="service"
            )
```

#### Step 3.3: Create Error Mapping Table

**File**: `docs/error-mapping.md`

| Core Exception | REST Status | REST Code | CLI Exit Code | CLI Message Format |
|----------------|-------------|-----------|---------------|-------------------|
| `ValidationError` | 400 | `VALIDATION_ERROR` | 1 | `Error: Invalid config: {message} (field: {field})` |
| `ResourceNotFoundError` | 404 | `RESOURCE_NOT_FOUND` | 1 | `Error: {resource_type} '{resource_id}' not found` |
| `AlreadyExistsError` | 409 | `RESOURCE_ALREADY_EXISTS` | 1 | `Error: {resource_type} '{resource_id}' already exists` |
| Generic `Exception` | 500 | `INTERNAL_ERROR` | 1 | `Error: An unexpected error occurred` |

---

### Phase 4: REST API Implementation (Day 7-9)

#### Step 4.1: Implement REST Adapter

**File**: `api/rest.py`

```python
from flask import Flask, request, jsonify
import uuid
import logging
from core.orchestrator import OrchestratorService
from core.exceptions import ValidationError, ResourceNotFoundError, AlreadyExistsError

app = Flask(__name__)
logger = logging.getLogger(__name__)


def generate_request_id():
    return str(uuid.uuid4())


@app.before_request
def set_request_id():
    request.request_id = request.headers.get("X-Request-ID", generate_request_id())


@app.after_request
def add_request_id_header(response):
    response.headers["X-Request-ID"] = request.request_id
    return response


@app.route("/api/v1/environments/<env_id>/deployments", methods=["POST"])
def create_deployment(env_id):
    """Create deployment endpoint (REST adapter)"""
    data = request.get_json()
    orchestrator = get_orchestrator_service()  # Dependency injection

    try:
        deployment = orchestrator.create_deployment(env_id, data)

        # Translate core object to JSON response
        response_body = {
            "id": deployment.id,
            "environment_id": deployment.environment_id,
            "service": deployment.service,
            "replicas": deployment.replicas,
            "status": deployment.status,
            "created_at": deployment.created_at.isoformat()
        }

        logger.info(f"Created deployment {deployment.id} in environment {env_id}")
        return jsonify(response_body), 201

    except ValidationError as e:
        # Map to 400 Bad Request
        logger.warning(f"Validation error: {e.message}")
        error_body = {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": e.message
            }
        }
        if e.field:
            error_body["error"]["field"] = e.field
        return jsonify(error_body), 400

    except ResourceNotFoundError as e:
        # Map to 404 Not Found
        logger.warning(f"Resource not found: {e.message}")
        return jsonify({
            "error": {
                "code": "RESOURCE_NOT_FOUND",
                "message": e.message
            }
        }), 404

    except Exception as e:
        # Catch-all for unexpected errors
        logger.exception(f"Unexpected error: {e}")
        return jsonify({
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred"
            }
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

#### Step 4.2: Validate Against OpenAPI Contract

**File**: `tests/test_contract_rest.py`

```python
import pytest
from openapi_spec_validator import validate_spec
import yaml

def test_openapi_spec_valid():
    """Ensure OpenAPI spec is valid"""
    with open("openapi.yaml") as f:
        spec = yaml.safe_load(f)
    validate_spec(spec)  # Raises if invalid


def test_create_deployment_matches_contract(client):
    """Test that REST endpoint matches OpenAPI contract"""
    response = client.post("/api/v1/environments/test/deployments", json={
        "service": "webapp",
        "replicas": 3,
        "image": "nginx:latest"
    })

    assert response.status_code == 201
    data = response.get_json()

    # Validate required fields from OpenAPI schema
    assert "id" in data
    assert "environment_id" in data
    assert data["service"] == "webapp"
    assert data["replicas"] == 3
    assert data["status"] in ["creating", "running", "failed"]
```

---

### Phase 5: CLI Implementation (Day 10-12)

#### Step 5.1: Implement CLI Adapter

**File**: `cli/commands.py`

```python
import click
import sys
import json
from core.orchestrator import OrchestratorService
from core.exceptions import ValidationError, ResourceNotFoundError


@click.group()
def cli():
    """Orchestrator CLI"""
    pass


@cli.group()
def deployment():
    """Deployment management commands"""
    pass


@deployment.command("create")
@click.option("--env", required=True, help="Environment ID")
@click.option("--service", required=True, help="Service name")
@click.option("--replicas", type=int, required=True, help="Number of replicas")
@click.option("--image", required=True, help="Container image")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def deployment_create(env, service, replicas, image, output_json):
    """Create a new deployment"""
    config = {
        "service": service,
        "replicas": replicas,
        "image": image
    }

    orchestrator = get_orchestrator_service()  # Dependency injection

    try:
        deployment = orchestrator.create_deployment(env, config)

        if output_json:
            # JSON output for scripting
            output = {
                "id": deployment.id,
                "environment_id": deployment.environment_id,
                "service": deployment.service,
                "replicas": deployment.replicas,
                "status": deployment.status
            }
            click.echo(json.dumps(output))
        else:
            # Human-readable output
            click.echo("✓ Deployment created successfully")
            click.echo(f"  ID:          {deployment.id}")
            click.echo(f"  Environment: {deployment.environment_id}")
            click.echo(f"  Service:     {deployment.service}")
            click.echo(f"  Replicas:    {deployment.replicas}")
            click.echo(f"  Status:      {deployment.status}")

        sys.exit(0)

    except ValidationError as e:
        # Map to CLI error message
        msg = f"Invalid deployment config: {e.message}"
        if e.field:
            msg += f" (field: {e.field})"
        click.echo(f"Error: {msg}", err=True)
        sys.exit(1)

    except ResourceNotFoundError as e:
        click.echo(f"Error: {e.message}", err=True)
        sys.exit(1)

    except Exception as e:
        click.echo(f"Error: An unexpected error occurred", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
```

#### Step 5.2: Add Help Documentation

Ensure `--help` is comprehensive:

```bash
$ chora-orch deployment create --help

Create a new deployment.

Usage:
  chora-orch deployment create [OPTIONS]

Options:
  --env <env-id>         Environment ID (required)
  --service <name>       Service name (required)
  --replicas <count>     Number of replicas (required, >= 1)
  --image <image>        Container image (required)
  --json                 Output as JSON
  -h, --help             Show this help message

Examples:
  chora-orch deployment create --env prod --service webapp --replicas 3 --image nginx:latest
  chora-orch deployment create --env staging --service api --replicas 5 --image myapp:v1.2 --json
```

---

### Phase 6: Testing & Documentation (Day 13-14)

#### Step 6.1: Interface Consistency Tests

**File**: `tests/test_consistency.py`

```python
import subprocess
import json

def test_rest_and_cli_consistency(api_client):
    """Ensure REST and CLI produce same deployment"""
    # Create via REST
    rest_response = api_client.post("/api/v1/environments/test/deployments", json={
        "service": "test-svc",
        "replicas": 2,
        "image": "nginx:1.21"
    })
    rest_data = rest_response.get_json()

    # Create via CLI
    cli_result = subprocess.run([
        "chora-orch", "deployment", "create",
        "--env", "test",
        "--service", "test-svc",
        "--replicas", "2",
        "--image", "nginx:1.21",
        "--json"
    ], capture_output=True, text=True)
    cli_data = json.loads(cli_result.stdout)

    # Compare (excluding auto-generated IDs)
    assert rest_data["service"] == cli_data["service"]
    assert rest_data["replicas"] == cli_data["replicas"]
    assert rest_data["image"] == cli_data["image"]
    assert rest_data["environment_id"] == cli_data["environment_id"]
```

#### Step 6.2: Write User Documentation

**File**: `docs/user-guide.md`

```markdown
# Orchestrator User Guide

## Creating Deployments

### Via REST API

```bash
curl -X POST http://localhost:8080/api/v1/environments/prod/deployments \
  -H "Content-Type: application/json" \
  -d '{"service":"webapp","replicas":3,"image":"nginx:latest"}'
```

### Via CLI

```bash
chora-orch deployment create --env prod --service webapp --replicas 3 --image nginx:latest
```

Both methods produce the same result.

## Error Handling

If you encounter an error, the message will indicate the issue:

```
Error: Invalid deployment config: replicas must be >= 1 (field: replicas)
```

Fix the configuration and retry.
```

---

## Recommended Tier: Versioning & Observability

### Phase 7: API Versioning (Day 15-17)

#### Step 7.1: Add Version to URLs

**Update**: `api/rest.py`

```python
# Change all routes from:
@app.route("/environments/<env_id>/deployments", methods=["POST"])

# To:
@app.route("/api/v1/environments/<env_id>/deployments", methods=["POST"])
```

**Update**: `openapi.yaml`

```yaml
servers:
  - url: http://localhost:8080/api/v1  # Explicit v1
```

#### Step 7.2: Define Version Support Policy

**File**: `docs/versioning-policy.md`

```markdown
# API Versioning Policy

## Supported Versions

- **v1**: Current (fully supported)
- Future versions will be announced 1 month before release

## Backward Compatibility

- **Minor versions** (v1.1, v1.2): Additive changes only (new endpoints, new optional fields)
- **Major versions** (v2): Breaking changes allowed

## Deprecation Process

1. Announce deprecation in release notes and API responses (add `X-API-Deprecated: true` header)
2. Support deprecated version for minimum 6 months
3. Remove after sunset date with final warning

## Migration Guides

When releasing v2, we will provide:
- List of breaking changes
- Code examples for migration
- Side-by-side v1/v2 comparison
```

---

### Phase 8: Observability (Day 18-20)

#### Step 8.1: Implement Correlation IDs

**Update**: `api/rest.py` (already done in Essential tier)

Ensure correlation ID is:
1. Accepted from client (`X-Request-ID` header)
2. Generated if not provided
3. Returned in response header
4. Logged in all log statements
5. Propagated to downstream service calls

#### Step 8.2: Add Structured Logging

**File**: `core/logging_config.py`

```python
import logging
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", None),
        }

        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ["name", "msg", "args", "created", "filename", "funcName",
                          "levelname", "levelno", "lineno", "module", "msecs",
                          "message", "pathname", "process", "processName", "relativeCreated",
                          "thread", "threadName", "request_id"]:
                log_data[key] = value

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
```

**Usage in code**:
```python
logger.info("Creating deployment", extra={
    "request_id": request.request_id,
    "env_id": env_id,
    "service": config["service"],
    "replicas": config["replicas"]
})
```

**Example log output**:
```json
{
  "timestamp": "2025-11-12T10:30:45.123Z",
  "level": "INFO",
  "logger": "api.rest",
  "message": "Creating deployment",
  "request_id": "3f8e9a7b-1234-5678-90ab-cdef12345678",
  "env_id": "prod",
  "service": "webapp",
  "replicas": 3
}
```

#### Step 8.3: Add Audit Logging

**File**: `core/audit.py`

```python
import logging
from datetime import datetime

audit_logger = logging.getLogger("audit")


def audit_log(operation: str, actor: str, resource_type: str, resource_id: str, status: str, **context):
    """Log security-relevant operations"""
    audit_record = {
        "timestamp": datetime.utcnow().isoformat(),
        "operation": operation,
        "actor": actor,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "status": status,
        **context
    }
    audit_logger.info(json.dumps(audit_record))
```

**Usage**:
```python
@app.route("/api/v1/deployments/<dep_id>", methods=["DELETE"])
@require_auth
def delete_deployment(dep_id):
    actor = g.current_user  # Set by auth middleware
    try:
        result = orchestrator.delete_deployment(dep_id)
        audit_log("deployment.delete", actor, "deployment", dep_id, "success")
        return jsonify(result), 200
    except Exception as e:
        audit_log("deployment.delete", actor, "deployment", dep_id, "failure", error=str(e))
        raise
```

---

### Phase 9: Backward Compatibility Testing (Day 21-22)

#### Step 9.1: Create Version Compatibility Tests

**File**: `tests/test_backward_compatibility.py`

```python
def test_v1_still_works_after_v1_1_release():
    """Ensure v1.0 clients work after v1.1 release"""
    # v1.0 request (minimal fields)
    v1_request = {
        "service": "webapp",
        "replicas": 3,
        "image": "nginx:latest"
    }
    response = client.post("/api/v1/environments/test/deployments", json=v1_request)
    assert response.status_code == 201

    # v1.1 request (with new optional field)
    v1_1_request = {
        "service": "webapp",
        "replicas": 3,
        "image": "nginx:latest",
        "health_check": {"path": "/health", "interval": 10}  # New in v1.1
    }
    response = client.post("/api/v1/environments/test/deployments", json=v1_1_request)
    assert response.status_code == 201
```

---

## Advanced Tier: Multi-Protocol & Optimization

### Phase 10: gRPC Interface (Week 4-5)

#### Step 10.1: Define Proto File

**File**: `proto/orchestrator.proto`

```protobuf
syntax = "proto3";

package chora.orchestrator.v1;

service OrchestratorService {
  rpc CreateDeployment(CreateDeploymentRequest) returns (Deployment);
  rpc GetDeployment(GetDeploymentRequest) returns (Deployment);
  rpc ListDeployments(ListDeploymentsRequest) returns (ListDeploymentsResponse);
  rpc DeleteDeployment(DeleteDeploymentRequest) returns (google.protobuf.Empty);
}

message CreateDeploymentRequest {
  string env_id = 1;
  DeploymentConfig config = 2;
}

message DeploymentConfig {
  string service = 1;
  int32 replicas = 2;
  string image = 3;
}

message Deployment {
  string id = 1;
  string environment_id = 2;
  string service = 3;
  int32 replicas = 4;
  DeploymentStatus status = 5;
}

enum DeploymentStatus {
  DEPLOYMENT_STATUS_UNSPECIFIED = 0;
  DEPLOYMENT_STATUS_CREATING = 1;
  DEPLOYMENT_STATUS_RUNNING = 2;
  DEPLOYMENT_STATUS_FAILED = 3;
}

// ... other messages
```

#### Step 10.2: Generate gRPC Code

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/orchestrator.proto
```

#### Step 10.3: Implement gRPC Server

**File**: `api/grpc_server.py`

```python
import grpc
from concurrent import futures
from proto import orchestrator_pb2, orchestrator_pb2_grpc
from core.orchestrator import OrchestratorService
from core.exceptions import ValidationError, ResourceNotFoundError


class OrchestratorServicer(orchestrator_pb2_grpc.OrchestratorServiceServicer):
    def __init__(self, orchestrator_service):
        self.orchestrator = orchestrator_service

    def CreateDeployment(self, request, context):
        config = {
            "service": request.config.service,
            "replicas": request.config.replicas,
            "image": request.config.image,
        }

        try:
            deployment = self.orchestrator.create_deployment(request.env_id, config)

            return orchestrator_pb2.Deployment(
                id=deployment.id,
                environment_id=deployment.environment_id,
                service=deployment.service,
                replicas=deployment.replicas,
                status=map_status_to_proto(deployment.status)
            )

        except ValidationError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(e.message)
            return orchestrator_pb2.Deployment()

        except ResourceNotFoundError as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(e.message)
            return orchestrator_pb2.Deployment()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orchestrator_pb2_grpc.add_OrchestratorServiceServicer_to_server(
        OrchestratorServicer(get_orchestrator_service()), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
```

---

### Phase 11: SDK Generation & Shell Autocompletion (Week 6-7)

#### Step 11.1: Generate Python SDK from OpenAPI

```bash
openapi-generator-cli generate \
  -i openapi.yaml \
  -g python \
  -o sdk/python \
  --package-name orchestrator_client
```

#### Step 11.2: Add Shell Autocompletion

**File**: `cli/completion.py`

```python
import click

@cli.command()
@click.option("--shell", type=click.Choice(["bash", "zsh", "fish"]), required=True)
def completion(shell):
    """Generate shell completion script"""
    if shell == "bash":
        click.echo(_BASH_COMPLETION_SCRIPT)
    elif shell == "zsh":
        click.echo(_ZSH_COMPLETION_SCRIPT)
    # ...

_BASH_COMPLETION_SCRIPT = """
_chora_orch_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    if [ $COMP_CWORD -eq 1 ]; then
        opts="deployment environment help"
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi

    # ... more completion logic
}
complete -F _chora_orch_completion chora-orch
"""
```

**Install**:
```bash
chora-orch completion --shell bash >> ~/.bashrc
source ~/.bashrc
```

---

## Validation & Quality Gates

### Quality Gate 1: Contract Validation

**Criteria**:
- [ ] OpenAPI spec passes `openapi-spec-validator`
- [ ] Proto files compile without errors
- [ ] CLI help text matches spec documentation

**Command**:
```bash
# Validate OpenAPI
openapi-spec-validator openapi.yaml

# Validate proto
protoc --proto_path=. --python_out=. proto/orchestrator.proto

# Check CLI help
chora-orch deployment create --help | grep --all required flags present
```

---

### Quality Gate 2: Interface Consistency

**Criteria**:
- [ ] REST and CLI produce same results for same operation
- [ ] Errors map consistently across interfaces
- [ ] Naming is consistent (REST `replicas` = CLI `--replicas`)

**Test**:
```bash
pytest tests/test_consistency.py
```

---

### Quality Gate 3: Backward Compatibility

**Criteria**:
- [ ] v1.0 clients still work after v1.1 release
- [ ] No breaking changes in minor versions
- [ ] Deprecated features have warnings

**Test**:
```bash
pytest tests/test_backward_compatibility.py
```

---

### Quality Gate 4: Observability

**Criteria**:
- [ ] 100% of requests have correlation ID
- [ ] Structured logs (JSON format) with request_id
- [ ] Security-relevant operations audit logged

**Validation**:
```bash
# Check logs have request_id
curl -X POST http://localhost:8080/api/v1/environments/test/deployments \
  -H "X-Request-ID: test-123" \
  -d '{"service":"test","replicas":1,"image":"nginx"}'

# Check logs
tail -f logs/app.log | jq '.request_id' | grep "test-123"
```

---

## Migration Guide (Existing Projects)

### Scenario: Retrofit Contract-First Design

**Starting Point**: Existing capability server with code-first API

**Steps**:

1. **Extract OpenAPI spec from existing code** (1-2 days)
   ```bash
   # If using FastAPI, auto-generate
   curl http://localhost:8080/openapi.json > openapi.yaml

   # If using Flask, manually document endpoints
   ```

2. **Review and fix inconsistencies** (1 day)
   - Check naming (camelCase vs snake_case)
   - Validate error responses
   - Ensure required/optional fields correct

3. **Implement core-interface separation** (3-5 days)
   - Extract business logic to `core/` module
   - Refactor Flask routes to be thin adapters
   - Move validation to core

4. **Add CLI** (2-3 days)
   - Write `cli-spec.md`
   - Implement CLI using Click
   - Ensure consistency with REST API

5. **Add tests** (2 days)
   - Contract tests (validate against OpenAPI)
   - Consistency tests (REST == CLI)
   - Backward compatibility tests

**Total Time**: 2-3 weeks

---

## Success Metrics

### Essential Tier

- [ ] OpenAPI spec exists and validates
- [ ] CLI spec documented
- [ ] Core logic has 0 imports of Flask/Click
- [ ] Error mapping table complete
- [ ] Consistency tests passing

**Time Saved**: 40% reduction in interface-related bugs, 2x faster client integration

### Recommended Tier

- [ ] API versioned (`/api/v1/`)
- [ ] Correlation IDs in 100% of requests
- [ ] Structured logging (JSON)
- [ ] Backward compatibility maintained

**Time Saved**: 50% reduction in debugging time, 0 backward compatibility breaks

### Advanced Tier

- [ ] gRPC interface working
- [ ] MCP integration complete
- [ ] SDKs auto-generated
- [ ] Shell autocompletion installed

**Time Saved**: 70% reduction in high-performance integration time

---

## Next Steps

1. **Track Progress**: Use checklist above and update [ledger.md](./ledger.md)
2. **Get Help**: See [AGENTS.md](./AGENTS.md) for quick reference
3. **Validate**: Run quality gates before marking tier complete
4. **Self-Evaluate**: Apply SAP-019 self-evaluation framework when done

---

**Version**: 1.0.0
**Last Updated**: 2025-11-12
