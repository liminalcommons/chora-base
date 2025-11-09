#!/usr/bin/env python3
"""
Add reverse dependencies and synergy metadata to sap-catalog.json

This script enhances the SAP catalog with:
1. Reverse dependencies (dependents field)
2. Synergy metadata (synergies array at catalog level)
3. Anti-patterns (anti_patterns array at catalog level)
"""

import json
from pathlib import Path

def calculate_reverse_dependencies(catalog):
    """Calculate which SAPs depend on each SAP."""
    reverse_deps = {}

    for sap in catalog['saps']:
        sap_id = sap['id']
        if sap_id not in reverse_deps:
            reverse_deps[sap_id] = []

        # Find all SAPs that depend on this one
        for dep_sap in catalog['saps']:
            if sap_id in dep_sap.get('dependencies', []):
                reverse_deps[sap_id].append(dep_sap['id'])

    return reverse_deps

def define_synergies():
    """Define known synergies between SAPs."""
    return [
        {
            "saps": ["SAP-004", "SAP-006"],
            "type": "complementary",
            "name": "Testing + Quality Gates",
            "benefit": "Automated coverage enforcement via pre-commit hooks",
            "time_multiplier": 1.2,
            "adoption_rate": 0.95,
            "description": "SAP-006 pre-commit hooks enforce SAP-004 coverage standards (85%+)",
            "integration_points": [
                "pre-commit hook calls pytest coverage check",
                "ruff linting validates test file structure",
                "CI workflows validate both"
            ]
        },
        {
            "saps": ["SAP-004", "SAP-005"],
            "type": "sequential",
            "name": "Testing + CI/CD",
            "benefit": "Continuous validation on every commit",
            "time_multiplier": 1.15,
            "adoption_rate": 0.90,
            "description": "SAP-005 CI workflows run SAP-004 test suites automatically",
            "integration_points": [
                "test.yml workflow calls pytest from SAP-004",
                "Matrix testing across Python versions",
                "Coverage reports uploaded to CI"
            ]
        },
        {
            "saps": ["SAP-005", "SAP-006"],
            "type": "complementary",
            "name": "CI/CD + Quality Gates",
            "benefit": "Dual validation (local + CI)",
            "time_multiplier": 1.1,
            "adoption_rate": 0.88,
            "description": "Pre-commit hooks (SAP-006) catch issues before CI (SAP-005)",
            "integration_points": [
                "Local pre-commit hooks as first line of defense",
                "CI workflows as second validation layer",
                "Consistent ruff/mypy config between both"
            ]
        },
        {
            "saps": ["SAP-009", "SAP-007"],
            "type": "enhancement",
            "name": "Agent Awareness + Documentation",
            "benefit": "Agents navigate using structured docs",
            "time_multiplier": 1.25,
            "adoption_rate": 0.75,
            "description": "AGENTS.md references 4-domain structure from SAP-007",
            "integration_points": [
                "Bidirectional translation layer uses doc glossary",
                "AGENTS.md points to docs/ for deeper context",
                "Documentation standards inform AGENTS.md structure"
            ]
        },
        {
            "saps": ["SAP-020", "SAP-021", "SAP-022"],
            "type": "layered",
            "name": "React Foundation Stack",
            "benefit": "Complete React development workflow",
            "time_multiplier": 2.8,
            "adoption_rate": 0.85,
            "description": "Foundation + Testing + Linting creates production-ready React setup",
            "integration_points": [
                "SAP-021 extends SAP-004 patterns to Vitest",
                "SAP-022 extends SAP-006 patterns to ESLint",
                "All three share Next.js 15 configuration"
            ]
        },
        {
            "saps": ["SAP-021", "SAP-026"],
            "type": "complementary",
            "name": "React Testing + Accessibility",
            "benefit": "Automated WCAG compliance checks",
            "time_multiplier": 1.3,
            "adoption_rate": 0.70,
            "description": "jest-axe testing integrated into Vitest suite",
            "integration_points": [
                "axe-core validates WCAG rules in tests",
                "RTL patterns test accessible interactions",
                "Test templates include a11y checks"
            ]
        },
        {
            "saps": ["SAP-003", "SAP-004"],
            "type": "sequential",
            "name": "Bootstrap + Testing",
            "benefit": "Tests directory scaffolded correctly",
            "time_multiplier": 1.1,
            "adoption_rate": 0.92,
            "description": "SAP-003 creates test structure that SAP-004 expects",
            "integration_points": [
                "static-template/tests/ directory",
                "conftest.py fixture scaffolding",
                "pytest.ini configuration"
            ]
        },
        {
            "saps": ["SAP-014", "SAP-004"],
            "type": "enhancement",
            "name": "MCP Server + Testing",
            "benefit": "MCP-specific test patterns",
            "time_multiplier": 1.4,
            "adoption_rate": 0.80,
            "description": "SAP-014 extends SAP-004 pytest patterns for MCP testing",
            "integration_points": [
                "FastMCP test fixtures",
                "MCP tool testing patterns",
                "Async MCP operation tests"
            ]
        },
        {
            "saps": ["SAP-020", "SAP-023", "SAP-024", "SAP-025", "SAP-026"],
            "type": "layered",
            "name": "Complete React Production Stack",
            "benefit": "Production-ready React apps (89% time savings)",
            "time_multiplier": 5.0,
            "adoption_rate": 0.65,
            "description": "Full React stack: Foundation + State + Styling + Performance + A11y",
            "integration_points": [
                "All SAPs share Next.js 15 foundation",
                "TanStack Query integrates with performance monitoring",
                "shadcn/ui components have built-in accessibility",
                "Lighthouse CI validates Core Web Vitals + WCAG"
            ]
        },
        {
            "saps": ["SAP-016", "SAP-000", "SAP-007"],
            "type": "enhancement",
            "name": "Link Validation + Documentation",
            "benefit": "Ensures documentation integrity",
            "time_multiplier": 1.2,
            "adoption_rate": 0.70,
            "description": "SAP-016 validates SAP-000/007 documentation standards compliance",
            "integration_points": [
                "Validates 4-domain structure links",
                "Checks SAP cross-references",
                "CI integration for automated validation"
            ]
        }
    ]

def define_anti_patterns():
    """Define known conflicts/anti-patterns between SAPs."""
    return [
        {
            "saps": ["SAP-014", "SAP-020"],
            "type": "technology_conflict",
            "reason": "MCP vs React - different project types (backend vs frontend)",
            "severity": "warning",
            "description": "SAP-014 (MCP servers) and SAP-020 (React apps) target different tech stacks",
            "resolution": "Choose one technology focus per project (or use monorepo pattern)",
            "acceptable_scenarios": [
                "Monorepo with separate packages for MCP server and React frontend",
                "MCP server that serves React UI (hybrid architecture)"
            ]
        },
        {
            "saps": ["SAP-011", "SAP-020"],
            "type": "infrastructure_mismatch",
            "reason": "Docker optimized for Python projects, React needs Node.js containers",
            "severity": "info",
            "description": "SAP-011 Docker patterns target Python apps; React needs different base images",
            "resolution": "Use SAP-011 patterns as reference, adapt for Node.js/Next.js",
            "acceptable_scenarios": [
                "Full-stack projects with Python backend + React frontend (multi-stage build)",
                "Separate containers for Python API and Next.js app"
            ]
        },
        {
            "saps": ["SAP-027", "SAP-029"],
            "type": "circular_dependency",
            "reason": "SAP-027 documents SAP-029, but was generated using SAP-029",
            "severity": "meta",
            "description": "Dogfooding meta-pattern: SAP-027 formalizes the pilot that created SAP-029",
            "resolution": "This is intentional meta-dogfooding, not a conflict",
            "acceptable_scenarios": [
                "SAP-029 generated SAP-027 to document its own validation methodology"
            ]
        }
    ]

def add_metadata_to_catalog(catalog_path):
    """Add reverse dependencies and synergy metadata to catalog."""
    # Read existing catalog
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    # Calculate reverse dependencies
    reverse_deps = calculate_reverse_dependencies(catalog)

    # Add dependents field to each SAP
    for sap in catalog['saps']:
        sap_id = sap['id']
        sap['dependents'] = sorted(reverse_deps.get(sap_id, []))

    # Add synergies array at catalog level
    catalog['synergies'] = define_synergies()

    # Add anti_patterns array at catalog level
    catalog['anti_patterns'] = define_anti_patterns()

    # Add metadata version
    catalog['metadata_version'] = "2.0.0"
    catalog['metadata_updated'] = "2025-11-03"

    # Write updated catalog
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"[OK] Updated {catalog_path}")
    print(f"   - Added 'dependents' field to {len(catalog['saps'])} SAPs")
    print(f"   - Added {len(catalog['synergies'])} synergy patterns")
    print(f"   - Added {len(catalog['anti_patterns'])} anti-patterns")
    print(f"   - Metadata version: 2.0.0")

if __name__ == "__main__":
    catalog_path = Path(__file__).parent.parent / "sap-catalog.json"
    add_metadata_to_catalog(catalog_path)
