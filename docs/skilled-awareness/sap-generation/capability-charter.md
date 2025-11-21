# Capability Charter: SAP Generation Automation

**SAP ID**: SAP-029
**Version**: 1.0.0
**Status**: pilot
**Owner**: Victor
**Created**: 2025-11-02
**Last Updated**: 2025-11-02

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

### SAP Generation Automation

SAP-029 provides template-based SAP generation using Jinja2 templates and sap-catalog.json metadata.

Key capabilities: 5 Jinja2 templates (one per artifact), MVP schema (9 generation fields), automatic structure generation, placeholder comments for manual content, INDEX.md auto-update, validation integration.

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

- INDEX.md auto-update functionality

- Validation integration with sap-evaluator.py

- justfile recipes for automation



### Out of Scope



- Full schema automation (30+ fields) - Post-pilot enhancement

- Content pre-fill beyond MVP fields - Future enhancement

- Multi-SAP batch generation - Future feature

- Custom template support - Future feature



---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Level 1):
- Generate first production SAP successfully (SAP-029 or similar)
- All 5 artifacts present and pass validation (sap-evaluator.py)
- INDEX.md automatically updated with correct coverage stats
- Time savings: ≤5 minutes for generation phase (vs 10 hours manual)
- Setup time: ≤11 hours (one-time investment: 8.5h setup + first SAP)

**Adoption Success** (Level 2):
- Generate 2+ production SAPs successfully across different domains
- Zero critical bugs across multiple SAP generations
- Manual TODO fill time: ≤4 hours per SAP
- Template consistency validated (meta vs technical SAPs)
- ROI positive after 2nd SAP (cumulative savings > setup investment)

**Adoption Success** (Level 3):
- Generate 5+ production SAPs with extended schema (15-20 fields)
- Batch generation workflow established (multiple SAPs per command)
- Domain-specific template variants implemented (meta/technical/UI)
- Community adoption: 3+ projects using generator in chora ecosystem
- Continuous improvement: Schema expansions and template refinements deployed

### Key Metrics

| Metric | Baseline (Manual) | Target (Level 2) | Target (Level 3) |
|--------|-------------------|------------------|------------------|
| **SAP Creation Time** | 10 hours | ≤2 hours (5x savings) | ≤1 hour (10x savings) |
| **Structure Generation** | 6-8 hours | ≤5 minutes (120x savings) | ≤5 minutes |
| **Validation Time** | 30 minutes | ≤30 seconds (60x savings) | ≤30 seconds |
| **Time Savings Multiple** | 1x (baseline) | 5x minimum | 10x+ goal |
| **Developer Satisfaction** | N/A | ≥85% (4.25/5) | ≥90% (4.5/5) |
| **Zero Critical Bugs** | N/A | 0 bugs (2 SAPs) | 0 bugs (5+ SAPs) |
| **TODO Count** | N/A | 60-105 per SAP | 30-50 per SAP (extended schema) |
| **Manual Fill Time** | 10 hours | 2-4 hours | 1-2 hours |

---

## 5. Stakeholders

### Primary Stakeholders

**SAP Generation Automation Owner**:
- **Owner**: Victor
- **Responsibilities**:
  - Maintain SAP artifacts and documentation
  - Review community feedback
  - Coordinate with related SAP owners
  
  - Coordinate with dependencies: SAP-000
  

**Primary Users**:
- **SAP Authors**: Need to create new SAPs quickly (10 hours → 2 hours) while maintaining consistency with SAP-000 framework structure
- **AI Agents (Claude, other LLMs)**: Need template-based generation commands and TODO-guided content fill workflows
- **Development Teams**: Need consistent SAP artifacts across projects, reducing onboarding time and documentation debt
- **Technical Leaders**: Need SAP velocity metrics, quality gates, and adoption tracking to measure documentation ROI

### Secondary Stakeholders

**Related SAP Maintainers**:

- **SAP-000 (SAP Framework)**: SAP-029 consumes SAP-000's 5-artifact structure specification (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger) as the template foundation. Changes to SAP-000 artifact requirements necessitate template updates in SAP-029.



**Community**:
- chora-base adopters
- Ecosystem contributors
- External users

---

## 6. Dependencies

### Required SAP Dependencies

- **SAP-000 (SAP Framework)**: Required because SAP-029 generates artifacts conforming to SAP-000's 5-artifact specification. Without SAP-000, there's no structure definition for templates to follow. SAP-029 validates generated artifacts against SAP-000's protocol-spec.md requirements.



### Optional SAP Dependencies

- **SAP-019 (Self-Evaluation)**: Enhances SAP-029 by providing automated validation of generated artifacts (structure completeness, link integrity, TODO count). Recommended for Level 2+ adoption.
- **SAP-005 (CI/CD Workflows)**: Enables Level 3 adoption with automated SAP generation pipelines triggered on sap-catalog.json updates. Quality gates enforce TODO thresholds before production deployment.
- **SAP-016 (Link Validation)**: Validates internal/external links in generated artifacts, preventing broken references in capability-charter and protocol-spec files.
- **SAP-027 (Dogfooding Patterns)**: Provides 6-week pilot methodology to validate SAP-029's effectiveness before ecosystem recommendation. Used to measure time savings and satisfaction metrics.

### External Dependencies

**Required**:
- **Python 3.8+**: Runtime for generation script (scripts/generate-sap.py) and template rendering
- **Jinja2 3.0+**: Template engine for rendering SAP artifacts from templates/sap/*.j2 files
- **sap-catalog.json**: Metadata source of truth containing 9+ MVP fields per SAP
- **Git**: Version control for tracking generated artifacts and template changes

**Optional**:
- **jq**: JSON query tool for sap-catalog.json manipulation and validation (enhances CLI workflows)
- **GitHub Actions**: CI/CD platform for Level 3 automated generation pipelines
- **pre-commit hooks**: Enforce quality gates (TODO threshold, link validation) before commits
- **VSCode + Jinja2 extension**: Syntax highlighting and validation for template editing

---

## 7. Constraints & Assumptions

### Constraints

1. **Template Rigidity**: Jinja2 templates enforce SAP-000's 5-artifact structure. Custom artifact layouts require template forks, increasing maintenance burden. Workaround: Use extended schema fields for domain-specific customization within existing structure.
2. **Manual Content Required**: 80/20 rule means 20% of content (domain-specific details, integration patterns, error handling) must be manually filled post-generation. Cannot achieve 100% automation without sacrificing content quality and context-awareness.
3. **Single-Project Scope**: MVP targets chora-base's sap-catalog.json format. Multi-project support (different catalog schemas) requires adapter layer. Workaround: Fork sap-catalog.json schema for each project, maintain template compatibility manually.
4. **Jinja2 Dependency**: Template syntax tied to Jinja2. Migrating to different template engine (e.g., Handlebars, Liquid) requires full template rewrite. Mitigates by using minimal Jinja2 features (variables, loops, conditionals only).

### Assumptions

1. **SAP Authors Have Domain Expertise**: Assume SAP authors possess domain knowledge to fill 20% manual content (technical specs, integration patterns, error handling). If false: Generated SAPs remain at 60-80% completion, requiring subject matter expert review before production.
2. **SAP-000 Structure Stability**: Assume SAP-000's 5-artifact structure remains stable across versions. If SAP-000 adds 6th artifact (e.g., FAQ.md), requires template addition and regeneration of existing SAPs. Mitigates with template versioning (v1, v2) and backward compatibility.
3. **Python + Jinja2 Accessibility**: Assume Python 3.8+ and Jinja2 are acceptable dependencies for target users. If false (e.g., Node.js-only teams): Port generator to JavaScript (Handlebars templates) or provide Docker image to avoid local Python installation.
4. **Git-Based Workflow**: Assume users commit generated artifacts to git for version tracking. If false (e.g., wiki-based documentation): Generated artifacts lose provenance metadata (generation timestamp, schema version), complicating regeneration decisions.

---

## 8. Risks & Mitigations

### Risk 1: Template Drift from SAP-000 Specification

**Risk**: SAP-000's artifact requirements evolve (new sections, deprecated fields) while SAP-029 templates remain static, causing generated SAPs to fail validation or miss critical sections.

**Likelihood**: Medium
**Impact**: High (affects all future SAP generations)

**Mitigation**:
- Establish template versioning (v1.0, v1.1) tied to SAP-000 versions, documented in template frontmatter
- Automated template validation against SAP-000's protocol-spec.md (quarterly checks via CI/CD)
- SAP-000 change notifications trigger template review (subscribe to SAP-000 ledger updates)
- Maintain template changelog mapping SAP-000 versions to template versions

### Risk 2: Accidental Regeneration Overwrites Manual Content

**Risk**: User runs `generate-sap.py SAP-030 --force` after manually filling TODOs, losing hours of domain-specific content when templates overwrite existing files.

**Likelihood**: High (especially during onboarding)
**Impact**: Medium (per-SAP basis, recoverable via git)

**Mitigation**:
- Add YAML frontmatter to generated files: `regeneration_safe: false` (default), warning in capability-charter header
- Implement `--dry-run` flag showing diff before overwrite confirmation prompt
- Git pre-commit hook detects regeneration of files with `completion_status: complete`, requires manual override
- Documentation emphasizes "backup → regenerate → merge" workflow for post-manual-edit regeneration

### Risk 3: Low Adoption Due to High Setup Investment

**Risk**: Level 1 setup (10-11 hours) discourages teams from adopting SAP-029, preferring manual SAP creation despite long-term inefficiency. ROI positive after 1st SAP, but upfront cost creates adoption barrier.

**Likelihood**: Medium
**Impact**: Medium (limits SAP-029 ecosystem reach)

**Mitigation**:
- Provide pre-built Docker image eliminating Python + Jinja2 installation (setup: 10h → 30min)
- Create "Quick Start" guide highlighting break-even point (1st SAP: time-neutral, 2nd SAP onward: 5x savings)
- SAP-027 dogfooding pilot demonstrates 120x time savings to validate adoption claims
- Offer hosted generation service (SaaS) for teams unwilling to self-host, reducing setup to account creation (5min)

---

## 9. Lifecycle

### Development Phase
**Status**: ✅ **Completed**
**Completion Date**: 2025-11-02

**Milestones**:
- [x] SAP catalog entry created
- [x] capability-charter.md (this document)
- [x] protocol-spec.md (technical contracts)
- [x] awareness-guide.md (AI agent guidance)
- [x] adoption-blueprint.md (installation guide)
- [x] ledger.md (adoption tracking)

### Pilot Phase
**Status**: 🔄 **In Progress**
**Started**: 2025-11-02
**Target Completion**: 2025-12-13 (6-week pilot per SAP-027)

**Activities**:
- [x] Generate first production SAP (SAP-029 self-generated)
- [x] Generate second production SAP (SAP-028 publishing-automation)
- [x] Measure time savings (120x vs 5x target - exceeded)
- [x] Collect satisfaction metrics (5/5 rating)
- [ ] 2-3 months production data collection (for L3 promotion)
- [ ] Iterate on documentation based on dogfooding feedback

### Active Phase
**Status**: ⏳ **Planned**
**Target Start**: 2025-12-15 (post-pilot GO decision)

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
- [Protocol Specification](./protocol-spec.md) - Technical contracts for SAP Generation Automation
- [Awareness Guide](./awareness-guide.md) - AI agent quick reference
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step installation
- [Traceability Ledger](./ledger.md) - Version history and adoption tracking

**Related SAPs**:
- [SAP-000: SAP Framework](../sap-framework/capability-charter.md) - Core SAP protocols defining 5-artifact structure
- [SAP-027: Dogfooding Patterns](../dogfooding-patterns/capability-charter.md) - Validation methodology for SAP-029 pilot
- [SAP-019: Self-Evaluation](../self-evaluation/capability-charter.md) - Validation integration for generated artifacts

**SAP Lifecycle Integration**:

SAP-029 initiates the **5-SAP development lifecycle**, generating SAPs that flow through verification, integration, distribution, and evaluation:

- **SAP-029** (sap-generation) - Generate SAP artifacts from templates (this SAP)
- **SAP-050** (sap-adoption-verification) - Verify generated SAP structure and quality
- **SAP-061** (sap-ecosystem-integration) - Validate ecosystem integration points
- **SAP-062** (sap-distribution-versioning) - Distribute SAPs via Copier templates
- **SAP-019** (sap-self-evaluation) - Evaluate adoption depth and maturity

**Integration**: Generated SAPs from SAP-029 flow through SAP-050 verification, SAP-061 ecosystem integration validation, SAP-062 distribution via Copier, and SAP-019 adoption evaluation to complete the lifecycle.

**SAP Catalog**:
- [sap-catalog.json](../../../sap-catalog.json) - Machine-readable SAP registry

### External Documentation

**Official Documentation**:
- [Jinja2 Official Documentation](https://jinja.palletsprojects.com/en/3.1.x/) - Template engine syntax, filters, best practices for SAP-029 templates
- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/) - Reference for template-based project generation patterns (design inspiration for SAP-029)
- [Yeoman Generator Guide](https://yeoman.io/authoring/) - Alternative template system with scaffolding patterns (comparison for migration paths)
- [Python argparse](https://docs.python.org/3/library/argparse.html) - CLI argument parsing for generate-sap.py script

**Community Resources**:
- [Template Method Pattern](https://refactoring.guru/design-patterns/template-method) - Design pattern underlying SAP-029's template architecture
- [Semantic Versioning 2.0.0](https://semver.org/) - Versioning strategy for SAP-029 templates and generated artifacts

---

## 11. Approval & Sign-Off

**Charter Author**: Victor
**Date**: 2025-11-02
**Version**: 1.0.0

**Approval Status**: ⏳ **Pilot**

**Review Cycle**:
- **Next Review**: 2026-02-02 (3 months post-creation, post-pilot)
- **Review Frequency**: Quarterly

**Change Log**:
- 2025-11-02: Initial charter (1.0.0) - Victor

---

**Version History**:
- **1.0.0** (2025-11-02): Initial charter for SAP Generation Automation