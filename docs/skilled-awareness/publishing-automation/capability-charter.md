# Capability Charter: Publishing Automation

**SAP ID**: SAP-028
**Version**: 1.0.0
**Status**: pilot
**Owner**: Victor
**Created**: 2025-11-02
**Last Updated**: 2025-11-02

---

## 1. Problem Statement

### Current Challenge

Python projects using long-lived PyPI API tokens face security risks: token leakage, broad permissions, manual rotation burden, and no provenance tracking.

Current challenge: Static templates default to token-based publishing, requiring developers to manually configure OIDC trusted publishing despite it being the industry best practice since 2023.

Developers face: secret management overhead, rotation fatigue, audit complexity, and lack of build attestations (PEP 740).

### Evidence



- PyPI introduced OIDC trusted publishing in 2023 as recommended default

- PEP 740 attestations require trusted publishing for build provenance

- Zero secrets management vs manual token rotation every 90 days

- GitHub/GitLab both support OIDC publishing workflows natively

- chora-compose migrated to trusted publishing (zero security incidents)



### Business Impact

Without publishing automation defaults:

- Security risk: Long-lived tokens in GitHub Secrets vulnerable to leakage
- Operational burden: Manual token rotation, expiry management, permission audits
- Compliance gaps: No build provenance (PEP 740), limited audit trail
- Developer friction: Additional setup steps, secret configuration, troubleshooting
- Ecosystem inconsistency: Generated projects use outdated publishing patterns

---

## 2. Proposed Solution

### Publishing Automation

SAP-028 provides secure PyPI publishing with OIDC trusted publishing as the default method for all chora-base generated projects.

Key capabilities: OIDC trusted publishing (zero secrets), token-based fallback (backward compat), PEP 740 attestations (build provenance), GitHub Actions release workflow, template variable (pypi_auth_method), migration guide (token → OIDC).

Setup time: 5 minutes for new projects (PyPI publisher configuration), 15 minutes for migrations.

### Key Principles



- Security-first: OIDC trusted publishing as default (zero secrets)

- Zero trust: Fine-grained GitHub → PyPI trust relationship per repository

- Provenance: PEP 740 attestations for supply chain security

- Backward compatible: Token-based publishing still supported for legacy workflows

- Template-driven: pypi_auth_method variable controls publishing method

- Migration support: Clear upgrade path from token → trusted publishing



---

## 3. Scope

### In Scope



- OIDC trusted publishing configuration (GitHub Actions → PyPI)

- Token-based publishing fallback (PYPI_API_TOKEN secret)

- PEP 740 attestation generation (build provenance)

- Release workflow template (.github/workflows/release.yml)

- PyPI setup documentation (PYPI_SETUP.md)

- Migration guide (token → trusted publishing)



### Out of Scope



- Non-PyPI registries (Artifactory, Nexus) - Future enhancement

- Non-GitHub CI platforms (GitLab, Bitbucket) - Future enhancement

- Automated version bumping - Covered by SAP-005 (CI/CD)

- Changelog generation - Covered by SAP-005 (CI/CD)



---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Level 1):
- OIDC trusted publishing configured on PyPI for one project
- First successful publish to PyPI using OIDC (zero secrets)
- PEP 740 attestations generated automatically
- Setup time: ≤5 minutes for new projects, ≤15 minutes for migrations
- Zero security incidents related to token leakage

**Adoption Success** (Level 2):
- Token-based projects migrated to OIDC trusted publishing
- Multi-project adoption (2+ repositories using OIDC)
- Build provenance verification working (PEP 740 attestations validated)
- Migration documentation complete with troubleshooting guide
- Backward compatibility maintained (token fallback tested)

**Adoption Success** (Level 3):
- Organization-wide OIDC adoption (5+ projects)
- Security audit passed (zero long-lived tokens in use)
- Advanced security monitoring (attestation verification automated)
- Community best practices documented and shared
- Cross-platform support (GitHub + GitLab OIDC)

### Key Metrics

| Metric | Baseline (Token-based) | Target (Level 2) | Target (Level 3) |
|--------|------------------------|------------------|------------------|
| **Setup Time** | 30 minutes (manual token) | 5 minutes (OIDC new) / 15 minutes (migration) | 5 minutes |
| **Token Rotation Burden** | Every 90 days (manual) | Never (zero secrets) | Never |
| **Security Incidents** | Variable (token leaks) | 0 incidents | 0 incidents |
| **Build Provenance** | None | PEP 740 attestations (100%) | PEP 740 + verification |
| **Secret Management** | Manual (GitHub Secrets) | Automatic (OIDC trust) | Automatic |
| **Migration Time** | N/A | ≤15 minutes per project | ≤10 minutes |
| **Audit Trail** | Limited | Complete (OIDC logs) | Complete + monitoring |
| **Publishing Success Rate** | Variable | ≥99.5% | ≥99.9% |

---

## 5. Stakeholders

### Primary Stakeholders

**Publishing Automation Owner**:
- **Owner**: Victor
- **Responsibilities**:
  - Maintain SAP artifacts and documentation
  - Review community feedback
  - Coordinate with related SAP owners
  
  - Coordinate with dependencies: SAP-003, SAP-005
  

**Primary Users**:
- <!-- TODO: Define primary user roles and their needs -->
- AI agents (Claude, other LLMs)
- Development teams
- Technical leaders

### Secondary Stakeholders

**Related SAP Maintainers**:


- **SAP-003**: [Integration point description]

- **SAP-005**: [Integration point description]



**Community**:
- chora-base adopters
- Ecosystem contributors
- External users

---

## 6. Dependencies

### Required SAP Dependencies



- **SAP-003**: [Why this dependency is required]

- **SAP-005**: [Why this dependency is required]



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

- Integration with SAP-003, SAP-005


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
- [Protocol Specification](./protocol-spec.md) - Technical contracts for Publishing Automation
- [Awareness Guide](./awareness-guide.md) - AI agent quick reference
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step installation
- [Traceability Ledger](./ledger.md) - Version history and adoption tracking

**Related SAPs**:
- [SAP-000: SAP Framework](../sap-framework/capability-charter.md) - Core SAP protocols


- [SAP-003: [Name]](../[directory]/capability-charter.md) - [Relationship]

- [SAP-005: [Name]](../[directory]/capability-charter.md) - [Relationship]



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
**Date**: 2025-11-02
**Version**: 1.0.0

**Approval Status**: ⏳ **Pilot**

**Review Cycle**:
- **Next Review**: [Date]
- **Review Frequency**: Quarterly

**Change Log**:
- 2025-11-02: Initial charter (1.0.0) - Victor

---

**Version History**:
- **1.0.0** (2025-11-02): Initial charter for Publishing Automation