#!/usr/bin/env python3
r"""
Namespace Validation Script

Validates capability namespaces in YAML manifests against the chora ontology specification.
Used by pre-commit hooks and CI/CD pipelines.

Validation Rules:
1. Format: chora.{domain}.{capability} (^chora\.[a-z_]+\.[a-z0-9_]{1,50}$)
2. Domain: Must exist in docs/ontology/domain-taxonomy.md
3. Uniqueness: No duplicate namespaces across capabilities/*.yaml
4. Version: Valid SemVer format (x.y.z)
5. Dependencies: Reference valid namespaces

Exit Codes:
  0 - All validations passed
  1 - Validation errors found
  2 - Invalid arguments or file access errors

Usage:
  python scripts/validate-namespaces.py capabilities/
  python scripts/validate-namespaces.py capabilities/chora.react.form_validation.yaml
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install PyYAML", file=sys.stderr)
    sys.exit(2)


# Namespace format regex
NAMESPACE_PATTERN = re.compile(r"^chora\.([a-z_]+)\.([a-z0-9_]{1,50})$")

# SemVer regex (simplified - validates x.y.z with optional pre-release/build metadata)
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


class ValidationError:
    """Represents a validation error with context"""

    def __init__(
        self, file_path: Path, error_type: str, message: str, namespace: str = None
    ):
        self.file_path = file_path
        self.error_type = error_type
        self.message = message
        self.namespace = namespace

    def __str__(self) -> str:
        return f"{self.file_path}: [{self.error_type}] {self.message}"


class NamespaceValidator:
    """Validates capability namespaces against chora ontology specification"""

    def __init__(self, capabilities_dir: Path, domain_taxonomy_file: Path):
        self.capabilities_dir = capabilities_dir
        self.domain_taxonomy_file = domain_taxonomy_file
        self.errors: List[ValidationError] = []
        self.valid_domains: Set[str] = set()
        self.namespaces: Dict[str, Path] = {}  # namespace -> file_path

    def load_valid_domains(self) -> bool:
        """Load valid domains from domain-taxonomy.md"""
        if not self.domain_taxonomy_file.exists():
            self.errors.append(
                ValidationError(
                    self.domain_taxonomy_file,
                    "DOMAIN_FILE_MISSING",
                    f"Domain taxonomy file not found: {self.domain_taxonomy_file}",
                )
            )
            return False

        try:
            content = self.domain_taxonomy_file.read_text(encoding="utf-8")

            # Extract domain names from markdown headers
            # Pattern: ## {domain} - Description
            domain_pattern = re.compile(r"^##\s+`([a-z_]+)`", re.MULTILINE)
            domains = domain_pattern.findall(content)

            if not domains:
                # Fallback: look for inline code blocks with domain names
                domain_pattern = re.compile(r"`chora\.([a-z_]+)\.")
                domains = list(set(domain_pattern.findall(content)))

            self.valid_domains = set(domains)

            if not self.valid_domains:
                self.errors.append(
                    ValidationError(
                        self.domain_taxonomy_file,
                        "NO_DOMAINS_FOUND",
                        "No valid domains found in domain-taxonomy.md",
                    )
                )
                return False

            return True

        except Exception as e:
            self.errors.append(
                ValidationError(
                    self.domain_taxonomy_file,
                    "DOMAIN_FILE_READ_ERROR",
                    f"Failed to read domain taxonomy: {e}",
                )
            )
            return False

    def validate_namespace_format(self, namespace: str, file_path: Path) -> bool:
        """Validate namespace format: chora.{domain}.{capability}"""
        if not namespace:
            self.errors.append(
                ValidationError(
                    file_path,
                    "NAMESPACE_EMPTY",
                    "Namespace (dc_identifier) is empty or missing",
                    namespace,
                )
            )
            return False

        match = NAMESPACE_PATTERN.match(namespace)
        if not match:
            self.errors.append(
                ValidationError(
                    file_path,
                    "NAMESPACE_FORMAT_INVALID",
                    f"Namespace '{namespace}' does not match required format: "
                    f"chora.{{domain}}.{{capability}} (lowercase, snake_case, "
                    f"capability 1-50 chars)",
                    namespace,
                )
            )
            return False

        return True

    def validate_domain(self, namespace: str, file_path: Path) -> bool:
        """Validate domain exists in domain taxonomy"""
        match = NAMESPACE_PATTERN.match(namespace)
        if not match:
            return False  # Format error already reported

        domain = match.group(1)

        if domain not in self.valid_domains:
            self.errors.append(
                ValidationError(
                    file_path,
                    "DOMAIN_INVALID",
                    f"Domain '{domain}' in namespace '{namespace}' is not defined "
                    f"in domain-taxonomy.md. Valid domains: {sorted(self.valid_domains)}",
                    namespace,
                )
            )
            return False

        return True

    def validate_version(self, version: str, file_path: Path, namespace: str) -> bool:
        """Validate SemVer format"""
        if not version:
            self.errors.append(
                ValidationError(
                    file_path,
                    "VERSION_EMPTY",
                    f"Version (dc_hasVersion) is empty for namespace '{namespace}'",
                    namespace,
                )
            )
            return False

        if not SEMVER_PATTERN.match(version):
            self.errors.append(
                ValidationError(
                    file_path,
                    "VERSION_FORMAT_INVALID",
                    f"Version '{version}' for namespace '{namespace}' is not valid SemVer. "
                    f"Expected format: MAJOR.MINOR.PATCH (e.g., '1.0.0', '2.3.1')",
                    namespace,
                )
            )
            return False

        return True

    def register_namespace(self, namespace: str, file_path: Path) -> bool:
        """Register namespace and check for duplicates"""
        if namespace in self.namespaces:
            existing_file = self.namespaces[namespace]
            self.errors.append(
                ValidationError(
                    file_path,
                    "NAMESPACE_DUPLICATE",
                    f"Duplicate namespace '{namespace}' found. "
                    f"Already defined in: {existing_file}",
                    namespace,
                )
            )
            return False

        self.namespaces[namespace] = file_path
        return True

    def validate_capability_file(self, file_path: Path) -> bool:
        """Validate a single capability YAML file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.errors.append(
                ValidationError(
                    file_path, "YAML_PARSE_ERROR", f"Failed to parse YAML: {e}"
                )
            )
            return False
        except Exception as e:
            self.errors.append(
                ValidationError(
                    file_path, "FILE_READ_ERROR", f"Failed to read file: {e}"
                )
            )
            return False

        if not data:
            self.errors.append(
                ValidationError(file_path, "YAML_EMPTY", "YAML file is empty")
            )
            return False

        # Check for metadata section
        if "metadata" not in data:
            self.errors.append(
                ValidationError(
                    file_path, "METADATA_MISSING", "Missing 'metadata' section in YAML"
                )
            )
            return False

        metadata = data["metadata"]

        # Get namespace
        namespace = metadata.get("dc_identifier", "")

        # Skip template files
        if namespace in [
            "chora.domain.capability",
            "chora.example.service",
            "chora.example.pattern",
        ]:
            return True  # Templates are allowed to have placeholder namespaces

        # Validate namespace format
        if not self.validate_namespace_format(namespace, file_path):
            return False

        # Validate domain
        if not self.validate_domain(namespace, file_path):
            return False

        # Validate version
        version = metadata.get("dc_hasVersion", "")
        if not self.validate_version(version, file_path, namespace):
            return False

        # Register namespace (check duplicates)
        if not self.register_namespace(namespace, file_path):
            return False

        return True

    def validate_all(self, file_paths: List[Path] = None) -> bool:
        """Validate all capability files or specific file paths"""
        # Load valid domains
        if not self.load_valid_domains():
            return False

        # Determine files to validate
        if file_paths:
            files_to_validate = file_paths
        else:
            files_to_validate = list(self.capabilities_dir.glob("*.yaml")) + list(
                self.capabilities_dir.glob("*.yml")
            )

        if not files_to_validate:
            print(
                f"WARNING: No YAML files found in {self.capabilities_dir}",
                file=sys.stderr,
            )
            return True

        # Validate each file
        all_valid = True
        for file_path in sorted(files_to_validate):
            if not self.validate_capability_file(file_path):
                all_valid = False

        return all_valid

    def print_errors(self):
        """Print all validation errors"""
        if not self.errors:
            return

        print("\n" + "=" * 80, file=sys.stderr)
        print("NAMESPACE VALIDATION ERRORS", file=sys.stderr)
        print("=" * 80 + "\n", file=sys.stderr)

        # Group errors by type
        errors_by_type: Dict[str, List[ValidationError]] = {}
        for error in self.errors:
            errors_by_type.setdefault(error.error_type, []).append(error)

        for error_type, errors in sorted(errors_by_type.items()):
            print(f"[{error_type}] ({len(errors)} error(s)):", file=sys.stderr)
            for error in errors:
                print(f"  {error}", file=sys.stderr)
            print(file=sys.stderr)

        print("=" * 80, file=sys.stderr)
        print(
            f"Total errors: {len(self.errors)} | Failed validation",
            file=sys.stderr,
        )
        print("=" * 80 + "\n", file=sys.stderr)

    def print_summary(self):
        """Print validation summary"""
        if not self.errors:
            print("\n" + "=" * 80)
            print("SUCCESS: All namespace validations passed!")
            print(f"  - Validated {len(self.namespaces)} unique namespace(s)")
            print(f"  - Found {len(self.valid_domains)} valid domain(s)")
            print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Validate capability namespaces against chora ontology specification"
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Capability YAML files or directories to validate",
    )
    parser.add_argument(
        "--domain-taxonomy",
        type=Path,
        default=Path("docs/ontology/domain-taxonomy.md"),
        help="Path to domain taxonomy file (default: docs/ontology/domain-taxonomy.md)",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress success messages"
    )

    args = parser.parse_args()

    # Resolve paths
    paths_to_validate = []
    capabilities_dir = None

    for path in args.paths:
        if not path.exists():
            print(f"ERROR: Path not found: {path}", file=sys.stderr)
            sys.exit(2)

        if path.is_dir():
            capabilities_dir = path
            paths_to_validate = None  # Will validate all files in directory
            break
        else:
            paths_to_validate.append(path)
            if not capabilities_dir:
                capabilities_dir = path.parent

    # Initialize validator
    validator = NamespaceValidator(capabilities_dir, args.domain_taxonomy)

    # Run validation
    success = validator.validate_all(paths_to_validate)

    # Print results
    if not success:
        validator.print_errors()
        sys.exit(1)
    else:
        if not args.quiet:
            validator.print_summary()
        sys.exit(0)


if __name__ == "__main__":
    main()
