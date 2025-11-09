#!/usr/bin/env python3
"""Quick audit of 4-domain cross-references in SAPs."""

import os
import glob


# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

saps = [
    "sap-framework", "inbox", "chora-base", "project-bootstrap",
    "testing-framework", "ci-cd-workflows", "quality-gates",
    "documentation-framework", "automation-scripts", "agent-awareness",
    "memory-system", "docker-operations", "development-lifecycle",
    "metrics-tracking", "link-validation-reference-management",
    "mcp-server-development", "chora-compose-integration", "chora-compose-meta"
]

print("4-Domain Cross-Reference Audit")
print("="*60)

for sap in saps:
    path = f"docs/skilled-awareness/{sap}"
    if not os.path.exists(path):
        print(f"{sap:40} MISSING")
        continue

    count = 0
    for md_file in glob.glob(f"{path}/*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            count += content.count("dev-docs/")
            count += content.count("user-docs/")
            count += content.count("project-docs/")
            count += content.count("standards/")

    status = "✅ GOOD" if count > 5 else "⚠️  LOW" if count > 0 else "❌ NONE"
    print(f"{sap:40} {count:3} refs {status}")
