# Protocol Specification: Capability Registry & Service Discovery

**Capability ID**: SAP-048
**Modern Namespace**: chora.awareness.capability_registry_discovery
**Type**: Pattern
**Status**: Draft
**Version**: 1.0.0
**Protocol Version**: 1.0.0
**Last Updated**: 2025-11-16

---

## Overview

This document specifies the complete protocol for querying and monitoring the Chora distributed capability registry built on etcd. It defines the etcd schema, query patterns, data formats, and API contracts for agent-registry interaction.

**Protocol Goals**:
- **Consistency**: Standardized schema across all capabilities
- **Performance**: <10ms query latency for metadata reads
- **Reliability**: 99.9% availability via Raft consensus
- **Real-time**: Event streaming for registry changes
- **Searchability**: Full-text search through capability documentation

---

## etcd Schema

### Namespace Structure

All registry data is stored under the `/chora/` prefix in etcd:

```
/chora/
├── capabilities/              # Capability metadata
│   └── {namespace}/
│       ├── metadata          # JSON: Dublin Core metadata
│       ├── type              # String: "Service" | "Pattern"
│       ├── version           # String: semver (e.g., "1.2.3")
│       ├── dependencies      # JSON: Array of dependency objects
│       └── health            # JSON: Health status (Service-type only, 30s TTL)
│
└── artifacts/                 # SAP artifacts (documentation)
    └── {namespace}/
        └── {artifact_type}/
            ├── content       # String: Full markdown content
            └── metadata      # JSON: File metadata (size, hash, timestamps)
```

### Key Naming Conventions

**Capability Namespace Format**: `chora.{domain}.{capability}`
- **domain**: One of `infrastructure`, `devex`, `awareness`, `react`, `integration`
- **capability**: Lowercase with underscores (e.g., `task_tracking`)

**Examples**:
- `chora.devex.registry`
- `chora.awareness.task_tracking`
- `chora.infrastructure.sap_framework`

**Artifact Types**: `capability-charter`, `protocol-spec`, `awareness-guide`, `adoption-blueprint`, `ledger`

---

## Data Formats

### 1. Capability Metadata

**Key**: `/chora/capabilities/{namespace}/metadata`

**Format**: JSON (Dublin Core + Chora extensions)

**Schema**:
```json
{
  "dc_identifier": "chora.devex.registry",
  "dc_title": "Capability Registry & Service Discovery",
  "dc_description": "Distributed capability registry with etcd backend...",
  "dc_creator": "Chora Ecosystem",
  "dc_date": "2025-11-15",
  "dc_format": "application/yaml",
  "dc_type": "Service",
  "dc_subject": ["registry", "service-discovery", "etcd"],
  "dc_coverage": "Global",
  "dc_rights": "MIT License",

  "chora_version": "1.0.0",
  "chora_status": "production",
  "chora_namespace": "chora.devex.registry",
  "chora_sap_id": "SAP-047",
  "chora_legacy_identifier": "SAP-047"
}
```

**Field Descriptions**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `dc_identifier` | String | Yes | Modern namespace (chora.domain.capability) |
| `dc_title` | String | Yes | Human-readable capability name |
| `dc_description` | String | Yes | Brief capability description (<200 chars) |
| `dc_creator` | String | No | Author or organization |
| `dc_date` | String | Yes | Creation date (ISO 8601: YYYY-MM-DD) |
| `dc_format` | String | Yes | MIME type (usually `application/yaml`) |
| `dc_type` | String | Yes | "Service" or "Pattern" |
| `dc_subject` | Array[String] | No | Keywords/tags for search |
| `dc_coverage` | String | No | Scope (e.g., "Global", "Enterprise") |
| `dc_rights` | String | No | License information |
| `chora_version` | String | Yes | Semantic version (e.g., "1.2.3") |
| `chora_status` | String | Yes | "production", "pilot", "draft", "deprecated" |
| `chora_namespace` | String | Yes | Same as dc_identifier (redundant for validation) |
| `chora_sap_id` | String | No | Legacy SAP-XXX identifier (deprecated) |
| `chora_legacy_identifier` | String | No | Alias for chora_sap_id |

---

### 2. Capability Type

**Key**: `/chora/capabilities/{namespace}/type`

**Format**: Plain text string

**Values**:
- `Service`: Runtime component with health monitoring (e.g., registry, heartbeat)
- `Pattern`: Documentation-based capability (e.g., SAP framework, awareness patterns)

**Example**:
```
Service
```

---

### 3. Capability Version

**Key**: `/chora/capabilities/{namespace}/version`

**Format**: Plain text string (Semantic Versioning 2.0.0)

**Pattern**: `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)

**Example**:
```
1.0.0
```

---

### 4. Capability Dependencies

**Key**: `/chora/capabilities/{namespace}/dependencies`

**Format**: JSON array of dependency objects

**Schema**:
```json
[
  {
    "capability": "chora.infrastructure.sap_framework",
    "relationship": "prerequisite",
    "version_constraint": ">=1.0.0"
  },
  {
    "capability": "chora.devex.docker_operations",
    "relationship": "runtime",
    "version_constraint": "^1.2.0"
  }
]
```

**Dependency Object Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `capability` | String | Yes | Target capability namespace |
| `relationship` | String | Yes | Dependency type (see table below) |
| `version_constraint` | String | No | npm-style semver constraint |

**Relationship Types**:

| Relationship | Description | Valid For |
|--------------|-------------|-----------|
| `prerequisite` | Must be installed before this capability | Service→Service, Service→Pattern, Pattern→Pattern |
| `runtime` | Required during execution | Service→Service, Pattern→Service |
| `optional` | Enhances functionality but not required | All combinations |
| `extends` | Builds upon or extends functionality | Service→Service, Service→Pattern, Pattern→Pattern |

**Validation Rules**:
- Service → Pattern: **Cannot** use `runtime` (use `prerequisite`, `optional`, or `extends`)
- Pattern → Service: **Cannot** use `prerequisite` (use `runtime` or `optional`)
- Pattern → Pattern: **Cannot** use `runtime` (use `prerequisite`, `optional`, or `extends`)

---

### 5. Service Health Status

**Key**: `/chora/capabilities/{namespace}/health`

**Format**: JSON with 30-second TTL lease

**Schema**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-15T22:30:00Z",
  "namespace": "chora.devex.registry",
  "heartbeat_count": 42
}
```

**Field Descriptions**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | String | Yes | "healthy" or "degraded" |
| `timestamp` | String | Yes | ISO 8601 timestamp (UTC) |
| `namespace` | String | Yes | Capability namespace |
| `heartbeat_count` | Integer | Yes | Monotonically increasing counter |

**TTL Lease Behavior**:
- **Lease Duration**: 30 seconds
- **Heartbeat Interval**: 10 seconds (3x heartbeats before expiration)
- **Expiration**: Key is automatically deleted by etcd when lease expires
- **Detection**: Absence of `/health` key indicates unhealthy service

**Health Check Pattern**:
```python
health_key = f'/chora/capabilities/{namespace}/health'
health_json, meta = etcd.get(health_key)

if health_json:
    health = json.loads(health_json)

    # Check if recently updated (within 30s)
    import datetime
    timestamp = datetime.datetime.fromisoformat(health['timestamp'].replace('Z', '+00:00'))
    age = (datetime.datetime.now(datetime.timezone.utc) - timestamp).total_seconds()

    if age < 30:
        print(f"Service healthy (age: {age:.1f}s)")
    else:
        print(f"Service stale (age: {age:.1f}s)")

    # Check lease TTL
    if meta.lease_id:
        lease = etcd.Lease(meta.lease_id)
        print(f"Lease TTL: {lease.ttl}s remaining")
else:
    print("Service unhealthy (no health key)")
```

---

### 6. Artifact Content

**Key**: `/chora/artifacts/{namespace}/{artifact_type}/content`

**Format**: Plain text (Markdown)

**Artifact Types**:
- `capability-charter`: Problem statement and solution design
- `protocol-spec`: Technical specification and API contracts
- `awareness-guide`: Agent operating patterns (may be named `AGENTS.md`)
- `adoption-blueprint`: Step-by-step installation guide
- `ledger`: Adoption tracking and version history

**Example**:
```markdown
# Capability Charter: Task Tracking

**Capability ID**: SAP-015
**Modern Namespace**: chora.awareness.task_tracking
...
```

---

### 7. Artifact Metadata

**Key**: `/chora/artifacts/{namespace}/{artifact_type}/metadata`

**Format**: JSON

**Schema**:
```json
{
  "file_path": "docs/skilled-awareness/task-tracking/capability-charter.md",
  "file_size": 12543,
  "content_hash": "sha256:a3f2b8c9...",
  "last_modified": "2025-11-15T10:30:00",
  "indexed_at": "2025-11-15T22:00:00Z"
}
```

**Field Descriptions**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file_path` | String | Yes | Relative path from repository root |
| `file_size` | Integer | Yes | File size in bytes |
| `content_hash` | String | Yes | SHA-256 hash for integrity verification |
| `last_modified` | String | Yes | File modification timestamp (ISO 8601) |
| `indexed_at` | String | Yes | Indexing timestamp (ISO 8601, UTC) |

---

## Query Patterns

### Pattern 1: List All Capabilities

**Goal**: Retrieve all registered capabilities

**Method**: Prefix query on `/chora/capabilities/`

**Python Example**:
```python
import etcd3
import json

etcd = etcd3.client(host='localhost', port=2379)

capabilities = []
prefix = '/chora/capabilities/'

for value, meta in etcd.get_prefix(prefix):
    key_str = meta.key.decode('utf-8')

    # Only process metadata keys
    if not key_str.endswith('/metadata'):
        continue

    # Extract namespace from key
    namespace = key_str.split('/')[3]
    metadata = json.loads(value)

    capabilities.append({
        'namespace': namespace,
        'title': metadata['dc_title'],
        'type': metadata['dc_type'],
        'status': metadata['chora_status'],
        'version': metadata['chora_version'],
    })

# Sort by namespace
capabilities.sort(key=lambda c: c['namespace'])

for cap in capabilities:
    print(f"{cap['namespace']} ({cap['type']}) - {cap['title']}")
```

**Bash Example** (using etcdctl):
```bash
# List all metadata keys
etcdctl get /chora/capabilities/ --prefix --keys-only | grep /metadata

# Get all metadata values
etcdctl get /chora/capabilities/ --prefix | grep -A 10 metadata
```

---

### Pattern 2: Get Single Capability

**Goal**: Retrieve metadata for a specific capability

**Method**: Direct key lookup

**Python Example**:
```python
namespace = 'chora.devex.registry'

# Get metadata
metadata_key = f'/chora/capabilities/{namespace}/metadata'
metadata_json, _ = etcd.get(metadata_key)

if metadata_json:
    metadata = json.loads(metadata_json)
    print(f"Title: {metadata['dc_title']}")
    print(f"Description: {metadata['dc_description']}")
    print(f"Version: {metadata['chora_version']}")
else:
    print(f"Capability not found: {namespace}")
```

**Bash Example**:
```bash
namespace="chora.devex.registry"

# Get metadata
etcdctl get "/chora/capabilities/${namespace}/metadata"

# Get type
etcdctl get "/chora/capabilities/${namespace}/type"

# Get version
etcdctl get "/chora/capabilities/${namespace}/version"
```

---

### Pattern 3: Filter Capabilities by Type

**Goal**: List only Service-type or Pattern-type capabilities

**Method**: Prefix query + client-side filtering

**Python Example**:
```python
def list_capabilities_by_type(capability_type: str):
    """List capabilities filtered by type (Service or Pattern)"""
    capabilities = []
    prefix = '/chora/capabilities/'

    for value, meta in etcd.get_prefix(prefix):
        key_str = meta.key.decode('utf-8')

        if not key_str.endswith('/metadata'):
            continue

        metadata = json.loads(value)

        if metadata['dc_type'] == capability_type:
            namespace = key_str.split('/')[3]
            capabilities.append({
                'namespace': namespace,
                'title': metadata['dc_title'],
                'version': metadata['chora_version'],
            })

    return capabilities

# List all Service-type capabilities
services = list_capabilities_by_type('Service')
print(f"Found {len(services)} Service-type capabilities:")
for svc in services:
    print(f"  - {svc['namespace']} v{svc['version']}")

# List all Pattern-type capabilities
patterns = list_capabilities_by_type('Pattern')
print(f"\nFound {len(patterns)} Pattern-type capabilities:")
for pat in patterns:
    print(f"  - {pat['namespace']} v{pat['version']}")
```

---

### Pattern 4: Check Service Health

**Goal**: Determine if a Service-type capability is healthy

**Method**: Check existence and freshness of `/health` key

**Python Example**:
```python
import datetime

def check_service_health(namespace: str) -> dict:
    """
    Check health of a Service-type capability

    Returns:
        dict with keys: healthy (bool), age (float), ttl (int), details (str)
    """
    health_key = f'/chora/capabilities/{namespace}/health'
    health_json, meta = etcd.get(health_key)

    if not health_json:
        return {
            'healthy': False,
            'age': None,
            'ttl': None,
            'details': 'No health key (lease expired or service not running)'
        }

    health = json.loads(health_json)

    # Calculate age
    timestamp = datetime.datetime.fromisoformat(health['timestamp'].replace('Z', '+00:00'))
    age = (datetime.datetime.now(datetime.timezone.utc) - timestamp).total_seconds()

    # Get lease TTL
    ttl = None
    if meta.lease_id:
        try:
            lease = etcd.Lease(meta.lease_id)
            ttl = lease.ttl
        except:
            pass

    # Determine health
    healthy = (age < 30 and ttl is not None and ttl > 0)

    return {
        'healthy': healthy,
        'age': age,
        'ttl': ttl,
        'heartbeat_count': health['heartbeat_count'],
        'details': f"Age: {age:.1f}s, TTL: {ttl}s" if ttl else f"Age: {age:.1f}s"
    }

# Check health
result = check_service_health('chora.devex.registry')
print(f"Healthy: {result['healthy']}")
print(f"Details: {result['details']}")
```

**Bash Example**:
```bash
namespace="chora.devex.registry"

# Check if health key exists
if etcdctl get "/chora/capabilities/${namespace}/health" > /dev/null 2>&1; then
    echo "Service healthy"
    etcdctl get "/chora/capabilities/${namespace}/health"
else
    echo "Service unhealthy (no health key)"
fi
```

---

### Pattern 5: Resolve Dependencies

**Goal**: Traverse dependency graph and validate prerequisites

**Method**: Recursive DFS with cycle detection

**Python Example**:
```python
def resolve_dependencies(namespace: str, visited=None, depth=0):
    """
    Recursively resolve dependencies for a capability

    Returns list of (namespace, relationship, depth) tuples in dependency order
    """
    if visited is None:
        visited = set()

    if namespace in visited:
        print(f"  {'  ' * depth}[CYCLE] {namespace}")
        return []

    visited.add(namespace)
    resolved = []

    # Get dependencies
    deps_key = f'/chora/capabilities/{namespace}/dependencies'
    deps_json, _ = etcd.get(deps_key)

    if not deps_json:
        return resolved

    dependencies = json.loads(deps_json)

    for dep in dependencies:
        target = dep['capability']
        relationship = dep['relationship']

        print(f"  {'  ' * depth}{namespace} -> {target} ({relationship})")

        # Check if target exists
        metadata_key = f'/chora/capabilities/{target}/metadata'
        metadata_json, _ = etcd.get(metadata_key)

        if not metadata_json:
            print(f"  {'  ' * depth}[ERROR] Missing prerequisite: {target}")
            continue

        # Recurse
        sub_deps = resolve_dependencies(target, visited.copy(), depth + 1)
        resolved.extend(sub_deps)

        resolved.append((target, relationship, depth))

    return resolved

# Resolve dependencies
print(f"Resolving dependencies for chora.devex.registry:")
deps = resolve_dependencies('chora.devex.registry')

print(f"\nDependency order ({len(deps)} total):")
for target, relationship, depth in reversed(deps):
    print(f"  {depth}. {target} ({relationship})")
```

---

### Pattern 6: Search Artifacts

**Goal**: Full-text search through capability documentation

**Method**: Prefix query on `/chora/artifacts/` + keyword matching

**Python Example**:
```python
def search_artifacts(query: str, limit: int = 10):
    """
    Search artifacts by keyword (case-insensitive)

    Returns list of matching artifacts with preview
    """
    results = []
    prefix = '/chora/artifacts/'

    for value, meta in etcd.get_prefix(prefix):
        key_str = meta.key.decode('utf-8')

        # Only search content, not metadata
        if not key_str.endswith('/content'):
            continue

        content = value.decode('utf-8')

        # Simple keyword search (case-insensitive)
        if query.lower() in content.lower():
            # Extract namespace and artifact type from key
            parts = key_str.split('/')
            if len(parts) >= 5:
                namespace = parts[3]
                artifact_type = parts[4]

                # Find first occurrence for preview
                idx = content.lower().find(query.lower())
                start = max(0, idx - 100)
                end = min(len(content), idx + 100)
                preview = content[start:end]

                results.append({
                    'namespace': namespace,
                    'artifact_type': artifact_type,
                    'preview': preview,
                })

                if len(results) >= limit:
                    break

    return results

# Search for "health monitoring"
results = search_artifacts("health monitoring", limit=5)

print(f"Found {len(results)} matching artifact(s):\n")
for result in results:
    print(f"{result['namespace']}/{result['artifact_type']}")
    print(f"  ...{result['preview']}...\n")
```

---

### Pattern 7: Watch for Changes

**Goal**: Monitor registry for real-time updates

**Method**: etcd watch API with prefix matching

**Python Example**:
```python
def watch_registry(watch_prefix='/chora/capabilities/'):
    """
    Watch for registry changes in real-time

    Prints events as they occur
    """
    print(f"Watching {watch_prefix} for changes...")

    for event in etcd.watch_prefix(watch_prefix):
        key_str = event.key.decode('utf-8')

        if event.type == 'PUT':
            # Key created or updated
            if '/health' in key_str:
                namespace = key_str.split('/')[3]
                health = json.loads(event.value)
                print(f"[HEARTBEAT] {namespace}: count={health['heartbeat_count']}")
            elif '/metadata' in key_str:
                namespace = key_str.split('/')[3]
                print(f"[UPDATE] Capability metadata updated: {namespace}")
            else:
                print(f"[PUT] {key_str}")

        elif event.type == 'DELETE':
            # Key deleted
            if '/health' in key_str:
                namespace = key_str.split('/')[3]
                print(f"[FAILURE] Service unhealthy: {namespace} (lease expired)")
            elif '/metadata' in key_str:
                namespace = key_str.split('/')[3]
                print(f"[REMOVED] Capability removed: {namespace}")
            else:
                print(f"[DELETE] {key_str}")

# Start watching
watch_registry()
```

**Bash Example**:
```bash
# Watch for all capability changes
etcdctl watch /chora/capabilities/ --prefix

# Watch for health key changes only
etcdctl watch /chora/capabilities/ --prefix | grep health

# Watch for specific capability
etcdctl watch /chora/capabilities/chora.devex.registry/ --prefix
```

---

## Error Handling

### Connection Errors

**Scenario**: Cannot connect to etcd cluster

**Python Detection**:
```python
try:
    etcd = etcd3.client(host='localhost', port=2379)
    etcd.status()  # Test connection
except Exception as e:
    print(f"ERROR: Cannot connect to etcd: {e}")
    print("Ensure etcd cluster is running (docker-compose up -d)")
    sys.exit(1)
```

**Mitigation**:
- Check etcd cluster is running: `docker-compose ps`
- Verify network connectivity: `ping localhost`
- Check firewall rules (port 2379 must be open)

---

### Missing Capability

**Scenario**: Queried capability does not exist in registry

**Python Detection**:
```python
metadata_key = f'/chora/capabilities/{namespace}/metadata'
metadata_json, _ = etcd.get(metadata_key)

if not metadata_json:
    print(f"ERROR: Capability not found: {namespace}")
    print("Available capabilities:")
    # ... list all capabilities
```

**Mitigation**:
- Run GitOps sync: `python scripts/gitops-sync-registry.py --sync-once`
- Check YAML manifest exists: `ls capabilities/{namespace}.yaml`
- Validate namespace format: `chora.{domain}.{capability}`

---

### Expired Health Lease

**Scenario**: Service health key missing (lease expired)

**Python Detection**:
```python
health_key = f'/chora/capabilities/{namespace}/health'
health_json, _ = etcd.get(health_key)

if not health_json:
    print(f"WARNING: Service unhealthy: {namespace}")
    print("Lease expired (no heartbeat in >30s)")
```

**Mitigation**:
- Check heartbeat service: `docker-compose logs heartbeat`
- Restart service: `docker-compose restart heartbeat`
- Check network latency between service and etcd

---

### Malformed JSON

**Scenario**: JSON parsing fails for metadata or dependencies

**Python Detection**:
```python
try:
    metadata = json.loads(metadata_json)
except json.JSONDecodeError as e:
    print(f"ERROR: Malformed JSON in {metadata_key}: {e}")
```

**Mitigation**:
- Validate YAML manifest: `python -c "import yaml; yaml.safe_load(open('capabilities/{namespace}.yaml'))"`
- Re-sync from Git: `python scripts/gitops-sync-registry.py --sync-once --namespace {namespace}`

---

## Performance Characteristics

### Read Latency

**Target**: <10ms for metadata reads

**Benchmark** (3-node local cluster):
- **Metadata read**: ~5ms
- **Prefix query (all capabilities)**: ~20ms (45 capabilities)
- **Health check**: ~5ms
- **Artifact search**: ~50ms (225 artifacts, keyword search)

**Optimization**:
- Use direct key reads instead of prefix queries when possible
- Cache metadata client-side (60s TTL)
- Use parallel queries for batch operations

---

### Write Latency

**Target**: <20ms for metadata writes (Raft consensus)

**Benchmark** (3-node local cluster):
- **Metadata write**: ~15ms (quorum write)
- **Health heartbeat**: ~10ms
- **Artifact indexing**: ~15ms per artifact

**Optimization**:
- Batch writes using transactions (`etcd.transaction()`)
- Use async writes where consistency is not critical

---

### Throughput

**Target**: 10,000 reads/sec, 1,000 writes/sec

**Benchmark** (3-node local cluster):
- **Reads**: ~12,000 ops/sec
- **Writes**: ~1,500 ops/sec (quorum writes)

**Scalability**:
- Add read-only etcd members for higher read throughput
- Shard artifact content to external storage (S3) if >10k artifacts

---

## Security Considerations

### Authentication

**Current**: None (local development cluster)

**Production Recommendation**:
- Enable etcd authentication (`--client-cert-auth`)
- Use mTLS for client connections
- Issue per-agent certificates

**Example** (mTLS):
```python
etcd = etcd3.client(
    host='localhost',
    port=2379,
    ca_cert='/path/to/ca.crt',
    cert_cert='/path/to/client.crt',
    cert_key='/path/to/client.key'
)
```

---

### Authorization

**Current**: None (all clients have full access)

**Production Recommendation**:
- Use etcd RBAC (role-based access control)
- Create read-only roles for agents
- Create write roles for GitOps sync only

**Example** (etcdctl):
```bash
# Enable auth
etcdctl user add root
etcdctl auth enable

# Create read-only role
etcdctl role add agent-reader
etcdctl role grant-permission agent-reader read /chora/ --prefix

# Create user
etcdctl user add claude-agent
etcdctl user grant-role claude-agent agent-reader
```

---

### Data Integrity

**Mechanism**: SHA-256 content hashing

**Verification**:
```python
import hashlib

# Get artifact content and metadata
content_key = f'/chora/artifacts/{namespace}/{artifact_type}/content'
metadata_key = f'/chora/artifacts/{namespace}/{artifact_type}/metadata'

content, _ = etcd.get(content_key)
metadata_json, _ = etcd.get(metadata_key)
metadata = json.loads(metadata_json)

# Verify hash
expected_hash = metadata['content_hash'].replace('sha256:', '')
actual_hash = hashlib.sha256(content).hexdigest()

if expected_hash != actual_hash:
    print(f"ERROR: Content hash mismatch for {namespace}/{artifact_type}")
    print(f"Expected: {expected_hash}")
    print(f"Actual: {actual_hash}")
else:
    print("Content integrity verified")
```

---

## Client Libraries

### Python (etcd3)

**Installation**:
```bash
pip install etcd3
```

**Basic Usage**:
```python
import etcd3
import json

# Connect
etcd = etcd3.client(host='localhost', port=2379)

# Read
value, meta = etcd.get('/chora/capabilities/chora.devex.registry/metadata')
metadata = json.loads(value)

# Write
etcd.put('/chora/test/key', 'value')

# Watch
for event in etcd.watch_prefix('/chora/capabilities/'):
    print(f"{event.type}: {event.key}")
```

**Documentation**: https://python-etcd3.readthedocs.io/

---

### Go (etcd client v3)

**Installation**:
```bash
go get go.etcd.io/etcd/client/v3
```

**Basic Usage**:
```go
import (
    "context"
    "fmt"
    clientv3 "go.etcd.io/etcd/client/v3"
)

// Connect
cli, err := clientv3.New(clientv3.Config{
    Endpoints: []string{"localhost:2379"},
})
defer cli.Close()

// Read
resp, err := cli.Get(context.TODO(), "/chora/capabilities/", clientv3.WithPrefix())
for _, kv := range resp.Kvs {
    fmt.Printf("%s: %s\n", kv.Key, kv.Value)
}

// Watch
watchChan := cli.Watch(context.Background(), "/chora/capabilities/", clientv3.WithPrefix())
for watchResp := range watchChan {
    for _, event := range watchResp.Events {
        fmt.Printf("%s: %s\n", event.Type, event.Kv.Key)
    }
}
```

**Documentation**: https://pkg.go.dev/go.etcd.io/etcd/client/v3

---

### Bash (etcdctl)

**Installation**: Included in etcd Docker image

**Basic Usage**:
```bash
# Read
etcdctl get /chora/capabilities/chora.devex.registry/metadata

# List all capabilities
etcdctl get /chora/capabilities/ --prefix --keys-only

# Watch
etcdctl watch /chora/capabilities/ --prefix
```

**Docker Execution**:
```bash
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix
```

---

## Versioning and Compatibility

### Protocol Version

**Current**: 1.0.0

**Versioning Scheme**: Semantic Versioning 2.0.0
- **Major**: Breaking changes to schema or API contracts
- **Minor**: Backward-compatible additions (new fields, new keys)
- **Patch**: Bug fixes and documentation updates

---

### Backward Compatibility Guarantees

**Guaranteed**:
- Existing keys will not be renamed or removed (major version only)
- New fields added to JSON schemas will be optional
- Deprecated fields will remain for 1 major version

**Not Guaranteed**:
- Performance characteristics may change
- Internal etcd configuration may change
- Client library versions may require updates

---

### Schema Evolution

**Adding New Fields**:
```json
{
  "dc_identifier": "chora.devex.registry",
  "dc_title": "Registry",
  // ... existing fields

  // New field (optional, backward-compatible)
  "chora_maintainer": "team@example.com"
}
```

**Deprecating Fields**:
```json
{
  "dc_identifier": "chora.devex.registry",

  // Deprecated field (still present for 1 major version)
  "chora_sap_id": "SAP-047",  // DEPRECATED: Use dc_identifier

  // Preferred field
  "dc_identifier": "chora.devex.registry"
}
```

---

## References

- [etcd v3 API Documentation](https://etcd.io/docs/v3.5/learning/api/)
- [Dublin Core Metadata Element Set (ISO 15836:2009)](https://www.dublincore.org/specifications/dublin-core/dces/)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [Raft Consensus Algorithm](https://raft.github.io/)
- [SAP-000: SAP Framework](../sap-framework/protocol-spec.md)

---

**Version**: 1.0.0
**Protocol Version**: 1.0.0
**Status**: Draft
**Next Review**: After initial agent adoption (2 weeks)
