# Capability Charter: Capability Registry & Service Discovery

**Capability ID**: SAP-048
**Modern Namespace**: chora.awareness.capability_registry_discovery
**Type**: Pattern
**Status**: Draft
**Version**: 1.0.0
**Created**: 2025-11-16
**Last Updated**: 2025-11-16

---

## Executive Summary

**SAP-048: Capability Registry & Service Discovery** formalizes agent awareness patterns for querying and monitoring the Chora distributed capability registry built on etcd. It provides standardized patterns for capability discovery, dependency resolution, service health monitoring, and artifact search.

**Key Benefits**:
- 🔍 **Standardized Discovery**: Consistent patterns for querying capabilities
- 💓 **Health Monitoring**: Real-time service health via TTL leases
- 🔗 **Dependency Resolution**: Automated dependency graph traversal
- 📄 **Artifact Search**: Full-text search through capability documentation
- ⚡ **Event-Driven**: Watch mode for real-time registry changes

---

## Problem Statement

### Current Challenges

Without standardized registry discovery patterns, agents face:

1. **Ad-Hoc Query Patterns**: Each agent must independently figure out etcd schema and query patterns
2. **Health Monitoring Confusion**: No standardized way to check Service-type capability health
3. **Dependency Discovery Complexity**: Manual dependency graph traversal and resolution
4. **Artifact Search Fragmentation**: No consistent approach to searching capability documentation
5. **Event Monitoring Gaps**: Missing patterns for real-time registry change notifications

### Business Impact

- **Reduced Agent Effectiveness**: Agents spend time discovering patterns instead of solving problems
- **Inconsistent Behavior**: Different agents query registry differently, leading to bugs
- **Missed Health Signals**: Agents don't detect unhealthy services, leading to failures
- **Poor User Experience**: Users must manually provide capability information to agents
- **Integration Friction**: New agents struggle to integrate with registry

### User Stories

**As an AI agent**, I want to:
- Query the registry to discover all capabilities and their metadata
- Check the health status of Service-type capabilities before using them
- Resolve dependency chains automatically without manual intervention
- Search capability documentation to find relevant patterns
- Monitor registry changes in real-time to stay up-to-date

**As a developer**, I want:
- Agents to automatically discover capabilities without hardcoded lists
- Agents to detect unhealthy services and suggest alternatives
- Agents to resolve dependencies and warn about missing prerequisites
- Agents to surface relevant documentation based on my queries

---

## Solution Design

### Approach

SAP-048 formalizes 5 core agent awareness patterns for registry interaction:

1. **Capability Discovery Pattern**: Query etcd to list and filter capabilities
2. **Health Monitoring Pattern**: Check TTL lease status for Service-type capabilities
3. **Dependency Resolution Pattern**: Traverse dependency graph and validate prerequisites
4. **Artifact Search Pattern**: Full-text search through indexed documentation
5. **Event Monitoring Pattern**: Watch etcd keys for real-time updates

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Agent (Claude Code)                      │
└─────────────────────────────────────────────────────────────┘
                             │
                             │ SAP-048 Patterns
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    etcd Registry (Port 2379)                 │
│                                                              │
│  /chora/capabilities/{namespace}/                            │
│    ├─ metadata      (JSON: dc_identifier, dc_title, etc.)   │
│    ├─ type          (Service | Pattern)                     │
│    ├─ version       (semver)                                │
│    ├─ dependencies  (JSON array)                            │
│    └─ health        (JSON with 30s TTL lease)               │
│                                                              │
│  /chora/artifacts/{namespace}/{artifact_type}/               │
│    ├─ content       (Full markdown)                         │
│    └─ metadata      (File size, hash, timestamps)           │
└─────────────────────────────────────────────────────────────┘
                             ▲
                             │ GitOps Sync (60s interval)
                             │
┌─────────────────────────────────────────────────────────────┐
│              capabilities/ Directory (Git Source)            │
│                                                              │
│  chora.{domain}.{capability}.yaml (45 manifests)             │
└─────────────────────────────────────────────────────────────┘
```

### Core Patterns

**1. Capability Discovery Pattern**

Query etcd to list all capabilities and filter by type, domain, or status:

```python
import etcd3
import json

etcd = etcd3.client(host='localhost', port=2379)

# List all capabilities
prefix = '/chora/capabilities/'
for value, meta in etcd.get_prefix(prefix):
    key_str = meta.key.decode('utf-8')

    # Extract namespace from key
    if '/metadata' in key_str:
        namespace = key_str.split('/')[3]
        metadata = json.loads(value)

        print(f"Capability: {namespace}")
        print(f"  Title: {metadata['dc_title']}")
        print(f"  Type: {metadata.get('chora_service') and 'Service' or 'Pattern'}")
```

**2. Health Monitoring Pattern**

Check TTL lease status for Service-type capabilities:

```python
# Check service health
health_key = f'/chora/capabilities/{namespace}/health'
health_json, meta = etcd.get(health_key)

if health_json:
    health = json.loads(health_json)
    print(f"Status: {health['status']}")  # 'healthy'
    print(f"Last heartbeat: {health['timestamp']}")
    print(f"Heartbeat count: {health['heartbeat_count']}")

    # Check lease TTL
    lease_id = meta.lease_id
    lease = etcd.Lease(lease_id)
    print(f"Lease TTL: {lease.ttl}s remaining")  # 0-30s
else:
    print("Service unhealthy (lease expired)")
```

**3. Dependency Resolution Pattern**

Traverse dependency graph and validate prerequisites:

```python
# Get dependencies
deps_key = f'/chora/capabilities/{namespace}/dependencies'
deps_json, _ = etcd.get(deps_key)
dependencies = json.loads(deps_json)

# Traverse graph (DFS)
def resolve_dependencies(namespace, visited=None):
    if visited is None:
        visited = set()

    if namespace in visited:
        return  # Cycle detection

    visited.add(namespace)

    deps_key = f'/chora/capabilities/{namespace}/dependencies'
    deps_json, _ = etcd.get(deps_key)
    dependencies = json.loads(deps_json)

    for dep in dependencies:
        target = dep['capability']
        relationship = dep['relationship']

        if relationship == 'prerequisite':
            # Check if prerequisite is satisfied
            metadata_key = f'/chora/capabilities/{target}/metadata'
            metadata_json, _ = etcd.get(metadata_key)

            if not metadata_json:
                print(f"ERROR: Missing prerequisite {target}")
            else:
                # Recurse
                resolve_dependencies(target, visited)
```

**4. Artifact Search Pattern**

Full-text search through indexed documentation:

```python
# Search artifacts by keyword
query = "health monitoring"
prefix = '/chora/artifacts/'

results = []
for value, meta in etcd.get_prefix(prefix):
    key_str = meta.key.decode('utf-8')

    # Only search content, not metadata
    if not key_str.endswith('/content'):
        continue

    content = value.decode('utf-8')
    if query.lower() in content.lower():
        # Extract namespace and artifact type
        parts = key_str.split('/')
        namespace = parts[3]
        artifact_type = parts[4]

        results.append({
            'namespace': namespace,
            'artifact_type': artifact_type,
            'preview': content[:200] + '...',
        })

for result in results[:10]:
    print(f"{result['namespace']}/{result['artifact_type']}")
    print(f"  {result['preview']}\n")
```

**5. Event Monitoring Pattern**

Watch etcd keys for real-time registry updates:

```python
# Watch for capability changes
watch_prefix = '/chora/capabilities/'

for event in etcd.watch_prefix(watch_prefix):
    key_str = event.key.decode('utf-8')

    if event.type == 'PUT':
        print(f"Capability updated: {key_str}")
    elif event.type == 'DELETE':
        print(f"Capability removed: {key_str}")

        # Special case: Health key deleted = service failed
        if '/health' in key_str:
            namespace = key_str.split('/')[3]
            print(f"WARNING: Service {namespace} failed (lease expired)")
```

---

## Success Metrics

**Adoption Metrics**:
- Number of agents using SAP-048 patterns
- Number of registry queries per day
- Number of health checks per day
- Number of artifact searches per day

**Quality Metrics**:
- Query response time (<10ms target)
- Health check accuracy (100% target)
- Dependency resolution correctness (100% target)
- Artifact search relevance score

**Business Metrics**:
- Reduced agent onboarding time (from hours to minutes)
- Increased capability discoverability (agents surface capabilities 10x more)
- Reduced service failures (early health detection)
- Improved user satisfaction (agents provide relevant documentation)

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| etcd cluster failure | Critical | 3-node Raft consensus, automatic failover |
| Query performance degradation | Medium | etcd benchmarks show <10ms reads, use indexing |
| Schema changes breaking agents | Medium | Versioned schema, backward compatibility guarantees |
| TTL lease false positives | Low | 3x heartbeat buffer (30s TTL, 10s interval) |
| Artifact search scalability | Low | Start with simple keyword search, upgrade to FTS later |

---

## Integration Points

**Prerequisites**:
- **etcd cluster**: 3-node cluster running (infrastructure/etcd/)
- **GitOps sync**: Syncing capabilities to etcd (services/gitops-sync/)
- **Heartbeat service**: Service-type health monitoring (services/registry-heartbeat/)
- **Artifact indexing**: SAP artifacts indexed (scripts/index-sap-artifacts.py)

**Dependents**:
- **Claude Code agents**: Use patterns for capability discovery
- **Claude Desktop agents**: Use patterns for documentation search
- **CLI tools**: Use patterns for registry queries
- **Web dashboards**: Use patterns for visualization

**Complements**:
- **SAP-049 (Namespace Resolution)**: Resolves legacy SAP-XXX identifiers
- **SAP-000 (SAP Framework)**: Defines capability schema
- **SAP-015 (Task Tracking)**: Uses registry for capability-tagged tasks

---

## Open Questions

1. **Search Performance**: Should we use etcd's built-in search or external FTS (Elasticsearch)?
   - **Decision**: Start with etcd keyword search, evaluate Elasticsearch if >10k artifacts

2. **Watch Mode Filtering**: Should agents filter events client-side or server-side?
   - **Decision**: Client-side filtering initially (simpler), server-side if performance issues

3. **Caching Strategy**: Should agents cache registry data or always query fresh?
   - **Decision**: Query fresh for critical operations (health), cache metadata for 60s

4. **Dependency Validation Depth**: How deep should dependency resolution traverse?
   - **Decision**: Full transitive closure with cycle detection

5. **Artifact Versioning**: Should artifact content be versioned separately from capability version?
   - **Decision**: No - artifacts tied to capability version, use GitOps for history

---

## References

- [SAP-000: SAP Framework](../sap-framework/protocol-spec.md) - Capability schema definition
- [etcd Documentation](https://etcd.io/docs/) - etcd API and client libraries
- [GitOps Sync Service](../../../services/gitops-sync/README.md) - Registry sync implementation
- [Heartbeat Service](../../../services/registry-heartbeat/README.md) - Health monitoring implementation
- [Artifact Indexing Script](../../../scripts/index-sap-artifacts.py) - Artifact indexing implementation

---

**Version**: 1.0.0
**Status**: Draft
**Next Review**: After initial agent adoption (2 weeks)
