# Capability Charter: Cross-Platform Python Environments

**SAP ID**: SAP-031
**Version**: 1.0.0
**Status**: pilot
**Owner**: Victor
**Created**: 2025-11-03
**Last Updated**: 2025-11-03

---

## 1. Problem Statement

### Current Challenge

Python environment setup varies dramatically across platforms: pyenv on macOS/Linux, py launcher on Windows, system packages on Linux, and different activation scripts (.venv/bin/activate vs .venv\Scripts\activate).

Current challenge: No standardized Python environment guidance leads to 'Python not found' errors, PATH issues on Windows, virtual environment activation confusion, and platform-specific dependency problems.

Developers face: onboarding friction, inconsistent Python versions across team, venv activation failures, and platform-specific quirks (Windows symlinks disabled, macOS Framework vs unix builds).

### Evidence



- chora-base requires Python 3.11+ but no installation guidance by platform

- SAP-029 UTF-8 encoding issue on Windows (PYTHONIOENCODING workaround)

- Virtual environment activation syntax differs (bin/activate vs Scripts\activate)

- Windows symlinks disabled by default (affects venv, node_modules)

- No systematic Python version validation across platforms



### Business Impact

Without Python environment standardization:

- Onboarding friction: 1-2 hours troubleshooting 'Python not found' errors
- Version inconsistency: Developers using Python 3.8-3.13 causing compatibility issues
- Windows-specific failures: UTF-8 encoding errors, symlink issues, PATH problems
- macOS-specific issues: Gatekeeper blocking pyenv installations, Framework build conflicts
- Linux system Python conflicts: Breaking system packages with user installations

---

## 2. Proposed Solution

### Cross-Platform Python Environments

SAP-031 provides comprehensive Python environment management patterns for all platforms.

Key capabilities: Python installation guides (pyenv/py launcher/system packages by platform), venv creation and activation (cross-platform examples), Python version matrix (3.11-3.13 support), platform-specific quirks documentation, check-python-env.py validation utility.

Setup time: 15-30 minutes for Python environment setup per platform, 5 minutes to run validation.

### Key Principles



- Use python -m venv: Works everywhere, no virtualenv dependency

- Support Python 3.11-3.13: Test matrix across all supported versions

- Platform-specific installation: pyenv (Mac/Linux), py launcher (Windows)

- Validate before build: check-python-env.py catches setup issues early

- Document quirks: Windows symlinks, macOS Framework builds, Linux system Python

- UTF-8 by default: PYTHONIOENCODING=utf-8 for Windows scripts



---

## 3. Scope

### In Scope



- Python installation guides (pyenv, py launcher, system packages)

- Virtual environment creation (python -m venv .venv)

- Cross-platform activation examples (bin/activate vs Scripts\activate)

- Python version matrix (3.11, 3.12, 3.13 support)

- Platform-specific quirks (Windows/macOS/Linux)

- check-python-env.py validation utility



### Out of Scope



- Poetry/pipenv support - Focus on standard pip + pyproject.toml

- Conda environments - Not chora-base's primary tooling

- Python 2.x or <3.11 support - Unsupported versions

- Docker Python environments - Covered by SAP-011



---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Level 1):
- <!-- TODO: Define Level 1 adoption success criteria -->
- SAP-031 installed (5 artifacts present)
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

**Cross-Platform Python Environments Owner**:
- **Owner**: Victor
- **Responsibilities**:
  - Maintain SAP artifacts and documentation
  - Review community feedback
  - Coordinate with related SAP owners
  
  - Coordinate with dependencies: SAP-000, SAP-030
  

**Primary Users**:
- <!-- TODO: Define primary user roles and their needs -->
- AI agents (Claude, other LLMs)
- Development teams
- Technical leaders

### Secondary Stakeholders

**Related SAP Maintainers**:


- **SAP-000**: [Integration point description]

- **SAP-030**: [Integration point description]



**Community**:
- chora-base adopters
- Ecosystem contributors
- External users

---

## 6. Dependencies

### Required SAP Dependencies



- **SAP-000**: [Why this dependency is required]

- **SAP-030**: [Why this dependency is required]



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

- Integration with SAP-000, SAP-030


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
- [Protocol Specification](./protocol-spec.md) - Technical contracts for Cross-Platform Python Environments
- [Awareness Guide](./awareness-guide.md) - AI agent quick reference
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step installation
- [Traceability Ledger](./ledger.md) - Version history and adoption tracking

**Related SAPs**:
- [SAP-000: SAP Framework](../sap-framework/capability-charter.md) - Core SAP protocols


- [SAP-000: [Name]](../[directory]/capability-charter.md) - [Relationship]

- [SAP-030: [Name]](../[directory]/capability-charter.md) - [Relationship]



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
- **1.0.0** (2025-11-03): Initial charter for Cross-Platform Python Environments