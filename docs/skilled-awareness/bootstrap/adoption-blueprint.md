# SAP-045: Bootstrap - Adoption Blueprint

**SAP ID**: SAP-045
**Name**: Bootstrap
**Version**: 1.0.0
**Status**: Pilot
**Created**: 2025-11-12
**Last Updated**: 2025-11-12

---

## Overview

This document provides a step-by-step guide for adopting SAP-045 (Bootstrap) in your capability server project. The guide is organized into three adoption tiers:

- **Essential Tier** (1-2 weeks, 40-80 hours): Core bootstrap functionality with SQLite backend
- **Recommended Tier** (2-4 weeks, 80-160 hours): Production-ready with etcd, monitoring, CLI
- **Advanced Tier** (4-8 weeks, 160-320 hours): High availability, security hardening, performance optimization

**Recommendation**: Start with Essential Tier for development environments, then progress to Recommended for staging/production.

---

## Prerequisites

### Technical Requirements

**System**:
- Linux or macOS (Windows with WSL2)
- 4+ CPU cores
- 8+ GB RAM
- 20+ GB disk space

**Software**:
- Docker 20.10+ (with Docker Compose v2)
- Python 3.9+
- Git 2.30+

**Knowledge**:
- Docker and containerization
- Python programming
- Bash scripting
- Service orchestration concepts

### Organizational Requirements

- **Stakeholder Buy-In**: Engineering lead approval for 1-2 week project
- **Dedicated Time**: 1 engineer × 1-2 weeks (full-time) OR 2 engineers × 1 week (paired)
- **Test Environment**: Clean VM or container for validation
- **Documentation Access**: Ability to create/update runbooks

---

## Essential Tier (1-2 Weeks)

**Goal**: Implement core bootstrap functionality for development environments.

**Deliverables**:
- ✅ Bootstrap CLI with `chora bootstrap` command
- ✅ Phased startup (Phase 0-4)
- ✅ Health validation with retry logic
- ✅ State persistence and resume capability
- ✅ SQLite backend for Manifest Registry
- ✅ Idempotent operations
- ✅ Rollback to previous phase

**Time Estimate**: 40-80 hours (1-2 weeks, 1 engineer)

**Cost**: $6,000 - $12,000 (at $150/hour)

---

### Phase 1: Setup Development Environment

**Duration**: Day 1-2 (8-16 hours)

**Goal**: Prepare development environment with all dependencies.

---

#### Step 1.1: Install Prerequisites

```bash
# Verify Python version
python3 --version  # Should be 3.9+

# Install Poetry (dependency management)
curl -sSL https://install.python-poetry.org | python3 -

# Verify Docker
docker --version  # Should be 20.10+
docker-compose version  # Should be v2.x
```

**Quality Gate**: All commands return expected versions, no errors.

---

#### Step 1.2: Create Project Structure

```bash
# Create bootstrap project directory
mkdir -p chora-bootstrap
cd chora-bootstrap

# Initialize Poetry project
poetry init \
  --name chora-bootstrap \
  --description "Phased bootstrap for capability server ecosystems" \
  --author "Your Team <team@yourorg.com>" \
  --python "^3.9" \
  --no-interaction

# Add dependencies
poetry add \
  click==8.1.7 \
  docker==7.0.0 \
  aiohttp==3.9.1 \
  pydantic==2.5.2 \
  cryptography==41.0.7 \
  rich==13.7.0 \
  pyyaml==6.0.1

# Add dev dependencies
poetry add --group dev \
  pytest==7.4.3 \
  pytest-asyncio==0.21.1 \
  pytest-cov==4.1.0 \
  black==23.12.1 \
  mypy==1.7.1 \
  ruff==0.1.8
```

**Directory Structure**:
```
chora-bootstrap/
├── pyproject.toml
├── README.md
├── chora_bootstrap/
│   ├── __init__.py
│   ├── cli.py          # Click CLI interface
│   ├── phases.py       # Phase implementations
│   ├── state.py        # State management
│   ├── health.py       # Health checking
│   ├── credentials.py  # Credential generation
│   └── config.py       # Configuration loading
├── tests/
│   ├── test_phases.py
│   ├── test_state.py
│   └── test_health.py
└── .chora/
    └── bootstrap-config.yml  # Default configuration
```

**Quality Gate**: `poetry install` completes without errors, project structure created.

---

#### Step 1.3: Configure Development Tools

**pyproject.toml** (add these sections):
```toml
[tool.black]
line-length = 100
target-version = ['py39', 'py310', 'py311']

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.9"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**Quality Gate**: `poetry run black .`, `poetry run ruff check .`, `poetry run mypy .` all pass.

---

### Phase 2: Implement Core Bootstrap Logic

**Duration**: Day 3-5 (16-24 hours)

**Goal**: Implement state management, phase orchestration, health checking.

---

#### Step 2.1: Implement State Management

**File**: `chora_bootstrap/state.py`

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict
import json

class BootstrapPhase(int, Enum):
    PHASE_0 = 0  # Pre-Bootstrap
    PHASE_1 = 1  # Core Services
    PHASE_2 = 2  # Infrastructure
    PHASE_3 = 3  # Capabilities
    PHASE_4 = 4  # Validation

class BootstrapStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

@dataclass
class BootstrapCheckpoint:
    phase: int
    timestamp: datetime
    services_running: List[str]
    health_status: Dict[str, bool]

@dataclass
class BootstrapState:
    current_phase: int
    status: BootstrapStatus
    completed_phases: List[int] = field(default_factory=list)
    services_started: List[str] = field(default_factory=list)
    services_healthy: List[str] = field(default_factory=list)
    credentials_generated: bool = False
    credential_files: List[str] = field(default_factory=list)
    checkpoints: List[BootstrapCheckpoint] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.utcnow)
    last_updated: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    last_error: Optional[str] = None
    retry_count: int = 0

    def to_dict(self) -> dict:
        """Serialize to dict for JSON persistence"""
        return {
            "current_phase": self.current_phase,
            "status": self.status.value,
            "completed_phases": self.completed_phases,
            "services_started": self.services_started,
            "services_healthy": self.services_healthy,
            "credentials_generated": self.credentials_generated,
            "credential_files": self.credential_files,
            "checkpoints": [
                {
                    "phase": cp.phase,
                    "timestamp": cp.timestamp.isoformat(),
                    "services_running": cp.services_running,
                    "health_status": cp.health_status,
                }
                for cp in self.checkpoints
            ],
            "started_at": self.started_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "last_error": self.last_error,
            "retry_count": self.retry_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BootstrapState":
        """Deserialize from dict"""
        return cls(
            current_phase=data["current_phase"],
            status=BootstrapStatus(data["status"]),
            completed_phases=data["completed_phases"],
            services_started=data["services_started"],
            services_healthy=data["services_healthy"],
            credentials_generated=data["credentials_generated"],
            credential_files=data["credential_files"],
            checkpoints=[
                BootstrapCheckpoint(
                    phase=cp["phase"],
                    timestamp=datetime.fromisoformat(cp["timestamp"]),
                    services_running=cp["services_running"],
                    health_status=cp["health_status"],
                )
                for cp in data["checkpoints"]
            ],
            started_at=datetime.fromisoformat(data["started_at"]),
            last_updated=datetime.fromisoformat(data["last_updated"]),
            completed_at=datetime.fromisoformat(data["completed_at"]) if data["completed_at"] else None,
            last_error=data["last_error"],
            retry_count=data["retry_count"],
        )

STATE_PATH = Path(".chora/bootstrap-state.json")

def save_state(state: BootstrapState) -> None:
    """Atomically save state to disk"""
    state.last_updated = datetime.utcnow()

    # Ensure directory exists
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Write to temporary file first
    temp_path = STATE_PATH.with_suffix(".tmp")
    temp_path.write_text(json.dumps(state.to_dict(), indent=2))

    # Atomic rename
    temp_path.rename(STATE_PATH)

def load_state() -> Optional[BootstrapState]:
    """Load state from disk"""
    if not STATE_PATH.exists():
        return None

    try:
        data = json.loads(STATE_PATH.read_text())
        return BootstrapState.from_dict(data)
    except Exception as e:
        print(f"⚠️  Warning: Failed to load state: {e}")
        return None
```

**Quality Gate**:
- Unit test: Create state, save, load, verify equality
- Unit test: State survives serialization/deserialization round-trip

---

#### Step 2.2: Implement Health Checking

**File**: `chora_bootstrap/health.py`

```python
import asyncio
import time
from typing import Optional
import aiohttp

async def wait_for_health(
    service_name: str,
    health_url: str,
    timeout: int = 120,
    required_consecutive: int = 3,
    verbose: bool = False
) -> bool:
    """
    Wait for service to become healthy.

    Args:
        service_name: Human-readable service name
        health_url: Health check endpoint URL
        timeout: Maximum time to wait (seconds)
        required_consecutive: Number of consecutive successful checks needed
        verbose: Print detailed progress

    Returns:
        True if service became healthy, False if timeout
    """
    start_time = time.time()
    delay = 1
    consecutive_successes = 0

    async with aiohttp.ClientSession() as session:
        while time.time() - start_time < timeout:
            try:
                async with session.get(health_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        consecutive_successes += 1
                        if consecutive_successes >= required_consecutive:
                            elapsed = time.time() - start_time
                            print(f"✓ {service_name} healthy ({elapsed:.1f}s)")
                            return True
                    else:
                        consecutive_successes = 0
                        if verbose:
                            print(f"⏳ {service_name} returned {response.status}, retrying...")
            except Exception as e:
                consecutive_successes = 0
                elapsed = time.time() - start_time
                if verbose:
                    print(f"⏳ Waiting for {service_name}... ({elapsed:.0f}s, retry in {delay}s): {e}")

            await asyncio.sleep(delay)
            delay = min(delay * 1.5, 30)  # Exponential backoff, max 30s

    print(f"✗ {service_name} failed to become healthy within {timeout}s")
    return False

async def check_port(host: str, port: int, timeout: int = 5) -> bool:
    """Check if port is open"""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return True
    except:
        return False

async def is_service_healthy(service_name: str, health_url: str) -> bool:
    """Quick health check (single attempt, 5s timeout)"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(health_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                return response.status == 200
    except:
        return False
```

**Quality Gate**:
- Unit test: Mock HTTP server, verify health check succeeds
- Unit test: Mock HTTP server with delays, verify exponential backoff
- Unit test: Mock HTTP server timeout, verify failure after max retries

---

#### Step 2.3: Implement Credential Generation

**File**: `chora_bootstrap/credentials.py`

```python
import secrets
import json
from pathlib import Path
from typing import Dict

CREDENTIALS_PATH = Path(".chora/credentials.json")

def generate_credentials(service_names: list[str]) -> Dict[str, str]:
    """Generate cryptographically secure credentials for all services"""
    credentials = {
        "jwt_secret": secrets.token_hex(32),  # 256 bits
    }

    # Generate API key for each service
    for service in service_names:
        credentials[f"api_key_{service}"] = secrets.token_urlsafe(32)  # 128 bits

    return credentials

def save_credentials(credentials: Dict[str, str]) -> None:
    """Save credentials with secure permissions"""
    # Ensure directory exists
    CREDENTIALS_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Write credentials
    CREDENTIALS_PATH.write_text(json.dumps(credentials, indent=2))

    # Set restrictive permissions (owner read/write only)
    CREDENTIALS_PATH.chmod(0o600)

    print(f"✓ Generated credentials (stored in {CREDENTIALS_PATH})")

def load_credentials() -> Dict[str, str]:
    """Load existing credentials"""
    if not CREDENTIALS_PATH.exists():
        raise FileNotFoundError(f"Credentials not found at {CREDENTIALS_PATH}")

    return json.loads(CREDENTIALS_PATH.read_text())
```

**Quality Gate**:
- Unit test: Generate credentials, verify all keys present
- Unit test: Generate credentials, verify sufficient entropy (length check)
- Unit test: Save credentials, verify file permissions are 0600
- Unit test: Save and load credentials, verify round-trip

---

#### Step 2.4: Implement Phase Orchestration

**File**: `chora_bootstrap/phases.py`

```python
import asyncio
import subprocess
from pathlib import Path
from typing import Optional
import docker
from rich.console import Console

from .state import BootstrapState, BootstrapStatus, save_state, load_state
from .health import wait_for_health, is_service_healthy
from .credentials import generate_credentials, save_credentials, load_credentials
from .config import load_config, ServiceConfig

console = Console()

class BootstrapOrchestrator:
    def __init__(self, config_path: str = ".chora/bootstrap-config.yml"):
        self.config = load_config(config_path)
        self.docker_client = docker.from_env()

    async def run(self, resume: bool = True, verbose: bool = False) -> bool:
        """Run full bootstrap process"""
        # Check if resuming from previous run
        state = load_state() if resume else None

        if state and state.status == BootstrapStatus.FAILED:
            console.print(f"[yellow]Resuming from Phase {state.current_phase}...[/yellow]")
        else:
            state = BootstrapState(
                current_phase=0,
                status=BootstrapStatus.IN_PROGRESS
            )

        # Run phases sequentially
        phases = [
            (0, "Pre-Bootstrap Validation", self.run_phase_0),
            (1, "Core Services", self.run_phase_1),
            (2, "Infrastructure Services", self.run_phase_2),
            (3, "Capability Services", self.run_phase_3),
            (4, "Validation", self.run_phase_4),
        ]

        for phase_num, phase_name, phase_func in phases:
            if state.current_phase > phase_num:
                console.print(f"[green]✓ Phase {phase_num}: {phase_name} (already completed)[/green]")
                continue

            console.print(f"\n[bold]Phase {phase_num}: {phase_name} ({phase_num+1}/5)[/bold]")

            state.current_phase = phase_num
            save_state(state)

            try:
                if not await phase_func(state, verbose):
                    state.status = BootstrapStatus.FAILED
                    save_state(state)
                    return False

                state.completed_phases.append(phase_num)
                save_state(state)

            except Exception as e:
                console.print(f"[red]✗ Phase {phase_num} failed: {e}[/red]")
                state.status = BootstrapStatus.FAILED
                state.last_error = str(e)
                save_state(state)
                return False

        # Mark bootstrap as completed
        state.status = BootstrapStatus.COMPLETED
        state.completed_at = datetime.utcnow()
        save_state(state)

        console.print("\n[green bold]✓ Bootstrap completed successfully[/green bold]")
        return True

    async def run_phase_0(self, state: BootstrapState, verbose: bool) -> bool:
        """Phase 0: Pre-Bootstrap Validation"""
        # Check Docker
        if not self.check_docker():
            return False

        # Check Python
        if not self.check_python():
            return False

        # Check ports
        if not await self.check_ports():
            return False

        # Create directories
        Path(".chora").mkdir(exist_ok=True)
        Path(".chora/logs").mkdir(exist_ok=True)
        Path(".chora/data").mkdir(exist_ok=True)
        console.print("  ✓ Created directory structure")

        # Generate credentials
        if not state.credentials_generated:
            service_names = [s.name for s in self.config.services]
            credentials = generate_credentials(service_names)
            save_credentials(credentials)
            state.credentials_generated = True
            save_state(state)

        return True

    async def run_phase_1(self, state: BootstrapState, verbose: bool) -> bool:
        """Phase 1: Core Services (Manifest Registry)"""
        manifest_config = next(s for s in self.config.services if s.name == "manifest")

        # Start Manifest
        if not await self.start_service(manifest_config, verbose):
            return False

        state.services_started.append("manifest")
        save_state(state)

        # Wait for health
        if not await wait_for_health("Manifest", manifest_config.health_endpoint, verbose=verbose):
            return False

        state.services_healthy.append("manifest")
        save_state(state)

        return True

    async def start_service(self, service_config: ServiceConfig, verbose: bool) -> bool:
        """Start a service via Docker Compose"""
        console.print(f"  ⏳ Starting {service_config.name}...")

        # Check if already running
        try:
            container = self.docker_client.containers.get(f"chora-{service_config.name}")
            if container.status == "running":
                console.print(f"  ✓ {service_config.name} already running")
                return True
        except docker.errors.NotFound:
            pass

        # Load credentials
        credentials = load_credentials()

        # Start via docker-compose
        env = {
            **credentials,
            "MANIFEST_URL": "http://manifest:8500",
        }

        cmd = f"docker-compose -f {service_config.docker_compose} up -d"
        result = subprocess.run(
            cmd,
            shell=True,
            env={**os.environ, **env},
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            console.print(f"  [red]✗ Failed to start {service_config.name}[/red]")
            if verbose:
                console.print(f"  Error: {result.stderr}")
            return False

        console.print(f"  ✓ {service_config.name} started")
        return True

    def check_docker(self) -> bool:
        """Check Docker is available"""
        try:
            version = self.docker_client.version()
            console.print(f"  ✓ Docker {version['Version']} detected")
            return True
        except Exception as e:
            console.print(f"  [red]✗ Docker not available: {e}[/red]")
            return False

    def check_python(self) -> bool:
        """Check Python version"""
        import sys
        version = sys.version_info
        if version < (3, 9):
            console.print(f"  [red]✗ Python {version.major}.{version.minor} too old (need 3.9+)[/red]")
            return False
        console.print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} detected")
        return True

    async def check_ports(self) -> bool:
        """Check required ports are available"""
        from .health import check_port

        required_ports = [8500, 8600, 8700, 8800, 8900, 9000]
        unavailable = []

        for port in required_ports:
            if await check_port("localhost", port):
                unavailable.append(port)

        if unavailable:
            console.print(f"  [red]✗ Ports unavailable: {', '.join(map(str, unavailable))}[/red]")
            return False

        console.print(f"  ✓ Ports {required_ports[0]}-{required_ports[-1]} available")
        return True
```

**Quality Gate**:
- Unit test: Mock Docker client, verify phase 0 checks pass/fail correctly
- Unit test: Mock service start, verify state updated correctly
- Integration test: Run Phase 0 on clean system, verify prerequisites checked

---

### Phase 3: Implement REST API

**Duration**: Day 6-8 (16-24 hours)

**Goal**: Implement CLI interface using Click.

---

#### Step 3.1: Implement CLI

**File**: `chora_bootstrap/cli.py`

```python
import click
import asyncio
from rich.console import Console

from .phases import BootstrapOrchestrator
from .state import load_state, BootstrapStatus

console = Console()

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Chora Bootstrap - Phased bootstrap for capability server ecosystems"""
    pass

@cli.command()
@click.option("--environment", default="dev", help="Target environment (dev, staging, prod)")
@click.option("--resume/--no-resume", default=True, help="Resume from checkpoint if previous run failed")
@click.option("--verbose", is_flag=True, help="Enable verbose logging")
@click.option("--config", default=".chora/bootstrap-config.yml", help="Path to bootstrap configuration")
def bootstrap(environment: str, resume: bool, verbose: bool, config: str):
    """Run full bootstrap process"""
    console.print("[bold]Chora Bootstrap v1.0.0[/bold]")
    console.print("━" * 60 + "\n")

    orchestrator = BootstrapOrchestrator(config_path=config)
    success = asyncio.run(orchestrator.run(resume=resume, verbose=verbose))

    if not success:
        console.print("\n[red bold]✗ Bootstrap failed[/red bold]")
        console.print("Run 'chora bootstrap' to resume or 'chora bootstrap rollback' to undo")
        raise click.Exit(1)

@cli.command()
@click.option("--format", default="table", type=click.Choice(["table", "json"]), help="Output format")
def status(format: str):
    """Display current system status"""
    state = load_state()

    if not state:
        console.print("[yellow]Bootstrap not started yet[/yellow]")
        console.print("Run 'chora bootstrap' to start")
        raise click.Exit(2)

    if format == "json":
        import json
        click.echo(json.dumps(state.to_dict(), indent=2))
    else:
        console.print("[bold]Chora System Status[/bold]")
        console.print("━" * 60 + "\n")

        console.print(f"Status: {state.status.value}")
        console.print(f"Current Phase: {state.current_phase}")
        console.print(f"Services Started: {', '.join(state.services_started)}")
        console.print(f"Services Healthy: {', '.join(state.services_healthy)}")

        if state.status == BootstrapStatus.COMPLETED:
            console.print(f"\n[green]✓ Bootstrap completed at {state.completed_at}[/green]")
        elif state.status == BootstrapStatus.FAILED:
            console.print(f"\n[red]✗ Bootstrap failed at Phase {state.current_phase}[/red]")
            if state.last_error:
                console.print(f"Error: {state.last_error}")

@cli.command()
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
def rollback(force: bool):
    """Rollback to previous phase"""
    state = load_state()

    if not state:
        console.print("[yellow]No bootstrap state found[/yellow]")
        raise click.Exit(2)

    if not force:
        click.confirm(f"Rollback to Phase {state.current_phase - 1}?", abort=True)

    # TODO: Implement rollback logic
    console.print("[yellow]Rollback not yet implemented[/yellow]")

@cli.command()
@click.option("--force", is_flag=True, help="Skip confirmation (dangerous!)")
def reset(force: bool):
    """Complete cleanup (stop all services, delete state)"""
    if not force:
        click.confirm("⚠️  WARNING: This will stop all services and delete bootstrap state! Are you sure?", abort=True)

    # TODO: Implement reset logic
    console.print("[yellow]Reset not yet implemented[/yellow]")

if __name__ == "__main__":
    cli()
```

**Setup Entry Point** (`pyproject.toml`):
```toml
[tool.poetry.scripts]
chora = "chora_bootstrap.cli:cli"
```

**Quality Gate**:
- Manual test: `poetry run chora --help` shows help
- Manual test: `poetry run chora bootstrap --help` shows bootstrap help
- Manual test: `poetry run chora status` shows "Bootstrap not started yet"

---

#### Step 3.2: Create Configuration File

**File**: `.chora/bootstrap-config.yml`

```yaml
version: "1.0"

environment: dev

services:
  - name: manifest
    phase: 1
    docker_compose: docker-compose.manifest.yml
    health_endpoint: http://localhost:8500/health
    timeout: 60
    dependencies: []

  - name: orchestrator
    phase: 2
    docker_compose: docker-compose.orchestrator.yml
    health_endpoint: http://localhost:8600/health
    timeout: 120
    dependencies: [manifest]

  - name: gateway
    phase: 2
    docker_compose: docker-compose.gateway.yml
    health_endpoint: http://localhost:8700/health
    timeout: 120
    dependencies: [manifest]

  - name: analyzer
    phase: 3
    deploy_via: orchestrator
    version: "1.0.0"
    timeout: 120
    dependencies: [manifest, orchestrator]

timeouts:
  health_check: 120
  phase_0: 300
  phase_1: 300
  phase_2: 600
  phase_3: 900
  phase_4: 120

retry:
  initial_delay: 1
  max_delay: 30
  backoff_factor: 2
  max_attempts: 10

credentials:
  jwt_secret_bits: 256
  api_key_bits: 128
  storage_path: .chora/credentials.json
  storage_permissions: "0600"
```

**Config Loader** (`chora_bootstrap/config.py`):
```python
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import yaml

@dataclass
class ServiceConfig:
    name: str
    phase: int
    docker_compose: Optional[str] = None
    deploy_via: Optional[str] = None
    version: Optional[str] = None
    health_endpoint: str = ""
    timeout: int = 120
    dependencies: List[str] = field(default_factory=list)

@dataclass
class BootstrapConfig:
    version: str
    environment: str
    services: List[ServiceConfig]
    timeouts: dict
    retry: dict
    credentials: dict

def load_config(path: str = ".chora/bootstrap-config.yml") -> BootstrapConfig:
    """Load bootstrap configuration from YAML"""
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration not found: {path}")

    data = yaml.safe_load(config_path.read_text())

    services = [ServiceConfig(**s) for s in data["services"]]

    return BootstrapConfig(
        version=data["version"],
        environment=data["environment"],
        services=services,
        timeouts=data["timeouts"],
        retry=data["retry"],
        credentials=data["credentials"],
    )
```

**Quality Gate**:
- Unit test: Load config, verify all services parsed correctly
- Unit test: Invalid YAML raises appropriate error

---

### Phase 4: Create Client Library

**Duration**: Day 9-10 (8-16 hours)

**Goal**: Package bootstrap CLI for easy installation.

---

#### Step 4.1: Add README and Documentation

**File**: `README.md`

```markdown
# Chora Bootstrap

Phased, idempotent bootstrap process for initializing capability server ecosystems.

## Installation

```bash
pip install chora-bootstrap
```

## Quick Start

```bash
# Run bootstrap
chora bootstrap

# Check status
chora bootstrap status

# Rollback if needed
chora bootstrap rollback
```

## Documentation

- [Capability Charter](capability-charter.md) - Problem statement and ROI
- [Protocol Spec](protocol-spec.md) - Complete technical specification
- [AGENTS.md](AGENTS.md) - Quick reference for AI agents
- [Adoption Blueprint](adoption-blueprint.md) - Step-by-step implementation guide

## License

MIT
```

---

#### Step 4.2: Build and Test Package

```bash
# Build package
poetry build

# Install locally for testing
pip install dist/chora_bootstrap-1.0.0-py3-none-any.whl

# Test CLI
chora --help
chora bootstrap --help
```

**Quality Gate**:
- Package builds without errors
- CLI accessible from terminal after install
- Help text displays correctly

---

### Phase 5: Deployment and Validation

**Duration**: Day 11-12 (8-16 hours)

**Goal**: Deploy to development environment and validate end-to-end.

---

#### Step 5.1: Create Docker Compose Files

**File**: `docker-compose.manifest.yml`

```yaml
version: '3.8'
services:
  manifest:
    image: chora/manifest:1.0.0
    container_name: chora-manifest
    environment:
      - STORAGE_BACKEND=sqlite
      - SQLITE_PATH=/data/manifest.db
      - API_KEY=${API_KEY_MANIFEST}
      - LOG_LEVEL=info
    ports:
      - "8500:8500"
    volumes:
      - manifest-data:/data
    networks:
      - chora
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8500/health"]
      interval: 5s
      timeout: 3s
      retries: 3

volumes:
  manifest-data:

networks:
  chora:
    driver: bridge
```

**(Create similar files for orchestrator, gateway, etc.)**

---

#### Step 5.2: Run End-to-End Test

```bash
# Clean environment
docker-compose down -v
rm -rf .chora/

# Run bootstrap
chora bootstrap

# Verify all services healthy
chora bootstrap status

# Test service discovery
curl http://localhost:8500/v1/services | jq '.'

# Test gateway routing
curl -X POST http://localhost:8700/api/v1/analyzer/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "test"}'
```

**Quality Gate**:
- Bootstrap completes without errors (exit code 0)
- All services showing "UP" and "healthy" in status
- Service discovery returns all expected services
- Gateway routing returns 200 OK

---

#### Step 5.3: Test Resume and Rollback

**Test Resume**:
```bash
# Simulate failure by stopping Orchestrator mid-bootstrap
docker stop chora-orchestrator

# Resume bootstrap
chora bootstrap --resume

# Verify resume worked (skipped Phase 0-1, re-ran Phase 2)
```

**Test Rollback**:
```bash
# Rollback to Phase 1
chora bootstrap rollback --force

# Verify only Manifest running
chora bootstrap status
# Should show: manifest UP, orchestrator/gateway not started
```

**Quality Gate**:
- Resume correctly detects previous phase and skips completed work
- Rollback stops services and updates state correctly

---

### Essential Tier Deliverables Checklist

- [ ] State management implemented and tested
- [ ] Health checking with exponential backoff implemented
- [ ] Credential generation with secure storage implemented
- [ ] Phase orchestration (Phase 0-4) implemented
- [ ] CLI with `bootstrap`, `status`, `rollback`, `reset` commands
- [ ] Configuration file format defined and loader implemented
- [ ] Docker Compose files created for all services
- [ ] Package built and installable via pip
- [ ] End-to-end test on clean VM passes
- [ ] Resume from checkpoint works correctly
- [ ] Rollback to previous phase works correctly
- [ ] Documentation (README, AGENTS.md) created

**Success Criteria**:
- [ ] `chora bootstrap` completes in < 15 minutes on clean VM
- [ ] All services healthy after bootstrap
- [ ] Bootstrap is idempotent (can run 5x without errors)
- [ ] Resume from Phase 2 failure works
- [ ] Rollback from Phase 3 to Phase 2 works

---

## Recommended Tier (2-4 Weeks)

**Goal**: Production-ready bootstrap with etcd backend, monitoring, advanced CLI.

**Additional Deliverables**:
- ✅ etcd backend for Manifest Registry (replace SQLite)
- ✅ Prometheus metrics endpoint
- ✅ CLI tool enhancements (validate, config commands)
- ✅ Monitoring dashboard (Grafana)
- ✅ CI/CD integration
- ✅ Runbook documentation

**Time Estimate**: 80-160 hours (2-4 weeks, 1 engineer)

**Cost**: $12,000 - $24,000 (at $150/hour)

---

### Phase 1: Replace SQLite with etcd

**Duration**: Week 3 Day 1-3 (16-24 hours)

---

#### Step 1.1: Add etcd Docker Compose

**File**: `docker-compose.etcd.yml`

```yaml
version: '3.8'
services:
  etcd1:
    image: quay.io/coreos/etcd:v3.5.10
    container_name: chora-etcd1
    command:
      - etcd
      - --name=etcd1
      - --initial-advertise-peer-urls=http://etcd1:2380
      - --listen-peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://etcd1:2379
      - --listen-client-urls=http://0.0.0.0:2379
      - --initial-cluster=etcd1=http://etcd1:2380,etcd2=http://etcd2:2380,etcd3=http://etcd3:2380
      - --initial-cluster-state=new
    ports:
      - "2379:2379"
      - "2380:2380"
    volumes:
      - etcd1-data:/etcd-data
    networks:
      - chora

  etcd2:
    image: quay.io/coreos/etcd:v3.5.10
    container_name: chora-etcd2
    command:
      - etcd
      - --name=etcd2
      - --initial-advertise-peer-urls=http://etcd2:2380
      - --listen-peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://etcd2:2379
      - --listen-client-urls=http://0.0.0.0:2379
      - --initial-cluster=etcd1=http://etcd1:2380,etcd2=http://etcd2:2380,etcd3=http://etcd3:2380
      - --initial-cluster-state=new
    ports:
      - "2479:2379"
      - "2480:2380"
    volumes:
      - etcd2-data:/etcd-data
    networks:
      - chora

  etcd3:
    image: quay.io/coreos/etcd:v3.5.10
    container_name: chora-etcd3
    command:
      - etcd
      - --name=etcd3
      - --initial-advertise-peer-urls=http://etcd3:2380
      - --listen-peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://etcd3:2379
      - --listen-client-urls=http://0.0.0.0:2379
      - --initial-cluster=etcd1=http://etcd1:2380,etcd2=http://etcd2:2380,etcd3=http://etcd3:2380
      - --initial-cluster-state=new
    ports:
      - "2579:2379"
      - "2580:2380"
    volumes:
      - etcd3-data:/etcd-data
    networks:
      - chora

volumes:
  etcd1-data:
  etcd2-data:
  etcd3-data:

networks:
  chora:
    external: true
```

---

#### Step 1.2: Update Phase 1 to Start etcd

```python
async def run_phase_1(self, state: BootstrapState, verbose: bool) -> bool:
    """Phase 1: Core Services (etcd + Manifest Registry)"""

    # Start etcd cluster (production only)
    if self.config.environment == "prod":
        console.print("  ⏳ Starting etcd cluster (3 nodes)...")
        if not await self.start_etcd_cluster(verbose):
            return False

    # Start Manifest
    manifest_config = next(s for s in self.config.services if s.name == "manifest")
    if not await self.start_service(manifest_config, verbose):
        return False

    # ... rest of Phase 1
```

---

### Phase 2: Add Prometheus Metrics

**Duration**: Week 3 Day 4-5 (8-16 hours)

**Add metrics endpoint to bootstrap CLI, expose to Prometheus.**

(Implementation details omitted for brevity, see protocol-spec.md for complete specification.)

---

### Phase 3: CI/CD Integration

**Duration**: Week 4 Day 1-2 (8-16 hours)

**Create GitHub Actions workflow for automated testing.**

**File**: `.github/workflows/bootstrap-test.yml`

```yaml
name: Bootstrap Integration Test
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install chora-bootstrap
        run: |
          pip install poetry
          poetry install

      - name: Run bootstrap
        run: |
          poetry run chora bootstrap --environment test

      - name: Verify all services healthy
        run: |
          poetry run chora bootstrap status --format json | jq '.services[] | select(.status != "up") | .name'
          # Should return empty (all services up)

      - name: Run validation tests
        run: |
          poetry run chora bootstrap validate

      - name: Cleanup
        if: always()
        run: |
          poetry run chora bootstrap reset --force
```

---

### Phase 4: Documentation and Runbook

**Duration**: Week 4 Day 3-5 (16-24 hours)

**Create comprehensive runbook for operators.**

(See ledger.md and adoption-blueprint.md for templates.)

---

## Advanced Tier (4-8 Weeks)

**Goal**: Enterprise-grade bootstrap with HA, security hardening, performance optimization.

**Additional Deliverables**:
- ✅ High availability (3-node etcd cluster, redundant infrastructure)
- ✅ Security hardening (mTLS, RBAC, secret management)
- ✅ Performance optimization (parallel deployment, caching)
- ✅ Web UI for bootstrap progress
- ✅ Advanced validation (load testing, security scanning)
- ✅ Multi-environment orchestration

**Time Estimate**: 160-320 hours (4-8 weeks, 1-2 engineers)

**Cost**: $24,000 - $48,000 (at $150/hour)

---

*(Advanced tier implementation details omitted for brevity. Contact Chora team for consultation.)*

---

## Rollback Plan

**If Essential Tier adoption fails**:
1. Document lessons learned
2. Roll back to manual deployment scripts
3. Preserve credentials if generated
4. Evaluate alternative approaches

**If Recommended Tier adoption fails**:
1. Roll back to Essential Tier (SQLite, basic config)
2. Continue using Essential Tier for dev
3. Defer production adoption to future quarter

**If Advanced Tier adoption fails**:
1. Roll back to Recommended Tier
2. Maintain current HA/security manually
3. Reassess resource allocation

---

## Success Metrics

### Essential Tier

| Metric | Target | Measurement |
|--------|--------|-------------|
| Bootstrap Time | < 15 min | Time from `chora bootstrap` to completion |
| Success Rate | ≥ 90% | Successful bootstraps / total attempts |
| Resume Success | 100% | Resumes work correctly after failure |
| Rollback Success | 100% | Rollback leaves system in good state |

### Recommended Tier

| Metric | Target | Measurement |
|--------|--------|-------------|
| Bootstrap Time | < 12 min | etcd adds ~2min, but parallel saves ~5min |
| CI/CD Integration | 100% | All PRs use bootstrap for test environment |
| Monitoring Coverage | 100% | All bootstrap operations emit metrics |

### Advanced Tier

| Metric | Target | Measurement |
|--------|--------|-------------|
| Bootstrap Time | < 10 min | Parallel deployment optimizations |
| HA Uptime | ≥ 99.9% | Cluster survives single node failure |
| Security Score | A+ | Pass all security audits |

---

## Support and Next Steps

**Questions?**
- Review [protocol-spec.md](protocol-spec.md) for implementation details
- Check [AGENTS.md](AGENTS.md) for quick reference
- Ask in #chora-bootstrap Slack channel

**Ready to Start?**
1. Ensure prerequisites met (Docker, Python, stakeholder buy-in)
2. Allocate dedicated time (1-2 weeks Essential, 2-4 weeks Recommended)
3. Follow Phase 1 of Essential Tier
4. Track progress in [ledger.md](ledger.md)

**Need Help?**
- Pair programming sessions available
- Code review support
- Architecture consultation

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-12
**Maintained By**: Chora Infrastructure Team
