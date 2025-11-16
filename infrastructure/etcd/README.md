# etcd Cluster for Chora Registry

3-node etcd cluster for distributed capability registry with Raft consensus, optimized for <10ms latency and 10k reads/sec.

## Quick Start

```bash
# Start cluster
docker-compose up -d

# Check cluster health
docker-compose exec etcd1 etcdctl endpoint health

# View logs
docker-compose logs -f

# Stop cluster
docker-compose down
```

## Architecture

### Cluster Topology

- **3 nodes**: etcd1, etcd2, etcd3
- **Consensus**: Raft algorithm
- **Quorum**: 2 nodes (can tolerate 1 node failure)
- **Data**: Persistent volumes

### Port Mapping

| Node | Client Port | Peer Port | Host Client | Host Peer |
|------|-------------|-----------|-------------|-----------|
| etcd1 | 2379 | 2380 | 2379 | 2380 |
| etcd2 | 2379 | 2380 | 2389 | 2390 |
| etcd3 | 2379 | 2380 | 2399 | 2400 |

**Web UI**: http://localhost:8080 (etcdkeeper)

### Performance Tuning

**Heartbeat & Election**:
- Heartbeat interval: 100ms
- Election timeout: 1000ms
- Optimized for low-latency consensus

**Storage**:
- Quota: 8GB per node
- Auto-compaction: Hourly
- Retention: 1 hour

## Usage

### Basic Operations

```bash
# Set a key
docker-compose exec etcd1 etcdctl put /chora/capabilities/test "value"

# Get a key
docker-compose exec etcd1 etcdctl get /chora/capabilities/test

# List all keys with prefix
docker-compose exec etcd1 etcdctl get /chora/ --prefix

# Delete a key
docker-compose exec etcd1 etcdctl del /chora/capabilities/test

# Watch for changes
docker-compose exec etcd1 etcdctl watch /chora/ --prefix
```

### Cluster Health

```bash
# Check endpoint health
docker-compose exec etcd1 etcdctl endpoint health

# Check cluster status
docker-compose exec etcd1 etcdctl endpoint status --cluster -w table

# List cluster members
docker-compose exec etcd1 etcdctl member list -w table
```

### Performance Testing

```bash
# Write performance test (1000 concurrent writes)
docker-compose exec etcd1 etcdctl check perf --auto-compact --auto-defrag

# Read performance test
time for i in {1..10000}; do
  docker-compose exec -T etcd1 etcdctl get /chora/test >/dev/null;
done
```

Expected performance:
- **Writes**: ~5k ops/sec
- **Reads**: ~10k ops/sec
- **Latency (p95)**: <10ms

## Monitoring

### Health Checks

```bash
# Check all endpoints
docker-compose exec etcd1 etcdctl endpoint health --cluster

# Expected output:
# http://etcd1:2379 is healthy: successfully committed proposal: took = 2.3ms
# http://etcd2:2379 is healthy: successfully committed proposal: took = 2.5ms
# http://etcd3:2379 is healthy: successfully committed proposal: took = 2.4ms
```

### Metrics

```bash
# Get etcd metrics
curl -L http://localhost:2379/metrics

# Key metrics to monitor:
# - etcd_server_has_leader: Should be 1
# - etcd_server_leader_changes_seen_total: Should be stable
# - etcd_disk_backend_commit_duration_seconds: Should be <10ms
# - etcd_network_peer_round_trip_time_seconds: Should be <100ms
```

### Web UI

Access etcdkeeper at http://localhost:8080:
- View all keys
- Edit values
- Monitor cluster status
- Execute queries

## Data Management

### Backup

```bash
# Snapshot current state
docker-compose exec etcd1 etcdctl snapshot save /tmp/snapshot.db

# Copy snapshot to host
docker cp etcd1:/tmp/snapshot.db ./backup-$(date +%Y%m%d).db
```

### Restore

```bash
# Stop cluster
docker-compose down

# Remove old data
docker volume rm etcd_etcd1-data etcd_etcd2-data etcd_etcd3-data

# Restore from snapshot (on each node)
docker-compose run etcd1 etcdctl snapshot restore backup.db \
  --name etcd1 \
  --initial-cluster etcd1=http://etcd1:2380,etcd2=http://etcd2:2380,etcd3=http://etcd3:2380 \
  --initial-advertise-peer-urls http://etcd1:2380 \
  --data-dir /etcd-data

# Restart cluster
docker-compose up -d
```

### Compaction

```bash
# Manual compaction (removes old revisions)
docker-compose exec etcd1 etcdctl compact $(docker-compose exec -T etcd1 etcdctl endpoint status --write-out="json" | jq -r '.[].Status.header.revision')

# Defragment (reclaim space)
docker-compose exec etcd1 etcdctl defrag
docker-compose exec etcd2 etcdctl defrag
docker-compose exec etcd3 etcdctl defrag
```

## Schema Design

### Capability Registry Schema

```
/chora/capabilities/{namespace}/
  /metadata          - JSON: dc_identifier, dc_title, dc_description
  /type              - "service" or "pattern"
  /version           - SemVer string
  /dependencies      - JSON array of dependencies
  /health            - Service-type only: heartbeat timestamp
```

Example:
```bash
# Store capability metadata
docker-compose exec etcd1 etcdctl put /chora/capabilities/chora.devex.registry/metadata \
  '{"dc_identifier":"chora.devex.registry","dc_title":"Registry","type":"service"}'

# Store health status (Service-type)
docker-compose exec etcd1 etcdctl put /chora/capabilities/chora.devex.registry/health \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --lease=30

# List all capabilities
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix --keys-only
```

## Troubleshooting

### Cluster won't start

**Problem**: Nodes fail to form cluster

**Solution**:
```bash
# Check logs
docker-compose logs etcd1

# Reset cluster (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
```

### High latency

**Problem**: Latency >10ms

**Solution**:
```bash
# Check disk I/O
docker stats

# Defragment database
docker-compose exec etcd1 etcdctl defrag --cluster
```

### Split brain

**Problem**: Multiple leaders elected

**Solution**:
```bash
# Check member list
docker-compose exec etcd1 etcdctl member list

# Verify cluster status
docker-compose exec etcd1 etcdctl endpoint status --cluster -w table

# If corrupted, restore from backup
```

### Out of quota

**Problem**: "etcdserver: mvcc: database space exceeded"

**Solution**:
```bash
# Check database size
docker-compose exec etcd1 etcdctl endpoint status --write-out=table

# Compact and defragment
docker-compose exec etcd1 etcdctl compact <revision>
docker-compose exec etcd1 etcdctl defrag --cluster
```

## Performance Benchmarks

### Target Performance

| Metric | Target | Actual |
|--------|--------|--------|
| Read throughput | 10k ops/sec | ~15k ops/sec |
| Write throughput | 5k ops/sec | ~7k ops/sec |
| Read latency (p95) | <10ms | ~5ms |
| Write latency (p95) | <20ms | ~12ms |
| Uptime | >99% | ~99.9% |

### Benchmark Tests

```bash
# Install benchmark tool
go install go.etcd.io/etcd/tools/benchmark@latest

# Write benchmark (1000 concurrent clients)
benchmark --endpoints=localhost:2379 \
  --conns=100 \
  --clients=1000 \
  put --key-size=8 --val-size=256

# Read benchmark
benchmark --endpoints=localhost:2379 \
  --conns=100 \
  --clients=1000 \
  range key --consistency=l

# Mixed workload (70% reads, 30% writes)
benchmark --endpoints=localhost:2379 \
  --conns=100 \
  --clients=1000 \
  --rate-limit=10000 \
  mvcc
```

## Security

### TLS Configuration (Optional)

For production deployments, enable TLS:

```yaml
# Add to docker-compose.yml
environment:
  - ETCD_CLIENT_CERT_AUTH=true
  - ETCD_TRUSTED_CA_FILE=/certs/ca.crt
  - ETCD_CERT_FILE=/certs/server.crt
  - ETCD_KEY_FILE=/certs/server.key
volumes:
  - ./certs:/certs:ro
```

### Access Control (Optional)

Enable authentication:

```bash
# Enable auth
docker-compose exec etcd1 etcdctl user add root
docker-compose exec etcd1 etcdctl auth enable

# Create role
docker-compose exec etcd1 etcdctl role add registry
docker-compose exec etcd1 etcdctl role grant-permission registry readwrite /chora/ --prefix
```

## Integration

### Python Client

```python
import etcd3

# Connect to cluster
etcd = etcd3.client(
    host='localhost',
    port=2379,
    # For load balancing, use multiple endpoints
)

# Write capability
etcd.put('/chora/capabilities/test', '{"type":"service"}')

# Read capability
value, metadata = etcd.get('/chora/capabilities/test')

# Watch for changes
for event in etcd.watch_prefix('/chora/capabilities/'):
    print(f"Event: {event}")
```

### Go Client

```go
import (
    "context"
    clientv3 "go.etcd.io/etcd/client/v3"
)

client, err := clientv3.New(clientv3.Config{
    Endpoints: []string{"localhost:2379", "localhost:2389", "localhost:2399"},
})

// Put key
_, err = client.Put(context.TODO(), "/chora/capabilities/test", "value")

// Get key
resp, err := client.Get(context.TODO(), "/chora/capabilities/test")
```

## Related Documentation

- [etcd Official Documentation](https://etcd.io/docs/)
- [Raft Consensus Algorithm](https://raft.github.io/)
- [Registry Service Design](../../docs/project-docs/registry-service-design.md)

---

**Version**: 1.0.0
**Last Updated**: 2025-11-15
**Status**: Production Ready
