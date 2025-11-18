# How to Install and Run Production etcd Registry Infrastructure

**Version**: 5.2.0
**Last Updated**: 2025-11-17
**Status**: Production Ready

This guide explains how to install and operate the complete etcd-based registry infrastructure for the chora ecosystem.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Infrastructure Components](#infrastructure-components)
5. [Installation Steps](#installation-steps)
6. [Verification](#verification)
7. [Management Commands](#management-commands)
8. [Troubleshooting](#troubleshooting)
9. [Monitoring](#monitoring)
10. [Backup and Recovery](#backup-and-recovery)

---

## Overview

The v5.2.0 registry infrastructure consists of:

- **etcd 3-node cluster**: Distributed key-value store with Raft consensus
- **GitOps Sync Service**: Automatically syncs capability manifests to etcd
- **Heartbeat Service**: Monitors Service-type capability health with 30s TTL leases

**Performance Targets**:
- Read throughput: 10k ops/sec
- Write throughput: 5k ops/sec
- Latency (p95): <10ms

---

## Prerequisites

### Required Software

- **Docker**: 20.10+ with Docker Compose v2
- **Git**: For cloning the repository
- **Python 3.11+**: For running tests and utilities (optional)

### System Requirements

- **CPU**: 2+ cores recommended
- **RAM**: 4GB+ available
- **Disk**: 10GB+ free space for etcd data volumes
- **Network**: Docker bridge networking enabled

### Optional Dependencies

```bash
# For running E2E tests
pip install etcd3==0.12.0 protobuf==3.20.3

# For advanced monitoring
pip install PyYAML==6.0.1
```

---

## Quick Start

```bash
# Navigate to infrastructure directory
cd chora-base/infrastructure/etcd

# Start the complete stack
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Run E2E tests (requires Python dependencies)
python test-e2e.py
```

Expected output:
```
Tests passed: 4/4
Pass rate: 100.0%
[SUCCESS] All tests passed!
```

---

## Infrastructure Components

### 1. etcd Cluster (3 nodes)

- **etcd1**: Primary node (ports 2379, 2380)
- **etcd2**: Secondary node (ports 2389, 2390)
- **etcd3**: Tertiary node (ports 2399, 2400)

**Configuration**:
- Heartbeat interval: 100ms
- Election timeout: 1000ms
- Storage quota: 8GB per node
- Auto-compaction: Every hour

### 2. GitOps Sync Service

Watches `capabilities/` directory and syncs manifest data to etcd.

**Synced Keys** (per capability):
- `/chora/capabilities/{namespace}/metadata` - Dublin Core metadata (JSON)
- `/chora/capabilities/{namespace}/type` - "service" or "pattern"
- `/chora/capabilities/{namespace}/version` - SemVer string
- `/chora/capabilities/{namespace}/dependencies` - Dependency list (JSON)

**Update Interval**: 60 seconds (configurable)

### 3. Heartbeat Service

Monitors Service-type capabilities with heartbeat leases.

**Heartbeat Schema**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-17T06:30:00.000Z",
  "namespace": "chora.awareness.sap_self_evaluation",
  "heartbeat_count": 42
}
```

**Configuration**:
- Heartbeat interval: 10 seconds
- Lease TTL: 30 seconds
- Auto-discovery: Scans `capabilities/` for Service-type manifests

---

## Installation Steps

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd chora-workspace/chora-base
```

### Step 2: Verify Capabilities Directory

Ensure capability manifests exist:

```bash
ls capabilities/*.yaml
```

You should see files like:
- `chora.devex.registry.yaml`
- `chora.awareness.sap_self_evaluation.yaml`
- etc.

### Step 3: Start Infrastructure

```bash
cd infrastructure/etcd
docker-compose up -d
```

This starts:
- 3 etcd nodes (etcd1, etcd2, etcd3)
- gitops-sync service
- registry-heartbeat service

### Step 4: Wait for Initialization

Services need 10-30 seconds to fully initialize:

```bash
# Check status
docker-compose ps

# Wait for all services to show "healthy"
watch docker-compose ps
```

### Step 5: Verify Deployment

```bash
# Check etcd cluster health
docker-compose exec etcd1 etcdctl endpoint health

# List capability keys in etcd
docker-compose exec etcd1 etcdctl get /chora/ --prefix --keys-only | head -20

# Check heartbeat logs
docker-compose logs --tail=20 heartbeat
```

---

## Verification

### Manual Verification

1. **Check etcd cluster**:
```bash
docker-compose exec etcd1 etcdctl endpoint status --cluster -w table
```

2. **Verify GitOps sync data**:
```bash
docker-compose exec etcd1 etcdctl get /chora/capabilities/chora.devex.registry/metadata
```

3. **Verify heartbeat health**:
```bash
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix | grep -A1 health
```

### Automated E2E Test

```bash
# Install dependencies
pip install etcd3==0.12.0 protobuf==3.20.3

# Run test suite
python test-e2e.py
```

The test validates:
- etcd cluster health (3 nodes)
- GitOps sync population (metadata, type, version, dependencies)
- Heartbeat service operation (lease renewals, persistence)
- Data persistence beyond lease TTL (35+ seconds)

---

## Management Commands

### Start/Stop Services

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart heartbeat

# Stop without removing volumes
docker-compose stop
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f heartbeat
docker-compose logs -f gitops-sync

# Last 50 lines
docker-compose logs --tail=50 heartbeat
```

### Check Service Health

```bash
# Docker health status
docker-compose ps

# etcd cluster health
docker-compose exec etcd1 etcdctl endpoint health --cluster

# Check heartbeat service is sending
docker-compose logs --tail=10 heartbeat | grep "Heartbeat sent"
```

### Data Operations

```bash
# List all capabilities
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix --keys-only

# Get specific capability metadata
docker-compose exec etcd1 etcdctl get /chora/capabilities/chora.devex.registry/metadata

# Watch for changes
docker-compose exec etcd1 etcdctl watch /chora/capabilities/ --prefix
```

---

## Troubleshooting

### Issue 1: Services Fail to Start

**Symptoms**:
```
ERROR: etcd3 not installed
TypeError: Descriptors cannot be created directly
```

**Solution**:
Rebuild services with correct dependencies:

```bash
docker-compose build heartbeat gitops-sync
docker-compose up -d
```

The Dockerfiles pin `protobuf==3.20.3` to avoid compatibility issues.

---

### Issue 2: Heartbeat Lease Expiration

**Symptoms**:
```
ERROR - Failed to send heartbeat: "etcdserver: requested lease not found"
```

**Root Cause**: Lease created too early or not renewed frequently enough.

**Solution**: The v5.2.0 fix includes:
- Just-in-time lease creation in `run()` method
- Lease refresh every 10 seconds (via `lease.refresh()`)

If you see this error, verify you're running the latest heartbeat.py:

```bash
docker-compose build heartbeat
docker-compose up -d heartbeat
docker-compose logs --tail=20 heartbeat
```

You should see:
```
INFO - [check mark] Heartbeat sent: ... (count: N)
INFO - [circling arrows] Lease renewed (TTL: 30s)
```

---

### Issue 3: No Data in etcd

**Symptoms**:
```bash
$ docker-compose exec etcd1 etcdctl get /chora/ --prefix
# (no output)
```

**Possible Causes**:
1. GitOps sync hasn't run yet (wait 60 seconds)
2. Capabilities directory is empty or not mounted
3. GitOps sync service failed to start

**Diagnosis**:
```bash
# Check gitops-sync logs
docker-compose logs gitops-sync

# Verify capabilities directory is mounted
docker-compose exec gitops-sync ls /app/capabilities

# Force sync by restarting service
docker-compose restart gitops-sync
```

---

### Issue 4: High Latency

**Symptoms**: etcd operations taking >10ms

**Diagnosis**:
```bash
# Check disk I/O
docker stats

# Check etcd metrics
curl -L http://localhost:2379/metrics | grep latency
```

**Solutions**:
1. Defragment etcd database:
```bash
docker-compose exec etcd1 etcdctl defrag --cluster
```

2. Compact old revisions:
```bash
# Get current revision
REV=$(docker-compose exec -T etcd1 etcdctl endpoint status --write-out=json | jq -r '.[0].Status.header.revision')

# Compact
docker-compose exec etcd1 etcdctl compact $REV
```

---

## Monitoring

### Health Checks

```bash
# Overall system health
docker-compose ps

# etcd cluster health
docker-compose exec etcd1 etcdctl endpoint health --cluster

# Check heartbeat count (should increase every 10s)
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix | grep heartbeat_count
```

### Metrics Collection

etcd exposes Prometheus metrics at `http://localhost:2379/metrics`:

```bash
# Key metrics to monitor
curl -s http://localhost:2379/metrics | grep -E "(etcd_server_has_leader|etcd_disk_backend_commit_duration)"
```

**Critical Metrics**:
- `etcd_server_has_leader`: Should be 1
- `etcd_server_leader_changes_seen_total`: Should be stable (no frequent elections)
- `etcd_disk_backend_commit_duration_seconds`: Should be <0.010 (10ms)
- `etcd_network_peer_round_trip_time_seconds`: Should be <0.100 (100ms)

### Log Monitoring

```bash
# Monitor heartbeat service
docker-compose logs -f heartbeat | grep -E "(Heartbeat sent|Lease renewed|ERROR)"

# Monitor gitops-sync
docker-compose logs -f gitops-sync | grep -E "(Synced|ERROR)"
```

---

## Backup and Recovery

### Create Backup

```bash
# Snapshot etcd data
docker-compose exec etcd1 etcdctl snapshot save /tmp/snapshot.db

# Copy to host
docker cp etcd1:/tmp/snapshot.db ./backup-$(date +%Y%m%d-%H%M%S).db
```

### Restore from Backup

```bash
# Stop cluster
docker-compose down

# Remove old data
docker volume rm etcd_etcd1-data etcd_etcd2-data etcd_etcd3-data

# Restore snapshot (example for etcd1)
docker-compose run etcd1 etcdctl snapshot restore backup.db \
  --name etcd1 \
  --initial-cluster etcd1=http://etcd1:2380,etcd2=http://etcd2:2380,etcd3=http://etcd3:2380 \
  --initial-advertise-peer-urls http://etcd1:2380 \
  --data-dir /etcd-data

# Restart cluster
docker-compose up -d
```

**Note**: Full restore procedure for all 3 nodes is documented in [README.md](README.md#restore).

---

## Additional Resources

- [etcd README](README.md) - Detailed etcd cluster documentation
- [E2E Test Script](test-e2e.py) - Automated integration tests
- [Heartbeat Service](../../services/registry-heartbeat/heartbeat.py) - Source code
- [GitOps Sync Script](../../scripts/gitops-sync-registry.py) - Source code
- [Official etcd Documentation](https://etcd.io/docs/)

---

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section above
2. Review service logs: `docker-compose logs <service>`
3. Run E2E tests: `python test-e2e.py`
4. Consult [etcd README](README.md) for cluster-specific issues

---

**Last Verified**: 2025-11-17
**Infrastructure Version**: 5.2.0
**Test Pass Rate**: 100% (4/4 tests)
