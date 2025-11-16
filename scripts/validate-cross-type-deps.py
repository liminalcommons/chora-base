#!/usr/bin/env python3
r"""
Cross-Type Dependency Validator

Validates dependencies between Service-type and Pattern-type capabilities,
ensuring correct relationship types and preventing circular dependencies.

Features:
- Validates Service -> Pattern dependencies
- Validates Pattern -> Service dependencies
- Checks relationship types (runtime, prerequisite, optional, etc.)
- Detects circular dependencies
- Validates dependency namespaces exist
- Reports missing dependencies
- Generates dependency graph

Usage:
  # Validate all capabilities
  python scripts/validate-cross-type-deps.py --validate-all

  # Validate specific capability
  python scripts/validate-cross-type-deps.py --capability chora.devex.registry

  # Export dependency graph
  python scripts/validate-cross-type-deps.py --export-graph dependencies.json

  # Show statistics
  python scripts/validate-cross-type-deps.py --stats

Exit Codes:
  0 - All dependencies valid
  1 - Dependency validation errors
  2 - Invalid arguments or file access errors
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install PyYAML", file=sys.stderr)
    sys.exit(2)


# Valid relationship types
VALID_RELATIONSHIPS = {
    "runtime",       # Service depends on another Service at runtime
    "prerequisite",  # Pattern requires another Pattern before adoption
    "optional",      # Optional dependency
    "extends",       # Extends another capability
    "replaces",      # Replaces another capability
    "conflicts",     # Conflicts with another capability
}

# Relationship type rules for Service <-> Pattern
SERVICE_TO_PATTERN_ALLOWED = {"prerequisite", "optional", "extends"}
PATTERN_TO_SERVICE_ALLOWED = {"runtime", "optional"}
SERVICE_TO_SERVICE_ALLOWED = {"runtime", "prerequisite", "optional", "extends"}
PATTERN_TO_PATTERN_ALLOWED = {"prerequisite", "optional", "extends"}


class DependencyValidator:
    """Validates cross-type dependencies between capabilities"""

    def __init__(self, capabilities_dir: Path = Path("capabilities")):
        self.capabilities_dir = capabilities_dir
        self.capabilities: Dict[str, Dict] = {}  # namespace -> manifest
        self.dependency_graph: Dict[str, List[Dict]] = defaultdict(list)
        self.reverse_graph: Dict[str, List[str]] = defaultdict(list)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.stats = {
            "total_capabilities": 0,
            "service_type": 0,
            "pattern_type": 0,
            "total_dependencies": 0,
            "service_to_pattern": 0,
            "pattern_to_service": 0,
            "service_to_service": 0,
            "pattern_to_pattern": 0,
            "circular_dependencies": 0,
            "missing_dependencies": 0,
            "invalid_relationships": 0,
        }

    def load_capabilities(self) -> bool:
        """Load all capability manifests"""
        if not self.capabilities_dir.exists():
            print(
                f"ERROR: Capabilities directory not found: {self.capabilities_dir}",
                file=sys.stderr,
            )
            return False

        yaml_files = list(self.capabilities_dir.glob("*.yaml")) + list(
            self.capabilities_dir.glob("*.yml")
        )

        if not yaml_files:
            print(
                f"WARNING: No YAML files found in {self.capabilities_dir}",
                file=sys.stderr,
            )
            return False

        for yaml_file in yaml_files:
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    manifest = yaml.safe_load(f)

                if not manifest or "metadata" not in manifest:
                    print(
                        f"WARNING: Invalid manifest structure in {yaml_file.name}",
                        file=sys.stderr,
                    )
                    continue

                metadata = manifest["metadata"]
                namespace = metadata.get("dc_identifier")
                cap_type = metadata.get("dc_type")

                if not namespace:
                    print(
                        f"WARNING: Missing dc_identifier in {yaml_file.name}",
                        file=sys.stderr,
                    )
                    continue

                self.capabilities[namespace] = manifest

                # Update stats
                self.stats["total_capabilities"] += 1
                if cap_type == "Service":
                    self.stats["service_type"] += 1
                elif cap_type == "Pattern":
                    self.stats["pattern_type"] += 1

            except yaml.YAMLError as e:
                print(
                    f"ERROR: Failed to parse {yaml_file.name}: {e}", file=sys.stderr
                )
                continue
            except Exception as e:
                print(
                    f"ERROR: Failed to load {yaml_file.name}: {e}", file=sys.stderr
                )
                continue

        print(
            f"Loaded {self.stats['total_capabilities']} capabilities "
            f"({self.stats['service_type']} Service, {self.stats['pattern_type']} Pattern)"
        )
        return True

    def build_dependency_graph(self):
        """Build dependency graph from all capabilities"""
        for namespace, manifest in self.capabilities.items():
            metadata = manifest["metadata"]
            dc_relation = manifest.get("dc_relation", {})
            requires = dc_relation.get("requires", [])

            if not requires:
                continue

            for dep in requires:
                if isinstance(dep, str):
                    # Simple string dependency (convert to dict)
                    dep = {"capability": dep, "relationship": "prerequisite"}
                elif not isinstance(dep, dict):
                    self.warnings.append(
                        f"[{namespace}] Invalid dependency format: {dep}"
                    )
                    continue

                dep_namespace = dep.get("capability")
                relationship = dep.get("relationship", "prerequisite")

                if not dep_namespace:
                    self.warnings.append(
                        f"[{namespace}] Dependency missing 'capability' field"
                    )
                    continue

                # Add to dependency graph
                self.dependency_graph[namespace].append(
                    {
                        "dependency": dep_namespace,
                        "relationship": relationship,
                        "version": dep.get("version", "*"),
                    }
                )

                # Add to reverse graph (for circular detection)
                self.reverse_graph[dep_namespace].append(namespace)

                self.stats["total_dependencies"] += 1

    def validate_dependency(
        self, source_namespace: str, dep_info: Dict
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate a single dependency

        Returns:
            Tuple of (is_valid, error_message)
        """
        dep_namespace = dep_info["dependency"]
        relationship = dep_info["relationship"]

        # Check if dependency exists
        if dep_namespace not in self.capabilities:
            self.stats["missing_dependencies"] += 1
            return (
                False,
                f"Dependency not found: {dep_namespace}",
            )

        # Get capability types
        source_manifest = self.capabilities[source_namespace]
        dep_manifest = self.capabilities[dep_namespace]

        source_type = source_manifest["metadata"].get("dc_type")
        dep_type = dep_manifest["metadata"].get("dc_type")

        # Validate relationship type
        if relationship not in VALID_RELATIONSHIPS:
            self.stats["invalid_relationships"] += 1
            return (
                False,
                f"Invalid relationship type: '{relationship}' (valid: {', '.join(VALID_RELATIONSHIPS)})",
            )

        # Validate cross-type relationship rules
        if source_type == "Service" and dep_type == "Pattern":
            self.stats["service_to_pattern"] += 1
            if relationship not in SERVICE_TO_PATTERN_ALLOWED:
                self.stats["invalid_relationships"] += 1
                return (
                    False,
                    f"Service -> Pattern: relationship '{relationship}' not allowed "
                    f"(allowed: {', '.join(SERVICE_TO_PATTERN_ALLOWED)})",
                )

        elif source_type == "Pattern" and dep_type == "Service":
            self.stats["pattern_to_service"] += 1
            if relationship not in PATTERN_TO_SERVICE_ALLOWED:
                self.stats["invalid_relationships"] += 1
                return (
                    False,
                    f"Pattern -> Service: relationship '{relationship}' not allowed "
                    f"(allowed: {', '.join(PATTERN_TO_SERVICE_ALLOWED)})",
                )

        elif source_type == "Service" and dep_type == "Service":
            self.stats["service_to_service"] += 1
            if relationship not in SERVICE_TO_SERVICE_ALLOWED:
                self.stats["invalid_relationships"] += 1
                return (
                    False,
                    f"Service -> Service: relationship '{relationship}' not allowed "
                    f"(allowed: {', '.join(SERVICE_TO_SERVICE_ALLOWED)})",
                )

        elif source_type == "Pattern" and dep_type == "Pattern":
            self.stats["pattern_to_pattern"] += 1
            if relationship not in PATTERN_TO_PATTERN_ALLOWED:
                self.stats["invalid_relationships"] += 1
                return (
                    False,
                    f"Pattern -> Pattern: relationship '{relationship}' not allowed "
                    f"(allowed: {', '.join(PATTERN_TO_PATTERN_ALLOWED)})",
                )

        return True, None

    def detect_circular_dependencies(self) -> List[List[str]]:
        """
        Detect circular dependencies using DFS

        Returns:
            List of circular dependency chains
        """
        visited = set()
        rec_stack = set()
        cycles = []

        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for dep_info in self.dependency_graph.get(node, []):
                dep = dep_info["dependency"]

                if dep not in visited:
                    dfs(dep, path[:])
                elif dep in rec_stack:
                    # Found cycle
                    cycle_start = path.index(dep)
                    cycle = path[cycle_start:] + [dep]
                    cycles.append(cycle)
                    self.stats["circular_dependencies"] += 1

            rec_stack.remove(node)

        for namespace in self.capabilities.keys():
            if namespace not in visited:
                dfs(namespace, [])

        return cycles

    def validate_all(self) -> bool:
        """
        Validate all dependencies

        Returns:
            True if all validations passed, False otherwise
        """
        print("\n" + "=" * 80)
        print("Cross-Type Dependency Validation")
        print("=" * 80)

        # Build dependency graph
        self.build_dependency_graph()

        # Validate each dependency
        for source_namespace, deps in self.dependency_graph.items():
            source_manifest = self.capabilities[source_namespace]
            source_title = source_manifest["metadata"].get("dc_title", "Unknown")
            source_type = source_manifest["metadata"].get("dc_type", "Unknown")

            print(f"\nValidating: {source_title} ({source_type})")
            print(f"  Namespace: {source_namespace}")

            if not deps:
                print(f"  [SKIP] No dependencies")
                continue

            for dep_info in deps:
                dep_namespace = dep_info["dependency"]
                relationship = dep_info["relationship"]

                is_valid, error_msg = self.validate_dependency(
                    source_namespace, dep_info
                )

                if is_valid:
                    # Get dependency info for display
                    if dep_namespace in self.capabilities:
                        dep_manifest = self.capabilities[dep_namespace]
                        dep_type = dep_manifest["metadata"].get("dc_type", "Unknown")
                        print(
                            f"  [PASS] {dep_namespace} ({dep_type}, {relationship})"
                        )
                    else:
                        print(f"  [PASS] {dep_namespace} ({relationship})")
                else:
                    print(
                        f"  [FAIL] {dep_namespace}: {error_msg}", file=sys.stderr
                    )
                    self.errors.append(
                        f"[{source_namespace}] -> [{dep_namespace}]: {error_msg}"
                    )

        # Detect circular dependencies
        print(f"\nChecking for circular dependencies...")
        cycles = self.detect_circular_dependencies()

        if cycles:
            print(f"\n[FAIL] Found {len(cycles)} circular dependency chain(s):")
            for i, cycle in enumerate(cycles, 1):
                print(f"  {i}. {' -> '.join(cycle)}")
                self.errors.append(f"Circular dependency: {' -> '.join(cycle)}")
        else:
            print(f"  [PASS] No circular dependencies found")

        return len(self.errors) == 0

    def validate_capability(self, namespace: str) -> bool:
        """Validate dependencies for a single capability"""
        if namespace not in self.capabilities:
            print(f"ERROR: Capability not found: {namespace}", file=sys.stderr)
            return False

        manifest = self.capabilities[namespace]
        title = manifest["metadata"].get("dc_title", "Unknown")
        cap_type = manifest["metadata"].get("dc_type", "Unknown")

        print("\n" + "=" * 80)
        print(f"Validating: {title} ({cap_type})")
        print("=" * 80)
        print(f"Namespace: {namespace}")

        dc_relation = manifest.get("dc_relation", {})
        requires = dc_relation.get("requires", [])

        if not requires:
            print(f"\n[SKIP] No dependencies")
            return True

        print(f"\nDependencies: {len(requires)}")

        for dep in requires:
            if isinstance(dep, str):
                dep = {"capability": dep, "relationship": "prerequisite"}

            dep_namespace = dep.get("capability")
            relationship = dep.get("relationship", "prerequisite")

            dep_info = {
                "dependency": dep_namespace,
                "relationship": relationship,
                "version": dep.get("version", "*"),
            }

            is_valid, error_msg = self.validate_dependency(namespace, dep_info)

            if is_valid:
                if dep_namespace in self.capabilities:
                    dep_manifest = self.capabilities[dep_namespace]
                    dep_type = dep_manifest["metadata"].get("dc_type", "Unknown")
                    print(f"  [PASS] {dep_namespace} ({dep_type}, {relationship})")
                else:
                    print(f"  [PASS] {dep_namespace} ({relationship})")
            else:
                print(f"  [FAIL] {dep_namespace}: {error_msg}", file=sys.stderr)
                self.errors.append(
                    f"[{namespace}] -> [{dep_namespace}]: {error_msg}"
                )

        return len(self.errors) == 0

    def print_summary(self):
        """Print validation summary"""
        print(f"\n{'=' * 80}")
        print("Validation Summary")
        print(f"{'=' * 80}")

        print(f"\nCapabilities:")
        print(f"  Total: {self.stats['total_capabilities']}")
        print(f"  Service-type: {self.stats['service_type']}")
        print(f"  Pattern-type: {self.stats['pattern_type']}")

        print(f"\nDependencies:")
        print(f"  Total: {self.stats['total_dependencies']}")
        print(f"  Service -> Pattern: {self.stats['service_to_pattern']}")
        print(f"  Pattern -> Service: {self.stats['pattern_to_service']}")
        print(f"  Service -> Service: {self.stats['service_to_service']}")
        print(f"  Pattern -> Pattern: {self.stats['pattern_to_pattern']}")

        print(f"\nValidation Results:")
        print(f"  Errors: {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")
        print(f"  Missing dependencies: {self.stats['missing_dependencies']}")
        print(f"  Invalid relationships: {self.stats['invalid_relationships']}")
        print(f"  Circular dependencies: {self.stats['circular_dependencies']}")

        if self.errors:
            print(f"\nErrors:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\nWarnings:")
            for warning in self.warnings:
                print(f"  - {warning}")

        if len(self.errors) == 0:
            print(f"\nSUCCESS: All dependency validations passed")
        else:
            print(f"\nERROR: {len(self.errors)} validation error(s) found")

        print(f"{'=' * 80}\n")

    def export_dependency_graph(self, output_file: Path):
        """Export dependency graph to JSON"""
        graph = {
            "version": "1.0.0",
            "capabilities": {},
            "statistics": self.stats,
        }

        for namespace, manifest in self.capabilities.items():
            metadata = manifest["metadata"]
            graph["capabilities"][namespace] = {
                "title": metadata.get("dc_title"),
                "type": metadata.get("dc_type"),
                "version": metadata.get("dc_hasVersion"),
                "dependencies": self.dependency_graph.get(namespace, []),
                "dependents": self.reverse_graph.get(namespace, []),
            }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=2)

        print(f"\nDependency graph exported to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate cross-type dependencies between capabilities"
    )

    # Actions
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "--validate-all",
        action="store_true",
        help="Validate all capabilities and dependencies",
    )
    action.add_argument(
        "--capability", type=str, help="Validate specific capability by namespace"
    )
    action.add_argument(
        "--export-graph",
        type=Path,
        help="Export dependency graph to JSON file (e.g., dependencies.json)",
    )
    action.add_argument(
        "--stats", action="store_true", help="Show dependency statistics only"
    )

    # Options
    parser.add_argument(
        "--capabilities-dir",
        type=Path,
        default=Path("capabilities"),
        help="Directory containing capability manifests (default: capabilities/)",
    )

    args = parser.parse_args()

    # Initialize validator
    validator = DependencyValidator(capabilities_dir=args.capabilities_dir)

    # Load capabilities
    if not validator.load_capabilities():
        sys.exit(2)

    # Execute action
    if args.validate_all:
        success = validator.validate_all()
        validator.print_summary()
        sys.exit(0 if success else 1)

    elif args.capability:
        success = validator.validate_capability(args.capability)
        validator.print_summary()
        sys.exit(0 if success else 1)

    elif args.export_graph:
        validator.build_dependency_graph()
        validator.export_dependency_graph(args.export_graph)
        validator.print_summary()
        sys.exit(0)

    elif args.stats:
        validator.build_dependency_graph()
        validator.print_summary()
        sys.exit(0)


if __name__ == "__main__":
    main()
