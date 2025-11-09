# Capability Charter: Cross-Platform Development Fundamentals

**SAP ID**: SAP-030
**Version**: 1.0.0
**Status**: pilot
**Owner**: Victor
**Created**: 2025-11-03
**Last Updated**: 2025-11-03

---

## 1. Problem Statement

### Current Challenge

Cross-platform development (Mac/Windows/Linux) requires careful attention to platform-specific concerns: file paths, line endings, permissions, scripting, and tooling.

Current challenge: chora-compose experienced 'significant rework' to fix platform-specific issues when migrating from Windows to Mac development. Platform concerns are scattered across multiple SAPs (SAP-008 states 'Linux + macOS only').

Developers face: bash scripts not portable to Windows, path separator issues, line ending conflicts, and no systematic cross-platform validation.

### Evidence



- chora-compose required significant rework for Windows→Mac migration

- SAP-008 explicitly excludes Windows ('Linux + macOS only')

- SAP-029 documents UTF-8 Windows encoding workaround (limitation L4)

- No multi-OS CI testing (Ubuntu only, no macOS/Windows validation)

- 5 bash scripts in repository not portable to Windows without WSL



### Business Impact

Without cross-platform patterns:

- Platform-specific rework: Hours to days fixing issues post-migration (chora-compose pain)
- Windows exclusion: 40-50% of potential contributors cannot participate
- CI blind spots: Platform-specific bugs caught in production, not pre-release
- Scattered knowledge: Cross-platform concerns documented inconsistently across SAPs
- Script portability: Bash scripts require WSL/Git Bash on Windows (friction)

---

## 2. Proposed Solution

### Cross-Platform Development Fundamentals

SAP-030 provides comprehensive cross-platform development patterns for Mac, Windows, and Linux.

Key capabilities: Platform setup guides (Python, Node.js, Docker), Python-first scripting policy (works everywhere), pathlib.Path patterns (never hardcoded separators), .gitattributes for line endings, platform detection utilities (platform-info.py), cross-platform CI/CD patterns.

Setup time: 30 minutes to adopt patterns, immediate value from utilities.

### Key Principles



- Python-first: Use Python for automation scripts (cross-platform by default)

- pathlib over strings: Always use pathlib.Path for file operations

- Normalize line endings: .gitattributes configuration (LF in repo, native on checkout)

- Design for Windows: Case-insensitive filesystems, works on all platforms

- Platform detection: Utilities to report environment and validate setup

- Centralized knowledge: Single source of truth for cross-platform patterns



---

## 3. Scope

### In Scope



- Platform setup guides (Python 3.11+, Node.js, Docker, just, git)

- Python-first scripting policy and decision tree

- File system patterns (pathlib.Path, line endings, case sensitivity)

- Path separator handling (no hardcoded / or \)

- Platform detection utilities (platform-info.py, validate-cross-platform.py)

- .gitattributes template for line ending normalization



### Out of Scope



- Python environment management - Covered by SAP-031

- Multi-OS CI/CD workflows - Covered by SAP-032

- Bash script migration - Covered by SAP-008 enhancement

- Docker multi-architecture builds - Covered by SAP-011



---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Level 1):
- <!-- TODO: Define Level 1 adoption success criteria -->
- SAP-030 installed (5 artifacts present)
- Basic functionality validated
- Time estimate: 1-2 hours

**Adoption Success** (Level 2):
- <!-- TODO: Define Level 2 adoption success criteria -->
- Advanced features integrated
- Workflow improvements measured
- Time estimate: 4-6 hours

**Adoption Success** (Level 3):
- <!-- TODO: Define Level 3 adoption success criteria -->
- Full mastery achieved
- Optimization and best practices applied
- Time estimate: 8-12 hours

### Key Metrics

<!-- TODO: Define measurable outcomes -->

| Metric | Baseline | Target (Level 2) | Target (Level 3) |
|--------|----------|------------------|------------------|
| Metric 1 | TBD | TBD | TBD |
| Metric 2 | TBD | TBD | TBD |

---

## 5. Stakeholders

### Primary Stakeholders

**Cross-Platform Development Fundamentals Owner**:
- **Owner**: Victor
- **Responsibilities**:
  - Maintain SAP artifacts and documentation
  - Review community feedback
  - Coordinate with related SAP owners
  
  - Coordinate with dependencies: SAP-000
  

**Primary Users**:
- <!-- TODO: Define primary user roles and their needs -->
- AI agents (Claude, other LLMs)
- Development teams
- Technical leaders

### Secondary Stakeholders

**Related SAP Maintainers**:


- **SAP-000**: [Integration point description]



**Community**:
- chora-base adopters
- Ecosystem contributors
- External users

---

## 6. Dependencies

### Required SAP Dependencies



- **SAP-000**: [Why this dependency is required]



### Optional SAP Dependencies

<!-- TODO: List optional dependencies that enhance this SAP -->
- [Optional dependency and benefit]

### External Dependencies

**Required**:
- <!-- TODO: List required external tools, libraries, services -->
- Python 3.9+ / Node.js 22+ / [Technology stack]

**Optional**:
- <!-- TODO: List optional external integrations -->

---

## 7. Constraints & Assumptions

### Constraints

<!-- TODO: List technical, organizational, or resource constraints -->

1. **Constraint 1**: [Description]
2. **Constraint 2**: [Description]
3. **Constraint 3**: [Description]

### Assumptions

<!-- TODO: List assumptions about users, environment, capabilities -->

1. **Assumption 1**: [Description]
2. **Assumption 2**: [Description]
3. **Assumption 3**: [Description]

---

## 8. Risks & Mitigations

### Risk 1: [Risk Name]

**Risk**: [Description of the risk]

**Likelihood**: Low / Medium / High
**Impact**: Low / Medium / High

**Mitigation**:
- [Mitigation strategy 1]
- [Mitigation strategy 2]
- [Mitigation strategy 3]

### Risk 2: [Risk Name]

**Risk**: [Description of the risk]

**Likelihood**: Low / Medium / High
**Impact**: Low / Medium / High

**Mitigation**:
- [Mitigation strategy 1]
- [Mitigation strategy 2]

### Risk 3: [Risk Name]

**Risk**: [Description of the risk]

**Likelihood**: Low / Medium / High
**Impact**: Low / Medium / High

**Mitigation**:
- [Mitigation strategy 1]
- [Mitigation strategy 2]

---

## 9. Lifecycle

### Development Phase
**Status**: ⏳ **Planned**
**Target Completion**: [Date]

**Milestones**:
- [ ] SAP catalog entry created
- [ ] capability-charter.md (this document)
- [ ] protocol-spec.md (technical contracts)
- [ ] awareness-guide.md (AI agent guidance)
- [ ] adoption-blueprint.md (installation guide)
- [ ] ledger.md (adoption tracking)

### Pilot Phase
**Status**: ⏳ **Planned**
**Target Start**: [Date]
**Duration**: 1-2 weeks

**Activities**:
- Install SAP in 2-3 test projects
- Measure adoption time (target: documented estimates)
- Agent execution validation
- Collect feedback from early adopters
- Iterate on documentation

### Active Phase
**Status**: ⏳ **Planned**
**Target Start**: [Date]

**Ongoing Activities**:
- Quarterly reviews and updates
- Community feedback integration
- Ledger maintenance (adoption tracking)

- Integration with SAP-000


### Maintenance Phase

**Maintenance SLA**:
- Critical issues: 24-48 hours
- Major updates: 1-2 weeks
- Minor updates: Quarterly batch updates
- Documentation improvements: Ad-hoc

---

## 10. Related Documents

### Within chora-base

**SAP Artifacts**:
- [Protocol Specification](./protocol-spec.md) - Technical contracts for Cross-Platform Development Fundamentals
- [Awareness Guide](./awareness-guide.md) - AI agent quick reference
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step installation
- [Traceability Ledger](./ledger.md) - Version history and adoption tracking

**Related SAPs**:
- [SAP-000: SAP Framework](../sap-framework/capability-charter.md) - Core SAP protocols


- [SAP-000: [Name]](../[directory]/capability-charter.md) - [Relationship]



**SAP Catalog**:
- [sap-catalog.json](../../../sap-catalog.json) - Machine-readable SAP registry

### External Documentation

<!-- TODO: Link to relevant external resources -->

**Official Documentation**:
- [External resource 1](https://example.com) - [Description]
- [External resource 2](https://example.com) - [Description]

**Community Resources**:
- [Community resource 1](https://example.com) - [Description]

---

## 11. Approval & Sign-Off

**Charter Author**: Victor
**Date**: 2025-11-03
**Version**: 1.0.0

**Approval Status**: ⏳ **Pilot**

**Review Cycle**:
- **Next Review**: [Date]
- **Review Frequency**: Quarterly

**Change Log**:
- 2025-11-03: Initial charter (1.0.0) - Victor

---

**Version History**:
- **1.0.0** (2025-11-03): Initial charter for Cross-Platform Development Fundamentals