# SAP-047: CapabilityServer-Template - Protocol Specification

**SAP ID**: SAP-047
**Name**: CapabilityServer-Template
**Version**: 1.0.0
**Status**: Pilot
**Created**: 2025-11-12
**Last Updated**: 2025-11-12

---

## Purpose

This document provides the complete technical specification for SAP-047 (CapabilityServer-Template), including:
- Template structure and generation script configuration
- Generated project file specifications
- Module interfaces and contracts
- Configuration file formats
- Build and deployment specifications
- Testing and CI/CD configurations

---

## 1. Template Structure

### 1.1 Generation Script Configuration

**Script**: `scripts/create-capability-server.py`

**CLI Arguments**:

```python
parser.add_argument('--name', required=True,
                   help='Capability name (e.g., "Analyzer", "Validator")')
parser.add_argument('--namespace', default='chora',
                   help='Python namespace (default: chora)')
parser.add_argument('--description', default='A capability server',
                   help='Project description')
parser.add_argument('--author', default='Your Name',
                   help='Author name')
parser.add_argument('--email', default='your.email@example.com',
                   help='Author email')
parser.add_argument('--python-version', default='3.11',
                   choices=['3.11', '3.10', '3.9'],
                   help='Python version (default: 3.11)')
parser.add_argument('--enable-mcp', action='store_true',
                   help='Enable MCP server interface')
parser.add_argument('--enable-saga', action='store_true',
                   help='Enable Saga orchestration pattern')
parser.add_argument('--enable-circuit-breaker', action='store_true',
                   help='Enable circuit breaker pattern')
parser.add_argument('--enable-event-bus', action='store_true',
                   help='Enable event bus pattern')
parser.add_argument('--license', default='MIT',
                   choices=['MIT', 'Apache-2.0', 'BSD-3-Clause', 'Proprietary'],
                   help='License type (default: MIT)')
parser.add_argument('--output', required=True,
                   help='Output directory for generated project')
```

**Derived Variables** (computed by script):
- `project_slug`: Auto-generated from name (lowercase, hyphens)
- `year`: Current year from `datetime.now().year`
- `fastapi_version`: Fixed at "0.104.1"
- `click_version`: Fixed at "8.1.7"
- `fastmcp_version`: Fixed at "0.1.0"

---

### 1.2 Directory Structure

**Generated Project Layout**:

```
{{project_slug}}/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── docker-compose.yml
│
├── src/
│   └── {{namespace}}/
│       └── {{project_slug}}/
│           ├── __init__.py
│           ├── __version__.py
│           │
│           ├── core/
│           │   ├── __init__.py
│           │   ├── capability.py
│           │   ├── models.py
│           │   └── exceptions.py
│           │
│           ├── interfaces/
│           │   ├── __init__.py
│           │   ├── cli.py
│           │   ├── rest.py
│           │   └── mcp.py          # If enable_mcp=yes
│           │
│           ├── registry/
│           │   ├── __init__.py
│           │   ├── client.py
│           │   └── heartbeat.py
│           │
│           ├── bootstrap/
│           │   ├── __init__.py
│           │   └── startup.py
│           │
│           └── composition/
│               ├── __init__.py
│               ├── saga.py         # If enable_saga=yes
│               ├── circuit_breaker.py  # If enable_circuit_breaker=yes
│               └── events.py       # If enable_event_bus=yes
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_core/
│   │   ├── __init__.py
│   │   ├── test_capability.py
│   │   └── test_models.py
│   ├── test_interfaces/
│   │   ├── __init__.py
│   │   ├── test_cli.py
│   │   ├── test_rest.py
│   │   └── test_mcp.py
│   └── test_integration/
│       ├── __init__.py
│       └── test_end_to_end.py
│
├── config/
│   ├── manifest.yaml
│   ├── config.yaml
│   ├── sagas.yaml              # If enable_saga=yes
│   └── circuit_breakers.yaml  # If enable_circuit_breaker=yes
│
├── docs/
│   ├── AGENTS.md
│   ├── API.md
│   ├── CLI.md
│   └── DEVELOPMENT.md
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── cd.yml
│       └── quality-gates.yml
│
└── scripts/
    ├── bootstrap.py
    ├── dev-setup.sh
    └── deploy.sh
```

---

## 2. Module Specifications

### 2.1 Core Capability Module

**File**: `src/{{namespace}}/{{project_slug}}/core/capability.py`

**Interface Contract**:

```python
"""
Core capability interface.
All capability servers MUST implement this interface.
"""
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel

class CapabilityInput(BaseModel):
    """Base input model for capability execution."""
    pass

class CapabilityOutput(BaseModel):
    """Base output model for capability execution."""
    status: str
    result: Dict[str, Any]

class BaseCapability(ABC):
    """
    Base capability interface.

    All capability servers must inherit from this class and implement
    the required methods.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize capability with configuration.

        Args:
            config: Configuration dictionary
        """
        self.config = config

    @abstractmethod
    async def execute(self, input_data: CapabilityInput) -> CapabilityOutput:
        """
        Execute capability (core business logic).

        Args:
            input_data: Input parameters

        Returns:
            Execution result

        Raises:
            CapabilityError: If execution fails
        """
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, str]:
        """
        Health check for service readiness.

        Returns:
            Health status: {"status": "healthy|degraded|unhealthy"}
        """
        pass

    async def initialize(self):
        """
        Initialize capability (optional override).

        Called during startup after config loaded but before serving.
        """
        pass

    async def shutdown(self):
        """
        Shutdown capability (optional override).

        Called during graceful shutdown, perform cleanup here.
        """
        pass

    @classmethod
    def from_config(cls, config_path: str) -> "BaseCapability":
        """
        Factory method to create capability from config file.

        Args:
            config_path: Path to configuration file

        Returns:
            Initialized capability instance
        """
        import yaml
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return cls(config)

    @classmethod
    def from_env(cls) -> "BaseCapability":
        """
        Factory method to create capability from environment variables.

        Returns:
            Initialized capability instance
        """
        import os
        config = {
            "manifest_url": os.getenv("MANIFEST_URL", "http://manifest:8080"),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            # Add more env vars as needed
        }
        return cls(config)
```

**Generated Implementation**:

```python
class {{project_name}}Capability(BaseCapability):
    """
    {{project_description}}
    """

    async def execute(self, input_data: CapabilityInput) -> CapabilityOutput:
        """
        Execute {{project_name}} capability.

        TODO: Implement your business logic here.
        """
        # Example implementation:
        result = {
            "processed": True,
            "message": "Capability executed successfully"
        }
        return CapabilityOutput(status="success", result=result)

    async def health_check(self) -> Dict[str, str]:
        """Health check."""
        # TODO: Add actual health checks (database, external services, etc.)
        return {"status": "healthy"}
```

---

### 2.2 CLI Interface Module

**File**: `src/{{namespace}}/{{project_slug}}/interfaces/cli.py`

**Specification**:

```python
"""
CLI interface using Click.

Standard commands:
- execute: Execute capability
- health: Check health status
- version: Print version
- config: Show configuration
"""
import click
import json
import sys
from typing import Optional

@click.group()
@click.option('--config', default='config/config.yaml', help='Config file path')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.option('--format', type=click.Choice(['json', 'text']), default='text', help='Output format')
@click.pass_context
def cli(ctx, config, verbose, format):
    """{{project_description}} CLI."""
    from {{namespace}}.{{project_slug}}.core.capability import {{project_name}}Capability

    ctx.ensure_object(dict)
    ctx.obj['capability'] = {{project_name}}Capability.from_config(config)
    ctx.obj['verbose'] = verbose
    ctx.obj['format'] = format

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file (default: stdout)')
@click.pass_context
async def execute(ctx, input_file, output):
    """Execute capability on input file."""
    capability = ctx.obj['capability']
    output_format = ctx.obj['format']

    # Load input
    with open(input_file) as f:
        if input_file.endswith('.json'):
            input_data = json.load(f)
        elif input_file.endswith('.yaml'):
            import yaml
            input_data = yaml.safe_load(f)
        else:
            raise click.UsageError("Input file must be .json or .yaml")

    # Execute
    try:
        result = await capability.execute(input_data)

        # Format output
        if output_format == 'json':
            output_text = json.dumps(result.dict(), indent=2)
        else:
            output_text = f"Status: {result.status}\nResult: {result.result}"

        # Write output
        if output:
            with open(output, 'w') as f:
                f.write(output_text)
        else:
            click.echo(output_text)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.pass_context
async def health(ctx):
    """Check health status."""
    capability = ctx.obj['capability']
    result = await capability.health_check()
    click.echo(json.dumps(result, indent=2))

@cli.command()
def version():
    """Print version."""
    from {{namespace}}.{{project_slug}}.__version__ import __version__
    click.echo(f"{{project_name}} v{__version__}")

@cli.command()
@click.pass_context
def config(ctx):
    """Show configuration."""
    capability = ctx.obj['capability']
    click.echo(json.dumps(capability.config, indent=2))

if __name__ == '__main__':
    cli()
```

---

### 2.3 REST API Interface Module

**File**: `src/{{namespace}}/{{project_slug}}/interfaces/rest.py`

**OpenAPI Specification**:

```yaml
openapi: 3.0.3
info:
  title: {{project_name}} API
  description: {{project_description}}
  version: 1.0.0

servers:
  - url: http://localhost:8080
    description: Local development server

paths:
  /api/v1/execute:
    post:
      summary: Execute capability
      operationId: execute
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ExecuteRequest'
      responses:
        '200':
          description: Execution successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ExecuteResponse'
        '400':
          description: Invalid input
        '500':
          description: Server error

  /health:
    get:
      summary: Health check
      responses:
        '200':
          description: Service healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    enum: [healthy, degraded, unhealthy]

  /ready:
    get:
      summary: Readiness probe
      responses:
        '200':
          description: Service ready

components:
  schemas:
    ExecuteRequest:
      type: object
      properties:
        input_data:
          type: object

    ExecuteResponse:
      type: object
      properties:
        status:
          type: string
        result:
          type: object
```

**FastAPI Implementation**:

```python
"""REST API interface using FastAPI."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any
import logging

from {{namespace}}.{{project_slug}}.core.capability import (
    {{project_name}}Capability,
    CapabilityInput,
    CapabilityOutput
)

app = FastAPI(
    title="{{project_name}} API",
    description="{{project_description}}",
    version="1.0.0"
)

# Initialize capability
capability = {{project_name}}Capability.from_env()

class ExecuteRequest(BaseModel):
    """Execute request model."""
    input_data: Dict[str, Any]

@app.post("/api/v1/execute", response_model=CapabilityOutput)
async def execute(request: ExecuteRequest):
    """Execute capability."""
    try:
        input_data = CapabilityInput(**request.input_data)
        result = await capability.execute(input_data)
        return result
    except Exception as e:
        logging.error(f"Execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check endpoint."""
    return await capability.health_check()

@app.get("/ready")
async def ready():
    """Readiness probe."""
    return {"status": "ready"}

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    # TODO: Implement actual metrics collection
    return {
        "requests_total": 0,
        "errors_total": 0,
        "duration_seconds": 0.0
    }

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": str(type(exc).__name__)}
    )

# Startup/shutdown events
@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    await capability.initialize()
    logging.info("{{project_name}} API started")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    await capability.shutdown()
    logging.info("{{project_name}} API stopped")
```

---

### 2.4 MCP Server Interface Module

**File**: `src/{{namespace}}/{{project_slug}}/interfaces/mcp.py`

(Generated only if `enable_mcp=yes`)

**Specification**:

```python
"""MCP server interface using FastMCP."""
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

from {{namespace}}.{{project_slug}}.core.capability import (
    {{project_name}}Capability
)

mcp = FastMCP("{{project_slug}}")
capability = {{project_name}}Capability.from_env()

@mcp.tool()
async def execute(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute {{project_name}} capability.

    Args:
        input_data: Input parameters for execution

    Returns:
        Execution result
    """
    result = await capability.execute(input_data)
    return result.dict()

@mcp.tool()
async def health() -> Dict[str, str]:
    """
    Check health status of {{project_name}} service.

    Returns:
        Health status (healthy, degraded, unhealthy)
    """
    return await capability.health_check()

if __name__ == "__main__":
    mcp.run()
```

---

## 3. Configuration File Formats

### 3.1 Service Manifest

**File**: `config/manifest.yaml`

```yaml
# Service manifest for registry (SAP-044)
service:
  name: "{{project_slug}}"
  version: "1.0.0"
  description: "{{project_description}}"
  namespace: "{{namespace}}"

  # Service endpoints
  endpoints:
    rest:
      url: "http://{{project_slug}}:8080"
      health_check: "/health"
      ready_check: "/ready"
      metrics: "/metrics"

    cli:
      command: "{{project_slug}}"
      available: true

    {% if enable_mcp %}
    mcp:
      url: "mcp://{{project_slug}}:8081"
      protocol_version: "1.0"
    {% endif %}

  # Dependencies
  dependencies:
    - name: "manifest-registry"
      version: ">=1.0.0"
      required: true
      health_check: "http://manifest:8080/health"

  # Health checks
  health:
    startup_timeout: 60  # seconds
    heartbeat_interval: 10  # seconds
    failure_threshold: 3

  # Capabilities
  capabilities:
    - execute
    - health_check

  # Metadata
  metadata:
    author: "{{author_name}}"
    license: "{{license}}"
    repository: "https://github.com/{{namespace}}/{{project_slug}}"
```

---

### 3.2 Runtime Configuration

**File**: `config/config.yaml`

```yaml
# Runtime configuration
service:
  name: "{{project_slug}}"
  port: 8080
  log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR

# Registry (v5.2.0+: Production EtcdRegistryBackend)
registry:
  enabled: true
  manifest_url: "http://manifest:8080"
  heartbeat_interval: 30  # seconds
  heartbeat_timeout: 30  # seconds
  # etcd connection (for chora-manifest EtcdRegistryBackend)
  etcd_host: "localhost"  # Use 'etcd1' inside Docker network
  etcd_port: 2379
  auto_discovery: true

# Capability-specific settings
capability:
  # TODO: Add your capability-specific settings here
  # Example:
  # max_workers: 4
  # timeout: 30

# Optional: Database settings
{% if enable_saga %}
database:
  connection_string: "sqlite:///saga_state.db"
  # For production: "postgresql://user:pass@localhost:5432/dbname"
{% endif %}

# Optional: Event bus settings
{% if enable_event_bus %}
event_bus:
  backend: "redis"  # redis, nats, memory
  redis:
    host: "localhost"
    port: 6379
    db: 0
{% endif %}
```

---

### 3.3 Configuration Loading Pattern

**Pattern**: Centralized config loading with helper utilities for parsing YAML configuration.

**File**: `src/{{namespace}}/{{project_slug}}/config/__init__.py`

```python
"""Configuration module for {{project_slug}}."""

from .loader import load_config

__all__ = ["load_config"]
```

**File**: `src/{{namespace}}/{{project_slug}}/config/loader.py`

```python
"""
Configuration loader for {{project_slug}}.

Loads runtime configuration from YAML file with sensible defaults.
"""

import yaml
from pathlib import Path
from typing import Dict, Optional


def load_config(config_path: Optional[str] = None) -> Dict:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to config.yaml file. If None, uses default location
                    (config/config.yaml relative to package root).

    Returns:
        Configuration dictionary with all settings.

    Raises:
        FileNotFoundError: If config file doesn't exist.
        yaml.YAMLError: If config file has invalid YAML syntax.

    Example:
        >>> config = load_config()
        >>> etcd_host = config['registry']['etcd_host']
        >>> print(f"Connecting to etcd at {etcd_host}")
    """
    if config_path is None:
        # Default: config/config.yaml relative to package root
        # This file is at: src/{{namespace}}/{{project_slug}}/config/loader.py
        # Package root is: ../../..
        # Config file is: ../../../config/config.yaml
        package_root = Path(__file__).parent.parent.parent.parent
        config_path = package_root / "config" / "config.yaml"
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}\n"
            f"Expected location: {config_path.absolute()}"
        )

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(
            f"Invalid YAML syntax in {config_path}: {e}"
        ) from e

    if config is None:
        config = {}

    return config


def get_registry_config(config: Dict) -> Dict:
    """
    Extract registry-specific configuration.

    Args:
        config: Full configuration dictionary.

    Returns:
        Registry configuration with etcd connection settings.
    """
    registry = config.get('registry', {})

    return {
        'enabled': registry.get('enabled', True),
        'etcd_host': registry.get('etcd_host', 'localhost'),
        'etcd_port': registry.get('etcd_port', 2379),
        'heartbeat_timeout': registry.get('heartbeat_timeout', 30),
        'heartbeat_interval': registry.get('heartbeat_interval', 30),
    }


def get_http_config(config: Dict) -> Dict:
    """
    Extract HTTP server configuration.

    Args:
        config: Full configuration dictionary.

    Returns:
        HTTP server configuration settings.
    """
    http = config.get('http', {})

    return {
        'host': http.get('host', '0.0.0.0'),
        'port': http.get('port', 8080),
        'cors_enabled': http.get('cors_enabled', True),
    }
```

**Usage in CLI**:

```python
from ...config.loader import load_config, get_registry_config, get_http_config
from ...bootstrap.startup import StartupSequence

@main.command()
@click.option("--config", default=None, help="Path to config.yaml file")
@click.option("--port", default=None, help="Port (overrides config)")
def serve(config: str, port: int):
    """Start server with full registry integration."""
    async def _serve():
        # Load configuration
        cfg = load_config(config)
        http_config = get_http_config(cfg)

        # Override port from CLI if provided
        if port is None:
            port = http_config.get('port', 8080)

        # Initialize with StartupSequence
        startup = StartupSequence(cfg)
        await startup.initialize()

        # Use startup.gateway, startup.orchestrator, etc.
        # TODO: Start server with initialized components

    asyncio.run(_serve())
```

**Benefits**:
- Centralized configuration management
- Sensible defaults for all settings
- Easy to override via CLI options
- Type-safe config parsing helpers
- Clear error messages for missing/invalid config

---

### 3.4 Saga Definitions

**File**: `config/sagas.yaml` (generated if `enable_saga=yes`)

```yaml
# Saga orchestration definitions (SAP-046)
sagas:
  example_workflow:
    name: "Example Multi-Step Workflow"
    description: "Template saga for multi-step operations"
    timeout: 600  # seconds

    steps:
      - id: "step_1"
        name: "First Step"
        operation: "step_1_execute"
        timeout: 30
        compensation: "step_1_compensate"
        idempotent: true

      - id: "step_2"
        name: "Second Step"
        operation: "step_2_execute"
        timeout: 60
        compensation: "step_2_compensate"
        idempotent: true
        depends_on: ["step_1"]

      - id: "step_3"
        name: "Third Step"
        operation: "step_3_execute"
        timeout: 30
        compensation: "step_3_compensate"
        idempotent: true
        depends_on: ["step_2"]
```

---

### 3.4 Circuit Breaker Configuration

**File**: `config/circuit_breakers.yaml` (generated if `enable_circuit_breaker=yes`)

```yaml
# Circuit breaker configurations (SAP-046)
circuit_breakers:
  external_service:
    failure_threshold: 5
    success_threshold: 3
    timeout: 30  # seconds
    half_open_max_calls: 3
    exceptions:
      - ConnectionError
      - TimeoutError
      - HTTPError.5xx

  # Add more circuit breakers as needed
```

---

## 4. Build Specifications

### 4.1 pyproject.toml

```toml
[tool.poetry]
name = "{{project_slug}}"
version = "1.0.0"
description = "{{project_description}}"
authors = ["{{author_name}} <{{author_email}}>"]
license = "{{license}}"
readme = "README.md"

[tool.poetry.dependencies]
python = "^{{python_version}}"
fastapi = "^{{fastapi_version}}"
uvicorn = "^0.24.0"
click = "^{{click_version}}"
pydantic = "^2.5.0"
httpx = "^0.25.0"
pyyaml = "^6.0.1"
{% if enable_mcp %}
fastmcp = "^{{fastmcp_version}}"
{% endif %}
{% if enable_saga %}
sqlalchemy = "^2.0.0"
asyncpg = "^0.29.0"  # For PostgreSQL
{% endif %}
{% if enable_event_bus %}
redis = "^5.0.0"
{% endif %}

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
pytest-cov = "^4.1.0"
pytest-mock = "^3.12.0"
black = "^23.12.0"
ruff = "^0.1.7"
mypy = "^1.7.0"
pre-commit = "^3.6.0"

[tool.poetry.scripts]
{{project_slug}} = "{{namespace}}.{{project_slug}}.interfaces.cli:cli"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=src/{{namespace}}/{{project_slug}} --cov-report=html --cov-report=term-missing"

[tool.black]
line-length = 100
target-version = ['py{{python_version.replace(".", "")}}']

[tool.ruff]
line-length = 100
target-version = "py{{python_version.replace(".", "")}}"

[tool.mypy]
python_version = "{{python_version}}"
strict = true
warn_return_any = true
warn_unused_configs = true

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

---

### 4.2 Dockerfile

```dockerfile
# Multi-stage production Dockerfile
FROM python:{{python_version}}-slim as builder

WORKDIR /app

# Install Poetry
RUN pip install poetry==1.7.1

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies (no dev dependencies)
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY src/ src/
COPY config/ config/

# Production stage
FROM python:{{python_version}}-slim

WORKDIR /app

# Copy from builder
COPY --from=builder /usr/local/lib/python{{python_version}}/site-packages /usr/local/lib/python{{python_version}}/site-packages
COPY --from=builder /app /app

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Run application
CMD ["uvicorn", "{{namespace}}.{{project_slug}}.interfaces.rest:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

### 4.3 docker-compose.yml

```yaml
version: '3.8'

services:
  {{project_slug}}:
    build: .
    ports:
      - "8080:8080"
    environment:
      - MANIFEST_URL=http://manifest:8080
      - LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    depends_on:
      - manifest
    restart: unless-stopped

  # Manifest registry (dependency)
  manifest:
    image: chora/manifest:latest
    ports:
      - "8081:8080"
    restart: unless-stopped

  {% if enable_event_bus %}
  # Redis (for event bus)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
  {% endif %}
```

---

## 5. Testing Specifications

### 5.1 Test Configuration

**File**: `tests/conftest.py`

```python
"""Pytest configuration and fixtures."""
import pytest
import asyncio
from typing import Generator

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def capability_config():
    """Test configuration."""
    return {
        "manifest_url": "http://localhost:8080",
        "log_level": "DEBUG",
    }

@pytest.fixture
async def capability(capability_config):
    """Create test capability instance."""
    from {{namespace}}.{{project_slug}}.core.capability import {{project_name}}Capability

    cap = {{project_name}}Capability(capability_config)
    await cap.initialize()
    yield cap
    await cap.shutdown()

@pytest.fixture
def mock_manifest_client(mocker):
    """Mock manifest registry client."""
    mock = mocker.AsyncMock()
    mock.register.return_value = "service_12345"
    mock.heartbeat.return_value = None
    mock.deregister.return_value = None
    return mock
```

---

### 5.2 CI/CD Workflow

**File**: `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [{{python_version}}]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Install dependencies
        run: poetry install

      - name: Run linters
        run: |
          poetry run black --check src/ tests/
          poetry run ruff check src/ tests/
          poetry run mypy src/

      - name: Run tests
        run: poetry run pytest tests/ --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  build:
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: docker build -t {{project_slug}}:latest .

      - name: Test Docker image
        run: |
          docker run -d --name test -p 8080:8080 {{project_slug}}:latest
          sleep 10
          curl -f http://localhost:8080/health || exit 1
          docker stop test
```

---

## 6. Documentation Specifications

### 6.1 AGENTS.md Template

**File**: `docs/AGENTS.md`

```markdown
# {{project_name}} - Agent Awareness Guide

**Service**: {{project_slug}}
**Description**: {{project_description}}
**Version**: 1.0.0

## Quick Reference

**Interfaces**:
- CLI: `{{project_slug}} execute <input_file>`
- REST: `POST /api/v1/execute`
{% if enable_mcp %}
- MCP: `execute(input_data)`
{% endif %}

**Common Operations**:
1. Execute capability: [command/endpoint]
2. Check health: [command/endpoint]
3. View configuration: [command/endpoint]

**Dependencies**:
- Manifest Registry (required)

**Success Criteria**:
- [Criteria 1]
- [Criteria 2]

[Full agent awareness guide here]
```

---

## 7. Versioning

**Protocol Version**: 1.0.0

**Compatibility**:
- **Breaking Changes**: Major version bump (e.g., 1.0.0 → 2.0.0)
- **New Features**: Minor version bump (e.g., 1.0.0 → 1.1.0)
- **Bug Fixes**: Patch version bump (e.g., 1.0.0 → 1.0.1)

---

**Document Version**: 1.0.0
**Status**: Pilot
**Last Updated**: 2025-11-12
