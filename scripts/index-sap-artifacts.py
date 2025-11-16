#!/usr/bin/env python3
"""
SAP Artifact Indexing Service

Extracts and indexes the 5 required SAP artifacts for each capability:
1. capability-charter.md
2. protocol-spec.md
3. awareness-guide.md (or AGENTS.md)
4. adoption-blueprint.md
5. ledger.md

Stores artifact content in etcd for full-text search and retrieval.

Schema in etcd:
  /chora/artifacts/{namespace}/{artifact_type}/content    - Full markdown content
  /chora/artifacts/{namespace}/{artifact_type}/metadata   - Metadata (size, hash, etc.)

Usage:
    # Index all artifacts
    python scripts/index-sap-artifacts.py --capabilities capabilities/

    # Index specific capability
    python scripts/index-sap-artifacts.py --namespace chora.devex.registry

    # Dry-run
    python scripts/index-sap-artifacts.py --capabilities capabilities/ --dry-run
"""

import argparse
import hashlib
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

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
logger = logging.getLogger('artifact-indexer')

# Required SAP artifacts
REQUIRED_ARTIFACTS = [
    'capability-charter',
    'protocol-spec',
    'awareness-guide',  # or AGENTS.md
    'adoption-blueprint',
    'ledger',
]


class ArtifactIndexer:
    """Indexes SAP artifacts for search and retrieval"""

    def __init__(
        self,
        capabilities_dir: Path,
        docs_dir: Path,
        etcd_host: str = 'localhost',
        etcd_port: int = 2379,
        dry_run: bool = False,
    ):
        self.capabilities_dir = capabilities_dir
        self.docs_dir = docs_dir
        self.etcd_host = etcd_host
        self.etcd_port = etcd_port
        self.dry_run = dry_run
        self.etcd = None
        self.stats = {
            'total_capabilities': 0,
            'total_artifacts': 0,
            'indexed_artifacts': 0,
            'missing_artifacts': 0,
            'errors': 0,
        }

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

    def find_artifact(self, capability_name: str, artifact_type: str) -> Optional[Path]:
        """Find artifact file for a capability"""
        # SAP directory path
        sap_dir = self.docs_dir / 'skilled-awareness' / capability_name

        if not sap_dir.exists():
            return None

        # Try standard filename
        artifact_file = sap_dir / f"{artifact_type}.md"
        if artifact_file.exists():
            return artifact_file

        # Special case: awareness-guide can be AGENTS.md
        if artifact_type == 'awareness-guide':
            agents_file = sap_dir / 'AGENTS.md'
            if agents_file.exists():
                return agents_file

        # Special case: protocol-spec can be in subdirectory
        if artifact_type == 'protocol-spec':
            protocol_file = sap_dir / 'protocol' / f"{artifact_type}.md"
            if protocol_file.exists():
                return protocol_file

        return None

    def extract_artifact(self, artifact_path: Path) -> Tuple[str, Dict]:
        """Extract artifact content and metadata"""
        try:
            # Read content
            with open(artifact_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Calculate hash
            content_hash = hashlib.sha256(content.encode()).hexdigest()

            # Build metadata
            metadata = {
                'file_path': str(artifact_path),
                'file_size': len(content),
                'content_hash': content_hash,
                'last_modified': datetime.fromtimestamp(artifact_path.stat().st_mtime).isoformat(),
                'indexed_at': datetime.utcnow().isoformat() + 'Z',
            }

            return content, metadata

        except Exception as e:
            logger.error(f"Failed to extract {artifact_path}: {e}")
            return None, None

    def index_artifact(
        self,
        namespace: str,
        artifact_type: str,
        content: str,
        metadata: Dict
    ) -> bool:
        """Index artifact in etcd"""
        try:
            if self.dry_run:
                logger.info(f"[DRY-RUN] Would index: {namespace}/{artifact_type}")
                return True

            # Store content
            content_key = f"/chora/artifacts/{namespace}/{artifact_type}/content"
            self.etcd.put(content_key, content)

            # Store metadata
            metadata_key = f"/chora/artifacts/{namespace}/{artifact_type}/metadata"
            self.etcd.put(metadata_key, json.dumps(metadata))

            logger.info(f"Indexed: {namespace}/{artifact_type} ({metadata['file_size']} bytes)")
            return True

        except Exception as e:
            logger.error(f"Failed to index {namespace}/{artifact_type}: {e}")
            return False

    def index_capability(self, namespace: str) -> Tuple[int, int]:
        """
        Index all artifacts for a capability

        Returns:
            Tuple of (indexed_count, missing_count)
        """
        # Extract capability name from namespace (e.g., chora.devex.registry -> registry)
        capability_name = namespace.split('.')[-1].replace('_', '-')

        indexed = 0
        missing = 0

        for artifact_type in REQUIRED_ARTIFACTS:
            # Find artifact
            artifact_path = self.find_artifact(capability_name, artifact_type)

            if not artifact_path:
                logger.warning(f"Missing artifact: {namespace}/{artifact_type}")
                missing += 1
                self.stats['missing_artifacts'] += 1
                continue

            # Extract artifact
            content, metadata = self.extract_artifact(artifact_path)

            if not content:
                logger.error(f"Failed to extract: {namespace}/{artifact_type}")
                self.stats['errors'] += 1
                continue

            # Index artifact
            if self.index_artifact(namespace, artifact_type, content, metadata):
                indexed += 1
                self.stats['indexed_artifacts'] += 1
            else:
                self.stats['errors'] += 1

        return indexed, missing

    def discover_capabilities(self) -> List[str]:
        """Discover all capabilities from YAML manifests"""
        if not self.capabilities_dir.exists():
            logger.error(f"Capabilities directory not found: {self.capabilities_dir}")
            return []

        # Find all YAML files
        yaml_files = list(self.capabilities_dir.glob("chora.*.yaml"))
        namespaces = []

        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    manifest = yaml.safe_load(f)

                namespace = manifest.get('metadata', {}).get('dc_identifier')
                if namespace:
                    namespaces.append(namespace)

            except Exception as e:
                logger.error(f"Error parsing {yaml_file.name}: {e}")

        logger.info(f"Discovered {len(namespaces)} capability/ies")
        return namespaces

    def index_all(self) -> bool:
        """Index all SAP artifacts"""
        # Discover capabilities
        namespaces = self.discover_capabilities()

        if not namespaces:
            logger.warning("No capabilities found")
            return False

        self.stats['total_capabilities'] = len(namespaces)
        self.stats['total_artifacts'] = len(namespaces) * len(REQUIRED_ARTIFACTS)

        logger.info(f"Indexing artifacts for {len(namespaces)} capability/ies...")

        # Index each capability
        for namespace in sorted(namespaces):
            indexed, missing = self.index_capability(namespace)

            if indexed > 0:
                logger.info(f"  {namespace}: {indexed} indexed, {missing} missing")

        # Print summary
        logger.info(
            f"Indexing complete: {self.stats['indexed_artifacts']} indexed, "
            f"{self.stats['missing_artifacts']} missing, "
            f"{self.stats['errors']} errors"
        )

        return self.stats['errors'] == 0

    def search_artifacts(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search artifacts by keyword (simple implementation)

        Returns list of matching artifacts with metadata
        """
        if self.dry_run:
            logger.info(f"[DRY-RUN] Would search for: {query}")
            return []

        try:
            results = []
            prefix = "/chora/artifacts/"

            # Get all artifact content keys
            for key, value in self.etcd.get_prefix(prefix):
                key_str = key.decode('utf-8')

                # Only search content, not metadata
                if not key_str.endswith('/content'):
                    continue

                # Simple keyword search (case-insensitive)
                content = value.decode('utf-8')
                if query.lower() in content.lower():
                    # Extract namespace and artifact type from key
                    parts = key_str.split('/')
                    if len(parts) >= 5:
                        namespace = parts[3]
                        artifact_type = parts[4]

                        results.append({
                            'namespace': namespace,
                            'artifact_type': artifact_type,
                            'preview': content[:200] + '...',
                        })

                        if len(results) >= limit:
                            break

            return results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def print_stats(self):
        """Print indexing statistics"""
        print("\n" + "=" * 80)
        print("Artifact Indexing Statistics")
        print("=" * 80)
        print(f"Total capabilities: {self.stats['total_capabilities']}")
        print(f"Total artifacts expected: {self.stats['total_artifacts']}")
        print(f"Indexed: {self.stats['indexed_artifacts']}")
        print(f"Missing: {self.stats['missing_artifacts']}")
        print(f"Errors: {self.stats['errors']}")

        if self.stats['total_artifacts'] > 0:
            completion = (self.stats['indexed_artifacts'] / self.stats['total_artifacts']) * 100
            print(f"Completion: {completion:.1f}%")

        print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Index SAP artifacts for search and retrieval"
    )

    # Input
    parser.add_argument(
        '--capabilities',
        type=Path,
        default=Path('capabilities'),
        help='Capabilities directory (default: capabilities/)',
    )
    parser.add_argument(
        '--docs',
        type=Path,
        default=Path('docs'),
        help='Documentation directory (default: docs/)',
    )
    parser.add_argument(
        '--namespace',
        help='Index specific capability namespace',
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

    # Options
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Dry-run mode (no etcd writes)',
    )

    # Search
    parser.add_argument(
        '--search',
        help='Search artifacts by keyword',
    )

    args = parser.parse_args()

    # Initialize indexer
    indexer = ArtifactIndexer(
        capabilities_dir=args.capabilities,
        docs_dir=args.docs,
        etcd_host=args.etcd_host,
        etcd_port=args.etcd_port,
        dry_run=args.dry_run,
    )

    # Connect to etcd
    if not indexer.connect_etcd():
        logger.error("Failed to connect to etcd. Exiting.")
        sys.exit(1)

    # Search mode
    if args.search:
        results = indexer.search_artifacts(args.search)
        print(f"\nFound {len(results)} matching artifact(s):\n")
        for result in results:
            print(f"  {result['namespace']}/{result['artifact_type']}")
            print(f"    {result['preview']}\n")
        sys.exit(0)

    # Index mode
    if args.namespace:
        # Index specific capability
        indexed, missing = indexer.index_capability(args.namespace)
        print(f"\n{args.namespace}: {indexed} indexed, {missing} missing\n")
        sys.exit(0)

    # Index all
    success = indexer.index_all()
    indexer.print_stats()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
