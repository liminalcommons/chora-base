# Orchestration Health Monitor

**Purpose**: Auto-recovery for MCP service infrastructure
**Status**: Production-ready
**Version**: 1.0.0

## Overview

The Orchestration Health Monitor provides zero-touch infrastructure recovery for chora-workspace MCP services. It monitors etcd for expired heartbeat leases and automatically restarts unhealthy Docker containers.

**Key Features**:
- **Automatic failure detection**: Monitors heartbeat leases in etcd (30s TTL)
- **Auto-restart**: Restarts unhealthy containers via Docker SDK
- **<60s recovery SLA**: Detection (30s) + restart (20s) + resume (<10s)
- **Rate limiting**: Max 3 restarts per service per hour (prevents restart loops)
- **Comprehensive logging**: All restart attempts logged with timestamps
- **Health metrics**: Checks performed, services monitored, restarts triggered

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  Orchestration Health Monitor                                       │
│                                                                      │
│  1. Query etcd for all /chora/capabilities/*/health keys            │
│  2. Check heartbeat timestamp (age > 30s = unhealthy)               │
│  3. Map namespace → container name (chora.mcp.manifest → ...)       │
│  4. Restart container via Docker SDK                                │
│  5. Wait 10s, loop                                                   │
└─────────────────────────────────────────────────────────────────────┘
                          │
                          │ Queries health keys
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│  etcd Cluster (3 nodes)                                              │
│                                                                      │
│  Keys:                                                               │
│    /chora/capabilities/chora.mcp.manifest/health → {..., ts: ...}   │
│    /chora/capabilities/chora.mcp.github/health → {..., ts: ...}     │
│    /chora/capabilities/chora.mcp.n8n/health → {..., ts: ...}        │
└─────────────────────────────────────────────────────────────────────┘
                          │
                          │ Restarts containers
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Docker Containers                                                   │
│                                                                      │
│  - chora-mcp-manifest                                                │
│  - chora-mcp-github                                                  │
│  - n8n-server                                                        │
│  - ... (all Service-type capabilities)                              │
└─────────────────────────────────────────────────────────────────────┘
```

## Usage

### Docker Compose (Production)

The health monitor runs automatically when you start the etcd infrastructure:

```bash
cd packages/chora-base/infrastructure/etcd
docker-compose up -d

# Check logs
docker logs -f orchestration-health-monitor

# Check stats
docker exec orchestration-health-monitor python -c "
import health_monitor
monitor = health_monitor.HealthMonitor()
monitor.print_stats()
"
```

### Standalone (Development)

```bash
# Monitor all services (recommended)
python health_monitor.py

# Custom check interval (15 seconds)
python health_monitor.py --interval 15

# Custom heartbeat TTL (60 seconds)
python health_monitor.py --ttl 60

# Custom etcd host
python health_monitor.py --etcd-host localhost --etcd-port 2379
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--etcd-host` | `etcd1` | etcd server hostname |
| `--etcd-port` | `2379` | etcd client port |
| `--interval` | `10` | Health check interval (seconds) |
| `--ttl` | `30` | Expected heartbeat TTL (seconds) |
| `--docker-host` | `unix://var/run/docker.sock` | Docker daemon URL |

**Tuning Recommendations**:
- **Low latency networks**: `--interval 5 --ttl 15` (faster detection, 15-20s recovery)
- **High latency networks**: `--interval 15 --ttl 60` (fewer false positives, 60-90s recovery)
- **Production (default)**: `--interval 10 --ttl 30` (balanced, <60s recovery)

## Recovery Timeline

**Example**: chora-mcp-manifest crashes at T+0s

```
T+0s   : Service fails (e.g., chora-mcp-manifest crashes)
T+10s  : registry-heartbeat misses heartbeat (10s interval)
T+30s  : Heartbeat lease expires in etcd (30s TTL)
T+40s  : Health monitor detects failure (10s check interval)
T+45s  : Docker container restart completes (~5s)
T+55s  : registry-heartbeat resumes, writes fresh lease to etcd
───────────────────────────────────────────────────────────────
Total  : <60 seconds (detection + restart + resume)
```

## Rate Limiting

To prevent restart loops (e.g., service crashes immediately after restart), the health monitor enforces:

- **Max restarts**: 3 per service per hour
- **Behavior**: If limit exceeded, service is marked as unhealthy but not restarted
- **Logging**: Rate limit events logged with warning level

**Example**:
```
2025-11-23 12:00:00 - health-monitor - WARNING - Rate limit exceeded for chora.mcp.manifest: 3 restarts in last 3600s
```

If you see rate limit warnings, investigate the root cause:
1. Check service logs: `docker logs chora-mcp-manifest`
2. Check container resource usage: `docker stats chora-mcp-manifest`
3. Check for config errors, missing dependencies, or resource exhaustion

## Namespace → Container Name Mapping

The health monitor uses the following rules to map namespaces to Docker container names:

| Namespace | Container Name | Note |
|-----------|----------------|------|
| `chora.mcp.manifest` | `chora-mcp-manifest` | Standard (dots → dashes) |
| `chora.mcp.github` | `chora-mcp-github` | Standard |
| `chora.mcp.n8n` | `n8n-server` | Special case |
| `chora.orchestration` | `chora-orchestration` | Standard |
| `chora.gateway` | `chora-gateway` | Standard |

**Custom mappings**: Edit `namespace_to_container_name()` in [health_monitor.py:162](health_monitor.py#L162)

## Monitoring & Metrics

The health monitor tracks the following metrics:

```python
{
    'checks_performed': 120,           # Total health checks
    'services_monitored': 9,           # Active services
    'unhealthy_detected': 2,           # Unhealthy services found
    'restarts_triggered': 2,           # Restart attempts
    'restarts_successful': 2,          # Successful restarts
    'restarts_failed': 0,              # Failed restarts
    'rate_limited': 0,                 # Rate limit violations
    'started_at': '2025-11-23T12:00:00'
}
```

**View metrics**:
```bash
# Docker logs
docker logs orchestration-health-monitor | grep "Statistics"

# Python REPL
docker exec -it orchestration-health-monitor python
>>> import health_monitor
>>> monitor = health_monitor.HealthMonitor()
>>> monitor.print_stats()
```

## Troubleshooting

### Problem 1: False Positives (Healthy Services Restarted)

**Symptom**: Services restarted even though they're healthy

**Causes**:
- Heartbeat TTL too short (network latency > TTL)
- Check interval too aggressive

**Solutions**:
```bash
# Increase TTL to 60s (more tolerance for latency)
docker-compose stop orchestration-health-monitor
docker-compose up -d orchestration-health-monitor \
    --interval 15 --ttl 60
```

### Problem 2: Container Restart Fails

**Symptom**: `Failed to restart container for chora.mcp.manifest: ...`

**Causes**:
- Container name mismatch (namespace → container name mapping wrong)
- Docker daemon not accessible (socket permission issue)
- Container doesn't exist

**Solutions**:
```bash
# Check container name
docker ps --format "table {{.Names}}\t{{.Status}}"

# Check Docker socket permissions
ls -la /var/run/docker.sock
# Should show: srw-rw---- 1 root docker

# Add user to docker group
sudo usermod -aG docker $USER
```

### Problem 3: Rate Limit Exceeded

**Symptom**: `Rate limit exceeded for chora.mcp.manifest: 3 restarts in last 3600s`

**Causes**:
- Service crashes immediately after restart (crash loop)
- Config error, missing dependency, resource exhaustion

**Solutions**:
```bash
# Check service logs
docker logs chora-mcp-manifest

# Check resource usage
docker stats chora-mcp-manifest

# Manually restart (bypasses rate limit)
docker restart chora-mcp-manifest

# Increase rate limit (edit health_monitor.py:78)
RestartLimiter(max_restarts=5, window_seconds=3600)
```

### Problem 4: etcd Connection Failed

**Symptom**: `Failed to connect to etcd: ...`

**Causes**:
- etcd cluster not running
- Wrong etcd host/port
- Network issue

**Solutions**:
```bash
# Check etcd cluster
docker ps | grep etcd

# Test etcd connection
docker exec etcd1 etcdctl endpoint health

# Check network (health monitor must be in chora-network)
docker network inspect chora-network
```

## Testing

### Unit Tests

```bash
cd packages/chora-base/services/orchestration-health-monitor
pytest tests/test_health_monitor.py
```

### Integration Tests

```bash
# Test failure detection
docker stop chora-mcp-manifest
sleep 40  # Wait for lease expiration (30s) + check (10s)
docker logs orchestration-health-monitor | grep "Unhealthy service detected"
docker logs orchestration-health-monitor | grep "Successfully restarted"

# Verify recovery
sleep 20
docker ps | grep chora-mcp-manifest  # Should show "Up X seconds"
```

## Related Documentation

- [Self-Healing Infrastructure How-To](../../docs/how-to/self-healing-infrastructure.md) - User guide
- [OPP-2025-046](../../project-docs/opportunities/open/OPP-2025-046-dynamic-service-mesh-self-healing.md) - Opportunity file
- [Registry Heartbeat Service](../registry-heartbeat/README.md) - Heartbeat service
- [etcd Infrastructure](../../infrastructure/etcd/README.md) - etcd cluster setup

## Future Enhancements

1. **Predictive Failure Detection** (with Graphiti):
   - Pattern mining: Detect heartbeat drift before crash (10s → 15s → 25s → crash)
   - Proactive restart before service fails completely
   - 50-70% failure prevention

2. **Temporal Workflow Debugging** (with Graphiti):
   - Point-in-time infrastructure state reconstruction
   - 95% faster incident investigation (60 min → 3 min)
   - Event correlation for root cause analysis

3. **Multi-Cluster Support**:
   - Monitor services across multiple Docker hosts
   - Failover to backup containers
   - Load balancing and auto-scaling

---

**Created**: 2025-11-23
**Version**: 1.0.0
**Maintainer**: chora-workspace
**License**: MIT

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
