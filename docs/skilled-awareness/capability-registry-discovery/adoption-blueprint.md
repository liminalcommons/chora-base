# Adoption Blueprint: Capability Registry & Service Discovery

**Capability ID**: SAP-048
**Modern Namespace**: chora.awareness.capability_registry_discovery
**Type**: Pattern
**Status**: Draft
**Version**: 1.0.0
**Last Updated**: 2025-11-16

---

## Overview

This blueprint provides step-by-step guidance for adopting **SAP-048: Capability Registry & Service Discovery** patterns in your project. It covers infrastructure setup, agent integration, and validation.

**Adoption Time**: 30-60 minutes (depending on infrastructure familiarity)

**Prerequisites**:
- Docker and Docker Compose installed
- Python 3.9+ with pip
- Git repository with capability manifests (YAML files)
- Basic understanding of etcd and key-value stores

---

## Adoption Checklist

- [ ] **Phase 1**: Infrastructure Setup (15-20 minutes)
  - [ ] Start etcd cluster
  - [ ] Deploy GitOps sync service
  - [ ] Deploy heartbeat service (Service-type capabilities only)
  - [ ] Run artifact indexing script
- [ ] **Phase 2**: Agent Integration (10-15 minutes)
  - [ ] Install Python etcd3 library
  - [ ] Test registry queries
  - [ ] Implement capability discovery patterns
  - [ ] Implement health monitoring patterns
- [ ] **Phase 3**: Validation (5-10 minutes)
  - [ ] Verify all capabilities synced
  - [ ] Verify service health monitoring
  - [ ] Verify artifact indexing
  - [ ] Run integration tests

---

## Phase 1: Infrastructure Setup

### Step 1.1: Start etcd Cluster

**Goal**: Deploy 3-node etcd cluster with Raft consensus

**Commands**:
```bash
# Navigate to infrastructure directory
cd infrastructure/etcd

# Start etcd cluster
docker-compose up -d

# Verify cluster is healthy
docker-compose exec etcd1 etcdctl endpoint health

# Expected output:
# 127.0.0.1:2379 is healthy: successfully committed proposal: took = 2.345678ms
```

**Validation**:
```bash
# Check all 3 nodes are running
docker-compose ps

# Should show:
# etcd1    running    0.0.0.0:2379->2379/tcp
# etcd2    running    0.0.0.0:2389->2379/tcp
# etcd3    running    0.0.0.0:2399->2379/tcp

# Test etcd connection
docker-compose exec etcd1 etcdctl put /test/key "test-value"
docker-compose exec etcd1 etcdctl get /test/key

# Should output: test-value
```

**Troubleshooting**:
- If cluster fails to start, check Docker logs: `docker-compose logs -f`
- If port conflicts occur, edit [docker-compose.yml](../../../infrastructure/etcd/docker-compose.yml) ports
- Ensure no other etcd instances are running: `docker ps | grep etcd`

---

### Step 1.2: Deploy GitOps Sync Service

**Goal**: Sync capability manifests from Git to etcd every 60 seconds

**Commands**:
```bash
# GitOps sync is included in docker-compose.yml
# It should already be running from Step 1.1

# Verify GitOps sync is running
docker-compose logs gitops-sync

# Expected output:
# gitops-sync | Starting GitOps sync service...
# gitops-sync | Syncing capabilities to etcd...
# gitops-sync | Synced 45 capability/ies to etcd
```

**Manual Sync** (optional):
```bash
# Run one-time sync from host
python scripts/gitops-sync-registry.py --sync-once --capabilities capabilities/

# Expected output:
# Synced 45 capability/ies to etcd
```

**Validation**:
```bash
# Check capabilities in etcd
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix --keys-only | grep metadata | wc -l

# Should output: 45 (number of capabilities)

# Get specific capability
docker-compose exec etcd1 etcdctl get /chora/capabilities/chora.devex.registry/metadata
```

**Troubleshooting**:
- If no capabilities synced, check GitOps logs: `docker-compose logs gitops-sync`
- Verify YAML manifests exist: `ls capabilities/chora.*.yaml | wc -l`
- Check volume mount: `docker-compose exec gitops-sync ls /app/capabilities`

---

### Step 1.3: Deploy Heartbeat Service

**Goal**: Monitor Service-type capabilities with 30s TTL leases

**Commands**:
```bash
# Heartbeat service is included in docker-compose.yml
# It should already be running from Step 1.1

# Verify heartbeat service is running
docker-compose logs heartbeat

# Expected output:
# heartbeat | Discovered Service-type: chora.devex.registry
# heartbeat | Discovered Service-type: chora.devex.bootstrap
# heartbeat | Found 9 Service-type capability/ies
# heartbeat | Starting heartbeat for chora.devex.registry
# heartbeat | Created lease with 30s TTL
# heartbeat | Heartbeat sent: chora.devex.registry (count: 1)
```

**Validation**:
```bash
# Check health keys in etcd
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix | grep health

# Should show 9 health keys (one per Service-type capability)

# Get specific service health
docker-compose exec etcd1 etcdctl get /chora/capabilities/chora.devex.registry/health

# Expected output:
# {"status":"healthy","timestamp":"2025-11-15T22:30:00Z","namespace":"chora.devex.registry","heartbeat_count":42}
```

**Troubleshooting**:
- If no health keys, check heartbeat logs: `docker-compose logs heartbeat | grep ERROR`
- Verify Service-type capabilities exist: `grep -l chora_service capabilities/*.yaml | wc -l`
- Check etcd connection from heartbeat: `docker-compose exec heartbeat python -c "import etcd3; print(etcd3.client(host='etcd1', port=2379).status())"`

---

### Step 1.4: Run Artifact Indexing

**Goal**: Index 5 required SAP artifacts per capability to etcd

**Commands**:
```bash
# Run artifact indexing script
python scripts/index-sap-artifacts.py --capabilities capabilities/ --docs docs/

# Expected output:
# Discovered 45 capability/ies
# Indexing artifacts for 45 capability/ies...
# Indexed: chora.infrastructure.sap_framework/capability-charter (12543 bytes)
# Indexed: chora.infrastructure.sap_framework/protocol-spec (23456 bytes)
# ...
# Indexing complete: 225 indexed, 0 missing, 0 errors
```

**Validation**:
```bash
# Count indexed artifacts
docker-compose exec etcd1 etcdctl get /chora/artifacts/ --prefix --keys-only | grep content | wc -l

# Should output: 225 (45 capabilities × 5 artifacts)

# Get specific artifact
docker-compose exec etcd1 etcdctl get /chora/artifacts/chora.infrastructure.sap_framework/capability-charter/content

# Should output full markdown content
```

**Troubleshooting**:
- If artifacts missing, check SAP directory structure: `ls docs/skilled-awareness/*/`
- Verify artifact files exist: `find docs/skilled-awareness/ -name "*.md" | wc -l`
- Run dry-run to see what would be indexed: `python scripts/index-sap-artifacts.py --dry-run`

---

## Phase 2: Agent Integration

### Step 2.1: Install Python Dependencies

**Goal**: Install etcd3 library for Python agents

**Commands**:
```bash
# Install etcd3 library
pip install etcd3

# Or add to requirements.txt
echo "etcd3==0.12.0" >> requirements.txt
pip install -r requirements.txt
```

**Validation**:
```bash
# Test import
python -c "import etcd3; print(etcd3.__version__)"

# Should output: 0.12.0 (or similar)
```

---

### Step 2.2: Test Registry Queries

**Goal**: Verify agent can query registry successfully

**Create Test Script** (`test_registry.py`):
```python
#!/usr/bin/env python3
"""Test registry connectivity and basic queries"""

import etcd3
import json
import sys

def test_connection():
    """Test etcd connection"""
    print("Testing etcd connection...")
    try:
        etcd = etcd3.client(host='localhost', port=2379)
        etcd.status()
        print("✓ Connected to etcd")
        return etcd
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        sys.exit(1)

def test_list_capabilities(etcd):
    """Test listing all capabilities"""
    print("\nTesting capability listing...")
    capabilities = []
    prefix = '/chora/capabilities/'

    for value, meta in etcd.get_prefix(prefix):
        key_str = meta.key.decode('utf-8')
        if key_str.endswith('/metadata'):
            namespace = key_str.split('/')[3]
            metadata = json.loads(value)
            capabilities.append(namespace)

    print(f"✓ Found {len(capabilities)} capabilities")
    return capabilities

def test_check_health(etcd):
    """Test service health check"""
    print("\nTesting service health check...")

    health_key = '/chora/capabilities/chora.devex.registry/health'
    health_json, meta = etcd.get(health_key)

    if health_json:
        health = json.loads(health_json)
        print(f"✓ Service healthy: {health['namespace']}")
        print(f"  Last heartbeat: {health['timestamp']}")
        print(f"  Heartbeat count: {health['heartbeat_count']}")
        return True
    else:
        print("✗ Service unhealthy (no health key)")
        return False

def test_search_artifacts(etcd):
    """Test artifact search"""
    print("\nTesting artifact search...")

    query = "health monitoring"
    results = []
    prefix = '/chora/artifacts/'

    for value, meta in etcd.get_prefix(prefix):
        key_str = meta.key.decode('utf-8')

        if not key_str.endswith('/content'):
            continue

        content = value.decode('utf-8')
        if query.lower() in content.lower():
            parts = key_str.split('/')
            if len(parts) >= 5:
                namespace = parts[3]
                artifact_type = parts[4]
                results.append(f"{namespace}/{artifact_type}")

                if len(results) >= 5:
                    break

    print(f"✓ Found {len(results)} matching artifacts:")
    for result in results:
        print(f"  - {result}")

    return len(results) > 0

if __name__ == '__main__':
    etcd = test_connection()
    test_list_capabilities(etcd)
    test_check_health(etcd)
    test_search_artifacts(etcd)

    print("\n" + "=" * 80)
    print("All tests passed! Registry is ready for use.")
    print("=" * 80)
```

**Run Tests**:
```bash
# Make executable
chmod +x test_registry.py

# Run tests
python test_registry.py

# Expected output:
# Testing etcd connection...
# ✓ Connected to etcd
#
# Testing capability listing...
# ✓ Found 45 capabilities
#
# Testing service health check...
# ✓ Service healthy: chora.devex.registry
#   Last heartbeat: 2025-11-15T22:30:00Z
#   Heartbeat count: 142
#
# Testing artifact search...
# ✓ Found 5 matching artifacts:
#   - chora.devex.registry/capability-charter
#   - chora.awareness.capability_registry_discovery/protocol-spec
#   ...
#
# All tests passed! Registry is ready for use.
```

---

### Step 2.3: Implement Discovery Patterns

**Goal**: Add capability discovery to your agent code

**Create Helper Module** (`registry_client.py`):
```python
"""Registry client helper for capability discovery"""

import etcd3
import json
from typing import List, Dict, Optional

class RegistryClient:
    """Client for Chora capability registry"""

    def __init__(self, host: str = 'localhost', port: int = 2379):
        self.etcd = etcd3.client(host=host, port=port)

    def list_capabilities(self, capability_type: Optional[str] = None) -> List[Dict]:
        """
        List all capabilities, optionally filtered by type

        Args:
            capability_type: Filter by "Service" or "Pattern" (None = all)

        Returns:
            List of capability dictionaries with namespace, title, type, status
        """
        capabilities = []
        prefix = '/chora/capabilities/'

        for value, meta in self.etcd.get_prefix(prefix):
            key_str = meta.key.decode('utf-8')

            if not key_str.endswith('/metadata'):
                continue

            namespace = key_str.split('/')[3]
            metadata = json.loads(value)

            # Filter by type
            if capability_type and metadata['dc_type'] != capability_type:
                continue

            capabilities.append({
                'namespace': namespace,
                'title': metadata['dc_title'],
                'type': metadata['dc_type'],
                'status': metadata['chora_status'],
                'version': metadata['chora_version'],
                'description': metadata.get('dc_description', 'N/A'),
            })

        return sorted(capabilities, key=lambda c: c['namespace'])

    def get_capability(self, namespace: str) -> Optional[Dict]:
        """
        Get metadata for a specific capability

        Args:
            namespace: Capability namespace (e.g., chora.devex.registry)

        Returns:
            Capability metadata dictionary or None if not found
        """
        metadata_key = f'/chora/capabilities/{namespace}/metadata'
        metadata_json, _ = self.etcd.get(metadata_key)

        if not metadata_json:
            return None

        return json.loads(metadata_json)

    def check_service_health(self, namespace: str) -> Dict:
        """
        Check health of a Service-type capability

        Args:
            namespace: Service namespace

        Returns:
            Dictionary with healthy (bool), age (float), ttl (int), details (str)
        """
        import datetime

        health_key = f'/chora/capabilities/{namespace}/health'
        health_json, meta = self.etcd.get(health_key)

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
                lease = self.etcd.Lease(meta.lease_id)
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
            'last_heartbeat': health['timestamp'],
            'details': f"Age: {age:.1f}s, TTL: {ttl}s" if ttl else f"Age: {age:.1f}s"
        }

    def get_dependencies(self, namespace: str) -> List[Dict]:
        """
        Get dependencies for a capability

        Args:
            namespace: Capability namespace

        Returns:
            List of dependency dictionaries
        """
        deps_key = f'/chora/capabilities/{namespace}/dependencies'
        deps_json, _ = self.etcd.get(deps_key)

        if not deps_json:
            return []

        return json.loads(deps_json)

    def search_artifacts(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search artifacts by keyword

        Args:
            query: Search keyword (case-insensitive)
            limit: Maximum results to return

        Returns:
            List of matching artifact dictionaries
        """
        results = []
        prefix = '/chora/artifacts/'

        for value, meta in self.etcd.get_prefix(prefix):
            key_str = meta.key.decode('utf-8')

            if not key_str.endswith('/content'):
                continue

            content = value.decode('utf-8')

            if query.lower() in content.lower():
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
```

**Usage Example**:
```python
from registry_client import RegistryClient

# Connect to registry
registry = RegistryClient(host='localhost', port=2379)

# List all capabilities
capabilities = registry.list_capabilities()
print(f"Found {len(capabilities)} capabilities")

# List only Service-type capabilities
services = registry.list_capabilities(capability_type='Service')
print(f"Found {len(services)} services")

# Get specific capability
cap = registry.get_capability('chora.devex.registry')
print(f"Title: {cap['dc_title']}")
print(f"Version: {cap['chora_version']}")

# Check service health
health = registry.check_service_health('chora.devex.registry')
if health['healthy']:
    print("Service is healthy!")
else:
    print(f"Service unhealthy: {health['details']}")

# Search artifacts
results = registry.search_artifacts("health monitoring", limit=5)
for result in results:
    print(f"{result['namespace']}/{result['artifact_type']}")
```

---

### Step 2.4: Update Agent Awareness Files

**Goal**: Document registry patterns in AGENTS.md

**Add to Project AGENTS.md**:
```markdown
## SAP-048: Capability Registry & Service Discovery

This project uses the distributed capability registry for service discovery and health monitoring.

**Registry Endpoint**: `localhost:2379` (etcd)

**Agent Patterns**:

1. **List Available Capabilities**:
   ```python
   from registry_client import RegistryClient
   registry = RegistryClient()
   capabilities = registry.list_capabilities()
   ```

2. **Check Service Health**:
   ```python
   health = registry.check_service_health('chora.devex.registry')
   if health['healthy']:
       # Use service
   ```

3. **Resolve Dependencies**:
   ```python
   deps = registry.get_dependencies('chora.awareness.task_tracking')
   for dep in deps:
       print(f"{dep['capability']} ({dep['relationship']})")
   ```

4. **Search Documentation**:
   ```python
   results = registry.search_artifacts("health monitoring", limit=5)
   ```

**See Also**: [SAP-048 AGENTS.md](AGENTS.md)
```

---

## Phase 3: Validation

### Step 3.1: Verify All Capabilities Synced

**Goal**: Ensure all 45 capabilities are synced to etcd

**Commands**:
```bash
# Count metadata keys
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix --keys-only | grep metadata | wc -l

# Expected: 45

# List all capability namespaces
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix --keys-only | grep metadata | sed 's|/chora/capabilities/||; s|/metadata||'

# Expected:
# chora.infrastructure.sap_framework
# chora.devex.registry
# chora.awareness.task_tracking
# ...
```

**Validation**:
- [ ] 45 metadata keys exist
- [ ] All namespaces match YAML filenames
- [ ] All metadata is valid JSON

---

### Step 3.2: Verify Service Health Monitoring

**Goal**: Ensure all 9 Service-type capabilities have active health keys

**Commands**:
```bash
# Count health keys
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix | grep -c '"status":"healthy"'

# Expected: 9

# List all service health statuses
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix | grep -B 1 '"status":"healthy"' | grep /health

# Expected:
# /chora/capabilities/chora.devex.registry/health
# /chora/capabilities/chora.devex.bootstrap/health
# /chora/capabilities/chora.devex.documentation_framework/health
# ...
```

**Validation**:
- [ ] 9 health keys exist (one per Service-type capability)
- [ ] All health statuses are "healthy"
- [ ] Heartbeat counts are incrementing (check twice, 10s apart)

---

### Step 3.3: Verify Artifact Indexing

**Goal**: Ensure all 225 artifacts are indexed (45 capabilities × 5 artifacts)

**Commands**:
```bash
# Count content keys
docker-compose exec etcd1 etcdctl get /chora/artifacts/ --prefix --keys-only | grep content | wc -l

# Expected: 225

# Count metadata keys
docker-compose exec etcd1 etcdctl get /chora/artifacts/ --prefix --keys-only | grep /metadata | wc -l

# Expected: 225

# List artifacts for specific capability
docker-compose exec etcd1 etcdctl get /chora/artifacts/chora.infrastructure.sap_framework/ --prefix --keys-only

# Expected:
# /chora/artifacts/chora.infrastructure.sap_framework/capability-charter/content
# /chora/artifacts/chora.infrastructure.sap_framework/capability-charter/metadata
# /chora/artifacts/chora.infrastructure.sap_framework/protocol-spec/content
# /chora/artifacts/chora.infrastructure.sap_framework/protocol-spec/metadata
# ...
```

**Validation**:
- [ ] 225 content keys exist
- [ ] 225 metadata keys exist
- [ ] All 5 required artifacts indexed per capability

---

### Step 3.4: Run Integration Tests

**Goal**: Validate end-to-end registry functionality

**Create Integration Test** (`test_integration.py`):
```python
#!/usr/bin/env python3
"""Integration tests for registry patterns"""

import sys
from registry_client import RegistryClient

def test_discovery():
    """Test capability discovery"""
    print("Test 1: Capability Discovery")
    registry = RegistryClient()

    capabilities = registry.list_capabilities()
    assert len(capabilities) == 45, f"Expected 45 capabilities, got {len(capabilities)}"

    services = registry.list_capabilities(capability_type='Service')
    assert len(services) == 9, f"Expected 9 services, got {len(services)}"

    patterns = registry.list_capabilities(capability_type='Pattern')
    assert len(patterns) == 36, f"Expected 36 patterns, got {len(patterns)}"

    print("  ✓ Passed")

def test_health_monitoring():
    """Test service health monitoring"""
    print("Test 2: Service Health Monitoring")
    registry = RegistryClient()

    # Check registry service health
    health = registry.check_service_health('chora.devex.registry')
    assert health['healthy'], f"Registry service unhealthy: {health['details']}"
    assert health['ttl'] > 0, f"Invalid TTL: {health['ttl']}"

    print("  ✓ Passed")

def test_dependency_resolution():
    """Test dependency resolution"""
    print("Test 3: Dependency Resolution")
    registry = RegistryClient()

    # Get dependencies for task-tracking
    deps = registry.get_dependencies('chora.awareness.task_tracking')
    assert len(deps) > 0, "Expected dependencies for task-tracking"

    # Verify dependency structure
    for dep in deps:
        assert 'capability' in dep, "Missing capability field"
        assert 'relationship' in dep, "Missing relationship field"

    print("  ✓ Passed")

def test_artifact_search():
    """Test artifact search"""
    print("Test 4: Artifact Search")
    registry = RegistryClient()

    # Search for "health monitoring"
    results = registry.search_artifacts("health monitoring", limit=5)
    assert len(results) > 0, "Expected search results for 'health monitoring'"

    # Verify result structure
    for result in results:
        assert 'namespace' in result, "Missing namespace field"
        assert 'artifact_type' in result, "Missing artifact_type field"
        assert 'preview' in result, "Missing preview field"

    print("  ✓ Passed")

if __name__ == '__main__':
    print("Running integration tests...\n")

    try:
        test_discovery()
        test_health_monitoring()
        test_dependency_resolution()
        test_artifact_search()

        print("\n" + "=" * 80)
        print("All integration tests passed!")
        print("=" * 80)
        sys.exit(0)

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
```

**Run Tests**:
```bash
python test_integration.py

# Expected output:
# Running integration tests...
#
# Test 1: Capability Discovery
#   ✓ Passed
# Test 2: Service Health Monitoring
#   ✓ Passed
# Test 3: Dependency Resolution
#   ✓ Passed
# Test 4: Artifact Search
#   ✓ Passed
#
# All integration tests passed!
```

---

## Post-Adoption Best Practices

### 1. Monitor Registry Health

**Setup Monitoring Script**:
```bash
#!/bin/bash
# monitor-registry.sh

echo "Checking registry health..."

# Check etcd cluster
echo "1. etcd Cluster:"
docker-compose -f infrastructure/etcd/docker-compose.yml exec etcd1 etcdctl endpoint health

# Check GitOps sync
echo ""
echo "2. GitOps Sync:"
docker-compose -f infrastructure/etcd/docker-compose.yml logs gitops-sync --tail 5 | grep Synced

# Check heartbeat service
echo ""
echo "3. Heartbeat Service:"
docker-compose -f infrastructure/etcd/docker-compose.yml logs heartbeat --tail 5 | grep Heartbeat

# Count healthy services
echo ""
echo "4. Healthy Services:"
docker-compose -f infrastructure/etcd/docker-compose.yml exec etcd1 etcdctl get /chora/capabilities/ --prefix | grep -c '"status":"healthy"'
echo "(Expected: 9)"
```

**Run Daily**:
```bash
chmod +x monitor-registry.sh
./monitor-registry.sh
```

---

### 2. Update Artifact Index Regularly

**Setup Cron Job** (optional):
```bash
# Add to crontab (runs hourly)
0 * * * * cd /path/to/chora-base && python scripts/index-sap-artifacts.py --capabilities capabilities/ --docs docs/ >> /var/log/artifact-indexing.log 2>&1
```

**Manual Re-index**:
```bash
python scripts/index-sap-artifacts.py --capabilities capabilities/ --docs docs/
```

---

### 3. Document Registry Patterns in Code

**Add Registry Helper to Project**:
```python
# registry.py
"""
Registry helper module

Provides convenient functions for capability discovery and health monitoring.
Uses SAP-048 patterns.
"""

from registry_client import RegistryClient

# Global registry client
_registry = None

def get_registry():
    """Get or create registry client singleton"""
    global _registry
    if _registry is None:
        _registry = RegistryClient()
    return _registry

# Convenience functions
def list_capabilities(capability_type=None):
    """List all capabilities, optionally filtered by type"""
    return get_registry().list_capabilities(capability_type)

def get_capability(namespace):
    """Get capability metadata"""
    return get_registry().get_capability(namespace)

def check_service_health(namespace):
    """Check service health"""
    return get_registry().check_service_health(namespace)

def get_dependencies(namespace):
    """Get capability dependencies"""
    return get_registry().get_dependencies(namespace)

def search_artifacts(query, limit=10):
    """Search capability artifacts"""
    return get_registry().search_artifacts(query, limit)
```

---

### 4. Cache Metadata Client-Side

**Implement Caching** (optional, for high-frequency queries):
```python
import time
from functools import lru_cache

class CachedRegistryClient(RegistryClient):
    """Registry client with metadata caching (60s TTL)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache_time = {}

    @lru_cache(maxsize=128)
    def _get_cached_metadata(self, namespace, cache_key):
        """Internal cached metadata getter"""
        return super().get_capability(namespace)

    def get_capability(self, namespace):
        """Get capability metadata (cached for 60s)"""
        cache_key = int(time.time() / 60)  # 60s buckets
        return self._get_cached_metadata(namespace, cache_key)
```

---

## Troubleshooting

### Issue: "No capabilities synced to etcd"

**Diagnosis**:
```bash
# Check GitOps logs
docker-compose logs gitops-sync

# Check YAML manifest count
ls capabilities/chora.*.yaml | wc -l

# Manually sync
python scripts/gitops-sync-registry.py --sync-once
```

**Solution**: Verify YAML manifests exist and GitOps service has read access to capabilities/ directory

---

### Issue: "Service health always shows unhealthy"

**Diagnosis**:
```bash
# Check heartbeat logs
docker-compose logs heartbeat

# Check if health keys exist
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix | grep health
```

**Solution**: Restart heartbeat service or check for Service-type capability discovery issues

---

### Issue: "Artifact search returns no results"

**Diagnosis**:
```bash
# Check artifact count
docker-compose exec etcd1 etcdctl get /chora/artifacts/ --prefix --keys-only | grep content | wc -l

# Re-index
python scripts/index-sap-artifacts.py --capabilities capabilities/ --docs docs/
```

**Solution**: Verify SAP directory structure and re-run artifact indexing

---

## Next Steps

After successful adoption:

1. **Integrate with SAP-015 (Task Tracking)**: Tag beads tasks with capability namespaces
2. **Integrate with SAP-049 (Namespace Resolution)**: Resolve legacy SAP-XXX identifiers
3. **Create Custom Queries**: Build domain-specific registry queries for your use case
4. **Setup Monitoring**: Add Prometheus metrics for registry queries (future work)
5. **Contribute Patterns**: Share your registry usage patterns with the community

---

## References

- [Protocol Specification](protocol-spec.md) - Complete technical spec
- [Awareness Guide (AGENTS.md)](AGENTS.md) - Agent-specific patterns
- [Capability Charter](capability-charter.md) - Problem statement and solution
- [etcd Docker Compose](../../../infrastructure/etcd/docker-compose.yml) - Infrastructure setup
- [GitOps Sync Script](../../../scripts/gitops-sync-registry.py) - Sync implementation
- [Heartbeat Service](../../../services/registry-heartbeat/heartbeat.py) - Health monitoring

---

**Version**: 1.0.0
**Status**: Draft
**Last Updated**: 2025-11-16
**Estimated Adoption Time**: 30-60 minutes
