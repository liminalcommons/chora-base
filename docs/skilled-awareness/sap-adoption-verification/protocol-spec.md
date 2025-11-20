# Protocol Specification: SAP Adoption Verification & Quality Assurance

**Capability ID**: SAP-050
**Modern Namespace**: chora.awareness.sap_adoption_verification
**Type**: Pattern
**Status**: Active
**Version**: 1.1.0
**Protocol Version**: 1.1.0
**Last Updated**: 2025-11-20

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

## Phase Completion Criteria

### Overview

SAP development follows a 4-phase lifecycle. Each phase has specific completion criteria that must be met before proceeding to the next phase.

**Phases**:
1. **Phase 1: Design** - Create 5 core artifacts (charter, spec, awareness, blueprint, ledger)
2. **Phase 2: Infrastructure** - Build scripts, tools, automation, tests
3. **Phase 3: Pilot** - Real-world validation with ≥1 adoption, collect feedback
4. **Phase 4: Distribution** - Ecosystem integration (INDEX, catalog, copier)

---

### Phase 1: Design Completion Criteria

**Goal**: Complete specification and design documentation

**Deliverables**:
- [x] capability-charter.md created (~400-600 lines)
  - Problem Statement section complete
  - Solution Design section complete
  - Success Metrics section complete
  - Stakeholders section complete
- [x] protocol-spec.md created (~600-1000 lines)
  - Schema/Data Formats section complete
  - Examples provided for all protocols
  - Error handling documented
- [x] awareness-guide.md (or AGENTS.md) created (~400-800 lines)
  - ≥3 agent workflows documented
  - Quick Reference Patterns section complete
  - Common Pitfalls section complete
- [x] adoption-blueprint.md created (~300-500 lines)
  - Phase 1-3 adoption steps defined
  - Prerequisites listed
  - Validation steps provided
- [x] ledger.md created (~200-400 lines)
  - Version history table initialized
  - Adoption tracking template created
  - Baseline metrics documented (if applicable)

**Success Criteria**:
- ✅ All 5 artifacts exist
- ✅ Total word count ≥2,000 words (comprehensive documentation)
- ✅ All required sections present (per artifact requirements above)
- ✅ Cross-references between artifacts validated
- ✅ No placeholder content ("TBD", "TODO") in critical sections

**Estimated Duration**: 3-6 hours (for new SAP), 1-2 hours (for existing SAP expansion)

**Output**: SAP at status=draft, version=1.0.0

---

### Phase 2: Infrastructure Completion Criteria

**Goal**: Build operational tools, scripts, tests, and automation

**Deliverables**:
- [x] Scripts/tools implemented (if SAP defines executable capabilities)
  - Source code in `scripts/` or appropriate directory
  - CLI interface defined (if applicable)
  - Unit tests written (≥80% code coverage)
- [x] Automation configured (if applicable)
  - Justfile recipes added (if SAP defines workflows)
  - Pre-commit hooks configured (if SAP defines quality gates)
  - CI/CD integration documented
- [x] Integration tests passing
  - End-to-end workflows validated
  - Error handling tested
  - Performance benchmarks met (if defined)

**Success Criteria**:
- ✅ All scripts/tools executable without errors
- ✅ Test suite passes (exit code 0)
- ✅ Performance targets met (if defined in protocol-spec.md)
- ✅ Justfile recipes validated (if applicable)
- ✅ Documentation updated with infrastructure details

**Estimated Duration**: 3-8 hours (varies by SAP complexity)

**Output**: SAP remains status=draft, operational infrastructure ready for pilot

**Note**: Phase 2 may be skipped for pattern-only SAPs (no executable code). In such cases, proceed directly to Phase 3.

---

### Phase 3: Pilot Completion Criteria

**Goal**: Real-world validation with documented adoption and feedback

**Deliverables**:
- [x] Pilot adoption documented (≥1 real-world usage)
  - Project name, adoption date, context recorded in ledger.md
  - Adoption process followed (from adoption-blueprint.md)
  - Validation steps completed
- [x] Feedback collected (≥1 feedback entry in ledger.md)
  - User experience documented
  - Pain points identified
  - Improvement suggestions captured
- [x] Bugs/issues resolved
  - Critical bugs fixed before pilot completion
  - Known issues documented in ledger.md or GitHub issues
- [x] Pilot validation report written
  - What worked well
  - Challenges encountered
  - Lessons learned
  - Recommendations for improvements

**Success Criteria**:
- ✅ ≥1 pilot adoption documented in ledger.md
- ✅ ≥1 feedback entry captured
- ✅ No critical bugs open (severity: high)
- ✅ Pilot validation report written (≥200 words)
- ✅ Adoption metrics tracked (time investment, value delivered)

**Estimated Duration**: 2-4 hours (pilot execution + feedback collection)

**Output**: SAP promoted to status=pilot, version=1.0.0 (or 1.1.0 if changes made)

---

### Phase 4: Distribution Completion Criteria

**Goal**: Ecosystem integration and public availability

**Deliverables**:
- [x] INDEX.md entry added
  - SAP listed in appropriate domain (e.g., "Developer Experience")
  - Metadata complete (version, status, description, dependencies, location, features)
- [x] sap-catalog.json entry added (if using machine-readable catalog)
  - SAP metadata machine-parseable
  - Dependencies declared
  - Features tagged
- [x] Copier template integration (if distributable via template)
  - SAP selectable in copier questionnaire
  - Conditional inclusion logic tested
  - Post-generation hooks validated
- [x] Adoption path documented (optional but recommended)
  - Progressive adoption levels defined
  - Entry points for different user personas
- [x] Dependencies validated
  - All referenced SAPs exist
  - Version compatibility confirmed
  - Circular dependencies avoided

**Success Criteria**:
- ✅ INDEX.md entry present and accurate
- ✅ sap-catalog.json entry valid (if applicable)
- ✅ Copier integration tested (if distributable)
- ✅ Ecosystem validation script passes (`scripts/validate-ecosystem-integration.py`)
- ✅ All documentation links validated (no broken cross-references)

**Estimated Duration**: 30-60 minutes

**Output**: SAP promoted to status=active (or production), version=1.0.0+

**Note**: Phase 4 criteria align with SAP-061 (Ecosystem Integration) requirements. See [SAP-061](../sap-ecosystem-integration/) for automated validation details.

---

## Maturity Progression Rules (L0-L5)

### Overview

SAP adoption follows a 6-level maturity progression from awareness to sustained excellence.

**Maturity Levels**:
- **L0 (Aware)**: Problem understood, SAP discovered
- **L1 (Planned)**: Adoption planned, design understood
- **L2 (Implemented)**: SAP operational, basic usage
- **L3 (Validated)**: Proven in real-world usage, feedback collected
- **L4 (Distributed)**: Available ecosystem-wide, publicly accessible
- **L5 (Sustained)**: Maintained long-term, continuous improvement

**Progression Strategy**: SAPs progress through L0→L5 as adoption deepens. Levels align with quality gates (draft/pilot/production status) but measure adoption maturity rather than artifact completeness.

---

### L0: Aware

**Definition**: Team/individual recognizes the problem SAP solves and has read the capability charter.

**Criteria**:
- [x] capability-charter.md read (~5-10 min)
- [x] Problem statement resonates with current pain points
- [x] Value proposition understood

**Activities**:
- Read Executive Summary
- Identify stakeholders who would benefit
- Assess relevance to current project needs

**Time Investment**: 10-15 minutes

**Output**: Decision to proceed with adoption (yes/no)

---

### L1: Planned

**Definition**: Adoption plan created, design understood, prerequisites met.

**Criteria**:
- [x] All 5 core artifacts read
  - capability-charter.md (problem + solution)
  - protocol-spec.md (technical details)
  - awareness-guide.md (agent patterns)
  - adoption-blueprint.md (implementation steps)
  - ledger.md (version history, metrics)
- [x] Prerequisites satisfied (dependencies installed, access granted)
- [x] Adoption timeline estimated (hours, days, weeks)
- [x] Stakeholders aligned on adoption plan

**Activities**:
- Deep read of protocol-spec.md
- Review adoption-blueprint.md checklist
- Install prerequisites
- Schedule adoption time

**Time Investment**: 30-60 minutes (planning), varies by SAP

**Output**: Adoption plan documented (checklist, timeline, responsible parties)

---

### L2: Implemented

**Definition**: SAP operational, basic functionality working, team trained.

**Criteria**:
- [x] All adoption phases complete (Phase 1, 2, 3 from adoption-blueprint.md)
- [x] Validation steps passed
- [x] Team trained on usage patterns
- [x] Basic workflows functional

**Activities**:
- Execute adoption-blueprint.md steps
- Run validation tests
- Train team members
- Document local customizations (if any)

**Time Investment**: Varies by SAP (30 min - 8 hours)

**Output**: SAP functional in project, team capable of basic usage

---

### L3: Validated

**Definition**: SAP proven in real-world usage, feedback collected, value demonstrated.

**Criteria**:
- [x] ≥4 weeks of real-world usage
- [x] Feedback documented (what worked, pain points, improvements)
- [x] Value metrics tracked (time saved, errors prevented, quality improved)
- [x] Lessons learned captured

**Activities**:
- Use SAP in production workflows
- Collect user feedback
- Measure adoption impact (metrics from ledger.md)
- Document lessons learned

**Time Investment**: 4-8 weeks of usage + 1-2 hours documentation

**Output**: Pilot validation report, metrics demonstrating value

---

### L4: Distributed

**Definition**: SAP available to broader ecosystem, integrated into project templates, discoverable.

**Criteria**:
- [x] SAP integrated into project templates (Copier, Cookiecutter, etc.)
- [x] SAP listed in ecosystem INDEX.md
- [x] SAP distributable via package managers (if applicable)
- [x] Documentation publicly accessible
- [x] ≥3 adoptions outside original team

**Activities**:
- Complete Phase 4 (Distribution) criteria
- Add to Copier template questionnaire
- Promote in community channels
- Support external adopters

**Time Investment**: 2-4 hours (distribution setup) + ongoing support

**Output**: SAP accessible ecosystem-wide, adoption growing

---

### L5: Sustained

**Definition**: SAP maintained long-term, continuous improvement, community contributions.

**Criteria**:
- [x] ≥6 months in L4 (Distributed)
- [x] Regular maintenance (quarterly reviews)
- [x] Feedback loop operational (users report issues, improvements implemented)
- [x] Version updates released (PATCH/MINOR/MAJOR per semantic versioning)
- [x] Community contributions accepted (if open source)
- [x] Adoption metrics tracked quarterly

**Activities**:
- Quarterly SAP review (metrics, feedback, issues)
- Release version updates (bug fixes, features)
- Respond to community feedback
- Maintain documentation currency

**Time Investment**: 2-4 hours/quarter

**Output**: SAP remains valuable long-term, adoption sustained or growing

---

## SAP Completion Matrix

### Overview

The SAP Completion Matrix provides a checklist-driven approach to SAP development, showing exactly what tasks remain to achieve each milestone (Phase 1-4, L0-L5).

**Use Cases**:
- **SAP Creators**: Generate checklist for new SAP ("What do I need to finish Phase 1?")
- **Project Managers**: Track SAP development progress across phases
- **AI Agents**: Programmatic SAP completion validation

---

### Matrix Structure

**Dimensions**:
1. **Phases** (rows): Phase 1 (Design), Phase 2 (Infrastructure), Phase 3 (Pilot), Phase 4 (Distribution)
2. **Status** (columns): draft, pilot, active/production
3. **Maturity Levels** (overlaid): L0-L5 progression

**Matrix Format** (Markdown checklist):

```markdown
## SAP-XXX Completion Matrix

**Current Status**: draft
**Current Phase**: Phase 1 (Design)
**Current Maturity**: L0 (Aware)

---

### Phase 1: Design
- [ ] capability-charter.md (400-600 lines)
- [ ] protocol-spec.md (600-1000 lines)
- [ ] awareness-guide.md or AGENTS.md (400-800 lines)
- [ ] adoption-blueprint.md (300-500 lines)
- [ ] ledger.md (200-400 lines)
- [ ] Cross-references validated
- [ ] No placeholder content in critical sections

**Completion**: 0/7 tasks → Estimated 3-6 hours remaining

---

### Phase 2: Infrastructure
- [ ] Scripts/tools implemented (if applicable)
- [ ] Unit tests written (≥80% coverage)
- [ ] Justfile recipes added
- [ ] Integration tests passing
- [ ] Performance benchmarks met

**Completion**: 0/5 tasks → Estimated 3-8 hours (or skip if pattern-only SAP)

---

### Phase 3: Pilot
- [ ] ≥1 pilot adoption documented
- [ ] ≥1 feedback entry in ledger.md
- [ ] Critical bugs resolved
- [ ] Pilot validation report written

**Completion**: 0/4 tasks → Estimated 2-4 hours

---

### Phase 4: Distribution
- [ ] INDEX.md entry added
- [ ] sap-catalog.json entry added
- [ ] Copier integration tested (if distributable)
- [ ] Ecosystem validation script passes
- [ ] All links validated

**Completion**: 0/5 tasks → Estimated 30-60 minutes

---

### Maturity Levels (L0-L5)
- [x] L0 (Aware): Problem understood → **CURRENT**
- [ ] L1 (Planned): Adoption planned
- [ ] L2 (Implemented): SAP operational
- [ ] L3 (Validated): Real-world usage proven
- [ ] L4 (Distributed): Ecosystem-wide availability
- [ ] L5 (Sustained): Long-term maintenance

**Maturity Progression**: L0 → L5 estimated 3-12 months (varies by SAP complexity)
```

---

### Programmatic Matrix Generation

**Python Implementation**:

```python
def generate_sap_completion_matrix(sap_name: str) -> dict:
    """Generate SAP Completion Matrix for a given SAP"""
    from pathlib import Path

    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')
    artifacts = ['capability-charter.md', 'protocol-spec.md',
                 'awareness-guide.md', 'adoption-blueprint.md', 'ledger.md']

    # Phase 1: Design
    phase1_tasks = {
        'capability-charter.md exists': (sap_dir / 'capability-charter.md').exists(),
        'protocol-spec.md exists': (sap_dir / 'protocol-spec.md').exists(),
        'awareness-guide.md exists': (sap_dir / 'awareness-guide.md').exists() or (sap_dir / 'AGENTS.md').exists(),
        'adoption-blueprint.md exists': (sap_dir / 'adoption-blueprint.md').exists(),
        'ledger.md exists': (sap_dir / 'ledger.md').exists(),
    }

    phase1_complete = sum(phase1_tasks.values())
    phase1_total = len(phase1_tasks)

    # Phase 4: Distribution
    phase4_tasks = {
        'INDEX.md entry': check_index_entry(sap_name),
        'sap-catalog.json entry': check_catalog_entry(sap_name),
        'Ecosystem validation passes': run_ecosystem_validation(sap_name),
    }

    phase4_complete = sum(phase4_tasks.values())
    phase4_total = len(phase4_tasks)

    return {
        'sap_name': sap_name,
        'phase1': {'complete': phase1_complete, 'total': phase1_total},
        'phase4': {'complete': phase4_complete, 'total': phase4_total},
        'next_milestone': determine_next_milestone(phase1_complete, phase4_complete),
    }

def check_index_entry(sap_name: str) -> bool:
    """Check if SAP listed in INDEX.md"""
    index_file = Path('docs/skilled-awareness/INDEX.md')
    if not index_file.exists():
        return False
    content = index_file.read_text()
    return sap_name in content

def check_catalog_entry(sap_name: str) -> bool:
    """Check if SAP listed in sap-catalog.json"""
    catalog_file = Path('docs/sap-catalog.json')
    if not catalog_file.exists():
        return False
    import json
    catalog = json.loads(catalog_file.read_text())
    return any(sap.get('id') == sap_name for sap in catalog.get('saps', []))

def run_ecosystem_validation(sap_name: str) -> bool:
    """Run ecosystem validation script"""
    import subprocess
    result = subprocess.run(
        ['python', 'scripts/validate-ecosystem-integration.py', sap_name],
        capture_output=True
    )
    return result.returncode == 0

def determine_next_milestone(phase1_complete: int, phase4_complete: int) -> str:
    """Determine next milestone based on completion"""
    if phase1_complete < 5:
        return "Complete Phase 1 (Design)"
    elif phase4_complete < 3:
        return "Complete Phase 4 (Distribution)"
    else:
        return "SAP Complete (L4+ maturity)"
```

---

### Usage Example

**CLI Command** (proposed):
```bash
# Generate completion matrix for SAP-053
sap-verify completion-matrix task-tracking

# Output:
# SAP-053 Completion Matrix
# =========================
# Phase 1 (Design): 5/5 ✓
# Phase 2 (Infrastructure): 3/5 (60%)
# Phase 3 (Pilot): 1/4 (25%)
# Phase 4 (Distribution): 0/5 (0%)
#
# Next Milestone: Complete Phase 2 (Infrastructure)
# Estimated Time: 2-4 hours remaining
```

---

### Integration with SAP-061

The SAP Completion Matrix integrates with **SAP-061: Ecosystem Integration** validation:

- **Phase 4 tasks** map directly to SAP-061 integration points (INDEX, catalog, copier)
- **Ecosystem validation** uses `scripts/validate-ecosystem-integration.py` (SAP-061 deliverable)
- **Automated quality gates** block Phase 4 completion until SAP-061 validation passes

See [SAP-061: Ecosystem Integration](../sap-ecosystem-integration/) for validation details.

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

**Version**: 1.1.0
**Protocol Version**: 1.1.0
**Status**: Active
