# Capability Charter: Example Capability for Pilot

**SAP ID**: SAP-029
**Version**: 1.0.0
**Status**: draft
**Owner**: Victor
**Created**: 2025-11-10
**Last Updated**: 2025-11-10

---

## 1. Problem Statement

### Current Challenge

Creating SAPs manually is time-consuming and error-prone. Each SAP requires 5 artifacts with overlapping structure, leading to 10 hours of work per SAP.

Current challenge: No automated way to generate SAP artifacts from metadata, resulting in inconsistent structure, manual duplication, and slow SAP creation velocity.

Developers face: writing repetitive sections, maintaining consistency across 5 files, and tracking TODO placeholders.

### Evidence



- Manual SAP creation takes 10 hours on average

- 28 existing SAPs with 5 artifacts each = 140 files

- chora-compose achieved 9x efficiency with dogfooding pattern

- Week 1 analysis identified 80% structure automation opportunity



### Business Impact

Without SAP generation automation:

- Slow velocity: 10 hours per SAP limits creation speed
- Inconsistency: Manual creation leads to structural variations
- Maintenance burden: Updates require touching 5 files per SAP
- Adoption friction: High effort discourages SAP creation

---

## 2. Proposed Solution

### Example Capability for Pilot

SAP-029 provides template-based SAP generation using Jinja2 templates and sap-catalog.json metadata.

Key capabilities: 5 Jinja2 templates (one per artifact), MVP schema (9 generation fields), automatic structure generation, placeholder comments for manual content.

Setup time: 7-11 hours one-time investment, 2 hours per SAP after (80% time savings).

### Key Principles



- 80/20 automation: Automate structure (80%), manual content (20%)

- Template-first: Jinja2 templates define consistent structure

- Metadata-driven: sap-catalog.json as single source of truth

- Placeholder guidance: TODO comments guide manual content

- Progressive enhancement: Start with MVP, expand schema over time

- Validation integration: Generated artifacts validate with sap-evaluator.py



---

## 3. Scope

### In Scope



- Jinja2 template system (5 templates for 5 artifacts)

- MVP generation schema (9 fields: owner, created_date, problem, evidence, impact, solution, principles, in_scope, out_of_scope, one_sentence_summary)

- Generator script (scripts/generate-sap.py)

- Test data and validation

- Documentation (week-1 and week-2 plans)



### Out of Scope



- Full schema automation (30+ fields) - Post-pilot enhancement

- INDEX.md auto-update - Week 3 feature

- justfile integration - Week 3 feature

- Cross-SAP dependency analysis - Future enhancement

- Content pre-fill beyond MVP fields - Post-pilot



---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Level 1):
- <!-- TODO: Define Level 1 adoption success criteria -->
- SAP-029 installed (5 artifacts present)
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

**Example Capability for Pilot Owner**:
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
- [Protocol Specification](./protocol-spec.md) - Technical contracts for Example Capability for Pilot
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
**Date**: 2025-11-10
**Version**: 1.0.0

**Approval Status**: ⏳ **Draft**

**Review Cycle**:
- **Next Review**: [Date]
- **Review Frequency**: Quarterly

**Change Log**:
- 2025-11-10: Initial charter (1.0.0) - Victor

---

**Version History**:
- **1.0.0** (2025-11-10): Initial charter for Example Capability for Pilot