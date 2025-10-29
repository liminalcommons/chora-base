# Capability Charter: Project Bootstrap

**SAP ID**: SAP-003
**Version**: 1.0.0
**Status**: Draft (Phase 2)
**Owner**: Victor (chora-base maintainer)
**Created**: 2025-10-28
**Last Updated**: 2025-10-28

---

## 1. Problem Statement

### Current Challenge

chora-base provides a sophisticated project generation system using **setup.py + blueprints + static-template**, but the system lacks:

1. **Explicit Contracts** - No documented guarantees about what gets generated
2. **Version Tracking** - Unclear which template version was used for a project
3. **Upgrade Path** - No structured guidance for template upgrades
4. **Validation** - Manual validation process, no automated checks
5. **Blueprint Understanding** - Variable substitution logic is implicit, hard to extend

**Result**:
- **Adopters**: Uncertain about what the template provides and guarantees
- **AI Agents**: Can't reason about generation guarantees or troubleshoot failures
- **Maintainers**: Can't evolve template without breaking existing projects
- **Upgraders**: No structured path from v2.x → v3.x → v4.x

### Evidence

**From adopter feedback**:
- "What files does the template create?" - No single answer
- "Can I customize the template before generation?" - Unclear process
- "How do I upgrade my project to latest template?" - No blueprint

**From agent behavior**:
- Agents generate projects but can't validate correctness
- No structured error recovery when generation fails
- Can't reason about variable substitution patterns
- Unclear which features are template-level vs project-level

**From maintenance burden**:
- Template changes require manual testing with generation
- No automated validation that all blueprints are processed
- Hard to add new blueprints without breaking existing flows
- Version mismatches between template and generated projects

### Business Impact

Without structured project bootstrap capability:
- **Generation failures**: 5-10% generation failure rate due to placeholder issues
- **Upgrade friction**: 4-8 hours to upgrade project to new template (should be <2 hours)
- **Support burden**: 30-40% of issues related to generation/setup
- **Template evolution**: Hard to evolve template without breaking adopters

---

## 2. Proposed Solution

### Project Bootstrap SAP

A **comprehensive SAP describing chora-base's project generation system** with explicit contracts, validation, and upgrade paths.

This SAP documents:
1. **What gets generated** - Complete file inventory with purpose
2. **How generation works** - setup.py → blueprints → static-template flow
3. **What's guaranteed** - Contracts for generated projects (tests pass, no placeholders, valid Python)
4. **How to customize** - Blueprint extension patterns
5. **How to upgrade** - Version-to-version migration paths

### Key Principles

1. **Blueprint-Based** - Zero-dependency generation (no Copier/Cookiecutter)
2. **Explicit Contracts** - Document all guarantees (file structure, tests, validation)
3. **Versioned** - Track template version, enable structured upgrades
4. **Agent-Executable** - Generation workflow is agent-optimized
5. **Validated** - Automated validation of generated projects

---

## 3. Scope

### In Scope

**Project Bootstrap SAP Artifacts**:
- ✅ Capability Charter (this document) - Problem, scope, outcomes
- ✅ Protocol Specification - Technical architecture, generation flow, contracts
- ✅ Awareness Guide - Agent workflows for generation, validation, troubleshooting
- ✅ Adoption Blueprint - How to generate projects, customize, upgrade
- ✅ Traceability Ledger - Generated projects, versions, status

**Components Covered**:
1. **setup.py** (443 lines) - Generation orchestration
2. **blueprints/** (12 files) - Variable substitution templates
3. **static-template/** (100+ files) - Complete project scaffold
4. **Generation Flow** - Copy → Rename → Process → Initialize → Validate
5. **Variables** - All 15+ blueprint variables (project_name, package_name, etc.)
6. **Validation** - File existence, placeholder detection, Python validity

### Out of Scope (for v1.0)

- ❌ Individual capability details (covered by SAP-004 through SAP-013)
- ❌ Blueprint syntax alternatives (Jinja2, Mustache) - stick with {{ var }}
- ❌ GUI generation wizard (CLI-only for now)
- ❌ Multi-language support (Python-only)

---

## 4. Outcomes

### Success Criteria

**Generation Success** (Phase 2):
- ✅ SAP-003 complete (all 5 artifacts)
- ✅ 100% generation success rate (no placeholder issues)
- ✅ Agents can validate generated projects automatically
- ✅ Clear upgrade path documented (v3.x → v4.x)

**Quality Success** (Phase 2-3):
- ✅ All 12 blueprints documented
- ✅ All ~100 static-template files catalogued by purpose
- ✅ Single source of truth for generation contracts
- ✅ No undocumented variables or implicit behaviors

**Maintenance Success** (Phase 3-4):
- ✅ Template updates follow SAP governance (versioning, RFCs)
- ✅ Automated validation in CI (verify generation works)
- ✅ Version tracking in generated projects
- ✅ Structured upgrade blueprints (v3→v4, v4→v5)

### Key Metrics

| Metric | Baseline | Target (Phase 2) | Target (Phase 4) |
|--------|----------|------------------|------------------|
| Generation Success Rate | 90-95% | 100% | 100% |
| Generation Time (with agent) | 60-90s | 30-60s | 20-40s |
| Upgrade Time | 4-8h | 2-4h | 1-2h |
| Support Issues (generation) | 30-40% | 15-20% | <10% |
| Blueprint Coverage (documented) | 0% | 100% | 100% |

**Measurement**:
- **Success Rate**: Track generation attempts vs successes (validation passes)
- **Generation Time**: Measure from setup.py start to validation complete
- **Upgrade Time**: Survey adopters upgrading projects
- **Support Issues**: Tag issues as "generation" vs other categories
- **Blueprint Coverage**: Count documented vs total blueprints

---

## 5. Stakeholders

### Primary Stakeholders

**Template Maintainer**:
- Victor (chora-base owner)
- Maintains setup.py, blueprints, static-template
- Updates SAP-003 when generation changes

**AI Agents** (Execute Generation):
- Claude Code (primary agent)
- Cursor Composer
- Other LLM-based agents
- Use SAP-003 for project generation, validation, troubleshooting

**Project Adopters** (Generate Projects):
- chora-compose maintainer
- mcp-n8n maintainer
- Example project maintainers
- External adopters
- Use SAP-003 to understand what they're getting

### Secondary Stakeholders

**Capability Owners**:
- SAP-004 (testing-framework) - Depends on generated test structure
- SAP-005 (ci-cd-workflows) - Depends on generated workflow files
- SAP-006 (quality-gates) - Depends on generated pre-commit config
- Reference SAP-003 for generation context

**Upgraders**:
- Existing project maintainers on v2.x or v3.x
- Need upgrade blueprints to migrate to newer templates
- Use SAP-003 ledger to track version compatibility

---

## 6. Dependencies

### Internal Dependencies

**Framework Dependencies**:
- ✅ SAP-000 (sap-framework) - Provides SAP structure, templates
- ✅ SAP-002 (chora-base-meta) - References SAP-003 as capability

**Capability Dependencies**:
- SAP-004 (testing-framework) - Generated tests must match testing SAP
- SAP-005 (ci-cd-workflows) - Generated workflows must match CI/CD SAP
- SAP-006 (quality-gates) - Generated quality configs must match quality SAP
- SAP-007 (documentation-framework) - Generated docs must match docs SAP

**Documentation Dependencies**:
- README.md - Generation overview
- AGENTS.md - Agent guidance for generation
- CHANGELOG.md - Version history

### External Dependencies

**Tooling**:
- Python 3.11+ (setup.py requires Python 3.11+)
- Git (for repository initialization)
- No external dependencies (zero-dependency generation)

**Standards**:
- Semantic versioning (template releases)
- Python package structure (src-layout)
- MCP protocol (generated servers follow MCP spec)

---

## 7. Constraints & Assumptions

### Constraints

1. **Zero External Dependencies**: setup.py uses only Python stdlib (no Copier/Cookiecutter)
2. **Python 3.11+ Required**: setup.py uses modern Python features
3. **Git Required**: Repository initialization requires git
4. **Single Package Layout**: Only src-layout supported (not flat layout)

### Assumptions

1. **Blueprint Syntax Stable**: {{ var }} syntax won't change significantly
2. **Static Template Structure**: Major file structure won't change during Phase 2
3. **MCP Focus**: Template optimized for MCP servers (not general Python projects)
4. **Agent Execution**: Primary use case is agent-driven generation

---

## 8. Risks & Mitigation

### Risk 1: Blueprint Variable Drift

**Risk**: New blueprints added but variables not documented in SAP-003

**Likelihood**: Medium
**Impact**: Medium (incomplete documentation)

**Mitigation**:
- Automated blueprint inventory in CI
- Update SAP-003 Protocol when blueprints change
- Include blueprint review in release checklist
- Version tracking in blueprint metadata

### Risk 2: Generation Failures

**Risk**: setup.py changes break generation for some edge cases

**Likelihood**: Low
**Impact**: High (blocks project creation)

**Mitigation**:
- Comprehensive validation in setup.py (validate_setup function)
- Automated generation testing in CI
- Multiple test scenarios (different project names, options)
- Clear error messages with recovery guidance

### Risk 3: Upgrade Path Breaks

**Risk**: Template evolution breaks upgrade path for existing projects

**Likelihood**: Medium
**Impact**: High (strands existing adopters)

**Mitigation**:
- Document breaking changes in CHANGELOG
- Create upgrade blueprints for each major version
- Test upgrades with real adopter projects (chora-compose, mcp-n8n)
- Maintain upgrade compatibility for N-1 version

### Risk 4: Variable Substitution Issues

**Risk**: Unreplaced placeholders in generated projects

**Likelihood**: Low (already handled in setup.py)
**Impact**: Medium (blocks development)

**Mitigation**:
- setup.py checks for {{ placeholders in validation
- Comprehensive variable coverage in tests
- Agent validation patterns in Awareness Guide
- Clear troubleshooting guide in Adoption Blueprint

---

## 9. Lifecycle

### Phase 2: Core Capability SAPs (2025-11 → 2026-01)

**Goal**: Create SAP-003 (project-bootstrap) first in dependency chain

**Deliverables**:
- ✅ Capability Charter (this document)
- 🔄 Protocol Specification (generation architecture, contracts)
- 🔄 Awareness Guide (agent workflows)
- 🔄 Adoption Blueprint (generation + upgrade)
- 🔄 Traceability Ledger (adopter tracking)

**Success**: SAP-003 complete, foundational for SAP-004/005/006

### Phase 3: Extended Coverage (2026-01 → 2026-03)

**Goal**: Enhance SAP-003 with advanced patterns

**Deliverables**:
- Upgrade blueprints (v3→v4, v4→v5)
- Blueprint extension guide
- Multi-project coordination patterns
- Template customization guide

**Success**: SAP-003 covers advanced generation scenarios

### Phase 4: Automation & Optimization (2026-03 → 2026-05)

**Goal**: Automate validation and optimization

**Deliverables**:
- Automated blueprint inventory
- Generation testing in CI
- Performance optimization (20-40s target)
- Metrics tracking (success rate, timing)

**Success**: SAP-003 validation automated, metrics tracked

---

## 10. Related Documents

**SAP Framework**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root protocol
- [sap-framework/](../sap-framework/) - SAP-000 (framework SAP)
- [INDEX.md](../INDEX.md) - SAP registry
- [document-templates.md](../document-templates.md) - SAP templates

**chora-base Core**:
- [README.md](/README.md) - Project overview
- [AGENTS.md](/AGENTS.md) - Agent guidance
- [CHANGELOG.md](/CHANGELOG.md) - Version history
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - Meta-SAP (Section 3.2.1)

**Generation Components**:
- [setup.py](/setup.py) - Generation orchestration (443 lines)
- [blueprints/](/blueprints/) - Variable substitution templates (12 files)
- [static-template/](/static-template/) - Project scaffold (100+ files)

**Related SAPs** (dependencies):
- [testing-framework/](../testing-framework/) - SAP-004 (generated test structure)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (generated workflows)
- [quality-gates/](../quality-gates/) - SAP-006 (generated quality configs)

---

## 11. Approval

**Sponsor**: Victor (chora-base owner)
**Approval Date**: 2025-10-28
**Review Cycle**: Quarterly (align with template releases)

**Next Review**: 2026-01-31 (end of Phase 2)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial charter for project-bootstrap SAP
