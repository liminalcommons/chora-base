#!/usr/bin/env python3
"""
Update INDEX.md with Wave 5 React SAPs

Part of Wave 5 React SAPs completion
Trace ID: WAVE5-COMPLETION
"""

import json
import re
from pathlib import Path

# Wave 5 SAP entries for INDEX.md (organized by domain)
WAVE5_INDEX_ENTRIES = {
    "Foundation": [
        {
            "id": "SAP-033",
            "name": "React Authentication & Authorization",
            "description": "Production-ready authentication with 4 providers (NextAuth v5, Clerk, Supabase Auth, Auth0) reducing setup from 3-4h to 15min (93.75% time savings)"
        },
        {
            "id": "SAP-034",
            "name": "React Database Integration",
            "description": "PostgreSQL integration with Prisma/Drizzle ORM decision framework reducing setup from 3-4h to 25min (89.6% time savings)"
        },
        {
            "id": "SAP-041",
            "name": "React Form Validation",
            "description": "React Hook Form + Zod reducing setup from 2-3h to 20min (88.9% time savings), type-safe validation, WCAG 2.2 Level AA accessibility"
        }
    ],
    "User-Facing": [
        {
            "id": "SAP-035",
            "name": "React File Upload & Storage",
            "description": "File upload with 4 providers (UploadThing, Vercel Blob, Supabase Storage, AWS S3) reducing setup from 6h to 30min (91.7% time savings)"
        },
        {
            "id": "SAP-036",
            "name": "React Error Handling",
            "description": "Error boundaries + Sentry monitoring reducing setup from 3-4h to 30min (87.5% time savings), GDPR/CCPA compliant PII scrubbing"
        }
    ],
    "Advanced": [
        {
            "id": "SAP-037",
            "name": "React Real-Time Synchronization",
            "description": "WebSocket/real-time with 4 providers (Socket.IO, Pusher, Ably, Supabase Realtime) reducing setup from 7h to 30min (92.9% time savings)"
        },
        {
            "id": "SAP-038",
            "name": "React Internationalization (i18n)",
            "description": "next-intl framework reducing setup from 5h to 30min (90% time savings), 20+ languages, Server Components support, type-safe translations"
        },
        {
            "id": "SAP-039",
            "name": "React E2E Testing",
            "description": "Playwright E2E testing reducing setup from 3.5h to 30min (85.7% time savings), cross-browser support, parallel execution, CI/CD integration"
        },
        {
            "id": "SAP-040",
            "name": "React Monorepo Architecture",
            "description": "Turborepo monorepo reducing setup from 7.5h to 30min (93.3% time savings), incremental builds, remote caching, pnpm workspaces"
        }
    ]
}


def format_sap_entry(sap):
    """Format a SAP entry for INDEX.md"""
    return f"""### {sap['id']}: {sap['name']}

**Path**: [docs/skilled-awareness/{get_sap_directory(sap['id'])}](docs/skilled-awareness/{get_sap_directory(sap['id'])})

{sap['description']}

**Status**: 🟡 Pilot
**Version**: 1.0.0

---
"""


def get_sap_directory(sap_id):
    """Get SAP directory name from ID"""
    directory_map = {
        "SAP-033": "react-authentication",
        "SAP-034": "react-database-integration",
        "SAP-035": "react-file-upload",
        "SAP-036": "react-error-handling",
        "SAP-037": "react-realtime-synchronization",
        "SAP-038": "react-internationalization",
        "SAP-039": "react-e2e-testing",
        "SAP-040": "react-monorepo-architecture",
        "SAP-041": "react-form-validation"
    }
    return directory_map.get(sap_id, "unknown")


def update_index_md():
    """Update INDEX.md with Wave 5 React SAPs"""
    repo_root = Path(__file__).parent.parent
    index_path = repo_root / "docs" / "skilled-awareness" / "INDEX.md"

    print(f"Reading {index_path}...")
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if SAPs already added
    if "SAP-033" in content:
        print("✅ Wave 5 SAPs already in INDEX.md")
        return

    print("Adding Wave 5 React SAPs to INDEX.md...")

    # Find domain sections and add SAPs
    for domain, saps in WAVE5_INDEX_ENTRIES.items():
        domain_pattern = f"## {domain} Domain"

        if domain_pattern not in content:
            print(f"⚠️  Warning: {domain} Domain section not found")
            continue

        # Find the domain section and insert SAPs after existing entries
        # This is a simplified approach - in production would need more sophisticated parsing

        # For now, just append to end of each domain section
        # Find next domain section
        domain_start = content.find(domain_pattern)
        next_domain = content.find("\n## ", domain_start + len(domain_pattern))

        if next_domain == -1:
            # Last domain, insert before "Progressive Adoption Path" or end
            next_section = content.find("\n## Progressive Adoption Path", domain_start)
            if next_section == -1:
                next_section = len(content)
        else:
            next_section = next_domain

        # Generate SAP entries
        new_entries = "\n".join([format_sap_entry(sap) for sap in saps])

        # Insert before next section
        content = content[:next_section] + "\n" + new_entries + "\n" + content[next_section:]

        print(f"  ✅ Added {len(saps)} SAPs to {domain} Domain")

    # Update SAP count in header
    content = re.sub(
        r"Total SAPs: \d+",
        "Total SAPs: 39",
        content
    )

    # Write updated INDEX.md
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ INDEX.md updated successfully!")
    print(f"   • Added 9 Wave 5 React SAPs")
    print(f"   • Updated total SAP count to 39")


if __name__ == "__main__":
    update_index_md()
