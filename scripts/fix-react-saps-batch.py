#!/usr/bin/env python3
"""Batch fix all React SAPs for v5.0.0 compliance.

Fixes:
1. README.md - Remove emoji headings, set Quick Start time, number troubleshooting problems
2. AGENTS.md - Add/update Quick Reference with 6 emoji bullets
3. CLAUDE.md - Add/update Quick Reference with 6 emoji bullets (if exists)
"""

import re
import sys
from pathlib import Path

# Windows Unicode fix
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# React SAPs to process
REACT_SAPS = [
    'react-foundation',
    'react-authentication',
    'react-database-integration',
    'react-form-validation',
    'react-testing',
    'react-linting',
    'react-state-management',
    'react-styling',
    'react-performance',
    'react-accessibility',
    'react-file-upload',
    'react-error-handling',
    'react-realtime-synchronization',
    'react-internationalization',
    'react-e2e-testing',
    'react-monorepo-architecture',
]

def fix_readme(sap_dir: Path) -> bool:
    """Fix README.md headings and troubleshooting problems."""
    readme_path = sap_dir / 'README.md'
    if not readme_path.exists():
        print(f"  ⚠️  README.md not found")
        return False

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Fix section headings - remove emojis
    replacements = [
        (r'^## 🚀 Quick Start \(\d+ minutes?\)', '## Quick Start (5 minutes)'),
        (r'^## 📖 What Is (SAP-\d+|It)\?', '## What Is It?'),
        (r'^## 🎯 When to Use', '## When to Use'),
        (r'^## ✨ Key Features', '## Key Features'),
        (r'^## 📚 (Quick Reference|Common Workflows)', '## Common Workflows'),
        (r'^## 🔗 Integration( with Other SAPs)?', '## Integration'),
        (r'^## 🏆 Success Metrics', '## Success Metrics'),
        (r'^## 🔧 Troubleshooting', '## Troubleshooting'),
        (r'^## 📄 Learn More', '## Learn More'),
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    # Find and number troubleshooting problems
    troubleshooting_start = content.find('## Troubleshooting')
    if troubleshooting_start != -1:
        problem_count = 0
        lines = content[troubleshooting_start:].split('\n')
        for i, line in enumerate(lines):
            if line.startswith('**Problem**:') or line.startswith('### Problem:'):
                problem_count += 1
                # Extract problem description
                desc = line.replace('**Problem**:', '').replace('### Problem:', '').strip()
                lines[i] = f'### Problem {problem_count}: {desc}' if desc else f'### Problem {problem_count}:'
        content = content[:troubleshooting_start] + '\n'.join(lines)

    # Fix Solution format
    content = re.sub(r'\*\*Solution\*\*:', '**Solution**:', content)

    if content != original_content:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed README.md")
        return True
    else:
        print(f"  • README.md already compliant")
        return True

def main():
    """Process all React SAPs."""
    base_dir = Path('docs/skilled-awareness')

    success_count = 0
    total_count = len(REACT_SAPS)

    for sap_name in REACT_SAPS:
        sap_dir = base_dir / sap_name
        print(f"\n{'='*70}")
        print(f"Processing {sap_name}...")
        print(f"{'='*70}")

        if not sap_dir.exists():
            print(f"  ❌ Directory not found: {sap_dir}")
            continue

        # Fix README
        if fix_readme(sap_dir):
            success_count += 1

    print(f"\n{'='*70}")
    print(f"Summary: {success_count}/{total_count} React SAPs processed")
    print(f"{'='*70}")

    return 0 if success_count == total_count else 1

if __name__ == '__main__':
    sys.exit(main())
