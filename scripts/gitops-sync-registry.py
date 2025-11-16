#!/usr/bin/env python3
"""
GitOps Registry Sync Service

Watches capabilities/ directory and syncs YAML manifests to etcd registry.
Runs on configurable interval (default: 60 seconds).

Features:
- Watches capabilities/ directory for changes
- Parses and validates YAML manifests
- Syncs to etcd with proper schema
- Handles both Service-type and Pattern-type capabilities
- Dry-run mode for testing
- Comprehensive error handling and logging

Schema in etcd:
  /chora/capabilities/{namespace}/metadata    - JSON: full metadata
  /chora/capabilities/{namespace}/type        - "service" or "pattern"
  /chora/capabilities/{namespace}/version     - SemVer string
  /chora/capabilities/{namespace}/dependencies - JSON array

Usage:
    # Sync once
    python scripts/gitops-sync-registry.py --capabilities capabilities/

    # Watch mode (continuous sync every 60s)
    python scripts/gitops-sync-registry.py --capabilities capabilities/ --watch

    # Custom interval
    python scripts/gitops-sync-registry.py --capabilities capabilities/ --watch --interval 30

    # Dry-run (no etcd writes)
    python scripts/gitops-sync-registry.py --capabilities capabilities/ --dry-run
"""

import argparse
import hashlib
import json
import logging
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
logger = logging.getLogger('gitops-sync')


class GitOpsSync:
    """GitOps sync service for capability registry"""

    def __init__(
        self,
        capabilities_dir: Path,
        etcd_host: str = 'localhost',
        etcd_port: int = 2379,
        dry_run: bool = False,
    ):
        self.capabilities_dir = capabilities_dir
        self.etcd_host = etcd_host
        self.etcd_port = etcd_port
        self.dry_run = dry_run
        self.etcd = None
        self.stats = {
            'total_files': 0,
            'synced': 0,
            'skipped': 0,
            'errors': 0,
            'last_sync': None,
        }
        self.file_hashes: Dict[str, str] = {}  # Track file changes

    def connect_etcd(self) -> bool:
        """Connect to etcd cluster"""
        if self.dry_run:
            logger.info("DRY-RUN mode: skipping etcd connection")
            return True

        try:
            self.etcd = etcd3.client(host=self.etcd_host, port=self.etcd_port)
            # Test connection
            self.etcd.status()
            logger.info(f"Connected to etcd at {self.etcd_host}:{self.etcd_port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to etcd: {e}")
            return False

    def get_file_hash(self, file_path: Path) -> str:
        """Calculate file hash to detect changes"""
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def parse_manifest(self, file_path: Path) -> Optional[Dict]:
        """Parse YAML manifest and extract metadata"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                manifest = yaml.safe_load(f)

            if not manifest or 'metadata' not in manifest:
                logger.warning(f"Invalid manifest (missing metadata): {file_path.name}")
                return None

            metadata = manifest.get('metadata', {})
            namespace = metadata.get('dc_identifier')

            if not namespace:
                logger.warning(f"Missing dc_identifier: {file_path.name}")
                return None

            # Determine capability type
            if 'chora_service' in manifest:
                cap_type = 'service'
            elif 'chora_pattern' in manifest:
                cap_type = 'pattern'
            else:
                logger.warning(f"Unknown capability type: {file_path.name}")
                return None

            # Extract dependencies
            dc_relation = manifest.get('dc_relation', {})
            requires = dc_relation.get('requires', [])

            dependencies = []
            for dep in requires:
                if isinstance(dep, dict):
                    dependencies.append({
                        'capability': dep.get('capability'),
                        'relationship': dep.get('relationship', 'prerequisite'),
                        'version': dep.get('version', '*'),
                    })
                elif isinstance(dep, str):
                    dependencies.append({
                        'capability': dep,
                        'relationship': 'prerequisite',
                        'version': '*',
                    })

            # Build capability data
            capability = {
                'namespace': namespace,
                'type': cap_type,
                'version': metadata.get('dc_date', '1.0.0'),  # Using dc_date as version proxy
                'title': metadata.get('dc_title', ''),
                'description': metadata.get('dc_description', ''),
                'creator': metadata.get('dc_creator', 'chora-base'),
                'dependencies': dependencies,
                'metadata': metadata,  # Full metadata for reference
            }

            return capability

        except yaml.YAMLError as e:
            logger.error(f"Failed to parse {file_path.name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {e}")
            return None

    def sync_to_etcd(self, capability: Dict) -> bool:
        """Sync capability to etcd"""
        namespace = capability['namespace']
        base_key = f"/chora/capabilities/{namespace}"

        try:
            if self.dry_run:
                logger.info(f"[DRY-RUN] Would sync: {namespace}")
                return True

            # Write metadata (full capability data as JSON)
            metadata_key = f"{base_key}/metadata"
            self.etcd.put(metadata_key, json.dumps(capability['metadata']))

            # Write type
            type_key = f"{base_key}/type"
            self.etcd.put(type_key, capability['type'])

            # Write version
            version_key = f"{base_key}/version"
            self.etcd.put(version_key, capability['version'])

            # Write dependencies
            deps_key = f"{base_key}/dependencies"
            self.etcd.put(deps_key, json.dumps(capability['dependencies']))

            logger.info(f"Synced: {namespace} ({capability['type']})")
            return True

        except Exception as e:
            logger.error(f"Failed to sync {namespace} to etcd: {e}")
            return False

    def sync_file(self, file_path: Path) -> bool:
        """Sync a single capability file to etcd"""
        # Check if file changed
        current_hash = self.get_file_hash(file_path)
        previous_hash = self.file_hashes.get(str(file_path))

        if previous_hash == current_hash:
            logger.debug(f"Skipped (unchanged): {file_path.name}")
            self.stats['skipped'] += 1
            return True

        # Parse manifest
        capability = self.parse_manifest(file_path)
        if not capability:
            self.stats['errors'] += 1
            return False

        # Sync to etcd
        success = self.sync_to_etcd(capability)

        if success:
            self.file_hashes[str(file_path)] = current_hash
            self.stats['synced'] += 1
        else:
            self.stats['errors'] += 1

        return success

    def sync_all(self) -> bool:
        """Sync all capability manifests to etcd"""
        if not self.capabilities_dir.exists():
            logger.error(f"Capabilities directory not found: {self.capabilities_dir}")
            return False

        # Find all YAML files
        yaml_files = list(self.capabilities_dir.glob("chora.*.yaml"))

        if not yaml_files:
            logger.warning(f"No capability manifests found in {self.capabilities_dir}")
            return False

        logger.info(f"Found {len(yaml_files)} capability manifest(s)")

        # Reset stats for this sync
        self.stats['total_files'] = len(yaml_files)
        self.stats['synced'] = 0
        self.stats['skipped'] = 0
        self.stats['errors'] = 0

        # Sync each file
        for yaml_file in sorted(yaml_files):
            self.sync_file(yaml_file)

        # Update last sync time
        self.stats['last_sync'] = datetime.utcnow().isoformat()

        # Print summary
        logger.info(
            f"Sync complete: {self.stats['synced']} synced, "
            f"{self.stats['skipped']} skipped, "
            f"{self.stats['errors']} errors"
        )

        return self.stats['errors'] == 0

    def watch(self, interval: int = 60):
        """Watch mode: sync on interval"""
        logger.info(f"Starting watch mode (interval: {interval}s)")
        logger.info(f"Watching: {self.capabilities_dir}")
        logger.info(f"Press Ctrl+C to stop")

        try:
            while True:
                logger.info("--- Sync cycle starting ---")
                self.sync_all()
                logger.info(f"--- Sync cycle complete. Next sync in {interval}s ---")
                time.sleep(interval)

        except KeyboardInterrupt:
            logger.info("Watch mode stopped by user")

    def list_capabilities(self) -> List[str]:
        """List all capabilities in etcd"""
        if self.dry_run:
            logger.info("[DRY-RUN] Would list capabilities from etcd")
            return []

        try:
            prefix = "/chora/capabilities/"
            results = self.etcd.get_prefix(prefix, keys_only=True)

            # Extract unique namespaces
            namespaces = set()
            for key, _ in results:
                key_str = key.decode('utf-8')
                # Extract namespace from key like /chora/capabilities/{namespace}/metadata
                parts = key_str.split('/')
                if len(parts) >= 4:
                    namespaces.add(parts[3])

            return sorted(namespaces)

        except Exception as e:
            logger.error(f"Failed to list capabilities: {e}")
            return []

    def print_stats(self):
        """Print sync statistics"""
        print("\n" + "=" * 80)
        print("GitOps Sync Statistics")
        print("=" * 80)
        print(f"Total files: {self.stats['total_files']}")
        print(f"Synced: {self.stats['synced']}")
        print(f"Skipped (unchanged): {self.stats['skipped']}")
        print(f"Errors: {self.stats['errors']}")
        if self.stats['last_sync']:
            print(f"Last sync: {self.stats['last_sync']}")
        print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="GitOps sync service for capability registry"
    )

    # Input
    parser.add_argument(
        '--capabilities',
        type=Path,
        default=Path('capabilities'),
        help='Capabilities directory to sync (default: capabilities/)',
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

    # Mode
    parser.add_argument(
        '--watch',
        action='store_true',
        help='Watch mode: continuous sync on interval',
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Sync interval in seconds (default: 60)',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Dry-run mode (no etcd writes)',
    )

    # Actions
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all capabilities in etcd',
    )

    args = parser.parse_args()

    # Initialize sync service
    sync = GitOpsSync(
        capabilities_dir=args.capabilities,
        etcd_host=args.etcd_host,
        etcd_port=args.etcd_port,
        dry_run=args.dry_run,
    )

    # Connect to etcd
    if not sync.connect_etcd():
        logger.error("Failed to connect to etcd. Exiting.")
        sys.exit(1)

    # List mode
    if args.list:
        capabilities = sync.list_capabilities()
        print(f"\nFound {len(capabilities)} capability/ies in etcd:\n")
        for cap in capabilities:
            print(f"  - {cap}")
        print()
        sys.exit(0)

    # Watch mode
    if args.watch:
        sync.watch(interval=args.interval)
        sys.exit(0)

    # Single sync
    success = sync.sync_all()
    sync.print_stats()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
