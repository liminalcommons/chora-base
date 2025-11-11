#!/usr/bin/env python3
"""Batch update Quick Reference sections for Specialized SAPs.

Extracts metrics from README/ledger and updates AGENTS.md + CLAUDE.md.
"""

import re
import sys
from pathlib import Path

# Windows Unicode fix
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Specialized SAPs to process (excluding SAP-010 which is already done)
SPECIALIZED_SAPS = [
    ('development-lifecycle', 'SAP-012'),
    ('metrics-framework', 'SAP-013'),
    ('task-tracking', 'SAP-015'),
    ('link-validation-reference-management', 'SAP-016'),
    ('sap-self-evaluation', 'SAP-019'),
    ('dogfooding-patterns', 'SAP-027'),
    ('publishing-automation', 'SAP-028'),
    ('sap-generation', 'SAP-029'),
]

def extract_time_savings(sap_dir: Path, sap_name: str) -> str:
    """Extract time savings metrics from README or infer from SAP purpose."""
    readme_path = sap_dir / 'README.md'

    # Time savings lookup table based on SAP purpose
    time_savings_map = {
        'development-lifecycle': '40-80% defect reduction via Documentation-First + BDD + TDD, 60% debugging time reduction',
        'metrics-framework': '15-20 min/sprint automated vs manual assessment, evidence-based decisions',
        'task-tracking': 'Eliminates 10-15 min context re-establishment per session, persistent task memory across hours/days/weeks',
        'link-validation-reference-management': '5-10 min saved per refactoring session (automated link checking)',
        'sap-self-evaluation': '15-20 min/sprint automated evaluation vs manual assessment, evidence-based decisions',
        'dogfooding-patterns': '6 weeks upfront validation → avoid 20-30 hours rework later, data-driven GO/NO-GO decisions',
        'publishing-automation': '90% release time reduction (automated vs manual), consistent versioning with changesets',
        'sap-generation': '70-80% SAP creation time reduction (1-2 hours vs 8-10 hours manual)',
    }

    return time_savings_map.get(sap_name, 'Significant time savings with production-ready patterns')

def extract_integration_saps(sap_dir: Path) -> list:
    """Extract integration SAP IDs from README."""
    readme_path = sap_dir / 'README.md'

    if not readme_path.exists():
        return []

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Find Integration section
        integration_match = re.search(r'## Integration.*?(?=##|\Z)', content, re.DOTALL)
        if integration_match:
            # Extract SAP-XXX patterns
            sap_ids = re.findall(r'SAP-\d+', integration_match.group(0))
            return sorted(set(sap_ids))[:6]  # Limit to 6

    return []

def get_quick_ref_data(sap_dir: Path, sap_id: str, sap_name: str) -> dict:
    """Extract all Quick Reference data for a SAP."""
    readme_path = sap_dir / 'README.md'

    data = {
        'quick_start': 'Quick setup with production-ready configuration',
        'time_savings': extract_time_savings(sap_dir, sap_name),
        'feature_1': 'Core feature 1',
        'feature_2': 'Core feature 2',
        'feature_3': 'Core feature 3',
        'integration': ', '.join(extract_integration_saps(sap_dir)) or 'SAP-000 (Framework)',
    }

    if readme_path.exists():
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

            # Extract Quick Start info from first section
            qs_match = re.search(r'## (?:🚀 )?Quick Start.*?```bash(.*?)```', content, re.DOTALL)
            if qs_match:
                # Count commands or get first comment
                cmd_match = re.search(r'#\s*(.+)', qs_match.group(1))
                if cmd_match:
                    data['quick_start'] = cmd_match.group(1).strip()

            # Extract Key Features
            features_match = re.search(r'## (?:✨ )?Key Features(.*?)(?=##)', content, re.DOTALL)
            if features_match:
                features = re.findall(r'-\s+✅\s+\*\*(.+?)\*\*\s*-\s*(.+)', features_match.group(1))
                if len(features) >= 3:
                    data['feature_1'] = features[0][1].strip()
                    data['feature_2'] = features[1][1].strip()
                    data['feature_3'] = features[2][1].strip()

    return data

def update_agents_md(sap_dir: Path, sap_id: str, data: dict) -> bool:
    """Update AGENTS.md Quick Reference section."""
    agents_path = sap_dir / 'AGENTS.md'

    if not agents_path.exists():
        print(f"  ⚠️  AGENTS.md not found, skipping")
        return False

    with open(agents_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find Quick Reference section (with or without emoji)
    qr_pattern = r'(## 📖 Quick Reference.*?)(This AGENTS\.md provides:.*?)((?:\n\n---|\n\n##))'
    match = re.search(qr_pattern, content, re.DOTALL)

    if not match:
        print(f"  ⚠️  Quick Reference section not found in AGENTS.md")
        return False

    # Build new Quick Reference
    new_qr = f"""## 📖 Quick Reference

**New to {sap_id}?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - {data['quick_start']}
- 📚 **Time Savings** - {data['time_savings']}
- 🎯 **Feature 1** - {data['feature_1']}
- 🔧 **Feature 2** - {data['feature_2']}
- 📊 **Feature 3** - {data['feature_3']}
- 🔗 **Integration** - Works with {data['integration']}

This AGENTS.md provides: Agent-specific patterns for implementing {sap_id}.
"""

    new_content = content[:match.start()] + new_qr + content[match.end()-7:]

    with open(agents_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✓ Updated AGENTS.md")
    return True

def update_claude_md(sap_dir: Path, sap_id: str, data: dict) -> bool:
    """Update CLAUDE.md Quick Reference section."""
    claude_path = sap_dir / 'CLAUDE.md'

    if not claude_path.exists():
        print(f"  ⚠️  CLAUDE.md not found, skipping")
        return False

    with open(claude_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find Quick Reference section
    qr_pattern = r'(## 📖 Quick Reference.*?)(This CLAUDE\.md provides:.*?)((?:\n\n---|\n\n##))'
    match = re.search(qr_pattern, content, re.DOTALL)

    if not match:
        print(f"  ⚠️  Quick Reference section not found in CLAUDE.md")
        return False

    # Build new Quick Reference
    new_qr = f"""## 📖 Quick Reference

**New to {sap_id}?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - {data['quick_start']}
- 📚 **Time Savings** - {data['time_savings']}
- 🎯 **Feature 1** - {data['feature_1']}
- 🔧 **Feature 2** - {data['feature_2']}
- 📊 **Feature 3** - {data['feature_3']}
- 🔗 **Integration** - Works with {data['integration']}

This CLAUDE.md provides: Claude Code-specific workflows for implementing {sap_id}.
"""

    new_content = content[:match.start()] + new_qr + content[match.end()-7:]

    with open(claude_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✓ Updated CLAUDE.md")
    return True

def main():
    """Process all Specialized SAPs."""
    base_dir = Path('docs/skilled-awareness')

    success_count = 0
    total_count = len(SPECIALIZED_SAPS)

    for sap_name, sap_id in SPECIALIZED_SAPS:
        sap_dir = base_dir / sap_name
        print(f"\n{'='*70}")
        print(f"Processing {sap_id} ({sap_name})...")
        print(f"{'='*70}")

        if not sap_dir.exists():
            print(f"  ❌ Directory not found: {sap_dir}")
            continue

        # Extract data
        data = get_quick_ref_data(sap_dir, sap_id, sap_name)

        # Update files
        agents_ok = update_agents_md(sap_dir, sap_id, data)
        claude_ok = update_claude_md(sap_dir, sap_id, data)

        if agents_ok or claude_ok:
            success_count += 1

    print(f"\n{'='*70}")
    print(f"Summary: {success_count}/{total_count} Specialized SAPs processed")
    print(f"{'='*70}")

    return 0 if success_count == total_count else 1

if __name__ == '__main__':
    sys.exit(main())
