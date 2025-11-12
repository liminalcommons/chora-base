# SAP-045: Bootstrap - Protocol Specification

**SAP ID**: SAP-045
**Name**: Bootstrap
**Version**: 1.0.0
**Status**: Pilot
**Created**: 2025-11-12
**Last Updated**: 2025-11-12

---

## 1. Overview

This document provides the complete technical specification for the Bootstrap capability (SAP-045), including CLI commands, phase protocols, state management, health checking, and rollback procedures.

**Scope**: Covers Essential and Recommended tier implementation details. Advanced tier features noted as future enhancements.

---

## 2. CLI Interface

### 2.1 Command Structure

```bash
chora bootstrap [COMMAND] [OPTIONS]
```

**Available Commands**:
- `chora bootstrap` - Run full bootstrap process (default: interactive mode)
- `chora bootstrap status` - Display current system status
- `chora bootstrap rollback` - Rollback to previous phase
- `chora bootstrap reset` - Complete cleanup (stop all services, delete state)
- `chora bootstrap validate` - Run validation checks only (Phase 4)
- `chora bootstrap config` - Display/edit bootstrap configuration

### 2.2 Main Command: `chora bootstrap`

**Purpose**: Execute phased bootstrap process

**Synopsis**:
```bash
chora bootstrap [OPTIONS]
```

**Options**:
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--environment` | string | `dev` | Target environment (dev, staging, prod) |
| `--resume` | flag | `true` | Resume from checkpoint if previous run failed |
| `--skip-validation` | flag | `false` | Skip Phase 4 validation (not recommended) |
| `--verbose` | flag | `false` | Enable verbose logging |
| `--dry-run` | flag | `false` | Show what would be done without executing |
| `--config` | path | `.chora/bootstrap-config.yml` | Path to bootstrap configuration |
| `--timeout` | int | `1800` | Global timeout in seconds (30 minutes) |
| `--parallel` | flag | `false` | Start independent services in parallel (experimental) |

**Examples**:

```bash
# Basic bootstrap (dev environment, interactive)
chora bootstrap

# Production bootstrap with custom config
chora bootstrap --environment prod --config /etc/chora/bootstrap-prod.yml

# Resume from failed bootstrap
chora bootstrap --resume

# Dry run to see what would happen
chora bootstrap --dry-run --verbose

# Skip validation (fast bootstrap for testing)
chora bootstrap --skip-validation
```

**Exit Codes**:
- `0`: Success (all phases completed)
- `1`: Pre-bootstrap validation failed (Phase 0)
- `2`: Core services failed (Phase 1)
- `3`: Infrastructure services failed (Phase 2)
- `4`: Capability services failed (Phase 3)
- `5`: Validation failed (Phase 4)
- `6`: User interrupted (Ctrl-C)
- `7`: Configuration error
- `8`: State corruption detected

**Output Format** (Default: Rich Console):
```
Chora Bootstrap v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 0: Pre-Bootstrap Validation
  ✓ Docker 24.0.6 detected
  ✓ Python 3.11.5 detected
  ✓ Ports 8500-9000 available
  ✓ Generated credentials

Phase 1: Core Services (1/4)
  ⏳ Starting Manifest Registry...
  ✓ Manifest Registry started (2.3s)

[... continues ...]

✓ Bootstrap completed successfully in 8m 34s
```

**Output Format** (`--format json`):
```json
{
  "status": "completed",
  "duration_seconds": 514,
  "phases": [
    {
      "phase": 0,
      "name": "Pre-Bootstrap Validation",
      "status": "completed",
      "duration_seconds": 5,
      "steps": [
        {"name": "Check Docker", "status": "passed"},
        {"name": "Check Python", "status": "passed"},
        {"name": "Check Ports", "status": "passed"},
        {"name": "Generate Credentials", "status": "passed"}
      ]
    },
    {
      "phase": 1,
      "name": "Core Services",
      "status": "completed",
      "duration_seconds": 120,
      "services_started": ["manifest"]
    }
  ],
  "services": [
    {"name": "manifest", "status": "up", "health": "healthy", "url": "http://localhost:8500"}
  ]
}
```

---

### 2.3 Status Command: `chora bootstrap status`

**Purpose**: Display current system status and bootstrap progress

**Synopsis**:
```bash
chora bootstrap status [OPTIONS]
```

**Options**:
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--format` | string | `table` | Output format (table, json, yaml) |
| `--watch` | flag | `false` | Continuously update status (refresh every 2s) |
| `--services` | string | `all` | Filter by services (comma-separated) |

**Examples**:

```bash
# Show current status
chora bootstrap status

# JSON output for scripting
chora bootstrap status --format json

# Watch status in real-time
chora bootstrap status --watch

# Check specific services
chora bootstrap status --services manifest,orchestrator
```

**Output** (Table Format):
```
Chora System Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Core Services:
  ✓ manifest       v1.0.0  http://localhost:8500  UP      (2s ago)

Infrastructure Services:
  ✓ orchestrator   v1.0.0  http://localhost:8600  UP      (1s ago)
  ✓ gateway        v1.0.0  http://localhost:8700  UP      (3s ago)

Capability Services:
  ✓ analyzer       v1.0.0  http://localhost:8800  UP      (1s ago)
  ✓ executor       v1.0.0  http://localhost:8900  UP      (2s ago)

Overall Status: HEALTHY
Bootstrap completed: 2025-11-12T10:15:00Z (2h ago)
Uptime: 2h 15m 32s
```

**Output** (JSON Format):
```json
{
  "overall_status": "healthy",
  "bootstrap_completed_at": "2025-11-12T10:15:00Z",
  "uptime_seconds": 8132,
  "services": [
    {
      "name": "manifest",
      "version": "1.0.0",
      "url": "http://localhost:8500",
      "status": "up",
      "health": "healthy",
      "last_heartbeat": "2025-11-12T12:30:28Z",
      "heartbeat_age_seconds": 2
    }
  ]
}
```

**Exit Codes**:
- `0`: All services healthy
- `1`: One or more services unhealthy
- `2`: Bootstrap not completed yet
- `3`: Bootstrap failed

---

### 2.4 Rollback Command: `chora bootstrap rollback`

**Purpose**: Rollback to previous phase or completely reset

**Synopsis**:
```bash
chora bootstrap rollback [OPTIONS]
```

**Options**:
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--to-phase` | int | `auto` | Target phase to rollback to (0-3) |
| `--force` | flag | `false` | Skip confirmation prompt |
| `--keep-data` | flag | `false` | Keep data volumes (only stop services) |

**Examples**:

```bash
# Rollback to previous phase (interactive)
chora bootstrap rollback

# Rollback to specific phase
chora bootstrap rollback --to-phase 1

# Force rollback without confirmation
chora bootstrap rollback --force
```

**Rollback Behavior**:

| Current Phase | Rollback Action | Services Stopped | Data Preserved |
|--------------|----------------|------------------|----------------|
| Phase 1 | Stop Manifest, delete credentials | manifest | No |
| Phase 2 | Stop Orchestrator & Gateway | orchestrator, gateway | Yes (Manifest keeps running) |
| Phase 3 | Undeploy capabilities via Orchestrator | All capabilities | Yes (Infrastructure intact) |
| Phase 4 | No-op (already completed) | None | Yes |

**Output**:
```
Rolling back to Phase 1...
  ⏳ Stopping Orchestrator...
  ✓ Orchestrator stopped
  ⏳ Stopping Gateway...
  ✓ Gateway stopped
  ✓ Updated state to Phase 1

Rollback completed. Run 'chora bootstrap' to resume.
```

**Exit Codes**:
- `0`: Rollback successful
- `1`: Rollback failed (services still running)
- `2`: Invalid target phase
- `3`: User cancelled

---

### 2.5 Reset Command: `chora bootstrap reset`

**Purpose**: Complete cleanup (nuclear option)

**Synopsis**:
```bash
chora bootstrap reset [OPTIONS]
```

**Options**:
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--force` | flag | `false` | Skip confirmation (dangerous!) |
| `--keep-credentials` | flag | `false` | Keep generated credentials |

**Warning**: This command stops ALL services and deletes all state. Use with caution!

**Examples**:

```bash
# Interactive reset (asks for confirmation)
chora bootstrap reset

# Force reset (no confirmation)
chora bootstrap reset --force

# Reset but keep credentials for reuse
chora bootstrap reset --keep-credentials
```

**Reset Actions**:
1. Stop all services (in reverse dependency order)
2. Remove Docker containers and networks
3. Delete `.chora/bootstrap-state.json`
4. Delete `.chora/credentials.json` (unless `--keep-credentials`)
5. Delete log files in `.chora/logs/`
6. Preserve data volumes by default (use `docker volume rm` to delete manually)

**Output**:
```
⚠️  WARNING: This will stop all services and delete bootstrap state!
Are you sure? (yes/no): yes

Resetting system...
  ⏳ Stopping 8 services...
  ✓ All services stopped
  ⏳ Removing containers and networks...
  ✓ Docker resources cleaned up
  ⏳ Deleting bootstrap state...
  ✓ State deleted
  ⏳ Deleting credentials...
  ✓ Credentials deleted

Reset complete. Run 'chora bootstrap' to start fresh.
```

---

### 2.6 Validate Command: `chora bootstrap validate`

**Purpose**: Run validation checks (Phase 4) without full bootstrap

**Synopsis**:
```bash
chora bootstrap validate [OPTIONS]
```

**Options**:
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--skip-discovery` | flag | `false` | Skip service discovery test |
| `--skip-routing` | flag | `false` | Skip gateway routing test |
| `--skip-control` | flag | `false` | Skip orchestrator control test |
| `--format` | string | `table` | Output format (table, json) |

**Examples**:

```bash
# Run all validation checks
chora bootstrap validate

# Run only service discovery test
chora bootstrap validate --skip-routing --skip-control

# JSON output for CI/CD
chora bootstrap validate --format json
```

**Validation Tests**:

1. **Service Discovery Test**: Query Manifest for all services
2. **Gateway Routing Test**: Send test request through Gateway to backend
3. **Orchestrator Control Test**: Stop and restart a service via Orchestrator
4. **Health Dashboard Test**: Verify all services reporting healthy

**Output**:
```
Running validation checks...

Service Discovery Test:
  ✓ Manifest API accessible
  ✓ Found 8 registered services
  ✓ All expected services present

Gateway Routing Test:
  ✓ Gateway accessible
  ✓ Routed request to analyzer
  ✓ Received valid response (42ms)

Orchestrator Control Test:
  ✓ Orchestrator API accessible
  ✓ Stopped analyzer successfully
  ✓ Restarted analyzer successfully
  ✓ Analyzer healthy after restart (4.2s)

Health Dashboard Test:
  ✓ All 8 services reporting healthy
  ✓ No services in unhealthy state

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ All validation checks passed
```

**Exit Codes**:
- `0`: All checks passed
- `1`: One or more checks failed
- `2`: Services not running (bootstrap not completed)

---

### 2.7 Config Command: `chora bootstrap config`

**Purpose**: Display or edit bootstrap configuration

**Synopsis**:
```bash
chora bootstrap config [SUBCOMMAND] [OPTIONS]
```

**Subcommands**:
- `show` - Display current configuration
- `edit` - Open configuration in $EDITOR
- `validate` - Validate configuration syntax

**Examples**:

```bash
# Show current config
chora bootstrap config show

# Edit config
chora bootstrap config edit

# Validate config file
chora bootstrap config validate --config /path/to/bootstrap-config.yml
```

---

## 3. Bootstrap Phases (Detailed Protocol)

### 3.1 Phase 0: Pre-Bootstrap Validation

**Goal**: Ensure environment is ready for bootstrap

**Steps**:

#### Step 0.1: Check Prerequisites

**Docker Check**:
```python
async def check_docker() -> bool:
    try:
        client = docker.from_env()
        version = client.version()
        if version['Version'] < "20.10":
            print(f"✗ Docker {version['Version']} too old (need 20.10+)")
            return False
        print(f"✓ Docker {version['Version']} detected")
        return True
    except docker.errors.DockerException:
        print("✗ Docker not running")
        return False
```

**Python Check**:
```python
import sys

def check_python() -> bool:
    version = sys.version_info
    if version < (3, 9):
        print(f"✗ Python {version.major}.{version.minor} too old (need 3.9+)")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True
```

**Port Availability Check**:
```python
import socket

async def check_port(port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0  # True if port is available (connect failed)

async def check_ports() -> bool:
    required_ports = [8500, 8600, 8700, 8800, 8900, 9000, 9100, 9200]
    unavailable = []

    for port in required_ports:
        if not await check_port(port):
            unavailable.append(port)

    if unavailable:
        print(f"✗ Ports unavailable: {', '.join(map(str, unavailable))}")
        return False

    print(f"✓ Ports {required_ports[0]}-{required_ports[-1]} available")
    return True
```

**Disk Space Check**:
```python
import shutil

def check_disk_space(path: str = ".", min_gb: int = 10) -> bool:
    stat = shutil.disk_usage(path)
    available_gb = stat.free / (1024 ** 3)

    if available_gb < min_gb:
        print(f"✗ Only {available_gb:.1f}GB available (need {min_gb}GB)")
        return False

    print(f"✓ Disk space: {available_gb:.1f}GB available")
    return True
```

#### Step 0.2: Check Existing State

```python
@dataclass
class BootstrapState:
    current_phase: int
    status: Literal["in_progress", "completed", "failed", "rolled_back"]
    services_started: List[str]
    started_at: datetime
    last_updated: datetime

async def load_state() -> Optional[BootstrapState]:
    state_path = Path(".chora/bootstrap-state.json")
    if not state_path.exists():
        return None

    data = json.loads(state_path.read_text())
    return BootstrapState(**data)

async def should_resume() -> bool:
    state = await load_state()
    if state is None:
        return False  # Fresh start

    if state.status == "completed":
        print("✓ Bootstrap already completed")
        return False

    if state.status == "failed":
        print(f"Detected failed bootstrap at Phase {state.current_phase}")
        print(f"Last updated: {state.last_updated}")
        if input("Resume from checkpoint? (y/n): ").lower() == 'y':
            return True

    return False
```

#### Step 0.3: Create Directory Structure

```python
async def create_directories():
    dirs = [
        ".chora",
        ".chora/logs",
        ".chora/data",
    ]

    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    print("✓ Created directory structure")
```

#### Step 0.4: Generate Credentials

```python
import secrets

def generate_credentials() -> Dict[str, str]:
    """Generate cryptographically secure credentials"""
    credentials = {
        "jwt_secret": secrets.token_hex(32),  # 256 bits
        "api_key_manifest": secrets.token_urlsafe(32),
        "api_key_orchestrator": secrets.token_urlsafe(32),
        "api_key_gateway": secrets.token_urlsafe(32),
        "api_key_analyzer": secrets.token_urlsafe(32),
        "api_key_executor": secrets.token_urlsafe(32),
        "api_key_storage": secrets.token_urlsafe(32),
    }
    return credentials

def save_credentials(credentials: Dict[str, str]):
    """Save credentials with secure permissions"""
    creds_path = Path(".chora/credentials.json")
    creds_path.write_text(json.dumps(credentials, indent=2))
    creds_path.chmod(0o600)  # Owner read/write only
    print("✓ Generated credentials (stored in .chora/credentials.json)")

def load_credentials() -> Dict[str, str]:
    """Load existing credentials"""
    creds_path = Path(".chora/credentials.json")
    if not creds_path.exists():
        raise FileNotFoundError("Credentials not found. Run Phase 0 first.")
    return json.loads(creds_path.read_text())
```

**Success Criteria**:
- All prerequisites met (Docker, Python, ports, disk)
- Directories created
- Credentials generated and stored securely
- State initialized (if fresh start) or loaded (if resume)

**Typical Duration**: 30-60 seconds

---

### 3.2 Phase 1: Core Services (Manifest Registry)

**Goal**: Start Manifest Registry (breaks circular dependency)

**Steps**:

#### Step 1.1: Start Storage Backend

**For Dev (SQLite)**:
```python
# SQLite is embedded, no separate process needed
print("✓ Using embedded SQLite storage")
```

**For Prod (etcd)**:
```yaml
# docker-compose.etcd.yml
version: '3.8'
services:
  etcd1:
    image: quay.io/coreos/etcd:v3.5.10
    command:
      - etcd
      - --name=etcd1
      - --initial-advertise-peer-urls=http://etcd1:2380
      - --listen-peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://etcd1:2379
      - --listen-client-urls=http://0.0.0.0:2379
      - --initial-cluster=etcd1=http://etcd1:2380,etcd2=http://etcd2:2380,etcd3=http://etcd3:2380
    networks:
      - chora

  etcd2:
    image: quay.io/coreos/etcd:v3.5.10
    # ... similar config

  etcd3:
    image: quay.io/coreos/etcd:v3.5.10
    # ... similar config

networks:
  chora:
    driver: bridge
```

```python
async def start_etcd_cluster():
    print("⏳ Starting etcd cluster (3 nodes)...")
    result = await run_command(
        "docker-compose -f docker-compose.etcd.yml up -d",
        timeout=60
    )

    if result.returncode != 0:
        print(f"✗ Failed to start etcd: {result.stderr}")
        return False

    # Wait for cluster to be healthy
    for i in range(30):  # 30 seconds max
        try:
            response = await http_client.get("http://localhost:2379/health")
            if response.status_code == 200:
                print("✓ etcd cluster healthy")
                return True
        except:
            await asyncio.sleep(1)

    print("✗ etcd cluster failed to become healthy")
    return False
```

#### Step 1.2: Start Manifest Registry

**Docker Compose File** (`docker-compose.manifest.yml`):
```yaml
version: '3.8'
services:
  manifest:
    image: chora/manifest:1.0.0
    environment:
      - STORAGE_BACKEND=${STORAGE_BACKEND:-sqlite}
      - ETCD_ENDPOINTS=${ETCD_ENDPOINTS:-http://etcd1:2379,http://etcd2:2379,http://etcd3:2379}
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
    external: true
```

**Start Command**:
```python
async def start_manifest(environment: Environment):
    print("⏳ Starting Manifest Registry...")

    # Load credentials
    credentials = load_credentials()

    # Set environment variables
    env_vars = {
        "STORAGE_BACKEND": "sqlite" if environment == Environment.DEV else "etcd",
        "ETCD_ENDPOINTS": "http://etcd1:2379,http://etcd2:2379,http://etcd3:2379",
        "API_KEY_MANIFEST": credentials["api_key_manifest"],
    }

    # Start via Docker Compose
    result = await run_command(
        "docker-compose -f docker-compose.manifest.yml up -d",
        env=env_vars,
        timeout=60
    )

    if result.returncode != 0:
        print(f"✗ Failed to start Manifest: {result.stderr}")
        return False

    print("✓ Manifest Registry started (http://localhost:8500)")
    return True
```

#### Step 1.3: Wait for Health

```python
async def wait_for_health(
    service_name: str,
    health_url: str,
    timeout: int = 120,
    required_consecutive: int = 3
) -> bool:
    """
    Wait for service to become healthy.

    Args:
        service_name: Human-readable service name
        health_url: Health check endpoint URL
        timeout: Maximum time to wait (seconds)
        required_consecutive: Number of consecutive successful checks needed

    Returns:
        True if service became healthy, False if timeout
    """
    start_time = time.time()
    delay = 1
    consecutive_successes = 0

    while time.time() - start_time < timeout:
        try:
            response = await http_client.get(health_url, timeout=5)
            if response.status_code == 200:
                consecutive_successes += 1
                if consecutive_successes >= required_consecutive:
                    elapsed = time.time() - start_time
                    print(f"✓ {service_name} healthy ({elapsed:.1f}s)")
                    return True
            else:
                consecutive_successes = 0
        except Exception as e:
            consecutive_successes = 0
            elapsed = time.time() - start_time
            print(f"⏳ Waiting for {service_name}... ({elapsed:.0f}s, retry in {delay}s)")

        await asyncio.sleep(delay)
        delay = min(delay * 1.5, 30)  # Exponential backoff, max 30s

    print(f"✗ {service_name} failed to become healthy within {timeout}s")
    return False
```

#### Step 1.4: Self-Register Manifest

```python
async def self_register_manifest():
    """Register Manifest in its own registry"""
    registration = {
        "name": "manifest",
        "version": "1.0.0",
        "interfaces": {
            "REST": "http://localhost:8500"
        },
        "metadata": {
            "description": "Service registry and discovery",
            "dependencies": [],
            "tags": ["core", "infrastructure"]
        }
    }

    try:
        response = await http_client.post(
            "http://localhost:8500/v1/services",
            json=registration,
            timeout=10
        )

        if response.status_code == 201:
            data = response.json()
            print(f"✓ Manifest self-registered (ID: {data['id']})")
            return True
        else:
            print(f"✗ Self-registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Self-registration failed: {e}")
        return False
```

**Success Criteria**:
- Manifest responding to health checks (200 OK)
- Manifest registered itself in its own registry
- Storage backend (SQLite or etcd) operational

**Typical Duration**: 1-2 minutes

---

### 3.3 Phase 2: Infrastructure Services

**Goal**: Start Orchestrator and Gateway

**Steps**:

#### Step 2.1: Start Orchestrator

**Docker Compose File** (`docker-compose.orchestrator.yml`):
```yaml
version: '3.8'
services:
  orchestrator:
    image: chora/orchestrator:1.0.0
    environment:
      - MANIFEST_URL=http://manifest:8500
      - API_KEY=${API_KEY_ORCHESTRATOR}
      - JWT_SECRET=${JWT_SECRET}
      - LOG_LEVEL=info
    ports:
      - "8600:8600"
    networks:
      - chora
    depends_on:
      - manifest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8600/health"]
      interval: 5s
      timeout: 3s
      retries: 3

networks:
  chora:
    external: true
```

**Start Command**:
```python
async def start_orchestrator():
    print("⏳ Starting Orchestrator...")

    credentials = load_credentials()

    env_vars = {
        "MANIFEST_URL": "http://manifest:8500",
        "API_KEY_ORCHESTRATOR": credentials["api_key_orchestrator"],
        "JWT_SECRET": credentials["jwt_secret"],
    }

    result = await run_command(
        "docker-compose -f docker-compose.orchestrator.yml up -d",
        env=env_vars,
        timeout=60
    )

    if result.returncode != 0:
        print(f"✗ Failed to start Orchestrator: {result.stderr}")
        return False

    print("✓ Orchestrator started (http://localhost:8600)")

    # Wait for health
    if not await wait_for_health("Orchestrator", "http://localhost:8600/health"):
        return False

    # Verify registration with Manifest
    if not await verify_registration("orchestrator"):
        return False

    return True

async def verify_registration(service_name: str) -> bool:
    """Verify service auto-registered with Manifest"""
    try:
        response = await http_client.get(
            f"http://localhost:8500/v1/services/{service_name}",
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✓ {service_name} registered with Manifest (status: {data['status']})")
            return True
        else:
            print(f"✗ {service_name} not found in Manifest")
            return False
    except Exception as e:
        print(f"✗ Failed to verify {service_name} registration: {e}")
        return False
```

#### Step 2.2: Start Gateway

Similar process to Orchestrator, using `docker-compose.gateway.yml`.

**Success Criteria**:
- Orchestrator and Gateway responding to health checks
- Both registered in Manifest with status "up"
- Orchestrator can query Manifest API successfully

**Typical Duration**: 2-3 minutes

---

### 3.4 Phase 3: Capability Services

**Goal**: Deploy remaining capabilities via Orchestrator

**Steps**:

#### Step 3.1: Deploy Capabilities

```python
@dataclass
class CapabilitySpec:
    name: str
    version: str
    image: str
    port: int
    dependencies: List[str]

CAPABILITIES = [
    CapabilitySpec("analyzer", "1.0.0", "chora/analyzer:1.0.0", 8800, ["manifest"]),
    CapabilitySpec("executor", "1.0.0", "chora/executor:1.0.0", 8900, ["manifest", "orchestrator"]),
    CapabilitySpec("storage", "1.0.0", "chora/storage:1.0.0", 9000, ["manifest"]),
    CapabilitySpec("monitor", "1.0.0", "chora/monitor:1.0.0", 9100, ["manifest"]),
    CapabilitySpec("logger", "1.0.0", "chora/logger:1.0.0", 9200, ["manifest"]),
]

async def deploy_capabilities():
    print(f"⏳ Deploying {len(CAPABILITIES)} capabilities via Orchestrator...")

    for cap in CAPABILITIES:
        if not await deploy_capability(cap):
            return False

    print(f"✓ All {len(CAPABILITIES)} capabilities deployed")

    # Wait for all to be healthy
    print("⏳ Waiting for all services to become healthy...")
    if not await wait_for_all_healthy():
        return False

    return True

async def deploy_capability(spec: CapabilitySpec) -> bool:
    """Deploy a capability via Orchestrator API"""
    credentials = load_credentials()

    deployment = {
        "name": spec.name,
        "version": spec.version,
        "image": spec.image,
        "port": spec.port,
        "environment": {
            "MANIFEST_URL": "http://manifest:8500",
            "API_KEY": credentials[f"api_key_{spec.name}"],
        },
        "dependencies": spec.dependencies,
    }

    try:
        response = await http_client.post(
            "http://localhost:8600/v1/deploy",
            json=deployment,
            headers={"Authorization": f"Bearer {credentials['jwt_secret']}"},
            timeout=30
        )

        if response.status_code == 201:
            data = response.json()
            print(f"✓ {spec.name} deployed (http://localhost:{spec.port})")
            return True
        else:
            print(f"✗ Failed to deploy {spec.name}: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Failed to deploy {spec.name}: {e}")
        return False

async def wait_for_all_healthy() -> bool:
    """Wait for all capabilities to report healthy"""
    start_time = time.time()
    timeout = 300  # 5 minutes

    while time.time() - start_time < timeout:
        # Query Manifest for all services
        try:
            response = await http_client.get(
                "http://localhost:8500/v1/services",
                timeout=10
            )

            if response.status_code == 200:
                services = response.json()
                unhealthy = [s for s in services if s["status"] != "up"]

                if len(unhealthy) == 0:
                    elapsed = time.time() - start_time
                    print(f"✓ All services healthy ({elapsed:.1f}s)")
                    return True

                # Show progress
                healthy_count = len(services) - len(unhealthy)
                print(f"⏳ {healthy_count}/{len(services)} healthy, waiting for: {', '.join(s['name'] for s in unhealthy)}")

        except Exception as e:
            print(f"⏳ Checking health... ({e})")

        await asyncio.sleep(5)

    print(f"✗ Not all services became healthy within {timeout}s")
    return False
```

**Success Criteria**:
- All capabilities deployed successfully
- All capabilities registered in Manifest
- All capabilities responding to health checks
- Gateway can route to all capabilities

**Typical Duration**: 3-5 minutes

---

### 3.5 Phase 4: Validation

**Goal**: Verify entire system is operational

**Validation Tests**:

#### Test 1: Service Discovery

```python
async def test_service_discovery() -> bool:
    """Verify all services are discoverable via Manifest"""
    print("Service Discovery Test:")
    print("  ⏳ Querying Manifest for all services...")

    try:
        response = await http_client.get(
            "http://localhost:8500/v1/services",
            timeout=10
        )

        if response.status_code != 200:
            print(f"  ✗ Manifest API error: {response.status_code}")
            return False

        services = response.json()
        print(f"  ✓ Manifest API accessible")
        print(f"  ✓ Found {len(services)} registered services")

        expected = ["manifest", "orchestrator", "gateway", "analyzer", "executor", "storage", "monitor", "logger"]
        found = [s["name"] for s in services]
        missing = set(expected) - set(found)

        if missing:
            print(f"  ✗ Missing services: {', '.join(missing)}")
            return False

        print(f"  ✓ All expected services present")
        return True

    except Exception as e:
        print(f"  ✗ Service discovery failed: {e}")
        return False
```

#### Test 2: Gateway Routing

```python
async def test_gateway_routing() -> bool:
    """Verify Gateway can route requests to backend services"""
    print("\nGateway Routing Test:")
    print("  ⏳ Sending test request through Gateway...")

    try:
        start_time = time.time()
        response = await http_client.post(
            "http://localhost:8700/api/v1/analyzer/analyze",
            json={"text": "bootstrap test"},
            timeout=10
        )

        elapsed_ms = (time.time() - start_time) * 1000

        if response.status_code != 200:
            print(f"  ✗ Gateway routing failed: {response.status_code}")
            return False

        data = response.json()
        print(f"  ✓ Gateway accessible")
        print(f"  ✓ Routed request to analyzer")
        print(f"  ✓ Received valid response ({elapsed_ms:.0f}ms)")
        return True

    except Exception as e:
        print(f"  ✗ Gateway routing test failed: {e}")
        return False
```

#### Test 3: Orchestrator Control

```python
async def test_orchestrator_control() -> bool:
    """Verify Orchestrator can control services"""
    print("\nOrchestrator Control Test:")
    print("  ⏳ Testing service control via Orchestrator...")

    credentials = load_credentials()
    headers = {"Authorization": f"Bearer {credentials['jwt_secret']}"}

    try:
        # Stop analyzer
        print("  ⏳ Stopping analyzer...")
        response = await http_client.post(
            "http://localhost:8600/v1/services/analyzer/stop",
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            print(f"  ✗ Failed to stop analyzer: {response.status_code}")
            return False

        print("  ✓ Stopped analyzer successfully")

        # Wait 2 seconds
        await asyncio.sleep(2)

        # Restart analyzer
        print("  ⏳ Restarting analyzer...")
        response = await http_client.post(
            "http://localhost:8600/v1/services/analyzer/start",
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            print(f"  ✗ Failed to restart analyzer: {response.status_code}")
            return False

        print("  ✓ Restarted analyzer successfully")

        # Wait for health
        if not await wait_for_health("analyzer", "http://localhost:8800/health", timeout=30):
            print("  ✗ Analyzer did not become healthy after restart")
            return False

        print("  ✓ Analyzer healthy after restart")
        print("  ✓ Orchestrator API accessible")
        return True

    except Exception as e:
        print(f"  ✗ Orchestrator control test failed: {e}")
        return False
```

#### Test 4: Health Dashboard

```python
async def test_health_dashboard() -> bool:
    """Verify all services reporting healthy"""
    print("\nHealth Dashboard Test:")
    print("  ⏳ Checking health status of all services...")

    try:
        response = await http_client.get(
            "http://localhost:8500/v1/services",
            timeout=10
        )

        if response.status_code != 200:
            print(f"  ✗ Failed to query Manifest: {response.status_code}")
            return False

        services = response.json()
        unhealthy = [s for s in services if s["status"] != "up"]

        if unhealthy:
            print(f"  ✗ {len(unhealthy)} services unhealthy:")
            for s in unhealthy:
                print(f"    - {s['name']}: {s['status']}")
            return False

        print(f"  ✓ All {len(services)} services reporting healthy")
        print(f"  ✓ No services in unhealthy state")
        return True

    except Exception as e:
        print(f"  ✗ Health dashboard test failed: {e}")
        return False
```

**Success Criteria**: All 4 validation tests pass

**Typical Duration**: 1-2 minutes

---

## 4. State Management

### 4.1 State Model

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict

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
    """Checkpoint for resume capability"""
    phase: int
    timestamp: datetime
    services_running: List[str]
    health_status: Dict[str, bool]

@dataclass
class BootstrapState:
    """Complete bootstrap state"""
    # Current state
    current_phase: int
    status: BootstrapStatus

    # Progress tracking
    completed_phases: List[int] = field(default_factory=list)
    services_started: List[str] = field(default_factory=list)
    services_healthy: List[str] = field(default_factory=list)

    # Credentials
    credentials_generated: bool = False
    credential_files: List[str] = field(default_factory=list)

    # Checkpoints for resume
    checkpoints: List[BootstrapCheckpoint] = field(default_factory=list)

    # Timestamps
    started_at: datetime = field(default_factory=datetime.utcnow)
    last_updated: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    # Error tracking
    last_error: Optional[str] = None
    retry_count: int = 0

    def to_json(self) -> str:
        """Serialize to JSON for persistence"""
        return json.dumps({
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
        }, indent=2)

    @classmethod
    def from_json(cls, data: str) -> "BootstrapState":
        """Deserialize from JSON"""
        obj = json.loads(data)
        return cls(
            current_phase=obj["current_phase"],
            status=BootstrapStatus(obj["status"]),
            completed_phases=obj["completed_phases"],
            services_started=obj["services_started"],
            services_healthy=obj["services_healthy"],
            credentials_generated=obj["credentials_generated"],
            credential_files=obj["credential_files"],
            checkpoints=[
                BootstrapCheckpoint(
                    phase=cp["phase"],
                    timestamp=datetime.fromisoformat(cp["timestamp"]),
                    services_running=cp["services_running"],
                    health_status=cp["health_status"],
                )
                for cp in obj["checkpoints"]
            ],
            started_at=datetime.fromisoformat(obj["started_at"]),
            last_updated=datetime.fromisoformat(obj["last_updated"]),
            completed_at=datetime.fromisoformat(obj["completed_at"]) if obj["completed_at"] else None,
            last_error=obj["last_error"],
            retry_count=obj["retry_count"],
        )
```

### 4.2 State Persistence

```python
STATE_PATH = Path(".chora/bootstrap-state.json")

async def save_state(state: BootstrapState):
    """Atomically save state to disk"""
    # Update last_updated timestamp
    state.last_updated = datetime.utcnow()

    # Write to temporary file first
    temp_path = STATE_PATH.with_suffix(".tmp")
    temp_path.write_text(state.to_json())

    # Atomic rename
    temp_path.rename(STATE_PATH)

async def load_state() -> Optional[BootstrapState]:
    """Load state from disk"""
    if not STATE_PATH.exists():
        return None

    try:
        data = STATE_PATH.read_text()
        return BootstrapState.from_json(data)
    except Exception as e:
        print(f"⚠️  Warning: Failed to load state: {e}")
        print("   Starting fresh bootstrap...")
        return None

async def create_checkpoint(state: BootstrapState):
    """Create checkpoint for current phase"""
    # Query Manifest for current services
    try:
        response = await http_client.get("http://localhost:8500/v1/services", timeout=10)
        if response.status_code == 200:
            services = response.json()
            checkpoint = BootstrapCheckpoint(
                phase=state.current_phase,
                timestamp=datetime.utcnow(),
                services_running=[s["name"] for s in services],
                health_status={s["name"]: s["status"] == "up" for s in services},
            )
            state.checkpoints.append(checkpoint)
            await save_state(state)
    except:
        pass  # Checkpoint is best-effort
```

### 4.3 Resume Logic

```python
async def resume_bootstrap(state: BootstrapState):
    """Resume bootstrap from previous failure"""
    print(f"Resuming from Phase {state.current_phase}...")
    print(f"Previous attempt: {state.started_at}")
    print(f"Services started: {', '.join(state.services_started)}")

    # Verify services from previous phases are still running
    for service in state.services_started:
        if not await is_service_healthy(service):
            print(f"⚠️  Warning: {service} no longer healthy")
            print(f"   Restarting {service}...")
            await start_service(service)

    # Continue from current phase
    if state.current_phase == 0:
        await run_phase_0(state)
    elif state.current_phase == 1:
        await run_phase_1(state)
    elif state.current_phase == 2:
        await run_phase_2(state)
    elif state.current_phase == 3:
        await run_phase_3(state)
    elif state.current_phase == 4:
        await run_phase_4(state)
```

---

## 5. Configuration File Format

### 5.1 Bootstrap Configuration

**File**: `.chora/bootstrap-config.yml`

```yaml
version: "1.0"

# Environment: dev, staging, prod
environment: dev

# Service definitions
services:
  manifest:
    phase: 1  # Core Services
    docker_compose: docker-compose.manifest.yml
    health_endpoint: http://localhost:8500/health
    timeout: 60
    dependencies: []

  orchestrator:
    phase: 2  # Infrastructure
    docker_compose: docker-compose.orchestrator.yml
    health_endpoint: http://localhost:8600/health
    timeout: 120
    dependencies: [manifest]

  gateway:
    phase: 2
    docker_compose: docker-compose.gateway.yml
    health_endpoint: http://localhost:8700/health
    timeout: 120
    dependencies: [manifest]

  analyzer:
    phase: 3  # Capabilities
    deploy_via: orchestrator  # Deploy via Orchestrator API
    version: "1.0.0"
    timeout: 120
    dependencies: [manifest, orchestrator]

  executor:
    phase: 3
    deploy_via: orchestrator
    version: "1.0.0"
    timeout: 120
    dependencies: [manifest, orchestrator, analyzer]

  storage:
    phase: 3
    deploy_via: orchestrator
    version: "1.0.0"
    timeout: 120
    dependencies: [manifest]

  monitor:
    phase: 3
    deploy_via: orchestrator
    version: "1.0.0"
    timeout: 120
    dependencies: [manifest]

  logger:
    phase: 3
    deploy_via: orchestrator
    version: "1.0.0"
    timeout: 120
    dependencies: [manifest]

# Timeout configurations (seconds)
timeouts:
  health_check: 120  # Max time to wait for service health
  phase_0: 300       # Pre-bootstrap (5 min)
  phase_1: 300       # Core services (5 min)
  phase_2: 600       # Infrastructure (10 min)
  phase_3: 900       # Capabilities (15 min)
  phase_4: 120       # Validation (2 min)

# Retry configuration
retry:
  initial_delay: 1     # Initial delay between retries (seconds)
  max_delay: 30        # Maximum delay between retries (seconds)
  backoff_factor: 2    # Exponential backoff multiplier
  max_attempts: 10     # Maximum retry attempts before failure

# Credential generation
credentials:
  jwt_secret_bits: 256
  api_key_bits: 128
  storage_path: .chora/credentials.json
  storage_permissions: "0600"

# Logging
logging:
  level: info  # debug, info, warning, error
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: .chora/logs/bootstrap.log
  max_bytes: 10485760  # 10 MB
  backup_count: 5

# Validation tests (Phase 4)
validation:
  tests:
    - name: service_discovery
      enabled: true
      timeout: 30
    - name: gateway_routing
      enabled: true
      timeout: 30
    - name: orchestrator_control
      enabled: true
      timeout: 60
    - name: health_dashboard
      enabled: true
      timeout: 30
```

---

## 6. Error Handling

### 6.1 Error Codes

| Exit Code | Name | Description | Recovery |
|-----------|------|-------------|----------|
| 0 | SUCCESS | Bootstrap completed | N/A |
| 1 | PREREQ_FAILED | Docker/Python/port check failed | Install dependencies, free ports |
| 2 | CORE_FAILED | Manifest failed to start | Check Docker, logs, rollback |
| 3 | INFRA_FAILED | Orchestrator/Gateway failed | Check dependencies, rollback |
| 4 | CAP_FAILED | Capability failed to deploy | Check Orchestrator, rollback |
| 5 | VALIDATION_FAILED | Phase 4 tests failed | Check logs, manual verification |
| 6 | USER_INTERRUPTED | User pressed Ctrl-C | Resume with `chora bootstrap` |
| 7 | CONFIG_ERROR | Invalid configuration file | Fix config, validate syntax |
| 8 | STATE_CORRUPTED | State file corrupted | Delete `.chora/bootstrap-state.json`, restart |

### 6.2 Error Messages

**Template**:
```
✗ [ERROR_CODE] Error description

Possible causes:
  - Cause 1
  - Cause 2
  - Cause 3

Suggested actions:
  1. Action 1
  2. Action 2
  3. If still failing, run: chora bootstrap rollback

For more details, see logs: .chora/logs/bootstrap.log
```

**Example**:
```
✗ [CORE_FAILED] Manifest Registry failed to start

Possible causes:
  - Port 8500 already in use
  - Docker daemon not running
  - Insufficient memory (need 2GB)

Suggested actions:
  1. Check if port is in use: lsof -i :8500
  2. Verify Docker is running: docker ps
  3. Check available memory: free -h
  4. View detailed logs: docker logs chora-manifest
  5. If still failing, run: chora bootstrap rollback

For more details, see logs: .chora/logs/bootstrap.log
```

---

## 7. Performance Specifications

### 7.1 Target Metrics

| Metric | Target | Acceptable | Unacceptable |
|--------|--------|------------|--------------|
| Total Bootstrap Time | < 10 min | 10-15 min | > 15 min |
| Phase 0 Duration | < 1 min | 1-2 min | > 2 min |
| Phase 1 Duration | < 2 min | 2-3 min | > 3 min |
| Phase 2 Duration | < 3 min | 3-5 min | > 5 min |
| Phase 3 Duration | < 5 min | 5-8 min | > 8 min |
| Phase 4 Duration | < 2 min | 2-3 min | > 3 min |
| Health Check Latency | < 100ms | 100-500ms | > 500ms |
| Resume Overhead | < 10s | 10-30s | > 30s |
| Rollback Time | < 30s | 30-60s | > 60s |

### 7.2 Scalability

**Services**: Bootstrap supports 3-50 services
- 3-10 services: Optimal (< 10 min)
- 10-30 services: Good (10-15 min)
- 30-50 services: Acceptable (15-25 min)
- 50+ services: Consider clustering or advanced tier

**Concurrency**: Phase 3 can deploy services in parallel (experimental)
- Sequential: 5 services × 1.5 min = 7.5 min
- Parallel (2x): 5 services / 2 × 1.5 min = 3.75 min
- Parallel (3x): 5 services / 3 × 1.5 min = 2.5 min

---

## 8. Security Specifications

### 8.1 Credential Security

**Generation**:
```python
import secrets

# JWT Secret: 256-bit (64 hex chars)
jwt_secret = secrets.token_hex(32)

# API Keys: 128-bit (32 base64 chars)
api_key = secrets.token_urlsafe(32)
```

**Storage**:
- File: `.chora/credentials.json`
- Permissions: `0600` (owner read/write only)
- Format: JSON (not logged, not displayed)

**Distribution**:
- Via environment variables (not command-line args)
- Injected into Docker containers at runtime
- Never logged to stdout/stderr

**Rotation** (Manual in v1.0):
```bash
# Generate new credentials
chora bootstrap config rotate-credentials

# Update all running services
chora bootstrap config apply-credentials
```

### 8.2 Network Security

**Development**:
- All services bind to `localhost` only
- No external exposure by default

**Production**:
- Services communicate via internal Docker network
- Gateway is only public-facing service
- TLS required for external traffic (configured separately)

### 8.3 Audit Logging

**Log Format**:
```json
{
  "timestamp": "2025-11-12T10:15:30Z",
  "level": "INFO",
  "phase": 1,
  "action": "start_service",
  "service": "manifest",
  "user": "operator",
  "result": "success",
  "duration_ms": 2300
}
```

**Log Retention**: 90 days (configurable)

**Log Location**: `.chora/logs/bootstrap.log`

---

## 9. Testing Protocol

### 9.1 Unit Tests

**Coverage Target**: ≥ 90%

**Key Test Cases**:
- State serialization/deserialization
- Health check retry logic with exponential backoff
- Credential generation entropy
- Rollback logic for each phase
- Configuration validation

**Example**:
```python
import pytest
from bootstrap.state import BootstrapState, BootstrapStatus

def test_state_serialization():
    """Test state can be serialized and deserialized"""
    state = BootstrapState(
        current_phase=2,
        status=BootstrapStatus.IN_PROGRESS,
        services_started=["manifest", "orchestrator"]
    )

    json_str = state.to_json()
    loaded = BootstrapState.from_json(json_str)

    assert loaded.current_phase == 2
    assert loaded.status == BootstrapStatus.IN_PROGRESS
    assert loaded.services_started == ["manifest", "orchestrator"]

def test_health_check_exponential_backoff():
    """Test health check uses exponential backoff"""
    delays = []

    async def mock_wait_for_health():
        nonlocal delays
        delay = 1
        for _ in range(5):
            delays.append(delay)
            await asyncio.sleep(delay)
            delay = min(delay * 2, 30)

    asyncio.run(mock_wait_for_health())
    assert delays == [1, 2, 4, 8, 16]
```

### 9.2 Integration Tests

**Scenarios**:
1. **Fresh Bootstrap**: Clean VM → full bootstrap → validation passes
2. **Resume from Phase 1 Failure**: Simulate Manifest crash, verify resume
3. **Resume from Phase 2 Failure**: Simulate Orchestrator crash, verify resume
4. **Resume from Phase 3 Failure**: Simulate capability deployment failure, verify resume
5. **Rollback from Phase 2**: Trigger failure, verify rollback to Phase 1
6. **Rollback from Phase 3**: Trigger failure, verify rollback to Phase 2
7. **Idempotency**: Run bootstrap 5x on same system, verify no errors
8. **Parallel Execution**: Deploy capabilities in parallel, verify all healthy
9. **Configuration Override**: Use custom config, verify applied
10. **Credential Security**: Verify credentials never logged

**Test Framework**: pytest + Docker-in-Docker

### 9.3 Performance Tests

**Benchmarks**:
- Measure total bootstrap time on standard VM (4 CPU, 8GB RAM, SSD)
- Measure phase-by-phase durations
- Measure health check latency (p50, p95, p99)
- Measure resume overhead
- Measure rollback time

**Load Tests**:
- Bootstrap with 10, 20, 30, 50 services
- Parallel deployment with 2x, 3x, 5x concurrency
- Simultaneous bootstraps on 5 VMs

---

## 10. Extensibility

### 10.1 Custom Phase Hooks

**Future Enhancement** (v1.1): Allow users to inject custom logic at phase transitions

**API**:
```yaml
# bootstrap-config.yml
hooks:
  pre_phase_1:
    - script: ./scripts/pre-manifest.sh
      timeout: 60
  post_phase_1:
    - script: ./scripts/post-manifest.sh
      timeout: 60
  post_phase_3:
    - script: ./scripts/send-notification.sh
      args: ["Bootstrap completed"]
```

### 10.2 Custom Validation Tests

**API**:
```yaml
# bootstrap-config.yml
validation:
  tests:
    - name: custom_api_test
      script: ./tests/test-api.sh
      timeout: 30
      required: true  # Fail bootstrap if this fails
    - name: custom_load_test
      script: ./tests/load-test.sh
      timeout: 120
      required: false  # Warning only
```

### 10.3 Plugin System

**Future Enhancement** (v2.0): Plugin architecture for custom bootstrap logic

**Example Plugin**:
```python
from bootstrap.plugin import BootstrapPlugin

class CustomPlugin(BootstrapPlugin):
    def on_phase_start(self, phase: int):
        print(f"Starting phase {phase}")

    def on_service_started(self, service: str):
        # Send metric to monitoring system
        metrics.send("bootstrap.service_started", {"service": service})

    def on_bootstrap_complete(self):
        # Send Slack notification
        slack.send("Bootstrap completed successfully!")
```

---

## Appendix A: Complete Example

**End-to-End Bootstrap Execution** (Fresh Dev Environment):

```bash
$ chora bootstrap

Chora Bootstrap v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 0: Pre-Bootstrap Validation
  ✓ Docker 24.0.6 detected
  ✓ Python 3.11.5 detected
  ✓ Ports 8500-9200 available
  ✓ Disk space: 45GB available
  ✓ Created directory structure
  ✓ Generated credentials

Phase 1: Core Services (1/4)
  ⏳ Starting Manifest Registry...
  ✓ Manifest Registry started (http://localhost:8500)
  ✓ Manifest healthy (2.3s)
  ✓ Manifest self-registered

Phase 2: Infrastructure Services (2/4)
  ⏳ Starting Orchestrator...
  ✓ Orchestrator started (http://localhost:8600)
  ✓ Orchestrator healthy (4.1s)
  ✓ Orchestrator registered with Manifest
  ⏳ Starting Gateway...
  ✓ Gateway started (http://localhost:8700)
  ✓ Gateway healthy (3.7s)
  ✓ Gateway registered with Manifest

Phase 3: Capability Services (3/4)
  ⏳ Deploying 5 capabilities via Orchestrator...
  ✓ analyzer deployed (http://localhost:8800)
  ✓ executor deployed (http://localhost:8900)
  ✓ storage deployed (http://localhost:9000)
  ✓ monitor deployed (http://localhost:9100)
  ✓ logger deployed (http://localhost:9200)
  ⏳ Waiting for all services to become healthy...
  ⏳ 3/5 healthy, waiting for: executor, logger
  ⏳ 4/5 healthy, waiting for: logger
  ✓ All services healthy (12.5s)

Phase 4: Validation (4/4)
  Service Discovery Test:
    ✓ Manifest API accessible
    ✓ Found 8 registered services
    ✓ All expected services present

  Gateway Routing Test:
    ✓ Gateway accessible
    ✓ Routed request to analyzer
    ✓ Received valid response (42ms)

  Orchestrator Control Test:
    ⏳ Stopping analyzer...
    ✓ Stopped analyzer successfully
    ⏳ Restarting analyzer...
    ✓ Restarted analyzer successfully
    ✓ Analyzer healthy after restart (4.2s)
    ✓ Orchestrator API accessible

  Health Dashboard Test:
    ✓ All 8 services reporting healthy
    ✓ No services in unhealthy state

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Bootstrap completed successfully in 8m 34s

System Status:
  8 services running
  8 services healthy
  0 services unhealthy

Next steps:
  1. View system status: chora bootstrap status
  2. Access Gateway: http://localhost:8700
  3. Access Orchestrator UI: http://localhost:8600/ui
  4. View logs: docker-compose logs -f

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Appendix B: State File Example

**File**: `.chora/bootstrap-state.json`

```json
{
  "current_phase": 4,
  "status": "completed",
  "completed_phases": [0, 1, 2, 3, 4],
  "services_started": [
    "manifest",
    "orchestrator",
    "gateway",
    "analyzer",
    "executor",
    "storage",
    "monitor",
    "logger"
  ],
  "services_healthy": [
    "manifest",
    "orchestrator",
    "gateway",
    "analyzer",
    "executor",
    "storage",
    "monitor",
    "logger"
  ],
  "credentials_generated": true,
  "credential_files": [".chora/credentials.json"],
  "checkpoints": [
    {
      "phase": 1,
      "timestamp": "2025-11-12T10:05:30Z",
      "services_running": ["manifest"],
      "health_status": {"manifest": true}
    },
    {
      "phase": 2,
      "timestamp": "2025-11-12T10:08:45Z",
      "services_running": ["manifest", "orchestrator", "gateway"],
      "health_status": {
        "manifest": true,
        "orchestrator": true,
        "gateway": true
      }
    },
    {
      "phase": 3,
      "timestamp": "2025-11-12T10:13:20Z",
      "services_running": [
        "manifest",
        "orchestrator",
        "gateway",
        "analyzer",
        "executor",
        "storage",
        "monitor",
        "logger"
      ],
      "health_status": {
        "manifest": true,
        "orchestrator": true,
        "gateway": true,
        "analyzer": true,
        "executor": true,
        "storage": true,
        "monitor": true,
        "logger": true
      }
    }
  ],
  "started_at": "2025-11-12T10:05:00Z",
  "last_updated": "2025-11-12T10:13:34Z",
  "completed_at": "2025-11-12T10:13:34Z",
  "last_error": null,
  "retry_count": 0
}
```

---

**Document Status**: DRAFT v1.0
**Review Status**: Pending review
**Approval Status**: Pending approval
**Next Review Date**: 2025-12-12
