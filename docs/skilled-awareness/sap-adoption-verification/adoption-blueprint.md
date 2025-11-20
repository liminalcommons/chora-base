# Adoption Blueprint: SAP Adoption Verification & Quality Assurance

**Capability ID**: SAP-050
**Modern Namespace**: chora.awareness.sap_adoption_verification
**Type**: Pattern
**Status**: Active
**Version**: 1.1.0
**Last Updated**: 2025-11-20

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

## Maturity Levels (L4-L5)

### Overview

Beyond basic adoption (Phase 1-3 → L0-L3), SAP-050 supports advanced maturity levels for ecosystem-wide distribution and sustained maintenance.

**Advanced Maturity Levels**:
- **L4 (Distributed)**: SAP-050 integrated into project templates, ecosystem-wide availability
- **L5 (Sustained)**: Long-term maintenance, continuous improvement, community contributions

These levels apply when SAP-050 itself (or any SAP using SAP-050 patterns) reaches ecosystem-scale adoption.

---

### L4: Distributed

**Definition**: SAP-050 verification patterns available ecosystem-wide via project templates (Copier, Cookiecutter, etc.).

**Criteria**:
- [x] SAP-050 integrated into chora-base Copier template
  - Verification scripts (`sap_verify.py`) included in template
  - Justfile recipes added (`sap-verify`, `sap-verify-all`)
  - Pre-commit hooks configured (optional selection)
- [x] SAP-050 listed in INDEX.md (Developer Experience domain)
- [x] sap-catalog.json entry created
- [x] Documentation publicly accessible
- [x] ≥3 projects using SAP-050 verification patterns
- [x] Adoption guide tested with external users

**Implementation Steps**:

1. **Add to Copier Template** (~30 min)
   ```yaml
   # copier.yml
   include_sap_050:
     type: bool
     help: "Include SAP verification patterns (SAP-050)?"
     default: true
   ```

   ```jinja
   # Conditional file inclusion
   {% if include_sap_050 %}
   scripts/sap_verify.py
   {% endif %}
   ```

2. **Create Justfile Recipes** (~15 min)
   ```makefile
   # justfile
   # Verify SAP structure
   sap-verify SAP_NAME:
       python scripts/sap_verify.py structure {{SAP_NAME}}

   # Verify all SAPs
   sap-verify-all:
       @for sap in docs/skilled-awareness/*/; do \
           sap_name=$$(basename "$$sap"); \
           python scripts/sap_verify.py structure "$$sap_name" || exit 1; \
       done
   ```

3. **Add INDEX.md Entry** (~10 min)
   - Domain: Developer Experience
   - Dependencies: SAP-000 (Framework)
   - Features: SAP verification, quality gates, maturity progression

4. **Test with External Projects** (~1-2 hours)
   - Generate 3 test projects using Copier template
   - Verify SAP-050 patterns work correctly
   - Collect feedback on adoption experience

**Success Criteria**:
- ✅ Template generates with SAP-050 verification scripts
- ✅ `just sap-verify task-tracking` command works
- ✅ Pre-commit hook blocks invalid SAPs (if enabled)
- ✅ External users successfully adopt SAP-050 patterns

**Time Investment**: 2-4 hours (template integration + testing)

**Output**: SAP-050 accessible to all projects using chora-base template

---

### L5: Sustained

**Definition**: SAP-050 maintained long-term with regular updates, feedback loops, and community contributions.

**Criteria**:
- [x] ≥6 months in L4 (Distributed)
- [x] Quarterly reviews conducted
  - Adoption metrics tracked (# projects using SAP-050, verification success rate)
  - User feedback collected and prioritized
  - Improvement backlog maintained
- [x] Version updates released regularly
  - Bug fixes (PATCH releases)
  - Feature enhancements (MINOR releases)
  - Breaking changes (MAJOR releases) with migration guides
- [x] Community contributions accepted
  - Pull requests reviewed within 1 week
  - Issues triaged and prioritized
  - Contributor guidelines documented
- [x] Documentation kept current
  - Examples updated for new patterns
  - Troubleshooting section expanded based on common issues
  - Performance benchmarks re-validated

**Quarterly Review Checklist**:

```markdown
## SAP-050 Quarterly Review (YYYY-QN)

**Date**: YYYY-MM-DD
**Participants**: [names]
**Review Period**: [start date] - [end date]

### Adoption Metrics
- Total projects using SAP-050: [count]
- New adoptions this quarter: [count]
- Verification success rate: [percentage]
- Average verification time: [seconds]

### Feedback Summary
- Positive feedback: [count] items
- Bug reports: [count] items
- Feature requests: [count] items
- Top 3 pain points:
  1. [pain point 1]
  2. [pain point 2]
  3. [pain point 3]

### Improvements Implemented
- [ ] [Improvement 1] (PATCH 1.0.1)
- [ ] [Improvement 2] (MINOR 1.1.0)
- [ ] [Improvement 3] (planned for next quarter)

### Next Quarter Goals
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

### Version Release Plan
- Next PATCH: [version] (target date: [date])
- Next MINOR: [version] (target date: [date])
- Next MAJOR: [version] (target date: [date])
```

**Maintenance Activities** (2-4 hours/quarter):
1. **Metrics Collection** (~30 min)
   - Query adoption tracking (from ledger.md files across ecosystem)
   - Measure verification performance benchmarks
   - Analyze common verification failures

2. **Feedback Review** (~30 min)
   - Read user feedback from GitHub issues, discussions
   - Prioritize improvements (high/medium/low impact)
   - Plan next version releases

3. **Version Updates** (~1-2 hours)
   - Implement high-priority bug fixes (PATCH)
   - Add requested features (MINOR)
   - Plan breaking changes (MAJOR, if needed)

4. **Documentation Updates** (~30 min)
   - Update examples with new patterns
   - Add troubleshooting entries for common issues
   - Refresh performance benchmarks

**Success Criteria**:
- ✅ Adoption metrics tracked quarterly
- ✅ ≥1 version update per quarter (PATCH or MINOR)
- ✅ User feedback response time <1 week
- ✅ Documentation accuracy ≥95% (no outdated examples)
- ✅ Community satisfaction ≥80% (from surveys)

**Time Investment**: 2-4 hours per quarter (ongoing)

**Output**: SAP-050 remains relevant, valuable, and well-maintained over years

---

### Progression Timeline

**Typical Timeline** (from L0 to L5):

| Level | Milestone | Typical Duration | Cumulative Time |
|-------|-----------|------------------|-----------------|
| **L0 (Aware)** | Read capability-charter.md | 10-15 min | 10-15 min |
| **L1 (Planned)** | Adoption plan created | +30-60 min | 40-75 min |
| **L2 (Implemented)** | SAP-050 operational in project | +10-20 min | 50-95 min |
| **L3 (Validated)** | Real-world usage proven (≥4 weeks) | +4-8 weeks | ~1-2 months |
| **L4 (Distributed)** | Ecosystem integration complete | +2-4 hours | ~2-3 months |
| **L5 (Sustained)** | Long-term maintenance (≥6 months) | +2-4 hours/quarter | ~9-12 months |

**Note**: L4-L5 typically apply to SAP-050 itself (the meta-SAP). Individual projects adopt SAP-050 patterns through L0-L3, while the ecosystem maintains SAP-050 at L4-L5.

---

## References

- [Protocol Specification](protocol-spec.md) - See Maturity Progression Rules (L0-L5) for complete details
- [AGENTS.md](AGENTS.md) - Agent patterns for SAP verification
- [Capability Charter](capability-charter.md) - Problem statement and solution design

---

**Version**: 1.1.0
**Status**: Active
**Estimated Adoption Time**: 10-20 minutes (L0-L2), 2-3 months (L0-L4), 9-12 months (L0-L5)
