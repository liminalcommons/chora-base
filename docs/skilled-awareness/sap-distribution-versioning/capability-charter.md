# SAP Distribution & Versioning: Capability Charter

**SAP ID**: SAP-062
**Version**: 1.0.0
**Status**: draft
**Last Updated**: 2025-11-20

---

## Problem Statement

**Real-World Example** (Trigger for SAP-062):

> During SAP-053 Phase 4 completion (2025-11-19), OPP-2025-022 identified a critical gap: the chora ecosystem lacks automated SAP distribution and versioning infrastructure. Current approach is entirely manual:
>
> - **Manual distribution**: Copy scripts, justfile recipes, docs from chora-base to new projects (10-15 min per SAP)
> - **Zero update propagation**: When SAPs improve (v1.0 → v1.1 → v2.0), existing projects don't get updates
> - **High adoption friction**: 50-70% of developers skip manual setup due to time investment
> - **No lifecycle management**: No formal versioning strategy, deprecation policy, or backward compatibility guidelines

**Root Causes**:
1. **Infrastructure Gap**: No project template/scaffolding tool for automated SAP distribution
2. **Organizational Gap**: SAP development lifecycle (SAP-050) documented structure verification but not distribution/versioning
3. **Cognitive Load Gap**: Developers must manually track SAP versions, dependencies, and compatibility
4. **Moving Target**: chora-base evolves continuously, but no mechanism to propagate improvements to existing projects

**Quantified Impact** (from OPP-2025-022 research):
- **Manual waste**: 10-15 min per SAP per project → 20-120 min per project (2-8 SAPs)
- **Adoption rate**: 30-50% (manual friction blocks adoption)
- **Update adoption**: 0-10% (no automated update mechanism)
- **Annual cost**: $7,500/year wasted (50 projects/year scenario @ $150/hr)

---

## Solution Overview

**SAP-062: SAP Distribution & Versioning** formalizes Copier-based template distribution and establishes semantic versioning practices for the chora ecosystem.

### Core Capabilities

**1. Copier Template Distribution**
- One-command project generation: `copier copy gh:liminalcommons/chora-base my-project`
- Conditional SAP inclusion via questionnaire (choose which SAPs to include)
- Post-generation hooks (git init, dependency install, configuration)
- Multi-tier selection (minimal/standard/comprehensive SAP bundles)

**2. Template Update Propagation**
- `copier update` command propagates SAP improvements to existing projects
- Smart merge handling (preserve local customizations, apply upstream fixes)
- Version pinning support (`_commit` field in `.copier-answers.yml`)
- Conflict resolution patterns for common update scenarios

**3. Semantic Versioning Strategy**
- **Patch** (1.0.X): Bug fixes, documentation updates, backward compatible
- **Minor** (1.X.0): New features, non-breaking enhancements
- **Major** (X.0.0): Breaking changes, deprecation removals, architecture changes
- Version tagging in chora-base repository (v1.0.0, v1.1.0, v2.0.0)

**4. Backward Compatibility Management**
- Deprecation warnings (N versions before removal)
- Migration guides for breaking changes
- Version compatibility matrix (SAP → chora-base version requirements)
- Graceful degradation patterns (new features don't break old projects)

**5. Multi-Tier SAP Selection**
- **Minimal** (2-3 SAPs): Core coordination + task tracking (SAP-001, SAP-015)
- **Standard** (4-6 SAPs): + memory + automation + validation (SAP-010, SAP-008, SAP-016)
- **Comprehensive** (8-12 SAPs): + advanced features (SAP-053, SAP-051, SAP-052, SAP-061)
- Custom selection: à la carte SAP selection via questionnaire

---

## Scope

### In Scope

**Phase 1: Template Creation (L0 → L1)**
- Create `copier.yml` questionnaire (SAP selection logic)
- Build `template/` directory structure (scripts, justfile, docs, configs)
- Integrate 6-8 SAPs initially (SAP-053, SAP-051, SAP-052, SAP-001, SAP-015, SAP-056, SAP-008, SAP-010)
- Implement post-generation hooks (git init, dependency install)
- Define variable naming conventions (project_name, sap_*, author_name)

**Phase 2: Versioning Strategy (L1 → L2)**
- Document semantic versioning rules for SAP artifacts
- Establish version tagging workflow (when to bump patch/minor/major)
- Create backward compatibility policy (deprecation timeline, migration support)
- Define `_commit` usage patterns (pin to specific template version)

**Phase 3: Update Propagation (L2 → L3)**
- Test `copier update` with real version bumps (v1.0 → v1.1 → v2.0)
- Document conflict resolution patterns (common merge scenarios)
- Create update workflow guide (when to update, how to resolve conflicts)
- Pilot with 2-3 real projects (chora-workspace, castalia, external)

**Phase 4: Distribution & Adoption (L3 → L4)**
- Publish template to chora-base repository (GitHub)
- Create documentation (1-page quick start + comprehensive guide)
- Establish adoption support process (issue triage, Q&A)
- Track adoption metrics (setup time, adoption rate, update frequency)

### Out of Scope

**Explicitly Excluded** (defer to future SAPs or versions):
- ❌ **Multi-language support**: Focus on Python-based projects initially (Node.js, Rust defer to v2.0)
- ❌ **Private template hosting**: GitHub-only initially (GitLab, Bitbucket defer to v1.1)
- ❌ **Template branching strategy**: Single main branch initially (stable/beta branches defer to v1.2)
- ❌ **SAP dependency resolution**: Manual SAP selection initially (auto-resolve deps defer to v2.0)
- ❌ **Template marketplace**: Single template initially (multi-template ecosystem defer to v3.0)

---

## Success Metrics

### Adoption Metrics (L2 → L3 → L4)

**L2 (Implementation Complete)**:
- ✅ Template generates project with 6-8 SAPs in <3 min
- ✅ All SAP scripts/recipes executable in generated project
- ✅ `copier update` propagates changes without breaking existing projects

**L3 (Pilot Validation)**:
- ✅ Pilot projects: 2-3 real adoptions (chora-workspace, castalia, external)
- ✅ Setup time: <3 min (vs 18 min manual baseline) = 85-90% reduction
- ✅ Developer satisfaction: 4-5/5 rating (exit survey)
- ✅ Zero blocking issues (all SAPs functional)

**L4 (Distributed)**:
- ✅ Template accessible via `copier copy gh:liminalcommons/chora-base`
- ✅ Documentation complete (1-page quick start + full guide)
- ✅ Adoption rate: ≥2 external adoptions within 1 month

### ROI Metrics (from OPP-2025-022)

**Time Savings**:
- **Minimal** (2 SAPs): 20-30 min → 2-3 min = 85-90% reduction (17-27 min saved)
- **Standard** (4 SAPs): 40-60 min → 3-4 min = 90-93% reduction (36-56 min saved)
- **Comprehensive** (8 SAPs): 80-120 min → 4-5 min = 94-96% reduction (75-115 min saved)

**Adoption Increase**:
- **Baseline**: 30-50% adopt SAPs (manual friction)
- **Target**: 80-95% adopt SAPs (automation removes friction)
- **Lift**: +50-65 percentage points

**Update Propagation**:
- **Baseline**: 0-10% adopt SAP updates (manual re-copy required)
- **Target**: 60-80% adopt updates (`copier update` command)
- **Lift**: 6-8x improvement in update adoption

**Financial Impact** (50 projects/year scenario):
- **Manual waste**: $7,500/year (50 hours @ $150/hr)
- **Copier cost**: $500/year (3.3 hours @ $150/hr)
- **Net savings**: $7,000/year
- **Break-even**: 1.3 years
- **5-year ROI**: +236% ($23,200 net benefit)

### Quality Metrics

**Template Quality**:
- ✅ Questionnaire completion time: <3 min
- ✅ Template generation time: <30 sec (minimal), <60 sec (comprehensive)
- ✅ Post-generation hook success rate: >95%
- ✅ Generated project validation: 100% pass rate (all SAP scripts executable)

**Update Quality**:
- ✅ Update success rate: >90% (no manual intervention required)
- ✅ Conflict resolution clarity: <5 min to resolve common conflicts
- ✅ Version pinning effectiveness: 100% (pinned projects don't auto-update)

**Documentation Quality**:
- ✅ Quick start guide: 1 page, <5 min read time
- ✅ Comprehensive guide: <15 min read time
- ✅ Troubleshooting coverage: >80% of common issues documented

---

## Strategic Value

### Enables SAP Lifecycle Meta-SAPs

SAP-062 is one of three foundational SAPs for sustainable SAP development:
- **SAP-061** (Ecosystem Integration): Validates SAPs meet ecosystem requirements (INDEX.md, catalog, dependencies)
- **SAP-062** (Distribution & Versioning): Automates SAP distribution and update propagation ← **This SAP**
- **SAP-050** (Development Lifecycle): Documents SAP development phases and maturity progression

**Dependency**: Can't have sustainable SAP development lifecycle without automated distribution. SAP-062 unblocks:
- SAP versioning (v1.0 → v1.1 → v2.0 with confidence)
- Breaking change management (deprecation → migration → removal)
- Ecosystem scalability (10 → 20 → 50 SAPs)

### Unblocks SAP-053 Phase 4 Completion

SAP-053 (Conflict Resolution) Phase 4 Milestone 5 was blocked by lack of distribution mechanism. SAP-062 provides:
- Copier template integration for SAP-053 artifacts
- Update propagation when SAP-053 improves (v1.0 → v1.1)
- Revised Phase 4 completion path (documented in SAP-053 ledger)

### Foundation for chora Ecosystem Scalability

As SAPs grow (10 → 20 → 50), manual distribution becomes impossible:
- **Current** (10 SAPs): 100-150 min manual setup per project → barely manageable
- **Future** (50 SAPs): 500-750 min manual setup per project → completely impractical
- **Copier** (50 SAPs): 5-7 min automated setup → scalable to any SAP count

---

## Assumptions

**Technical Assumptions**:
1. Copier is the correct distribution tool (validated in OPP-2025-022 waypoint: 78% fit vs 43% for Cookiecutter)
2. chora-base will remain Python-based (template assumes Python tooling)
3. GitHub is primary hosting platform (template URL: `gh:liminalcommons/chora-base`)
4. Jinja2 templating is sufficient for conditional logic (no need for custom preprocessing)

**Organizational Assumptions**:
1. chora-base maintainers will adopt semantic versioning for chora-base repository (tag releases as v1.0.0, v1.1.0, v2.0.0)
2. SAP authors will follow backward compatibility guidelines (deprecation warnings, migration guides)
3. Template will be maintained alongside chora-base (quarterly sync to keep in sync)
4. Adoption support will be available (issue triage, Q&A for early adopters)

**User Assumptions**:
1. Developers have Copier installed (`pipx install copier` or `pip install copier`)
2. Developers are comfortable with command-line tools (bash, git, copier)
3. Developers will read 1-page quick start guide before first use
4. Developers will run `copier update` periodically (quarterly recommended)

---

## Dependencies

**Upstream Dependencies**:
- **SAP-061** (Ecosystem Integration): Validation script ensures template-generated projects meet ecosystem requirements
- **SAP-050** (Development Lifecycle): Phase gates define when to promote SAPs (draft → pilot → active)
- **OPP-2025-022** (Copier Distribution Research): Tool selection research (Copier vs Cookiecutter decision)

**Downstream Dependents** (blocked by SAP-062):
- **SAP-053 Phase 4**: Distribution milestone completion (Copier template for Conflict Resolution)
- **SAP-000 v1.1.0**: SAP Framework revision (reference SAP-062 as distribution mechanism)
- **Future SAPs**: All future SAPs will use Copier distribution (SAP-062 is foundational)

**External Dependencies**:
- **Copier tool**: chora ecosystem depends on Copier remaining actively maintained
  - **Risk mitigation**: Copier actively maintained 2018-2025, fallback to `cruft` if Copier abandoned
- **chora-base repository**: Template lives in chora-base, requires repository access
- **GitHub hosting**: Template URL assumes GitHub hosting (`gh:liminalcommons/chora-base`)

---

## Risks & Mitigation

### Technical Risks

**Risk 1: Template complexity overwhelms maintainability**
- **Impact**: Template becomes out-of-sync with chora-base, generates broken projects
- **Probability**: Medium (30-40%)
- **Mitigation**:
  - Start with 6-8 SAPs (incremental approach)
  - Automated sync scripts (detect chora-base changes)
  - Quarterly template review cadence

**Risk 2: `copier update` causes merge conflicts**
- **Impact**: Developers skip updates due to conflict resolution friction
- **Probability**: Medium-High (40-50%)
- **Mitigation**:
  - Document common conflict patterns (justfile, README, scripts)
  - Provide conflict resolution examples (before/after diffs)
  - Test updates with real projects during pilot (Phase 3)

**Risk 3: Cross-platform compatibility issues**
- **Impact**: Template works on macOS but fails on Linux/Windows
- **Probability**: Low-Medium (20-30%)
- **Mitigation**:
  - Test on 2+ platforms during Phase 2 (macOS + Linux minimum)
  - Use platform-agnostic paths (`pathlib` vs hardcoded `/` or `\`)
  - Document platform-specific quirks (Windows Git Bash, WSL, etc.)

### Adoption Risks

**Risk 4: Developer learning curve for Copier**
- **Impact**: Developers abandon template due to unfamiliar tool
- **Probability**: Low (10-20%)
- **Mitigation**:
  - 1-page quick start guide (<5 min read)
  - Video walkthrough (optional, 3-5 min)
  - Clear error messages with actionable fixes

**Risk 5: Template maintenance burden**
- **Impact**: Template maintainer burnout, template becomes stale
- **Probability**: Medium (30-40%)
- **Mitigation**:
  - Shared maintenance responsibility (2-3 maintainers)
  - Automated testing (CI/CD for template generation)
  - Quarterly review cadence (not weekly/monthly)

### Integration Risks

**Risk 6: Copier tool abandonment**
- **Impact**: Template becomes unmaintained if Copier project dies
- **Probability**: Low (10% over 5 years)
- **Mitigation**:
  - Copier actively maintained (2018-2025, growing community)
  - Fallback option: `cruft` (similar tool, API-compatible)
  - Worst case: Fork Copier or revert to manual distribution

---

## Related Work

**OPP-2025-022** (Copier-based SAP Distribution System):
- Strategic opportunity that triggered SAP-062 creation
- Research findings: Copier selected over Cookiecutter (78% fit vs 43%)
- ROI analysis: Break-even 1.3 years, 5-year ROI +236%
- 4-phase implementation plan (38-60 hours, 5-7 weeks)

**SAP-053** (Conflict Resolution):
- Phase 4 Milestone 5 blocked by lack of distribution mechanism
- Copier template integration will unblock completion
- Case study for SAP distribution (first SAP to use template)

**SAP-061** (Ecosystem Integration):
- Validation script ensures template-generated projects meet requirements
- Pre-commit hook blocks commits with missing integrations
- SAP-062 templates will be validated by SAP-061 scripts

**SAP-050** (Development Lifecycle):
- Documents SAP development phases (Vision → DDD → BDD/TDD → Distribution)
- Phase gates define when to promote SAPs (draft → pilot → active)
- SAP-062 distribution aligns with Phase 4 (Distribution) requirements

---

## Version History

### v1.0.0 (2025-11-20) - Initial Release

**Changes**:
- Initial capability charter for SAP-062
- Problem statement: OPP-2025-022 gap analysis (manual distribution, no versioning)
- Solution overview: Copier-based template with semantic versioning
- Scope: 4 phases (Template Creation, Versioning, Update Propagation, Distribution)
- Success metrics: ROI analysis from OPP-2025-022 (85-90% time savings, +50-65pp adoption)

**Context**:
- Created as part of CORD-2025-023 (3-SAP Suite Delivery)
- Phase 3 deliverable (parallel with Phase 4 SAP-050 promotion)
- Trace ID: sap-development-lifecycle-meta-saps-2025-11-20

**Author**: Claude (Anthropic) via tab-2 (chora-workspace)

---

**Created**: 2025-11-20
**Last Updated**: 2025-11-20
**Status**: draft
**Next Review**: After protocol-spec.md completion
