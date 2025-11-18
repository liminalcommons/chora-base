#!/usr/bin/env python3
"""
CODEOWNERS Template Generator

Generates GitHub/GitLab-compatible CODEOWNERS files based on domain ownership mappings.
Part of SAP-052 (Ownership Zones) infrastructure.

Usage:
    # Generate for chora-workspace (default template)
    python codeowners-generator.py --template chora-workspace --owner @victorpiper

    # Generate for custom project with multiple domains
    python codeowners-generator.py --domains docs:@alice scripts:@bob

    # Generate with team ownership
    python codeowners-generator.py --template chora-workspace --org myorg --teams docs-team

    # Output to file
    python codeowners-generator.py --template chora-workspace --owner @alice --output CODEOWNERS

Features:
- Pre-defined templates (chora-workspace, generic)
- Custom domain-to-owner mapping
- Multi-owner support (fallback reviewers)
- Team ownership (@org/team-name)
- Syntax validation (leading /, @ symbols)
- Comment generation with domain descriptions

References:
- SAP-052: docs/skilled-awareness/ownership-zones/
- Protocol Spec: docs/skilled-awareness/ownership-zones/protocol-spec.md
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class CodeownersGenerator:
    """Generates CODEOWNERS files from domain ownership mappings."""

    # Pre-defined templates
    TEMPLATES = {
        "chora-workspace": {
            "docs": {
                "patterns": ["/docs/", "*.md"],
                "description": "Documentation domain",
            },
            "scripts": {
                "patterns": ["/scripts/", "justfile"],
                "description": "Scripts/Automation domain",
            },
            "inbox": {
                "patterns": ["/inbox/"],
                "description": "Coordination/Inbox domain",
            },
            "memory": {
                "patterns": ["/.chora/"],
                "description": "Memory system domain",
            },
            "project-docs": {
                "patterns": ["/project-docs/"],
                "description": "Project management domain",
            },
            "shared": {
                "patterns": ["/AGENTS.md", "/CLAUDE.md", "/README.md"],
                "description": "Shared files",
            },
        },
        "generic": {
            "docs": {
                "patterns": ["/docs/", "*.md"],
                "description": "Documentation",
            },
            "src": {
                "patterns": ["/src/"],
                "description": "Source code",
            },
            "tests": {
                "patterns": ["/tests/"],
                "description": "Test suite",
            },
            "config": {
                "patterns": ["/.github/", "*.yml", "*.yaml", "*.json"],
                "description": "Configuration files",
            },
        },
    }

    def __init__(self, template: str = "chora-workspace"):
        """Initialize generator with template."""
        if template not in self.TEMPLATES:
            raise ValueError(
                f"Unknown template: {template}. Available: {', '.join(self.TEMPLATES.keys())}"
            )
        self.template = self.TEMPLATES[template]
        self.domain_owners: Dict[str, List[str]] = {}

    def set_owner(self, domain: str, owners: List[str]) -> None:
        """Set owner(s) for a domain."""
        # Validate owner format (@username or @org/team)
        for owner in owners:
            if not owner.startswith("@"):
                raise ValueError(
                    f"Invalid owner format: {owner}. Must start with '@' (e.g., @username or @org/team)"
                )
        self.domain_owners[domain] = owners

    def set_all_owners(self, owner: str) -> None:
        """Set the same owner for all domains."""
        if not owner.startswith("@"):
            raise ValueError(
                f"Invalid owner format: {owner}. Must start with '@'"
            )
        for domain in self.template.keys():
            self.domain_owners[domain] = [owner]

    def add_custom_domain(
        self, domain: str, patterns: List[str], description: str = ""
    ) -> None:
        """Add a custom domain with patterns."""
        self.template[domain] = {
            "patterns": patterns,
            "description": description or f"{domain.capitalize()} files",
        }

    def validate_patterns(self) -> List[str]:
        """Validate patterns and return list of warnings."""
        warnings = []
        for domain, config in self.template.items():
            for pattern in config["patterns"]:
                # Check for leading / on directory patterns
                if pattern.endswith("/") and not pattern.startswith("/"):
                    warnings.append(
                        f"Pattern '{pattern}' in domain '{domain}' should start with '/' for absolute path"
                    )
                # Check for wildcards without leading /
                if "*" in pattern and not pattern.startswith("/") and "/" in pattern:
                    warnings.append(
                        f"Pattern '{pattern}' in domain '{domain}' may not match as intended. Use '/' prefix for absolute paths."
                    )
        return warnings

    def generate(self) -> str:
        """Generate CODEOWNERS file content."""
        lines = [
            "# CODEOWNERS",
            "#",
            "# Defines code ownership for automatic reviewer assignment.",
            "# See: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners",
            "#",
            "# Pattern format: <file-pattern> @username1 @username2",
            "# Last matching pattern determines ownership.",
            "#",
            "# Generated by: scripts/codeowners-generator.py (SAP-052)",
            "",
        ]

        # Check if all domains have owners assigned
        missing_owners = [
            domain for domain in self.template.keys() if domain not in self.domain_owners
        ]
        if missing_owners:
            lines.append(
                f"# WARNING: The following domains do not have owners assigned:"
            )
            for domain in missing_owners:
                lines.append(f"#   - {domain}")
            lines.append("")

        # Generate ownership patterns
        for domain, config in self.template.items():
            # Domain header comment
            lines.append(f"# {config['description']}")

            # Get owners for this domain
            owners = self.domain_owners.get(domain, [])
            if not owners:
                lines.append(f"# TODO: Assign owner for {domain} domain")
                for pattern in config["patterns"]:
                    lines.append(f"# {pattern} @OWNER_NEEDED")
            else:
                owner_str = " ".join(owners)
                for pattern in config["patterns"]:
                    lines.append(f"{pattern} {owner_str}")

            lines.append("")  # Blank line between domains

        return "\n".join(lines)

    def write_to_file(self, output_path: Path) -> None:
        """Write generated CODEOWNERS to file."""
        content = self.generate()
        output_path.write_text(content, encoding="utf-8")


def parse_domain_mapping(mappings: List[str]) -> Dict[str, List[str]]:
    """Parse domain:owner mappings from CLI arguments.

    Args:
        mappings: List of "domain:@owner1,@owner2" strings

    Returns:
        Dict mapping domain names to list of owners

    Examples:
        ["docs:@alice", "scripts:@bob"] -> {"docs": ["@alice"], "scripts": ["@bob"]}
        ["docs:@alice,@bob"] -> {"docs": ["@alice", "@bob"]}
    """
    result = {}
    for mapping in mappings:
        if ":" not in mapping:
            raise ValueError(
                f"Invalid domain mapping: {mapping}. Expected format: domain:@owner"
            )
        domain, owners_str = mapping.split(":", 1)
        owners = [o.strip() for o in owners_str.split(",")]
        result[domain] = owners
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Generate CODEOWNERS file for automatic reviewer assignment (SAP-052)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate for chora-workspace with single owner
  %(prog)s --template chora-workspace --owner @victorpiper

  # Generate with custom domain mappings
  %(prog)s --domains docs:@alice scripts:@bob,@charlie

  # Generate with team ownership
  %(prog)s --template chora-workspace --org myorg --teams docs-team,eng-team

  # Output to file
  %(prog)s --template chora-workspace --owner @alice --output CODEOWNERS

  # Validate patterns only (no output)
  %(prog)s --template chora-workspace --owner @alice --validate-only
        """,
    )

    parser.add_argument(
        "--template",
        choices=["chora-workspace", "generic"],
        default="chora-workspace",
        help="Template to use (default: chora-workspace)",
    )

    parser.add_argument(
        "--owner",
        help="Set the same owner for all domains (e.g., @victorpiper)",
    )

    parser.add_argument(
        "--domains",
        nargs="+",
        help="Custom domain-to-owner mappings (format: domain:@owner1,@owner2)",
    )

    parser.add_argument(
        "--org",
        help="GitHub organization name (for team ownership)",
    )

    parser.add_argument(
        "--teams",
        nargs="+",
        help="Team names to assign to all domains (requires --org)",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path (default: stdout)",
    )

    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate patterns only, do not generate output",
    )

    args = parser.parse_args()

    try:
        # Initialize generator
        generator = CodeownersGenerator(template=args.template)

        # Set owners
        if args.owner:
            generator.set_all_owners(args.owner)
        elif args.domains:
            domain_mappings = parse_domain_mapping(args.domains)
            for domain, owners in domain_mappings.items():
                generator.set_owner(domain, owners)
        elif args.teams:
            if not args.org:
                print(
                    "Error: --org is required when using --teams",
                    file=sys.stderr,
                )
                return 1
            team_owners = [f"@{args.org}/{team}" for team in args.teams]
            for domain in generator.template.keys():
                generator.set_owner(domain, team_owners)
        else:
            print(
                "Error: Must provide --owner, --domains, or --teams",
                file=sys.stderr,
            )
            parser.print_help()
            return 1

        # Validate patterns
        warnings = generator.validate_patterns()
        if warnings:
            print("Validation warnings:", file=sys.stderr)
            for warning in warnings:
                print(f"  - {warning}", file=sys.stderr)
            print(file=sys.stderr)

        if args.validate_only:
            if warnings:
                print("Validation completed with warnings.", file=sys.stderr)
                return 1
            else:
                print("Validation completed successfully.", file=sys.stderr)
                return 0

        # Generate CODEOWNERS
        if args.output:
            generator.write_to_file(args.output)
            print(f"CODEOWNERS file written to: {args.output}", file=sys.stderr)
        else:
            print(generator.generate())

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
