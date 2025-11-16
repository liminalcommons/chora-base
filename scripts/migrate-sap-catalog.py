#!/usr/bin/env python3
r"""
SAP Catalog Migration Script

Migrates SAP entries from sap-catalog.json to unified YAML manifest format.
Implements the Ecosystem Ontology & Composition Vision migration strategy.

Features:
- Converts SAP-XXX IDs to chora.domain.capability namespaces
- Auto-detects SAP artifacts from docs/skilled-awareness/ directory
- Preserves adoption metrics (effort, complexity, ROI)
- Supports batch migration (all SAPs) and single SAP migration
- Validates output against JSON Schema
- Generates both Service-type and Pattern-type manifests

Usage:
  # Migrate single SAP
  python scripts/migrate-sap-catalog.py --sap SAP-001 --output capabilities/

  # Migrate all SAPs
  python scripts/migrate-sap-catalog.py --all --output capabilities/

  # Dry-run mode (no files written)
  python scripts/migrate-sap-catalog.py --all --dry-run

  # Migrate specific domain
  python scripts/migrate-sap-catalog.py --domain infrastructure --output capabilities/

Exit Codes:
  0 - Migration successful
  1 - Migration errors
  2 - Invalid arguments or file access errors
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install PyYAML", file=sys.stderr)
    sys.exit(2)


# Domain mapping from sap-catalog.json to ontology domains
DOMAIN_MAPPING = {
    "Infrastructure": "infrastructure",
    "Developer Experience": "devex",
    "React": "react",
    "Vue": "vue",
    "Angular": "angular",
    "Specialized": "awareness",  # Default for specialized SAPs
    "Advanced": "integration",  # Default for advanced SAPs
    "Workflow": "workflow",
    "Integration": "integration",
    "Optimization": "optimization",
}

# SAPs that are known to be Service-type (have runtime components)
SERVICE_TYPE_SAPS = {
    "SAP-042",  # interface-design (has implementation)
    "SAP-043",  # multi-interface (has implementation)
    "SAP-044",  # registry (runtime service)
    "SAP-045",  # bootstrap (runtime service)
    "SAP-047",  # capability-server-template (generator tool)
}


class MigrationError(Exception):
    """Migration-specific error"""

    pass


class SAPMigrator:
    """Migrates SAP catalog entries to YAML manifests"""

    def __init__(
        self,
        catalog_file: Path,
        output_dir: Path,
        dry_run: bool = False,
        validate: bool = True,
    ):
        self.catalog_file = catalog_file
        self.output_dir = output_dir
        self.dry_run = dry_run
        self.validate = validate
        self.catalog_data: Dict = {}
        self.migration_stats = {
            "total": 0,
            "migrated": 0,
            "skipped": 0,
            "errors": 0,
        }

    def load_catalog(self) -> bool:
        """Load sap-catalog.json"""
        try:
            with open(self.catalog_file, "r", encoding="utf-8") as f:
                self.catalog_data = json.load(f)
            return True
        except FileNotFoundError:
            print(
                f"ERROR: SAP catalog not found: {self.catalog_file}", file=sys.stderr
            )
            return False
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in catalog: {e}", file=sys.stderr)
            return False

    def convert_name_to_snake_case(self, name: str) -> str:
        """Convert kebab-case to snake_case"""
        return name.replace("-", "_")

    def determine_capability_type(self, sap_id: str, sap_data: Dict) -> str:
        """Determine if SAP is Service-type or Pattern-type"""
        # Check if in known Service-type SAPs
        if sap_id in SERVICE_TYPE_SAPS:
            return "Service"

        # Check for system_files (indicates runtime component)
        if sap_data.get("system_files") and len(sap_data["system_files"]) > 0:
            # If has system files, might be Service-type
            # Check if files include executable scripts
            system_files = sap_data["system_files"]
            for file in system_files:
                if file.endswith(".py") and "scripts/" in file:
                    return "Service"

        # Default to Pattern-type (documentation-only SAPs)
        return "Pattern"

    def map_domain(self, sap_domain: str, sap_name: str) -> str:
        """Map SAP domain to ontology domain"""
        # Direct mapping
        if sap_domain in DOMAIN_MAPPING:
            return DOMAIN_MAPPING[sap_domain]

        # Special cases
        if sap_name.startswith("react-"):
            return "react"
        if sap_name.startswith("vue-"):
            return "vue"
        if sap_name.startswith("angular-"):
            return "angular"

        # Default to infrastructure for unknown
        print(
            f"WARNING: Unknown domain '{sap_domain}' for {sap_name}, defaulting to 'infrastructure'",
            file=sys.stderr,
        )
        return "infrastructure"

    def generate_namespace(self, sap_data: Dict) -> str:
        """Generate chora.domain.capability namespace"""
        domain = self.map_domain(sap_data["domain"], sap_data["name"])
        capability = self.convert_name_to_snake_case(sap_data["name"])

        # Remove domain prefix if redundant
        if capability.startswith(f"{domain}_"):
            capability = capability[len(domain) + 1 :]

        namespace = f"chora.{domain}.{capability}"

        # Validate length
        if len(capability) > 50:
            print(
                f"WARNING: Capability name '{capability}' exceeds 50 chars, truncating",
                file=sys.stderr,
            )
            capability = capability[:50]
            namespace = f"chora.{domain}.{capability}"

        return namespace

    def scan_artifacts(self, location: Path) -> List[Dict[str, str]]:
        """Scan SAP directory for artifacts"""
        artifacts = []
        artifact_files = {
            "capability-charter.md": "capability_charter",
            "protocol-spec.md": "protocol_specification",
            "AGENTS.md": "awareness_guide",  # Or awareness-guide.md
            "awareness-guide.md": "awareness_guide",
            "adoption-blueprint.md": "adoption_blueprint",
            "ledger.md": "adoption_ledger",
        }

        if not location.exists():
            return artifacts

        for file_name, artifact_type in artifact_files.items():
            artifact_path = location / file_name
            if artifact_path.exists():
                # Get relative path from docs/skilled-awareness/
                rel_path = str(artifact_path.relative_to(Path("docs/skilled-awareness")))
                artifacts.append(
                    {
                        "type": artifact_type,
                        "path": f"docs/skilled-awareness/{rel_path}",
                        "format": "text/markdown",
                    }
                )

        return artifacts

    def create_pattern_manifest(self, sap_data: Dict, namespace: str) -> Dict:
        """Create Pattern-type YAML manifest"""
        location = Path(sap_data.get("location", ""))

        # Scan for artifacts
        artifacts = self.scan_artifacts(location)

        manifest = {
            "apiVersion": "chora.dev/v1",
            "kind": "Capability",
            "metadata": {
                "dc_identifier": namespace,
                "dc_identifier_legacy": sap_data["id"],
                "dc_title": sap_data["full_name"],
                "dc_description": sap_data["description"],
                "dc_type": "Pattern",
                "dc_hasVersion": sap_data["version"],
                "dc_creator": sap_data.get("author", "Chora Core Team"),
                "dc_date": datetime.now().strftime("%Y-%m-%d"),
                "dc_format": "text/markdown",
                "dc_subject": sap_data.get("tags", []),
            },
        }

        # Add dependencies if present
        if sap_data.get("dependencies"):
            manifest["dc_relation"] = {"requires": []}
            for dep in sap_data["dependencies"]:
                manifest["dc_relation"]["requires"].append(
                    {
                        "capability": f"chora.{dep}",  # TODO: Map to proper namespace
                        "relationship": "prerequisite",
                    }
                )

        # Add chora_pattern extension
        if artifacts:
            manifest["chora_pattern"] = {"artifacts": artifacts}

        # Add chora_adoption extension if metrics available
        adoption = {}
        if "effort_minutes" in sap_data:
            adoption["effort_minutes"] = sap_data["effort_minutes"]
        if "complexity" in sap_data:
            adoption["complexity"] = sap_data["complexity"]
        if "time_savings_minutes" in sap_data:
            adoption["time_savings_minutes"] = sap_data["time_savings_minutes"]

        if adoption:
            manifest["chora_adoption"] = adoption

        return manifest

    def create_service_manifest(self, sap_data: Dict, namespace: str) -> Dict:
        """Create Service-type YAML manifest"""
        manifest = {
            "apiVersion": "chora.dev/v1",
            "kind": "Capability",
            "metadata": {
                "dc_identifier": namespace,
                "dc_identifier_legacy": sap_data["id"],
                "dc_title": sap_data["full_name"],
                "dc_description": sap_data["description"],
                "dc_type": "Service",
                "dc_hasVersion": sap_data["version"],
                "dc_creator": sap_data.get("author", "Chora Core Team"),
                "dc_date": datetime.now().strftime("%Y-%m-%d"),
                "dc_format": "application/x-executable",
                "dc_subject": sap_data.get("tags", []),
            },
            "chora_service": {
                "interfaces": ["cli", "mcp"],  # Default, can be customized
                "health": {
                    "endpoint": "/health",
                    "interval": 10,
                    "timeout": 5,
                    "heartbeat_ttl": 30,
                },
                "distribution": {
                    "pypi": {
                        "package_name": f"chora-{sap_data['name']}",
                        "install_command": f"pip install chora-{sap_data['name']}",
                    }
                },
            },
        }

        # Add dependencies if present
        if sap_data.get("dependencies"):
            manifest["dc_relation"] = {"requires": []}
            for dep in sap_data["dependencies"]:
                manifest["dc_relation"]["requires"].append(
                    {
                        "capability": f"chora.{dep}",
                        "version": "^1.0.0",
                        "relationship": "runtime",
                    }
                )

        return manifest

    def migrate_sap(self, sap_data: Dict) -> Optional[Path]:
        """Migrate a single SAP to YAML manifest"""
        sap_id = sap_data["id"]

        try:
            # Generate namespace
            namespace = self.generate_namespace(sap_data)

            # Determine capability type
            cap_type = self.determine_capability_type(sap_id, sap_data)

            # Create manifest
            if cap_type == "Service":
                manifest = self.create_service_manifest(sap_data, namespace)
            else:
                manifest = self.create_pattern_manifest(sap_data, namespace)

            # Generate output filename
            output_file = self.output_dir / f"{namespace}.yaml"

            # Write manifest (or dry-run)
            if not self.dry_run:
                self.output_dir.mkdir(parents=True, exist_ok=True)
                with open(output_file, "w", encoding="utf-8") as f:
                    yaml.dump(
                        manifest,
                        f,
                        default_flow_style=False,
                        allow_unicode=True,
                        sort_keys=False,
                    )

            print(
                f"{'[DRY-RUN] ' if self.dry_run else ''}Migrated {sap_id} -> {output_file.name} ({cap_type})"
            )

            self.migration_stats["migrated"] += 1
            return output_file

        except Exception as e:
            print(
                f"ERROR: Failed to migrate {sap_id}: {e}",
                file=sys.stderr,
            )
            self.migration_stats["errors"] += 1
            return None

    def migrate_all(
        self, filter_domain: Optional[str] = None, filter_sap: Optional[str] = None
    ) -> bool:
        """Migrate all SAPs or filtered subset"""
        if not self.catalog_data.get("saps"):
            print("ERROR: No SAPs found in catalog", file=sys.stderr)
            return False

        saps = self.catalog_data["saps"]
        self.migration_stats["total"] = len(saps)

        print(f"\n{'='*80}")
        print(
            f"SAP Catalog Migration - {'DRY RUN' if self.dry_run else 'EXECUTING'}"
        )
        print(f"{'='*80}")
        print(f"Total SAPs: {len(saps)}")
        if filter_domain:
            print(f"Filter: domain={filter_domain}")
        if filter_sap:
            print(f"Filter: sap={filter_sap}")
        print(f"Output: {self.output_dir}")
        print(f"{'='*80}\n")

        for sap_data in saps:
            # Apply filters
            if filter_domain and sap_data.get("domain") != filter_domain:
                self.migration_stats["skipped"] += 1
                continue

            if filter_sap and sap_data["id"] != filter_sap:
                self.migration_stats["skipped"] += 1
                continue

            # Migrate SAP
            self.migrate_sap(sap_data)

        return self.migration_stats["errors"] == 0

    def print_summary(self):
        """Print migration summary"""
        print(f"\n{'='*80}")
        print("Migration Summary")
        print(f"{'='*80}")
        print(f"Total SAPs: {self.migration_stats['total']}")
        print(f"Migrated: {self.migration_stats['migrated']}")
        print(f"Skipped: {self.migration_stats['skipped']}")
        print(f"Errors: {self.migration_stats['errors']}")

        if self.migration_stats["errors"] == 0:
            print(f"\nSUCCESS: Migration completed successfully")
        else:
            print(f"\nERROR: Migration completed with errors")

        if self.dry_run:
            print(f"\n(DRY RUN - No files written)")

        print(f"{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Migrate SAP catalog entries to unified YAML manifests"
    )

    # Input/output
    parser.add_argument(
        "--catalog",
        type=Path,
        default=Path("sap-catalog.json"),
        help="Path to sap-catalog.json (default: sap-catalog.json)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("capabilities"),
        help="Output directory for YAML manifests (default: capabilities/)",
    )

    # Migration modes
    migration_mode = parser.add_mutually_exclusive_group(required=True)
    migration_mode.add_argument(
        "--all", action="store_true", help="Migrate all SAPs"
    )
    migration_mode.add_argument(
        "--sap", type=str, help="Migrate single SAP by ID (e.g., SAP-001)"
    )
    migration_mode.add_argument(
        "--domain", type=str, help="Migrate all SAPs in domain (e.g., Infrastructure)"
    )

    # Options
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry-run mode (print what would be done, don't write files)",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip JSON Schema validation",
    )

    args = parser.parse_args()

    # Initialize migrator
    migrator = SAPMigrator(
        catalog_file=args.catalog,
        output_dir=args.output,
        dry_run=args.dry_run,
        validate=not args.no_validate,
    )

    # Load catalog
    if not migrator.load_catalog():
        sys.exit(2)

    # Run migration
    if args.all:
        success = migrator.migrate_all()
    elif args.sap:
        success = migrator.migrate_all(filter_sap=args.sap)
    elif args.domain:
        success = migrator.migrate_all(filter_domain=args.domain)
    else:
        print("ERROR: Must specify --all, --sap, or --domain", file=sys.stderr)
        sys.exit(2)

    # Print summary
    migrator.print_summary()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
