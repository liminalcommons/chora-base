#!/usr/bin/env python3
"""
Add domain field to all SAPs in sap-catalog.json

Part of SAP-DISCO-V5 Feature 6: Domain Taxonomy & Organization
Trace ID: DISCO-V5
"""

import json
import sys
from pathlib import Path

# Domain mapping based on approved plan
DOMAIN_MAPPING = {
    'Infrastructure': ['sap-framework', 'inbox', 'chora-base'],
    'Developer Experience': [
        'project-bootstrap', 'testing-framework', 'ci-cd-workflows',
        'quality-gates', 'documentation-framework', 'automation-scripts',
        'docker-operations', 'mcp-server-development'
    ],
    'Foundation': ['react-foundation', 'react-testing', 'react-linting'],
    'User-Facing': ['react-state-management', 'react-styling'],
    'Advanced': [
        'chora-compose-integration', 'chora-compose-meta',
        'react-performance', 'react-accessibility'
    ],
    'Specialized': [
        'agent-awareness', 'memory-system', 'development-lifecycle',
        'metrics-tracking', 'task-tracking', 'link-validation-reference-management',
        'sap-self-evaluation', 'dogfooding-patterns', 'publishing-automation',
        'sap-generation'
    ]
}

# Create reverse mapping (name -> domain)
NAME_TO_DOMAIN = {}
for domain, sap_names in DOMAIN_MAPPING.items():
    for sap_name in sap_names:
        NAME_TO_DOMAIN[sap_name] = domain


def add_domain_fields(catalog_path: Path) -> None:
    """Add domain field to all SAPs in catalog"""

    # Read catalog
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    # Track changes
    added_domains = 0
    marked_incomplete = 0

    # Update each SAP
    for sap in catalog['saps']:
        sap_name = sap['name']

        # Add domain field
        if sap_name in NAME_TO_DOMAIN:
            domain = NAME_TO_DOMAIN[sap_name]
            sap['domain'] = domain
            added_domains += 1
            print(f"✅ {sap['id']:8s} ({sap_name:40s}) → {domain}")
        else:
            print(f"⚠️  {sap['id']:8s} ({sap_name:40s}) → UNMAPPED", file=sys.stderr)

        # Mark SAP-013 as incomplete (no README.md)
        if sap['id'] == 'SAP-013':
            sap['complete'] = False
            marked_incomplete += 1
            print(f"   └─ Marked as incomplete (no README.md)")

    # Write updated catalog
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
        f.write('\n')  # Add trailing newline

    print(f"\n📊 Summary:")
    print(f"   • Added domain field to {added_domains} SAPs")
    print(f"   • Marked {marked_incomplete} SAP as incomplete")
    print(f"   • Updated: {catalog_path}")
    print(f"\n✅ sap-catalog.json updated successfully!")


def main():
    # Find catalog file
    repo_root = Path(__file__).parent.parent
    catalog_path = repo_root / 'sap-catalog.json'

    if not catalog_path.exists():
        print(f"❌ Error: sap-catalog.json not found at {catalog_path}", file=sys.stderr)
        sys.exit(1)

    # Add domain fields
    add_domain_fields(catalog_path)


if __name__ == '__main__':
    main()
