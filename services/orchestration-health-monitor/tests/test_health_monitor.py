"""
Unit tests for orchestration health monitor.

Tests health checking logic, container restart logic, and rate limiting.
"""

import json
import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, MagicMock, patch, call
import sys
from pathlib import Path

# Add parent directory to path to import health_monitor
sys.path.insert(0, str(Path(__file__).parent.parent))

from health_monitor import HealthMonitor, RestartLimiter


class TestHealthMonitorInitialization:
    """Test HealthMonitor initialization"""

    def test_health_monitor_initialization(self):
        """Test HealthMonitor initializes with correct defaults"""
        monitor = HealthMonitor(
            etcd_host='localhost',
            etcd_port=2379,
            check_interval=10,
            heartbeat_ttl=30,
        )

        assert monitor.etcd_host == 'localhost'
        assert monitor.etcd_port == 2379
        assert monitor.check_interval == 10
        assert monitor.heartbeat_ttl == 30
        assert monitor.etcd is None  # Not connected yet
        assert monitor.docker_client is None  # Not connected yet
        assert monitor.running is False
        assert monitor.stats['checks_performed'] == 0
        assert monitor.stats['restarts_triggered'] == 0


class TestNamespaceMapping:
    """Test namespace to container name mapping"""

    def test_namespace_to_container_name_standard(self):
        """Test standard namespace mapping (dots → dashes)"""
        monitor = HealthMonitor()

        # Standard cases: replace dots with dashes
        assert monitor.namespace_to_container_name('chora.mcp.manifest') == 'chora-mcp-manifest'
        assert monitor.namespace_to_container_name('chora.mcp.github') == 'chora-mcp-github'
        assert monitor.namespace_to_container_name('chora.orchestration') == 'chora-orchestration'
        assert monitor.namespace_to_container_name('chora.gateway') == 'chora-gateway'

    def test_namespace_to_container_name_special_cases(self):
        """Test special case namespace mappings"""
        monitor = HealthMonitor()

        # Special case: chora.mcp.n8n → n8n-server
        assert monitor.namespace_to_container_name('chora.mcp.n8n') == 'n8n-server'


class TestServiceHealthChecking:
    """Test service health checking logic"""

    def test_check_service_health_healthy(self):
        """Test service with recent heartbeat is healthy"""
        monitor = HealthMonitor(heartbeat_ttl=30)

        # Create health data with timestamp 10 seconds ago (within TTL)
        now = datetime.now(timezone.utc)
        timestamp = (now - timedelta(seconds=10)).isoformat()

        health_data = json.dumps({
            'status': 'healthy',
            'timestamp': timestamp,
            'namespace': 'chora.mcp.manifest',
            'heartbeat_count': 5,
        })

        # Should return True (healthy)
        is_healthy = monitor.check_service_health(
            '/chora/capabilities/chora.mcp.manifest/health',
            health_data
        )

        assert is_healthy is True

    def test_check_service_health_unhealthy(self):
        """Test service with expired heartbeat is unhealthy"""
        monitor = HealthMonitor(heartbeat_ttl=30)

        # Create health data with timestamp 45 seconds ago (beyond TTL)
        now = datetime.now(timezone.utc)
        timestamp = (now - timedelta(seconds=45)).isoformat()

        health_data = json.dumps({
            'status': 'healthy',
            'timestamp': timestamp,
            'namespace': 'chora.mcp.manifest',
            'heartbeat_count': 5,
        })

        # Should return False (unhealthy)
        is_healthy = monitor.check_service_health(
            '/chora/capabilities/chora.mcp.manifest/health',
            health_data
        )

        assert is_healthy is False

    def test_check_service_health_invalid_data(self):
        """Test service with invalid health data returns unhealthy"""
        monitor = HealthMonitor(heartbeat_ttl=30)

        # Invalid JSON
        is_healthy = monitor.check_service_health(
            '/chora/capabilities/chora.mcp.manifest/health',
            'invalid json'
        )
        assert is_healthy is False

        # Missing timestamp
        health_data = json.dumps({'status': 'healthy'})
        is_healthy = monitor.check_service_health(
            '/chora/capabilities/chora.mcp.manifest/health',
            health_data
        )
        assert is_healthy is False


class TestRestartLimiter:
    """Test restart rate limiting logic"""

    def test_restart_limiter_allows_restart(self):
        """Test rate limiter allows restarts under limit"""
        limiter = RestartLimiter(max_restarts=3, window_seconds=3600)

        # First restart: allowed
        assert limiter.can_restart('chora.mcp.manifest') is True
        limiter.record_restart('chora.mcp.manifest')

        # Second restart: allowed
        assert limiter.can_restart('chora.mcp.manifest') is True
        limiter.record_restart('chora.mcp.manifest')

        # Third restart: allowed
        assert limiter.can_restart('chora.mcp.manifest') is True
        limiter.record_restart('chora.mcp.manifest')

    def test_restart_limiter_blocks_restart(self):
        """Test rate limiter blocks restarts over limit"""
        limiter = RestartLimiter(max_restarts=3, window_seconds=3600)

        # Record 3 restarts
        for _ in range(3):
            limiter.record_restart('chora.mcp.manifest')

        # Fourth restart: blocked
        assert limiter.can_restart('chora.mcp.manifest') is False

    def test_restart_limiter_per_service(self):
        """Test rate limiter is per-service"""
        limiter = RestartLimiter(max_restarts=3, window_seconds=3600)

        # Record 3 restarts for service A
        for _ in range(3):
            limiter.record_restart('chora.mcp.manifest')

        # Service A: blocked
        assert limiter.can_restart('chora.mcp.manifest') is False

        # Service B: allowed (different service)
        assert limiter.can_restart('chora.mcp.github') is True


class TestEtcdHealthKeyRetrieval:
    """Test etcd health key retrieval"""

    @patch('health_monitor.etcd3')
    def test_get_all_health_keys(self, mock_etcd3):
        """Test querying etcd for all health keys"""
        monitor = HealthMonitor()

        # Mock etcd client
        mock_client = MagicMock()
        monitor.etcd = mock_client

        # Create mock health data
        now = datetime.now(timezone.utc).isoformat()
        health_data = {
            'status': 'healthy',
            'timestamp': now,
            'namespace': 'chora.mcp.manifest',
        }

        # Mock etcd get_prefix response
        mock_client.get_prefix.return_value = [
            (json.dumps(health_data).encode('utf-8'), MagicMock(key=b'/chora/capabilities/chora.mcp.manifest/health')),
            (json.dumps(health_data).encode('utf-8'), MagicMock(key=b'/chora/capabilities/chora.mcp.github/health')),
            (b'other data', MagicMock(key=b'/chora/capabilities/chora.mcp.manifest/metadata')),  # Non-health key
        ]

        # Get all health keys
        health_keys = monitor.get_all_health_keys()

        # Should return 2 health keys (exclude non-health key)
        assert len(health_keys) == 2
        assert health_keys[0][0] == '/chora/capabilities/chora.mcp.manifest/health'
        assert health_keys[1][0] == '/chora/capabilities/chora.mcp.github/health'


class TestContainerRestart:
    """Test Docker container restart logic"""

    @patch('health_monitor.docker')
    def test_restart_container_success(self, mock_docker):
        """Test successful container restart"""
        monitor = HealthMonitor()

        # Mock Docker client
        mock_docker_client = MagicMock()
        monitor.docker_client = mock_docker_client

        # Mock container
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_docker_client.containers.get.return_value = mock_container

        # Restart container
        success = monitor.restart_container('chora.mcp.manifest')

        # Should succeed
        assert success is True
        assert monitor.stats['restarts_successful'] == 1
        mock_container.restart.assert_called_once_with(timeout=20)

    @patch('health_monitor.docker')
    def test_restart_container_not_found(self, mock_docker):
        """Test container restart fails when container not found"""
        monitor = HealthMonitor()

        # Mock Docker client
        mock_docker_client = MagicMock()
        monitor.docker_client = mock_docker_client

        # Mock container not found
        import docker.errors
        mock_docker_client.containers.get.side_effect = docker.errors.NotFound('Container not found')

        # Restart container
        success = monitor.restart_container('chora.mcp.manifest')

        # Should fail
        assert success is False
        assert monitor.stats['restarts_failed'] == 1

    @patch('health_monitor.docker')
    def test_restart_container_rate_limited(self, mock_docker):
        """Test container restart is blocked by rate limiter"""
        monitor = HealthMonitor()

        # Exhaust rate limit
        for _ in range(3):
            monitor.restart_limiter.record_restart('chora.mcp.manifest')

        # Mock Docker client
        mock_docker_client = MagicMock()
        monitor.docker_client = mock_docker_client

        # Attempt restart (should be rate limited)
        success = monitor.restart_container('chora.mcp.manifest')

        # Should fail due to rate limit
        assert success is False
        assert monitor.stats['rate_limited'] == 1

        # Docker restart should NOT be called
        mock_docker_client.containers.get.assert_not_called()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
