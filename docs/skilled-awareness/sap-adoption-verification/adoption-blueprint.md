# Adoption Blueprint: SAP Adoption Verification & Quality Assurance

**Capability ID**: SAP-050
**Modern Namespace**: chora.awareness.sap_adoption_verification
**Type**: Pattern
**Status**: Draft
**Version**: 1.0.0
**Last Updated**: 2025-11-16

---

## Overview

This blueprint provides step-by-step guidance for adopting **SAP-050: SAP Adoption Verification & Quality Assurance** patterns.

**Adoption Time**: 10-20 minutes

**Prerequisites**:
- Python 3.9+ with `pyyaml`
- Access to SAP directories (`docs/skilled-awareness/`, `capabilities/`)

---

## Adoption Checklist

- [ ] **Phase 1**: Setup (5 minutes)
  - [ ] Install Python dependencies
  - [ ] Test verification functions
- [ ] **Phase 2**: Integration (5-10 minutes)
  - [ ] Create verification helper module
  - [ ] Test on existing SAPs
  - [ ] Add to project AGENTS.md
- [ ] **Phase 3**: Automation (5 minutes)
  - [ ] Add to CI/CD pipeline (optional)
  - [ ] Create pre-commit hook (optional)

---

## Phase 1: Setup

### Step 1.1: Install Dependencies

```bash
pip install pyyaml
```

### Step 1.2: Test Verification

Create `test_sap_verification.py`:

```python
from pathlib import Path

def verify_sap_structure(sap_name: str) -> dict:
    """Verify SAP has all 5 required artifacts"""
    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')
    missing = []

    required = ['capability-charter.md', 'protocol-spec.md',
                'adoption-blueprint.md', 'ledger.md']
    for artifact in required:
        if not (sap_dir / artifact).exists():
            missing.append(artifact)

    if not (sap_dir / 'AGENTS.md').exists() and not (sap_dir / 'awareness-guide.md').exists():
        missing.append('AGENTS.md (or awareness-guide.md)')

    return {'passed': len(missing) == 0, 'missing': missing}

# Test
result = verify_sap_structure('task-tracking')
print(f"Test: {'PASS' if result['passed'] else 'FAIL'}")
```

Run: `python test_sap_verification.py`

---

## Phase 2: Integration

### Step 2.1: Create Verification Module

Create `sap_verify.py`:

```python
"""SAP Verification Helper Module"""

from pathlib import Path
import re

def verify_structure(sap_name: str) -> dict:
    """Verify SAP structure (5 artifacts + manifest)"""
    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')
    missing = []

    required = ['capability-charter.md', 'protocol-spec.md',
                'adoption-blueprint.md', 'ledger.md']
    for artifact in required:
        if not (sap_dir / artifact).exists():
            missing.append(artifact)

    if not (sap_dir / 'AGENTS.md').exists() and not (sap_dir / 'awareness-guide.md').exists():
        missing.append('AGENTS.md')

    manifest_found = any(
        sap_name.replace('-', '_') in str(m)
        for m in Path('capabilities').glob('chora.*.yaml')
    )
    if not manifest_found:
        missing.append('capability manifest (YAML)')

    return {'passed': len(missing) == 0, 'missing': missing}

def verify_completeness(sap_name: str) -> dict:
    """Verify required sections present"""
    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')
    issues = []

    charter = sap_dir / 'capability-charter.md'
    if charter.exists():
        content = charter.read_text()
        for section in ['Problem Statement', 'Solution Design', 'Success Metrics']:
            if section not in content:
                issues.append(f"capability-charter.md missing: {section}")

    return {'passed': len(issues) == 0, 'issues': issues}

def verify_links(sap_name: str) -> dict:
    """Verify markdown links"""
    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')
    broken = []

    for md_file in sap_dir.glob('*.md'):
        content = md_file.read_text()
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)

        for text, url in links:
            if url.startswith('http') or url.startswith('#'):
                continue
            target = (md_file.parent / url).resolve()
            if not target.exists():
                broken.append({'file': md_file.name, 'link': url})

    return {'passed': len(broken) == 0, 'broken_links': broken}

# CLI
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python sap_verify.py <command> <sap-name>")
        sys.exit(1)

    command = sys.argv[1]
    sap_name = sys.argv[2]

    if command == 'structure':
        result = verify_structure(sap_name)
        if result['passed']:
            print(f"✓ {sap_name}: Structure valid")
        else:
            print(f"✗ {sap_name}: Missing {result['missing']}")
            sys.exit(1)

    elif command == 'completeness':
        result = verify_completeness(sap_name)
        if result['passed']:
            print(f"✓ {sap_name}: Completeness valid")
        else:
            print(f"✗ {sap_name}: {len(result['issues'])} issues")
            sys.exit(1)

    elif command == 'links':
        result = verify_links(sap_name)
        if result['passed']:
            print(f"✓ {sap_name}: No broken links")
        else:
            print(f"✗ {sap_name}: {len(result['broken_links'])} broken links")
            sys.exit(1)
```

### Step 2.2: Test on Existing SAPs

```bash
# Test structure
python sap_verify.py structure task-tracking

# Test completeness
python sap_verify.py completeness task-tracking

# Test links
python sap_verify.py links task-tracking
```

### Step 2.3: Update Project AGENTS.md

Add to `AGENTS.md`:

```markdown
## SAP-050: SAP Adoption Verification

This project uses SAP verification patterns to ensure quality.

**Agent Patterns**:

\```python
from sap_verify import verify_structure, verify_completeness, verify_links

# Verify SAP before recommending
result = verify_structure('task-tracking')
if result['passed']:
    # Safe to recommend
\```

**See**: [SAP-050 AGENTS.md](AGENTS.md)
```

---

## Phase 3: Automation (Optional)

### Step 3.1: Add to CI/CD

`.github/workflows/sap-verification.yml`:

```yaml
name: SAP Verification

on:
  pull_request:
    paths:
      - 'docs/skilled-awareness/**'

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install pyyaml
      - run: |
          for sap in docs/skilled-awareness/*/; do
            sap_name=$(basename "$sap")
            python sap_verify.py structure "$sap_name"
          done
```

### Step 3.2: Pre-commit Hook

`.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Verify modified SAPs
for file in $(git diff --cached --name-only | grep "docs/skilled-awareness/"); do
  sap_name=$(echo "$file" | cut -d'/' -f3)
  python sap_verify.py structure "$sap_name" || exit 1
done
```

Make executable: `chmod +x .git/hooks/pre-commit`

---

## Validation

### Test All Verifications

```python
#!/usr/bin/env python3
"""Test SAP-050 patterns on all SAPs"""

from pathlib import Path
from sap_verify import verify_structure, verify_completeness, verify_links

failed = []

for sap_dir in Path('docs/skilled-awareness').iterdir():
    if not sap_dir.is_dir():
        continue

    sap_name = sap_dir.name

    # Run all verifications
    structure = verify_structure(sap_name)
    completeness = verify_completeness(sap_name)
    links = verify_links(sap_name)

    if not (structure['passed'] and completeness['passed'] and links['passed']):
        failed.append(sap_name)

print(f"Verified {len(list(Path('docs/skilled-awareness').iterdir()))} SAPs")
print(f"Failed: {len(failed)}")
if failed:
    print(f"Failed SAPs: {', '.join(failed)}")
```

---

## Troubleshooting

### Issue: "pyyaml not installed"

**Solution**: `pip install pyyaml`

### Issue: "SAP directory not found"

**Solution**: Verify SAP name matches directory name

---

## References

- [Protocol Specification](protocol-spec.md)
- [AGENTS.md](AGENTS.md)
- [Capability Charter](capability-charter.md)

---

**Version**: 1.0.0
**Status**: Draft
**Estimated Adoption Time**: 10-20 minutes
