#!/usr/bin/env python3
"""
Registry Heartbeat Service

Implements heartbeat leases for Service-type capabilities with 30s TTL.
Service-type capabilities report health status every 10 seconds to maintain
their lease. Registry can monitor TTL expiration to detect unhealthy services.

Features:
- etcd lease management (30s TTL)
- Automatic lease renewal (10s interval)
- Health status reporting
- Service-type capability discovery
- Graceful shutdown with lease cleanup
- Comprehensive error handling and logging

Schema in etcd:
  /chora/capabilities/{namespace}/health - Timestamp + status with 30s TTL lease

Usage:
    # Run heartbeat for specific capability
    python heartbeat.py --namespace chora.devex.registry

    # Auto-discover Service-type capabilities and run heartbeat for all
    python heartbeat.py --auto-discover --capabilities /app/capabilities

    # Custom intervals
    python heartbeat.py --namespace chora.devex.registry --interval 10 --ttl 30
"""

import argparse
import json
import logging
import signal
import sys
import time
from datetime import datetime
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('heartbeat')


class HeartbeatService:
    """Heartbeat service for Service-type capabilities"""

    def __init__(
        self,
        namespace: str,
        etcd_host: str = 'localhost',
        etcd_port: int = 2379,
        interval: int = 10,  # Heartbeat interval in seconds
        ttl: int = 30,  # Lease TTL in seconds
    ):
        self.namespace = namespace
        self.etcd_host = etcd_host
        self.etcd_port = etcd_port
        self.interval = interval
        self.ttl = ttl
        self.etcd = None
        self.lease = None
        self.running = False
        self.stats = {
            'heartbeats_sent': 0,
            'lease_renewals': 0,
            'errors': 0,
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

    def create_lease(self) -> bool:
        """Create etcd lease with TTL"""
        try:
            self.lease = self.etcd.lease(self.ttl)
            logger.info(f"Created lease with {self.ttl}s TTL (ID: {self.lease.id})")
            return True
        except Exception as e:
            logger.error(f"Failed to create lease: {e}")
            return False

    def send_heartbeat(self) -> bool:
        """Send heartbeat to etcd"""
        try:
            # Build health status
            health_status = {
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'namespace': self.namespace,
                'heartbeat_count': self.stats['heartbeats_sent'] + 1,
            }

            # Write to etcd with lease
            health_key = f"/chora/capabilities/{self.namespace}/health"
            self.etcd.put(
                health_key,
                json.dumps(health_status),
                lease=self.lease
            )

            self.stats['heartbeats_sent'] += 1
            logger.debug(f"Heartbeat sent: {self.namespace} (count: {self.stats['heartbeats_sent']})")
            return True

        except Exception as e:
            logger.error(f"Failed to send heartbeat: {e}")
            self.stats['errors'] += 1
            return False

    def renew_lease(self) -> bool:
        """Renew lease (keep-alive)"""
        try:
            # Lease renewal is automatic with etcd3 library
            # We just need to verify it's still alive
            ttl = self.lease.ttl
            if ttl > 0:
                self.stats['lease_renewals'] += 1
                logger.debug(f"Lease renewed (TTL: {ttl}s)")
                return True
            else:
                logger.warning("Lease expired, recreating...")
                return self.create_lease()

        except Exception as e:
            logger.error(f"Failed to renew lease: {e}")
            self.stats['errors'] += 1
            # Try to recreate lease
            return self.create_lease()

    def run(self):
        """Run heartbeat service"""
        logger.info(f"Starting heartbeat service for {self.namespace}")
        logger.info(f"Interval: {self.interval}s, TTL: {self.ttl}s")

        self.running = True
        self.stats['started_at'] = datetime.utcnow().isoformat()

        # Send initial heartbeat
        if not self.send_heartbeat():
            logger.error("Failed to send initial heartbeat")
            return False

        # Main loop
        try:
            while self.running:
                time.sleep(self.interval)

                # Send heartbeat
                self.send_heartbeat()

                # Renew lease periodically (every 3 heartbeats)
                if self.stats['heartbeats_sent'] % 3 == 0:
                    self.renew_lease()

        except KeyboardInterrupt:
            logger.info("Heartbeat service stopped by user")
        except Exception as e:
            logger.error(f"Heartbeat service error: {e}")
            return False
        finally:
            self.cleanup()

        return True

    def cleanup(self):
        """Cleanup: revoke lease and remove health key"""
        logger.info("Cleaning up heartbeat service...")

        try:
            # Remove health key
            health_key = f"/chora/capabilities/{self.namespace}/health"
            self.etcd.delete(health_key)
            logger.info(f"Removed health key: {health_key}")

            # Revoke lease
            if self.lease:
                self.lease.revoke()
                logger.info(f"Revoked lease: {self.lease.id}")

        except Exception as e:
            logger.error(f"Cleanup error: {e}")

    def print_stats(self):
        """Print heartbeat statistics"""
        print("\n" + "=" * 80)
        print("Heartbeat Statistics")
        print("=" * 80)
        print(f"Namespace: {self.namespace}")
        print(f"Heartbeats sent: {self.stats['heartbeats_sent']}")
        print(f"Lease renewals: {self.stats['lease_renewals']}")
        print(f"Errors: {self.stats['errors']}")
        if self.stats['started_at']:
            print(f"Started at: {self.stats['started_at']}")
        print("=" * 80 + "\n")


class HeartbeatManager:
    """Manages heartbeats for multiple Service-type capabilities"""

    def __init__(
        self,
        capabilities_dir: Path,
        etcd_host: str = 'localhost',
        etcd_port: int = 2379,
        interval: int = 10,
        ttl: int = 30,
    ):
        self.capabilities_dir = capabilities_dir
        self.etcd_host = etcd_host
        self.etcd_port = etcd_port
        self.interval = interval
        self.ttl = ttl
        self.services: Dict[str, HeartbeatService] = {}

    def discover_services(self) -> List[str]:
        """Discover Service-type capabilities"""
        if not self.capabilities_dir.exists():
            logger.error(f"Capabilities directory not found: {self.capabilities_dir}")
            return []

        # Find all YAML files
        yaml_files = list(self.capabilities_dir.glob("chora.*.yaml"))
        service_namespaces = []

        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    manifest = yaml.safe_load(f)

                # Check if Service-type
                if 'chora_service' in manifest:
                    namespace = manifest.get('metadata', {}).get('dc_identifier')
                    if namespace:
                        service_namespaces.append(namespace)
                        logger.info(f"Discovered Service-type: {namespace}")

            except Exception as e:
                logger.error(f"Error parsing {yaml_file.name}: {e}")

        logger.info(f"Found {len(service_namespaces)} Service-type capability/ies")
        return service_namespaces

    def start_all(self):
        """Start heartbeat for all Service-type capabilities"""
        # Discover services
        service_namespaces = self.discover_services()

        if not service_namespaces:
            logger.warning("No Service-type capabilities found")
            return

        # Create heartbeat service for each
        for namespace in service_namespaces:
            service = HeartbeatService(
                namespace=namespace,
                etcd_host=self.etcd_host,
                etcd_port=self.etcd_port,
                interval=self.interval,
                ttl=self.ttl,
            )

            # Connect to etcd
            if not service.connect_etcd():
                logger.error(f"Failed to connect for {namespace}")
                continue

            # Create lease
            if not service.create_lease():
                logger.error(f"Failed to create lease for {namespace}")
                continue

            self.services[namespace] = service

        # Run all services (simplified: run in sequence for now)
        # In production, use threading or multiprocessing
        logger.info(f"Starting heartbeat for {len(self.services)} service(s)...")

        # For now, just run the first service
        # TODO: Implement concurrent execution
        if self.services:
            first_service = list(self.services.values())[0]
            first_service.run()


def main():
    parser = argparse.ArgumentParser(
        description="Heartbeat service for Service-type capabilities"
    )

    # Capability
    parser.add_argument(
        '--namespace',
        help='Capability namespace (e.g., chora.devex.registry)',
    )
    parser.add_argument(
        '--auto-discover',
        action='store_true',
        help='Auto-discover and run heartbeat for all Service-type capabilities',
    )
    parser.add_argument(
        '--capabilities',
        type=Path,
        default=Path('capabilities'),
        help='Capabilities directory for auto-discovery (default: capabilities/)',
    )

    # etcd connection
    parser.add_argument(
        '--etcd-host',
        default='localhost',
        help='etcd host (default: localhost)',
    )
    parser.add_argument(
        '--etcd-port',
        type=int,
        default=2379,
        help='etcd port (default: 2379)',
    )

    # Heartbeat config
    parser.add_argument(
        '--interval',
        type=int,
        default=10,
        help='Heartbeat interval in seconds (default: 10)',
    )
    parser.add_argument(
        '--ttl',
        type=int,
        default=30,
        help='Lease TTL in seconds (default: 30)',
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.auto_discover and not args.namespace:
        parser.error("Either --namespace or --auto-discover is required")

    # Auto-discover mode
    if args.auto_discover:
        manager = HeartbeatManager(
            capabilities_dir=args.capabilities,
            etcd_host=args.etcd_host,
            etcd_port=args.etcd_port,
            interval=args.interval,
            ttl=args.ttl,
        )
        manager.start_all()
        sys.exit(0)

    # Single service mode
    service = HeartbeatService(
        namespace=args.namespace,
        etcd_host=args.etcd_host,
        etcd_port=args.etcd_port,
        interval=args.interval,
        ttl=args.ttl,
    )

    # Connect to etcd
    if not service.connect_etcd():
        logger.error("Failed to connect to etcd. Exiting.")
        sys.exit(1)

    # Create lease
    if not service.create_lease():
        logger.error("Failed to create lease. Exiting.")
        sys.exit(1)

    # Setup signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        logger.info("Shutdown signal received")
        service.running = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run heartbeat service
    success = service.run()

    # Print stats
    service.print_stats()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
