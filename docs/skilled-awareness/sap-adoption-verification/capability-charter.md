# Capability Charter: SAP Adoption Verification & Quality Assurance

**Capability ID**: SAP-050
**Modern Namespace**: chora.awareness.sap_adoption_verification
**Type**: Pattern
**Status**: Draft
**Version**: 1.0.0
**Created**: 2025-11-16
**Last Updated**: 2025-11-16

---

## Executive Summary

**SAP-050: SAP Adoption Verification & Quality Assurance** formalizes agent awareness patterns for validating SAP structure, completeness, and quality. It provides standardized verification patterns, quality gates for status promotion (draft → pilot → production), and automated tooling for SAP validation.

**Key Benefits**:
- ✅ **Automated Verification**: Validate SAP structure and completeness automatically
- 📊 **Quality Metrics**: Measure SAP quality with objective criteria
- 🚦 **Promotion Gates**: Clear criteria for draft → pilot → production status changes
- 🔍 **Link Validation**: Detect broken cross-references and documentation links
- 📈 **Adoption Tracking**: Monitor SAP adoption progress and metrics

---

## Problem Statement

### Current Challenges

The SAP framework (SAP-000) defines requirements for capability packaging, but lacks automated verification and quality assurance. Without standardized validation patterns, SAP creators face:

1. **Manual Verification**: SAP creators must manually check 5 required artifacts exist and are complete
2. **Inconsistent Quality**: No objective criteria for what makes a SAP "production-ready"
3. **Broken Links**: Cross-references between SAPs become stale without automated validation
4. **Unclear Promotion Path**: No clear criteria for promoting SAP status (draft → pilot → production)
5. **Missing Metrics**: No standardized way to track SAP adoption and effectiveness

### Business Impact

- **Reduced SAP Quality**: Inconsistent verification leads to incomplete or low-quality SAPs
- **Slow Adoption**: Users hesitant to adopt SAPs without quality guarantees
- **Maintenance Burden**: Broken links and stale documentation require manual maintenance
- **No Accountability**: Can't measure SAP effectiveness without adoption metrics
- **Status Confusion**: Unclear when SAPs should be promoted from draft → pilot → production

### User Stories

**As a SAP creator**, I want to:
- Automatically verify my SAP has all 5 required artifacts
- Check that all cross-references and links are valid
- Know what criteria must be met before promoting to production status
- Track adoption metrics to measure SAP effectiveness

**As a SAP adopter**, I want:
- Confidence that production-status SAPs meet quality standards
- Clear understanding of what "pilot" vs "production" means
- Assurance that documentation links won't be broken
- Visibility into SAP adoption rates and user feedback

**As a project maintainer**, I want:
- Automated quality gates in CI/CD pipelines
- Objective criteria for accepting SAP contributions
- Dashboard showing SAP quality metrics
- Tools to detect and fix broken documentation links

---

## Solution Design

### Approach

SAP-050 formalizes 5 core verification patterns for SAP quality assurance:

1. **Structure Verification Pattern**: Validate 5 required artifacts exist and follow naming conventions
2. **Completeness Verification Pattern**: Check artifacts contain required sections and metadata
3. **Link Validation Pattern**: Verify all cross-references and external links are valid
4. **Quality Gate Pattern**: Define criteria for status promotion (draft → pilot → production)
5. **Adoption Metrics Pattern**: Track SAP usage, feedback, and effectiveness

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                SAP Creator / Maintainer                      │
└─────────────────────────────────────────────────────────────┘
                             │
                             │ SAP-050 Patterns
                             ▼
┌─────────────────────────────────────────────────────────────┐
│             SAP Verification Tool (Python CLI)               │
│                                                              │
│  Commands:                                                   │
│    sap-verify structure <sap-name>                          │
│    sap-verify completeness <sap-name>                       │
│    sap-verify links <sap-name>                              │
│    sap-verify quality-gate <sap-name> --target-status=pilot │
│    sap-verify adoption <sap-name>                           │
│                                                              │
│  Output: JSON report with pass/fail/warnings                │
└─────────────────────────────────────────────────────────────┘
                             │
                             │ Reads
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              SAP Directory Structure                         │
│                                                              │
│  docs/skilled-awareness/{sap-name}/                          │
│    ├─ capability-charter.md                                 │
│    ├─ protocol-spec.md                                      │
│    ├─ awareness-guide.md (or AGENTS.md)                     │
│    ├─ adoption-blueprint.md                                 │
│    └─ ledger.md                                             │
│                                                              │
│  capabilities/chora.{domain}.{capability}.yaml               │
└─────────────────────────────────────────────────────────────┘
```

### Core Patterns

**1. Structure Verification Pattern**

Validate SAP has 5 required artifacts with correct naming:

```python
def verify_structure(sap_name: str) -> dict:
    """
    Verify SAP structure (5 required artifacts)

    Returns:
        dict with passed (bool), missing_artifacts (list), warnings (list)
    """
    required_artifacts = [
        'capability-charter.md',
        'protocol-spec.md',
        'awareness-guide.md',  # or AGENTS.md
        'adoption-blueprint.md',
        'ledger.md'
    ]

    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')
    missing = []

    for artifact in required_artifacts:
        # Special case: awareness-guide can be AGENTS.md
        if artifact == 'awareness-guide.md':
            if not (sap_dir / artifact).exists() and not (sap_dir / 'AGENTS.md').exists():
                missing.append(artifact)
        elif not (sap_dir / artifact).exists():
            missing.append(artifact)

    # Check YAML manifest
    manifest_found = False
    for manifest_file in Path('capabilities').glob('chora.*.yaml'):
        with open(manifest_file) as f:
            data = yaml.safe_load(f)
            if sap_name.replace('-', '_') in data.get('metadata', {}).get('dc_identifier', ''):
                manifest_found = True
                break

    if not manifest_found:
        missing.append('capability manifest (YAML)')

    return {
        'passed': len(missing) == 0,
        'missing_artifacts': missing,
        'warnings': []
    }
```

**2. Completeness Verification Pattern**

Check artifacts contain required sections:

```python
def verify_completeness(sap_name: str) -> dict:
    """
    Verify artifacts contain required sections

    Returns:
        dict with passed (bool), issues (list)
    """
    issues = []

    # Charter: Must have Problem Statement, Solution Design, Success Metrics
    charter = Path(f'docs/skilled-awareness/{sap_name}/capability-charter.md')
    if charter.exists():
        content = charter.read_text()
        required_sections = ['Problem Statement', 'Solution Design', 'Success Metrics']
        for section in required_sections:
            if section not in content:
                issues.append(f"capability-charter.md missing section: {section}")

    # Protocol Spec: Must have Overview, Data Formats, Examples
    protocol = Path(f'docs/skilled-awareness/{sap_name}/protocol-spec.md')
    if protocol.exists():
        content = protocol.read_text()
        required_sections = ['Overview', 'Schema', 'Example']
        for section in required_sections:
            if section not in content:
                issues.append(f"protocol-spec.md missing section: {section}")

    # Awareness Guide: Must have Quick Start, Common Workflows
    awareness = Path(f'docs/skilled-awareness/{sap_name}/AGENTS.md')
    if not awareness.exists():
        awareness = Path(f'docs/skilled-awareness/{sap_name}/awareness-guide.md')

    if awareness.exists():
        content = awareness.read_text()
        required_sections = ['Quick Start', 'Workflow']
        for section in required_sections:
            if section not in content:
                issues.append(f"awareness-guide missing section: {section}")

    # Adoption Blueprint: Must have Adoption Checklist, Prerequisites
    blueprint = Path(f'docs/skilled-awareness/{sap_name}/adoption-blueprint.md')
    if blueprint.exists():
        content = blueprint.read_text()
        required_sections = ['Adoption Checklist', 'Prerequisites']
        for section in required_sections:
            if section not in content:
                issues.append(f"adoption-blueprint.md missing section: {section}")

    # Ledger: Must have Version History
    ledger = Path(f'docs/skilled-awareness/{sap_name}/ledger.md')
    if ledger.exists():
        content = ledger.read_text()
        if 'Version History' not in content:
            issues.append("ledger.md missing Version History section")

    return {
        'passed': len(issues) == 0,
        'issues': issues
    }
```

**3. Link Validation Pattern**

Verify all cross-references are valid:

```python
import re

def verify_links(sap_name: str) -> dict:
    """
    Verify all markdown links are valid

    Returns:
        dict with passed (bool), broken_links (list)
    """
    broken_links = []
    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')

    # Find all markdown files
    for md_file in sap_dir.glob('*.md'):
        content = md_file.read_text()

        # Extract markdown links: [text](url)
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)

        for link_text, link_url in links:
            # Skip external URLs
            if link_url.startswith('http'):
                continue

            # Resolve relative path
            target = (md_file.parent / link_url).resolve()

            if not target.exists():
                broken_links.append({
                    'file': str(md_file),
                    'link': link_url,
                    'text': link_text
                })

    return {
        'passed': len(broken_links) == 0,
        'broken_links': broken_links
    }
```

**4. Quality Gate Pattern**

Define criteria for status promotion:

```python
def verify_quality_gate(sap_name: str, target_status: str) -> dict:
    """
    Verify SAP meets criteria for target status

    Args:
        sap_name: SAP name (e.g., 'task-tracking')
        target_status: 'pilot' or 'production'

    Returns:
        dict with passed (bool), unmet_criteria (list)
    """
    unmet = []

    # Always required: Structure + Completeness + Links
    structure = verify_structure(sap_name)
    if not structure['passed']:
        unmet.append(f"Structure verification failed: {structure['missing_artifacts']}")

    completeness = verify_completeness(sap_name)
    if not completeness['passed']:
        unmet.append(f"Completeness verification failed: {len(completeness['issues'])} issues")

    links = verify_links(sap_name)
    if not links['passed']:
        unmet.append(f"Link validation failed: {len(links['broken_links'])} broken links")

    # Pilot status requirements
    if target_status in ['pilot', 'production']:
        # Must have been dogfooded (check ledger)
        ledger = Path(f'docs/skilled-awareness/{sap_name}/ledger.md')
        if ledger.exists():
            content = ledger.read_text()
            if 'dogfooding' not in content.lower():
                unmet.append("No evidence of dogfooding in ledger")
        else:
            unmet.append("Missing ledger.md")

        # Must have at least 1 adoption (check ledger)
        # (Simplified check - look for "Adoption Status")

    # Production status requirements
    if target_status == 'production':
        # Must have metrics (check ledger)
        if ledger.exists():
            content = ledger.read_text()
            if 'metrics' not in content.lower():
                unmet.append("No metrics tracked in ledger")

        # Must have positive feedback
        if 'feedback' not in content.lower():
            unmet.append("No feedback tracked in ledger")

    return {
        'passed': len(unmet) == 0,
        'target_status': target_status,
        'unmet_criteria': unmet
    }
```

**5. Adoption Metrics Pattern**

Track SAP usage and effectiveness:

```python
def track_adoption_metrics(sap_name: str) -> dict:
    """
    Track SAP adoption metrics from ledger

    Returns:
        dict with metrics (adoptions, feedback_count, issues_count, etc.)
    """
    ledger = Path(f'docs/skilled-awareness/{sap_name}/ledger.md')

    if not ledger.exists():
        return {'error': 'Ledger not found'}

    content = ledger.read_text()

    # Parse metrics from ledger (simplified)
    metrics = {
        'adoptions': content.lower().count('adopted'),
        'feedback_entries': content.lower().count('feedback:'),
        'issues_reported': content.lower().count('issue'),
        'version_count': content.lower().count('version'),
    }

    return metrics
```

---

## Success Metrics

**Adoption Metrics**:
- Number of SAPs using verification patterns
- Number of automated verifications run per day
- Number of quality gates enforced in CI/CD

**Quality Metrics**:
- Percentage of SAPs passing structure verification (100% target)
- Percentage of SAPs with all required sections (100% target)
- Percentage of SAPs with no broken links (>95% target)
- Average time to fix verification failures (<1 day target)

**Business Metrics**:
- Increased SAP adoption confidence (user survey: >4/5)
- Reduced SAP maintenance burden (50% fewer broken links)
- Faster status promotions (automated gates reduce approval time by 80%)
- Higher SAP quality scores (objective metrics improve by 40%)

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| False positives in verification | Medium | Allow manual overrides with justification |
| Strict gates slow SAP creation | Medium | Provide draft → pilot fast-track for simple SAPs |
| Link validation performance | Low | Cache results, run incrementally |
| Metrics manipulation | Low | Require ledger updates via git history |
| Quality gate subjectivity | Medium | Define objective, measurable criteria |

---

## Integration Points

**Prerequisites**:
- **SAP Framework** (SAP-000): Defines 5 required artifacts and structure
- **Agent Awareness** (SAP-009): AGENTS.md/CLAUDE.md patterns

**Dependents**:
- **CI/CD Pipelines**: Run verification on pull requests
- **SAP Creators**: Use verification tool before submitting
- **Project Maintainers**: Use quality gates for approving status changes

**Complements**:
- **SAP-027 (Dogfooding Patterns)**: Validation includes dogfooding evidence
- **SAP-029 (SAP Generation)**: Generate SAPs with verification built-in

---

## Open Questions

1. **Manual Override Policy**: When should verification failures be overridden?
   - **Decision**: Allow overrides with documented justification in ledger

2. **Verification Frequency**: How often should verification run?
   - **Decision**: On every PR + daily scheduled check + manual on-demand

3. **Quality Score Weighting**: How to weight different verification criteria?
   - **Decision**: Equal weight initially, refine based on feedback

4. **Adoption Threshold for Production**: How many adoptions required?
   - **Decision**: ≥3 adoptions with positive feedback

5. **Link Validation Scope**: Should external URLs be validated?
   - **Decision**: Yes, but as warnings (not failures)

---

## References

- [SAP-000: SAP Framework](../sap-framework/protocol-spec.md) - Defines SAP structure requirements
- [SAP-016: Link Validation](../link-validation-reference-management/protocol-spec.md) - Provides link validation infrastructure (used by SAP-050)
- [SAP-027: Dogfooding Patterns](../dogfooding-patterns/AGENTS.md) - Validation patterns
- [SAP-029: SAP Generation](../sap-generation/AGENTS.md) - Automated SAP creation

---

**Version**: 1.0.0
**Status**: Draft
**Next Review**: After initial implementation (2 weeks)
