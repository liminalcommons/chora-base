# Protocol Specification: SAP Adoption Verification & Quality Assurance

**Capability ID**: SAP-050
**Modern Namespace**: chora.awareness.sap_adoption_verification
**Type**: Pattern
**Status**: Draft
**Version**: 1.0.0
**Protocol Version**: 1.0.0
**Last Updated**: 2025-11-16

---

## Overview

This document specifies the complete protocol for verifying SAP structure, completeness, and quality. It defines verification schemas, quality gate criteria, CLI tool specification, and JSON report formats.

**Protocol Goals**:
- **Automated Verification**: 100% of SAPs can be verified programmatically
- **Objective Criteria**: Clear, measurable quality gates
- **Fast Validation**: <5s verification time per SAP
- **Actionable Reports**: JSON output with specific failure details
- **CI/CD Integration**: Exit codes and formats suitable for automation

---

## Verification Schema

### SAP Structure Requirements

**Required Artifacts** (5 total):

| Artifact | Filename | Required | Alternative |
|----------|----------|----------|-------------|
| Capability Charter | capability-charter.md | Yes | None |
| Protocol Specification | protocol-spec.md | Yes | None |
| Awareness Guide | awareness-guide.md | Yes | AGENTS.md |
| Adoption Blueprint | adoption-blueprint.md | Yes | None |
| Ledger | ledger.md | Yes | None |
| Capability Manifest | chora.{domain}.{capability}.yaml | Yes | None |

**Directory Structure**:
```
docs/skilled-awareness/{sap-name}/
├── capability-charter.md
├── protocol-spec.md
├── awareness-guide.md (or AGENTS.md)
├── adoption-blueprint.md
└── ledger.md

capabilities/
└── chora.{domain}.{capability}.yaml
```

---

### Required Sections by Artifact

#### capability-charter.md

**Required Sections**:
- Executive Summary
- Problem Statement
- Solution Design
- Success Metrics
- Risks and Mitigations
- Integration Points

**Metadata** (frontmatter):
- Capability ID
- Modern Namespace
- Type (Service | Pattern)
- Status (draft | pilot | production)
- Version (semver)

---

#### protocol-spec.md

**Required Sections**:
- Overview
- Schema / Data Formats
- Examples
- Error Handling (if applicable)
- Performance Characteristics (if applicable)

**Metadata**:
- Protocol Version
- Backward Compatibility notes

---

#### AGENTS.md / awareness-guide.md

**Required Sections**:
- Quick Start for Agents
- Common Agent Workflows (≥3 workflows)
- Quick Reference Patterns
- Common Agent Pitfalls
- Integration with Other SAPs

---

#### adoption-blueprint.md

**Required Sections**:
- Overview
- Adoption Checklist
- Prerequisites
- Step-by-step Installation (Phase 1, Phase 2, Phase 3)
- Validation Steps
- Troubleshooting

---

#### ledger.md

**Required Sections**:
- Version History
- Adoption Tracking
- Adoption Metrics
- Feedback Log

**Required Fields per Version**:
- Version number
- Date
- Status
- Changes
- Contributors

---

## Quality Gate Criteria

### Draft Status

**Criteria** (no requirements - all SAPs start as draft):
- [ ] 5 required artifacts created
- [ ] Basic structure present

**Purpose**: Work in progress, not ready for adoption

---

### Pilot Status

**Criteria**:
- [x] Structure verification: 100% (all 5 artifacts present)
- [x] Completeness verification: 100% (all required sections present)
- [x] Link validation: ≥95% (max 2-3 broken links acceptable)
- [x] Dogfooding evidence: ≥1 real-world usage documented in ledger
- [x] Feedback: ≥1 feedback entry in ledger
- [x] No critical issues open

**Purpose**: Ready for real-world testing, not production-stable yet

---

### Production Status

**Criteria**:
- [x] All pilot criteria met
- [x] Adoptions: ≥3 documented adoptions in ledger
- [x] Positive feedback: ≥80% positive sentiment
- [x] Metrics tracked: Adoption metrics, quality metrics documented
- [x] Stability: ≥4 weeks in pilot with no major issues
- [x] Documentation quality: No broken links, all examples tested

**Purpose**: Production-ready, recommended for general adoption

---

## CLI Tool Specification

### Command: sap-verify

**Usage**:
```bash
sap-verify [COMMAND] [OPTIONS] <sap-name>
```

**Global Options**:
- `--json`: Output JSON report
- `--verbose`: Show detailed output
- `--exit-code`: Return non-zero on failures

---

### Command: structure

**Purpose**: Verify SAP has all 5 required artifacts

**Usage**:
```bash
sap-verify structure task-tracking
sap-verify structure task-tracking --json
```

**Exit Codes**:
- `0`: All artifacts present
- `1`: Missing artifacts

**JSON Output**:
```json
{
  "command": "structure",
  "sap_name": "task-tracking",
  "passed": true,
  "missing_artifacts": [],
  "warnings": [],
  "timestamp": "2025-11-16T22:00:00Z"
}
```

**Example Failure**:
```json
{
  "command": "structure",
  "sap_name": "example-sap",
  "passed": false,
  "missing_artifacts": [
    "protocol-spec.md",
    "capability manifest (YAML)"
  ],
  "warnings": [],
  "timestamp": "2025-11-16T22:00:00Z"
}
```

---

### Command: completeness

**Purpose**: Verify artifacts contain required sections

**Usage**:
```bash
sap-verify completeness task-tracking
sap-verify completeness task-tracking --json
```

**Exit Codes**:
- `0`: All required sections present
- `1`: Missing sections

**JSON Output**:
```json
{
  "command": "completeness",
  "sap_name": "task-tracking",
  "passed": true,
  "issues": [],
  "timestamp": "2025-11-16T22:00:00Z"
}
```

**Example Failure**:
```json
{
  "command": "completeness",
  "sap_name": "example-sap",
  "passed": false,
  "issues": [
    "capability-charter.md missing section: Success Metrics",
    "AGENTS.md missing section: Common Agent Workflows"
  ],
  "timestamp": "2025-11-16T22:00:00Z"
}
```

---

### Command: links

**Purpose**: Validate all markdown links (internal and external)

**Usage**:
```bash
sap-verify links task-tracking
sap-verify links task-tracking --check-external
sap-verify links task-tracking --json
```

**Options**:
- `--check-external`: Validate external URLs (slower)
- `--ignore-pattern <regex>`: Ignore links matching pattern

**Exit Codes**:
- `0`: No broken links
- `1`: Broken links found

**JSON Output**:
```json
{
  "command": "links",
  "sap_name": "task-tracking",
  "passed": true,
  "broken_links": [],
  "external_links_checked": false,
  "timestamp": "2025-11-16T22:00:00Z"
}
```

**Example Failure**:
```json
{
  "command": "links",
  "sap_name": "example-sap",
  "passed": false,
  "broken_links": [
    {
      "file": "docs/skilled-awareness/example-sap/capability-charter.md",
      "link": "../../../nonexistent-file.md",
      "line": 42,
      "text": "See related documentation"
    }
  ],
  "external_links_checked": false,
  "timestamp": "2025-11-16T22:00:00Z"
}
```

---

### Command: quality-gate

**Purpose**: Verify SAP meets criteria for target status

**Usage**:
```bash
sap-verify quality-gate task-tracking --target-status=pilot
sap-verify quality-gate task-tracking --target-status=production --json
```

**Options**:
- `--target-status <status>`: pilot or production (required)
- `--override <criteria>`: Override specific criteria with justification

**Exit Codes**:
- `0`: All criteria met
- `1`: Criteria unmet

**JSON Output**:
```json
{
  "command": "quality-gate",
  "sap_name": "task-tracking",
  "target_status": "pilot",
  "passed": true,
  "unmet_criteria": [],
  "met_criteria": [
    "Structure verification: PASS",
    "Completeness verification: PASS",
    "Link validation: PASS (0 broken links)",
    "Dogfooding evidence: PASS (2 usage examples)",
    "Feedback: PASS (3 entries)"
  ],
  "timestamp": "2025-11-16T22:00:00Z"
}
```

**Example Failure**:
```json
{
  "command": "quality-gate",
  "sap_name": "example-sap",
  "target_status": "production",
  "passed": false,
  "unmet_criteria": [
    "Adoptions: FAIL (1/3 required)",
    "Positive feedback: FAIL (50%/80% required)",
    "Stability: FAIL (1 week / 4 weeks required)"
  ],
  "met_criteria": [
    "Structure verification: PASS",
    "Completeness verification: PASS",
    "Link validation: PASS"
  ],
  "timestamp": "2025-11-16T22:00:00Z"
}
```

---

### Command: adoption

**Purpose**: Track SAP adoption metrics from ledger

**Usage**:
```bash
sap-verify adoption task-tracking
sap-verify adoption task-tracking --json
```

**JSON Output**:
```json
{
  "command": "adoption",
  "sap_name": "task-tracking",
  "metrics": {
    "total_adoptions": 5,
    "feedback_entries": 8,
    "issues_reported": 2,
    "issues_resolved": 2,
    "version_count": 3,
    "days_since_creation": 45,
    "current_status": "pilot"
  },
  "recent_feedback": [
    {
      "date": "2025-11-15",
      "sentiment": "positive",
      "summary": "Beads integration works well"
    }
  ],
  "timestamp": "2025-11-16T22:00:00Z"
}
```

---

### Command: all

**Purpose**: Run all verifications (structure + completeness + links + quality-gate)

**Usage**:
```bash
sap-verify all task-tracking
sap-verify all task-tracking --target-status=pilot --json
```

**JSON Output**:
```json
{
  "command": "all",
  "sap_name": "task-tracking",
  "target_status": "pilot",
  "overall_passed": true,
  "results": {
    "structure": { "passed": true },
    "completeness": { "passed": true },
    "links": { "passed": true },
    "quality_gate": { "passed": true }
  },
  "timestamp": "2025-11-16T22:00:00Z"
}
```

---

## Verification Algorithms

### Algorithm: Structure Verification

```python
def verify_structure(sap_name: str) -> dict:
    """Verify SAP structure"""
    from pathlib import Path
    import yaml

    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')
    missing = []

    # Check 5 required artifacts
    required = [
        'capability-charter.md',
        'protocol-spec.md',
        ('awareness-guide.md', 'AGENTS.md'),  # Either one
        'adoption-blueprint.md',
        'ledger.md'
    ]

    for artifact in required:
        if isinstance(artifact, tuple):
            # Either alternative is acceptable
            if not any((sap_dir / alt).exists() for alt in artifact):
                missing.append(f"{artifact[0]} (or {artifact[1]})")
        else:
            if not (sap_dir / artifact).exists():
                missing.append(artifact)

    # Check YAML manifest
    manifest_pattern = sap_name.replace('-', '_')
    manifest_found = any(
        manifest_pattern in manifest.name
        for manifest in Path('capabilities').glob('chora.*.yaml')
    )

    if not manifest_found:
        missing.append('capability manifest (YAML)')

    return {
        'passed': len(missing) == 0,
        'missing_artifacts': missing
    }
```

---

### Algorithm: Completeness Verification

```python
def verify_completeness(sap_name: str) -> dict:
    """Verify required sections present"""
    from pathlib import Path

    issues = []
    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')

    # Charter sections
    charter = sap_dir / 'capability-charter.md'
    if charter.exists():
        content = charter.read_text()
        required = [
            'Executive Summary',
            'Problem Statement',
            'Solution Design',
            'Success Metrics',
            'Risks and Mitigations'
        ]
        for section in required:
            if section not in content:
                issues.append(f"capability-charter.md missing: {section}")

    # Protocol sections
    protocol = sap_dir / 'protocol-spec.md'
    if protocol.exists():
        content = protocol.read_text()
        required = ['Overview', 'Schema', 'Example']
        for section in required:
            if section not in content:
                issues.append(f"protocol-spec.md missing: {section}")

    # AGENTS sections
    agents = sap_dir / 'AGENTS.md'
    if not agents.exists():
        agents = sap_dir / 'awareness-guide.md'

    if agents.exists():
        content = agents.read_text()
        required = ['Quick Start', 'Workflow']
        for section in required:
            if section not in content:
                issues.append(f"AGENTS.md missing: {section}")

    # Blueprint sections
    blueprint = sap_dir / 'adoption-blueprint.md'
    if blueprint.exists():
        content = blueprint.read_text()
        required = ['Adoption Checklist', 'Prerequisites']
        for section in required:
            if section not in content:
                issues.append(f"adoption-blueprint.md missing: {section}")

    # Ledger sections
    ledger = sap_dir / 'ledger.md'
    if ledger.exists():
        content = ledger.read_text()
        if 'Version History' not in content:
            issues.append("ledger.md missing: Version History")

    return {
        'passed': len(issues) == 0,
        'issues': issues
    }
```

---

### Algorithm: Link Validation

```python
def verify_links(sap_name: str, check_external: bool = False) -> dict:
    """Verify markdown links"""
    from pathlib import Path
    import re

    broken = []
    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')

    for md_file in sap_dir.glob('*.md'):
        content = md_file.read_text()

        # Extract markdown links: [text](url)
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)

        for text, url in links:
            # Skip external URLs unless requested
            if url.startswith('http'):
                if check_external:
                    # TODO: Check URL with HTTP request
                    pass
                continue

            # Skip anchors
            if url.startswith('#'):
                continue

            # Resolve relative path
            target = (md_file.parent / url).resolve()

            if not target.exists():
                # Find line number
                line_num = content[:content.find(url)].count('\n') + 1

                broken.append({
                    'file': str(md_file.relative_to(Path.cwd())),
                    'link': url,
                    'line': line_num,
                    'text': text
                })

    return {
        'passed': len(broken) == 0,
        'broken_links': broken,
        'external_links_checked': check_external
    }
```

---

### Algorithm: Quality Gate Verification

```python
def verify_quality_gate(sap_name: str, target_status: str) -> dict:
    """Verify quality gate criteria"""
    unmet = []
    met = []

    # Always required
    structure = verify_structure(sap_name)
    if structure['passed']:
        met.append("Structure verification: PASS")
    else:
        unmet.append(f"Structure verification: FAIL ({len(structure['missing_artifacts'])} missing)")

    completeness = verify_completeness(sap_name)
    if completeness['passed']:
        met.append("Completeness verification: PASS")
    else:
        unmet.append(f"Completeness verification: FAIL ({len(completeness['issues'])} issues)")

    links = verify_links(sap_name)
    if links['passed']:
        met.append("Link validation: PASS (0 broken links)")
    else:
        broken_count = len(links['broken_links'])
        if target_status == 'pilot' and broken_count <= 3:
            met.append(f"Link validation: PASS ({broken_count} broken links, ≤3 acceptable for pilot)")
        else:
            unmet.append(f"Link validation: FAIL ({broken_count} broken links)")

    # Pilot requirements
    if target_status in ['pilot', 'production']:
        ledger = Path(f'docs/skilled-awareness/{sap_name}/ledger.md')
        if ledger.exists():
            content = ledger.read_text().lower()

            # Dogfooding evidence
            if 'dogfooding' in content or 'usage' in content:
                met.append("Dogfooding evidence: PASS")
            else:
                unmet.append("Dogfooding evidence: FAIL (no evidence in ledger)")

            # Feedback
            feedback_count = content.count('feedback:')
            if feedback_count >= 1:
                met.append(f"Feedback: PASS ({feedback_count} entries)")
            else:
                unmet.append("Feedback: FAIL (no feedback in ledger)")

    # Production requirements
    if target_status == 'production':
        if ledger.exists():
            content = ledger.read_text().lower()

            # Adoptions
            adoption_count = content.count('adopted')
            if adoption_count >= 3:
                met.append(f"Adoptions: PASS ({adoption_count} adoptions)")
            else:
                unmet.append(f"Adoptions: FAIL ({adoption_count}/3 required)")

            # Metrics
            if 'metrics' in content:
                met.append("Metrics tracked: PASS")
            else:
                unmet.append("Metrics tracked: FAIL")

            # Stability (4 weeks in pilot)
            # TODO: Parse version history dates

    return {
        'passed': len(unmet) == 0,
        'target_status': target_status,
        'unmet_criteria': unmet,
        'met_criteria': met
    }
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: SAP Verification

on:
  pull_request:
    paths:
      - 'docs/skilled-awareness/**'
      - 'capabilities/**'

jobs:
  verify-sap:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pyyaml

      - name: Detect modified SAPs
        id: detect
        run: |
          # Find modified SAPs
          git diff --name-only origin/main... | grep "docs/skilled-awareness/" | cut -d'/' -f3 | sort -u

      - name: Run SAP verification
        run: |
          for sap in $(git diff --name-only origin/main... | grep "docs/skilled-awareness/" | cut -d'/' -f3 | sort -u); do
            echo "Verifying $sap..."
            python scripts/sap-verify.py all "$sap" --json
          done
```

---

## Performance Characteristics

**Target Latency**:
- Structure verification: <1s
- Completeness verification: <2s
- Link validation: <3s (without external URLs)
- Link validation: <30s (with external URLs)
- Quality gate: <5s
- All verifications: <10s

**Scalability**:
- Verify 50 SAPs: <5 minutes
- Parallel execution: <1 minute for all SAPs

---

## Error Handling

### Missing SAP Directory

**Error**:
```json
{
  "error": "sap_not_found",
  "message": "SAP directory not found: docs/skilled-awareness/nonexistent-sap/",
  "sap_name": "nonexistent-sap"
}
```

**Exit Code**: 2

---

### Invalid Target Status

**Error**:
```json
{
  "error": "invalid_target_status",
  "message": "Invalid target status: 'unknown'. Must be 'pilot' or 'production'.",
  "provided": "unknown",
  "allowed": ["pilot", "production"]
}
```

**Exit Code**: 2

---

## Versioning

**Protocol Version**: 1.0.0

**Backward Compatibility**: Changes to quality gate criteria will be versioned separately

---

## References

- [SAP-000: SAP Framework](../sap-framework/protocol-spec.md)
- [SAP-016: Link Validation](../link-validation-reference-management/protocol-spec.md) - Link validation infrastructure
- [SAP-027: Dogfooding Patterns](../dogfooding-patterns/AGENTS.md)

---

**Version**: 1.0.0
**Protocol Version**: 1.0.0
**Status**: Draft
