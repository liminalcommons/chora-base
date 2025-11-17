#!/usr/bin/env python
"""Add SAP-051 (Git Workflow Patterns) to sap-catalog.json"""

import json
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    catalog_path = Path(__file__).parent.parent / 'sap-catalog.json'

    # Load catalog
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    # Check if SAP-051 already exists
    for sap in catalog['saps']:
        if sap['id'] == 'SAP-051':
            print('SAP-051 already exists in catalog')
            return

    # Create SAP-051 entry
    sap_051 = {
        'id': 'SAP-051',
        'name': 'git-workflow-patterns',
        'full_name': 'Git Workflow Patterns',
        'status': 'active',
        'version': '1.0.0',
        'included_by_default': False,
        'size_kb': 180,
        'description': 'Standardized git workflows (branch naming, conventional commits, merge strategies, git hooks) enabling 30-50% conflict reduction and automated changelog generation',
        'capabilities': [
            'Branch naming conventions (feature/bugfix/hotfix/chore/docs)',
            'Conventional Commits v1.0.0 schema enforcement',
            'Merge strategy decision tree (squash vs merge vs rebase)',
            'Client-side git hooks (commit-msg, pre-push, pre-commit)',
            'Justfile automation (git-setup, validate-commits, changelog)',
            'Integration with SAP-001 (Inbox), SAP-010 (Memory), SAP-015 (Beads)',
            'Level 2 custom configuration (types, lengths, strict mode)',
            'Level 2 SAP integration (auto-extract IDs from branch names)',
            'Level 3 CI/CD workflow (GitHub Actions)',
            'Level 3 team onboarding (5-10 min setup)',
            'Level 3 A-MEM integration patterns',
            'Level 3 quarterly maintenance schedule'
        ],
        'dependencies': [],
        'tags': ['git', 'workflow', 'conventional-commits', 'multi-developer', 'conflict-reduction', 'foundation'],
        'author': 'chora-base maintainer + Claude',
        'location': 'docs/skilled-awareness/git-workflow-patterns/',
        'artifacts': {
            'capability_charter': True,
            'protocol_spec': True,
            'awareness_guide': True,
            'adoption_blueprint': True,
            'ledger': True
        },
        'system_files': [
            '.githooks/commit-msg',
            '.githooks/pre-push',
            '.githooks/pre-commit',
            'justfile (12 git recipes)',
            'tests/test_sap_051/',
            '.github/workflows/git-validation.yml',
            'docs/git-workflow-quickstart.md',
            'docs/git-workflow-amem-integration.md',
            'docs/git-workflow-maintenance.md'
        ],
        'phase': 'Phase 3',
        'priority': 'P1',
        'domain': 'Multi-Developer Collaboration'
    }

    # Insert SAP-051 in order
    inserted = False
    for i, sap in enumerate(catalog['saps']):
        if sap['id'] > 'SAP-051':
            catalog['saps'].insert(i, sap_051)
            inserted = True
            break

    if not inserted:
        catalog['saps'].append(sap_051)

    # Write back to file
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print('SAP-051 added to catalog successfully')

if __name__ == '__main__':
    main()
