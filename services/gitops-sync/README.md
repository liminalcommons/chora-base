# GitOps Sync Service

Automated capability registry synchronization service that watches the `capabilities/` directory and syncs YAML manifests to etcd.

## Overview

The GitOps Sync service provides automated, continuous synchronization of capability manifests from Git to the etcd registry. It watches for changes in the capabilities directory and automatically updates the registry within 60 seconds.

**Features**:
- ✅ Automatic capability discovery and parsing
- ✅ YAML validation and metadata extraction
- ✅ etcd schema-compliant writes
- ✅ Change detection (only syncs modified files)
- ✅ Continuous watch mode (60s interval)
- ✅ Dry-run mode for testing
- ✅ Comprehensive error handling and logging

## Quick Start

### Docker Deployment (Recommended)

```bash
# Start etcd cluster + GitOps sync
cd infrastructure/etcd
docker-compose up -d

# Check sync logs
docker-compose logs -f gitops-sync

# Verify capabilities synced to etcd
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix --keys-only
```

### Standalone Usage

```bash
# Install dependencies
pip install PyYAML etcd3

# Sync once
python scripts/gitops-sync-registry.py --capabilities capabilities/

# Watch mode (continuous sync every 60s)
python scripts/gitops-sync-registry.py --capabilities capabilities/ --watch

# Custom interval
python scripts/gitops-sync-registry.py --capabilities capabilities/ --watch --interval 30

# Dry-run (no etcd writes)
python scripts/gitops-sync-registry.py --capabilities capabilities/ --dry-run
```

## Architecture

### Data Flow

```
capabilities/*.yaml → GitOps Sync → etcd → Registry API
     (Git)           (Watch mode)   (KV Store)  (Consumers)
```

### etcd Schema

Each capability is stored with the following keys:

```
/chora/capabilities/{namespace}/
  /metadata          - JSON: Full Dublin Core metadata
  /type              - String: "service" or "pattern"
  /version           - String: SemVer version
  /dependencies      - JSON: Array of dependency objects
```

**Example**:
```bash
# Metadata
/chora/capabilities/chora.devex.registry/metadata
{
  "dc_identifier": "chora.devex.registry",
  "dc_title": "Capability Registry",
  "dc_description": "Service discovery and health monitoring",
  ...
}

# Type
/chora/capabilities/chora.devex.registry/type
"service"

# Version
/chora/capabilities/chora.devex.registry/version
"1.0.0"

# Dependencies
/chora/capabilities/chora.devex.registry/dependencies
[
  {
    "capability": "chora.infrastructure.sap_framework",
    "relationship": "prerequisite",
    "version": "^1.0.0"
  }
]
```

## Usage Examples

### Single Sync

Sync all capabilities once and exit:

```bash
python scripts/gitops-sync-registry.py --capabilities capabilities/
```

**Output**:
```
2025-11-15 22:30:00 - gitops-sync - INFO - Connected to etcd at localhost:2379
2025-11-15 22:30:00 - gitops-sync - INFO - Found 45 capability manifest(s)
2025-11-15 22:30:01 - gitops-sync - INFO - Synced: chora.infrastructure.sap_framework (pattern)
2025-11-15 22:30:01 - gitops-sync - INFO - Synced: chora.devex.registry (service)
...
2025-11-15 22:30:05 - gitops-sync - INFO - Sync complete: 45 synced, 0 skipped, 0 errors
```

### Watch Mode

Continuous sync with 60-second interval:

```bash
python scripts/gitops-sync-registry.py \
    --capabilities capabilities/ \
    --watch \
    --interval 60
```

**Output**:
```
2025-11-15 22:30:00 - gitops-sync - INFO - Starting watch mode (interval: 60s)
2025-11-15 22:30:00 - gitops-sync - INFO - Watching: capabilities
2025-11-15 22:30:00 - gitops-sync - INFO - Press Ctrl+C to stop
2025-11-15 22:30:00 - gitops-sync - INFO - --- Sync cycle starting ---
...
2025-11-15 22:30:05 - gitops-sync - INFO - --- Sync cycle complete. Next sync in 60s ---
```

### List Capabilities

List all capabilities currently in etcd:

```bash
python scripts/gitops-sync-registry.py --list
```

**Output**:
```
Found 45 capability/ies in etcd:

  - chora.awareness.agent_awareness
  - chora.awareness.development_lifecycle
  - chora.devex.registry
  - chora.infrastructure.sap_framework
  ...
```

### Dry-Run Mode

Preview changes without writing to etcd:

```bash
python scripts/gitops-sync-registry.py \
    --capabilities capabilities/ \
    --dry-run
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `info` | Logging level (debug, info, warning, error) |

### Command-Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--capabilities` | `capabilities/` | Directory containing YAML manifests |
| `--etcd-host` | `localhost` | etcd host address |
| `--etcd-port` | `2379` | etcd port |
| `--watch` | `false` | Enable continuous sync mode |
| `--interval` | `60` | Sync interval (seconds) |
| `--dry-run` | `false` | Preview changes without writing |
| `--list` | `false` | List capabilities in etcd |

## Monitoring

### Logs

```bash
# Docker logs
docker-compose logs -f gitops-sync

# Filter for errors
docker-compose logs gitops-sync | grep ERROR

# Follow specific capability
docker-compose logs gitops-sync | grep "chora.devex.registry"
```

### Health Check

The Docker container includes a health check that verifies etcd connectivity:

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' gitops-sync

# Expected: "healthy"
```

### Verify Sync

```bash
# Count capabilities in etcd
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix --keys-only | wc -l

# Expected: 180 keys (45 capabilities × 4 keys each)

# Check specific capability
docker-compose exec etcd1 etcdctl get /chora/capabilities/chora.devex.registry/metadata
```

## Troubleshooting

### Sync not working

**Problem**: Capabilities not appearing in etcd

**Solution**:
```bash
# Check GitOps sync logs
docker-compose logs gitops-sync

# Verify etcd connectivity
docker-compose exec gitops-sync python -c "import etcd3; etcd3.client(host='etcd1', port=2379).status()"

# Manual sync test
docker-compose exec gitops-sync python /app/gitops-sync.py \
    --capabilities /app/capabilities \
    --etcd-host etcd1 \
    --etcd-port 2379
```

### Parse errors

**Problem**: "Failed to parse manifest" errors

**Solution**:
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('capabilities/chora.devex.registry.yaml'))"

# Check for missing fields
grep -E "(dc_identifier|chora_service|chora_pattern)" capabilities/chora.devex.registry.yaml
```

### etcd connection refused

**Problem**: "Failed to connect to etcd"

**Solution**:
```bash
# Verify etcd cluster is running
docker-compose ps

# Check etcd health
docker-compose exec etcd1 etcdctl endpoint health

# Restart if needed
docker-compose restart etcd1 etcd2 etcd3
```

### High memory usage

**Problem**: GitOps sync consuming too much memory

**Solution**:
```bash
# Check stats
docker stats gitops-sync

# Increase sync interval to reduce frequency
docker-compose exec gitops-sync python /app/gitops-sync.py \
    --watch --interval 300  # 5 minutes
```

## Performance

### Sync Performance

| Metric | Target | Actual |
|--------|--------|--------|
| Sync latency | <5s for 45 capabilities | ~4s |
| Change detection | <1s | ~0.5s |
| Memory usage | <50MB | ~30MB |
| CPU usage | <5% | ~2% |

### Optimization

**File hashing**: Only syncs files that have changed since last sync
**Batch operations**: Syncs all capabilities in single pass
**Connection pooling**: Reuses etcd connection across syncs

## Integration

### Python Client

```python
import etcd3

# Connect to etcd
etcd = etcd3.client(host='localhost', port=2379)

# Read capability metadata
metadata_json = etcd.get('/chora/capabilities/chora.devex.registry/metadata')[0]
metadata = json.loads(metadata_json)

print(f"Capability: {metadata['dc_identifier']}")
print(f"Type: {etcd.get('/chora/capabilities/chora.devex.registry/type')[0].decode()}")
```

### Watch for Changes

```python
# Watch for capability updates
for event in etcd.watch_prefix('/chora/capabilities/'):
    print(f"Change detected: {event.key}")
```

## Development

### Running Tests

```bash
# Unit tests
python -m pytest tests/test_gitops_sync.py

# Integration test with local etcd
python scripts/gitops-sync-registry.py \
    --capabilities test/fixtures/capabilities \
    --dry-run
```

### Adding New Capability Types

To support additional capability types beyond `service` and `pattern`:

1. Update `parse_manifest()` to detect new type
2. Add type-specific metadata extraction
3. Update etcd schema if needed
4. Update documentation

## Related Services

- **etcd Cluster**: [infrastructure/etcd/README.md](../../infrastructure/etcd/README.md)
- **Alias Redirect Service**: [services/alias-redirect/README.md](../alias-redirect/README.md)
- **Registry API** (Future): REST API for querying capabilities

## Roadmap

### Planned Features

- [ ] Webhook support (notify on sync completion)
- [ ] Metrics export (Prometheus)
- [ ] Batch API for bulk updates
- [ ] Conflict resolution (handle concurrent edits)
- [ ] Schema validation (enforce capability manifest standards)

---

**Version**: 1.0.0
**Last Updated**: 2025-11-15
**Status**: Production Ready
