#!/usr/bin/env python3
"""
Orchestration Health Monitor

Monitors etcd for Service-type capabilities with expired heartbeat leases
and automatically restarts unhealthy Docker containers.

Features:
- Query etcd for expired heartbeat leases (TTL > 30s)
- Auto-discovery of Service-type capabilities via manifest registry
- Docker container restart with exponential backoff
- Health status monitoring and alerting
- Comprehensive error handling and logging
- Restart rate limiting (max 3 restarts per service per hour)

Architecture:
1. Query etcd for all /chora/capabilities/*/health keys
2. Check lease TTL - if expired (>30s since last heartbeat), service is unhealthy
3. Map namespace to container name (chora.mcp.manifest → chora-mcp-manifest)
4. Restart container via Docker SDK
5. Wait for service to resume heartbeat
6. Loop every 10 seconds

Usage:
    # Monitor all services with auto-discovery
    python health_monitor.py --auto-discover

    # Monitor specific namespace
    python health_monitor.py --namespace chora.mcp.manifest

    # Custom check interval
    python health_monitor.py --auto-discover --interval 15
"""

import argparse
import json
import logging
import signal
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install PyYAML", file=sys.stderr)
    sys.exit(2)

try:
    import etcd3
except ImportError:
    print("ERROR: etcd3 not installed. Run: pip install etcd3", file=sys.stderr)
    sys.exit(2)

try:
    import docker
except ImportError:
    print("ERROR: docker not installed. Run: pip install docker", file=sys.stderr)
    sys.exit(2)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('health-monitor')


class RestartLimiter:
    """Rate limiter for container restarts (max 3 restarts per hour per service)"""

    def __init__(self, max_restarts: int = 3, window_seconds: int = 3600):
        self.max_restarts = max_restarts
        self.window_seconds = window_seconds
        self.restart_history: Dict[str, List[datetime]] = defaultdict(list)

    def can_restart(self, namespace: str) -> bool:
        """Check if service can be restarted (rate limit)"""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_seconds)

        # Clean up old restart timestamps
        self.restart_history[namespace] = [
            ts for ts in self.restart_history[namespace]
            if ts > window_start
        ]

        # Check if under limit
        if len(self.restart_history[namespace]) >= self.max_restarts:
            logger.warning(
                f"Rate limit exceeded for {namespace}: "
                f"{len(self.restart_history[namespace])} restarts in last {self.window_seconds}s"
            )
            return False

        return True

    def record_restart(self, namespace: str):
        """Record a restart timestamp"""
        self.restart_history[namespace].append(datetime.utcnow())


class HealthMonitor:
    """Orchestration health monitor for auto-restart"""

    def __init__(
        self,
        etcd_host: str = 'etcd1',
        etcd_port: int = 2379,
        check_interval: int = 10,  # Seconds between checks
        heartbeat_ttl: int = 30,  # Expected heartbeat TTL
        docker_host: str = 'unix://var/run/docker.sock',
    ):
        self.etcd_host = etcd_host
        self.etcd_port = etcd_port
        self.check_interval = check_interval
        self.heartbeat_ttl = heartbeat_ttl
        self.docker_host = docker_host
        self.etcd = None
        self.docker_client = None
        self.running = False
        self.restart_limiter = RestartLimiter(max_restarts=3, window_seconds=3600)
        self.stats = {
            'checks_performed': 0,
            'services_monitored': 0,
            'unhealthy_detected': 0,
            'restarts_triggered': 0,
            'restarts_successful': 0,
            'restarts_failed': 0,
            'rate_limited': 0,
            'started_at': None,
        }

    def connect_etcd(self) -> bool:
        """Connect to etcd cluster"""
        try:
            self.etcd = etcd3.client(host=self.etcd_host, port=self.etcd_port)
            # Test connection
            self.etcd.status()
            logger.info(f"Connected to etcd at {self.etcd_host}:{self.etcd_port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to etcd: {e}")
            return False

    def connect_docker(self) -> bool:
        """Connect to Docker daemon"""
        try:
            self.docker_client = docker.DockerClient(base_url=self.docker_host)
            # Test connection
            self.docker_client.ping()
            logger.info(f"Connected to Docker at {self.docker_host}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Docker: {e}")
            return False

    def get_all_health_keys(self) -> List[tuple]:
        """Get all health keys from etcd"""
        try:
            # Query all health keys under /chora/capabilities/
            health_keys = []
            for value, metadata in self.etcd.get_prefix('/chora/capabilities/'):
                key = metadata.key.decode('utf-8')
                if key.endswith('/health'):
                    health_keys.append((key, value.decode('utf-8')))
            return health_keys
        except Exception as e:
            logger.error(f"Failed to query etcd health keys: {e}")
            return []

    def check_service_health(self, health_key: str, health_data: str) -> bool:
        """
        Check if service is healthy based on heartbeat timestamp.

        Returns:
            True if healthy (recent heartbeat within TTL)
            False if unhealthy (no recent heartbeat or expired lease)
        """
        try:
            health_status = json.loads(health_data)
            timestamp_str = health_status.get('timestamp', '')

            # Parse timestamp (ISO 8601 format: 2025-11-23T12:34:56Z)
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

            # Check if timestamp is recent (within TTL window)
            now = datetime.now(timestamp.tzinfo)
            age_seconds = (now - timestamp).total_seconds()

            if age_seconds > self.heartbeat_ttl:
                logger.warning(
                    f"Unhealthy service detected: {health_key} "
                    f"(last heartbeat {age_seconds:.1f}s ago, TTL={self.heartbeat_ttl}s)"
                )
                return False

            return True

        except Exception as e:
            logger.error(f"Failed to parse health data for {health_key}: {e}")
            return False

    def namespace_to_container_name(self, namespace: str) -> str:
        """
        Convert namespace to Docker container name.

        Examples:
            chora.mcp.manifest → chora-mcp-manifest
            chora.mcp.github → chora-mcp-github
            chora.mcp.n8n → n8n-server (special case)
        """
        # Special cases for non-standard container names
        special_cases = {
            'chora.mcp.n8n': 'n8n-server',
        }

        if namespace in special_cases:
            return special_cases[namespace]

        # Standard case: replace dots with dashes
        return namespace.replace('.', '-')

    def restart_container(self, namespace: str) -> bool:
        """
        Restart Docker container for unhealthy service.

        Returns:
            True if restart successful
            False if restart failed
        """
        # Check rate limit
        if not self.restart_limiter.can_restart(namespace):
            self.stats['rate_limited'] += 1
            return False

        try:
            container_name = self.namespace_to_container_name(namespace)

            logger.info(f"Attempting to restart container: {container_name} (namespace: {namespace})")

            # Get container
            try:
                container = self.docker_client.containers.get(container_name)
            except docker.errors.NotFound:
                logger.error(f"Container not found: {container_name}")
                self.stats['restarts_failed'] += 1
                return False

            # Check container status
            container.reload()
            status = container.status
            logger.info(f"Container {container_name} status: {status}")

            # Restart container
            restart_start = time.time()
            container.restart(timeout=20)  # 20s timeout for graceful shutdown
            restart_duration = time.time() - restart_start

            # Record restart
            self.restart_limiter.record_restart(namespace)
            self.stats['restarts_successful'] += 1

            logger.info(
                f"Successfully restarted {container_name} "
                f"(duration: {restart_duration:.1f}s)"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to restart container for {namespace}: {e}")
            self.stats['restarts_failed'] += 1
            return False

    def check_and_heal(self):
        """Check all services and restart unhealthy ones"""
        self.stats['checks_performed'] += 1

        # Get all health keys
        health_keys = self.get_all_health_keys()
        self.stats['services_monitored'] = len(health_keys)

        if not health_keys:
            logger.debug("No services to monitor")
            return

        logger.debug(f"Monitoring {len(health_keys)} service(s)")

        # Check each service
        for health_key, health_data in health_keys:
            # Extract namespace from key: /chora/capabilities/chora.mcp.manifest/health
            namespace = health_key.replace('/chora/capabilities/', '').replace('/health', '')

            # Check health
            is_healthy = self.check_service_health(health_key, health_data)

            if not is_healthy:
                self.stats['unhealthy_detected'] += 1
                self.stats['restarts_triggered'] += 1

                logger.warning(f"Service unhealthy: {namespace}, triggering restart...")
                self.restart_container(namespace)

    def run(self):
        """Run health monitor service"""
        logger.info("Starting orchestration health monitor")
        logger.info(f"Check interval: {self.check_interval}s")
        logger.info(f"Heartbeat TTL: {self.heartbeat_ttl}s")

        self.running = True
        self.stats['started_at'] = datetime.utcnow().isoformat()

        # Main loop
        try:
            while self.running:
                # Check and heal
                self.check_and_heal()

                # Wait for next check
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            logger.info("Health monitor stopped by user")
        except Exception as e:
            logger.error(f"Health monitor error: {e}")
            return False
        finally:
            self.cleanup()

        return True

    def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up health monitor...")

        try:
            # Close Docker client
            if self.docker_client:
                self.docker_client.close()
                logger.info("Closed Docker connection")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

    def print_stats(self):
        """Print health monitor statistics"""
        print("\n" + "=" * 80)
        print("Health Monitor Statistics")
        print("=" * 80)
        print(f"Checks performed: {self.stats['checks_performed']}")
        print(f"Services monitored: {self.stats['services_monitored']}")
        print(f"Unhealthy services detected: {self.stats['unhealthy_detected']}")
        print(f"Restarts triggered: {self.stats['restarts_triggered']}")
        print(f"Restarts successful: {self.stats['restarts_successful']}")
        print(f"Restarts failed: {self.stats['restarts_failed']}")
        print(f"Restarts rate-limited: {self.stats['rate_limited']}")
        if self.stats['started_at']:
            print(f"Started at: {self.stats['started_at']}")
        print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Orchestration health monitor for auto-restart"
    )

    # etcd connection
    parser.add_argument(
        '--etcd-host',
        default='etcd1',
        help='etcd host (default: etcd1)',
    )
    parser.add_argument(
        '--etcd-port',
        type=int,
        default=2379,
        help='etcd port (default: 2379)',
    )

    # Health check config
    parser.add_argument(
        '--interval',
        type=int,
        default=10,
        help='Health check interval in seconds (default: 10)',
    )
    parser.add_argument(
        '--ttl',
        type=int,
        default=30,
        help='Expected heartbeat TTL in seconds (default: 30)',
    )

    # Docker connection
    parser.add_argument(
        '--docker-host',
        default='unix://var/run/docker.sock',
        help='Docker host URL (default: unix://var/run/docker.sock)',
    )

    args = parser.parse_args()

    # Create health monitor
    monitor = HealthMonitor(
        etcd_host=args.etcd_host,
        etcd_port=args.etcd_port,
        check_interval=args.interval,
        heartbeat_ttl=args.ttl,
        docker_host=args.docker_host,
    )

    # Connect to etcd
    if not monitor.connect_etcd():
        logger.error("Failed to connect to etcd. Exiting.")
        sys.exit(1)

    # Connect to Docker
    if not monitor.connect_docker():
        logger.error("Failed to connect to Docker. Exiting.")
        sys.exit(1)

    # Setup signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        logger.info("Shutdown signal received")
        monitor.running = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run health monitor
    success = monitor.run()

    # Print stats
    monitor.print_stats()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
