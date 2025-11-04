# Capability Charter: Documentation Framework

**SAP ID**: SAP-007
**Version**: 1.0.0
**Status**: Draft (Phase 3)
**Owner**: Victor (chora-base maintainer)
**Created**: 2025-10-28
**Last Updated**: 2025-10-28

---

## 1. Problem Statement

### Current Challenge

chora-base provides **Diataxis-based documentation framework** with YAML frontmatter, executable How-Tos, and test extraction via scripts/extract_tests.py, but the framework lacks:

1. **Explicit Documentation Contracts** - No documented guarantees about doc structure, frontmatter schema, validation rules
2. **Diataxis Rationale** - Why 4 types (Tutorial, How-To, Reference, Explanation) exist, when to use each, what belongs where
3. **Test Extraction Clarity** - How executable How-Tos convert to pytest tests, what syntax required, how tests validated
4. **Quality Standards** - Documentation quality metrics not defined (completeness, accuracy, maintainability)
5. **Directory Organization** - user-docs/, dev-docs/, project-docs/ structure exists but rationale unclear

**Result**:
- **Adopters**: Write inconsistent docs, unsure which Diataxis type to use, documentation quality varies
- **AI Agents**: Can't reason about doc quality, generate docs that don't match framework, miss test extraction opportunities
- **Maintainers**: Can't enforce doc standards consistently, duplicated content across types
- **Testing**: Test extraction underutilized (only ~20% of How-Tos have extractable tests)

### Evidence

**From adopter feedback**:
- "Should I write a Tutorial or How-To for this workflow?" - Diataxis distinction unclear
- "What frontmatter fields are required?" - Schema not documented
- "How do I make my How-To executable?" - Test extraction syntax unclear
- "Where should API documentation go?" - Directory structure rationale unclear

**From agent behavior**:
- Agents write Tutorials that should be How-Tos (common confusion)
- Frontmatter missing or inconsistent (no validation)
- Executable code blocks lack test extraction markers
- Documentation types mixed (Explanation content in Tutorials)

**From maintenance burden**:
- Doc reviews take 30-60 min due to Diataxis confusion
- Test extraction manual (agents don't know syntax)
- No automated doc validation
- Duplicated content across Tutorial/How-To/Explanation

### Business Impact

Without structured documentation framework:
- **Quality Risk**: Documentation quality varies 40-90% (no standards)
- **Adoption Friction**: 2-4 hours to understand Diataxis (should be <1 hour)
- **Testing Gap**: Only 20% of How-Tos extractable to tests (should be 80%)
- **Maintenance Overhead**: 30-60 min per doc review (should be 15-30 min)

---

## 2. Proposed Solution

### Documentation Framework SAP

A **comprehensive SAP describing Diataxis framework, frontmatter schema, executable How-Tos, and test extraction** to provide explicit contracts for all documentation.

This SAP documents:
1. **What documentation types exist** - 4 Diataxis types, when to use each, what content belongs where
2. **How docs are structured** - Frontmatter schema, required fields, directory organization
3. **What's guaranteed** - Doc quality contracts (frontmatter valid, Diataxis type correct, test-extractable)
4. **How test extraction works** - Executable How-To syntax, pytest test generation, validation
5. **How to write docs** - Templates, patterns, quality standards

### Key Principles

1. **Diataxis-Based** - 4 document types by user intent (Tutorial, How-To, Reference, Explanation)
2. **Frontmatter-Validated** - YAML metadata with required schema (type, title, description, etc.)
3. **Executable How-Tos** - Code examples in How-Tos → pytest tests via scripts/extract_tests.py
4. **Documentation-Driven** - Write docs before code (DDD in development lifecycle)
5. **Directory-Organized** - user-docs/, dev-docs/, project-docs/ separate concerns

### Design Trade-offs and Rationale

**Why Diataxis (4 types) instead of simple user/developer split?**
- **Trade-off**: Simplicity (2 categories) vs. precision (4 Diataxis types based on user intent)
- **Decision**: Diataxis 4-type framework aligns docs with user intent (learning vs. solving vs. understanding vs. reference), reducing doc confusion and improving discoverability
- **Alternative considered**: Simple user/developer split → rejected because it doesn't capture intent differences (learning a feature vs. troubleshooting it)

**Why YAML frontmatter instead of inline metadata or no metadata?**
- **Trade-off**: Simplicity (no metadata) vs. structured metadata (frontmatter)
- **Decision**: Frontmatter enables automated validation, search/filtering, and agent reasoning about doc type and status
- **Alternative considered**: No metadata, rely on filename/directory → rejected because it's error-prone and doesn't enable validation

**Why executable How-Tos (test extraction) instead of separate test files?**
- **Trade-off**: Traditional testing (separate test files) vs. docs-as-tests (extract from How-Tos)
- **Decision**: Executable How-Tos ensure docs stay current with code (tests fail if docs outdated) and provide working examples
- **Alternative considered**: Separate test files → rejected because docs and tests drift over time, causing stale documentation

**Why scripts/extract_tests.py instead of manual test writing?**
- **Trade-off**: Manual test writing (full control) vs. automated extraction (consistency)
- **Decision**: Automated extraction reduces duplicated effort (write once in docs, extract to tests) and enforces doc quality (must be executable)
- **Alternative considered**: Manual test duplication → rejected due to high maintenance overhead and doc-code drift

**Why 3 doc directories (user-docs/, dev-docs/, project-docs/) instead of flat structure?**
- **Trade-off**: Simplicity (flat structure) vs. organization (role-based directories)
- **Decision**: Role-based directories reduce context switching (users don't see dev internals, devs don't wade through user tutorials) and improve navigability
- **Alternative considered**: Flat docs/ directory → rejected because it mixes audiences and makes docs harder to find

---

## 3. Scope

### In Scope

**Documentation Framework SAP Artifacts**:
- ✅ Capability Charter (this document) - Problem, scope, outcomes
- ✅ Protocol Specification - Diataxis types, frontmatter schema, directory structure, test extraction
- ✅ Awareness Guide - Agent workflows for writing docs, extracting tests, validating
- ✅ Adoption Blueprint - How to use documentation framework, write each type, extract tests
- ✅ Traceability Ledger - Projects using documentation framework, compliance tracking

**Components Covered**:
1. **DOCUMENTATION_STANDARD.md** (~700 lines) - Complete documentation framework specification
2. **Diataxis Structure** - user-docs/, dev-docs/, project-docs/ organization with 4 types
3. **Frontmatter Schema** - Required fields (type, title, description, status, etc.)
4. **Test Extraction** - scripts/extract_tests.py for converting How-Tos to pytest tests
5. **Validation Rules** - Frontmatter validation, Diataxis type checking, test extraction validation
6. **Templates** - Templates for each Diataxis type (Tutorial, How-To, Reference, Explanation)

### Out of Scope (for v1.0)

- ❌ API documentation generators (Sphinx, MkDocs integration)
- ❌ Automated doc generation from code (docstrings → docs)
- ❌ Interactive documentation platforms (Docusaurus, GitBook)
- ❌ Multi-language documentation (English only for v1.0)

---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Phase 3):
- ✅ SAP-007 complete (all 5 artifacts)
- ✅ All 4 Diataxis types documented with examples
- ✅ Frontmatter schema validated and enforced
- ✅ Test extraction workflow explained with concrete examples
- ✅ Agents use SAP-007 to write compliant docs

**Quality Success** (Phase 3-4):
- ✅ 100% of generated docs have valid frontmatter
- ✅ Correct Diataxis type usage (≥90% accuracy)
- ✅ Test extraction rate: 80% of How-Tos extractable
- ✅ Single source of truth for documentation standards

**Maintenance Success** (Phase 4):
- ✅ Automated frontmatter validation
- ✅ Automated Diataxis type checking
- ✅ Documentation quality metrics tracked
- ✅ Continuous improvement of templates

### Key Metrics

| Metric | Baseline | Target (Phase 3) | Target (Phase 4) |
|--------|----------|------------------|------------------|
| Frontmatter Compliance | ~60% | 90% | 100% |
| Diataxis Type Accuracy | ~50% | 80% | 90% |
| Test Extraction Rate | ~20% | 60% | 80% |
| Doc Review Time | 30-60 min | 20-40 min | 15-30 min |
| Doc Quality Score | 40-90% (varies) | 70-90% | 80-95% |

**Measurement**:
- **Frontmatter Compliance**: % of docs with valid frontmatter (all required fields)
- **Diataxis Accuracy**: % of docs using correct Diataxis type for content
- **Test Extraction**: % of How-Tos successfully extractable to pytest tests
- **Review Time**: Time to review doc during code review
- **Quality Score**: Composite score (frontmatter valid + correct type + extractable + complete)

---

## 5. Stakeholders

### Primary Stakeholders

**Template Maintainer**:
- Victor (chora-base owner)
- Maintains DOCUMENTATION_STANDARD.md and frontmatter schema
- Updates SAP-007 when documentation patterns change

**AI Agents** (Write Documentation):
- Claude Code (primary agent)
- Cursor Composer
- Other LLM-based agents
- Use SAP-007 to generate compliant docs, extract tests

**Project Developers** (Write/Review Documentation):
- chora-compose maintainer
- mcp-n8n maintainer
- Example project maintainers
- External adopters
- Use SAP-007 for Diataxis guidance, frontmatter, test extraction

### Secondary Stakeholders

**End Users**:
- Read Tutorials (learning-oriented)
- Read How-To Guides (task-oriented)
- Benefit from accurate, up-to-date documentation

**Quality Reviewers**:
- Code reviewers validating doc quality
- Pre-commit hooks checking frontmatter
- Use SAP-007 standards for review criteria

---

## 6. Dependencies

### Internal Dependencies

**Framework Dependencies**:
- ✅ SAP-000 (sap-framework) - Provides SAP structure (SAPs use Diataxis)
- ✅ SAP-002 (chora-base-meta) - References SAP-007 as capability
- ✅ SAP-003 (project-bootstrap) - Generates initial docs/ structure

**Capability Dependencies**:
- SAP-012 (development-lifecycle) - DDD phase writes docs before code
- SAP-004 (testing-framework) - Test extraction generates pytest tests
- SAP-009 (agent-awareness) - AGENTS.md and CLAUDE.md follow Diataxis (Explanation type)
- SAP-006 (quality-gates) - Pre-commit hooks validate frontmatter

**Documentation Dependencies**:
- [DOCUMENTATION_STANDARD.md](/static-template/DOCUMENTATION_STANDARD.md) - Complete framework spec
- [scripts/extract_tests.py](/static-template/scripts/extract_tests.py) - Test extraction script

### External Dependencies

**Tooling**:
- Python 3.11+ (for scripts/extract_tests.py)
- pytest (for extracted tests)
- YAML parser (for frontmatter validation)
- Git (version control for docs)

**Standards**:
- Diataxis framework (4 document types)
- YAML 1.2 (frontmatter format)
- Markdown (document format)
- pytest conventions (for extracted tests)

---

## 7. Constraints & Assumptions

### Constraints

1. **Diataxis Framework**: Must follow 4 Diataxis types (not customize or extend)
2. **Markdown Format**: Documentation must be markdown (human-readable, git-friendly)
3. **YAML Frontmatter**: Must use YAML 1.2 (not TOML, JSON, or other formats)
4. **Test Extraction Syntax**: How-Tos must use specific code block markers for extraction

### Assumptions

1. **Developer Familiarity**: Developers understand basic markdown and YAML
2. **Agent Capability**: Agents can parse YAML frontmatter and markdown structure
3. **Test Extraction Value**: Executable How-Tos provide sufficient value to justify maintenance overhead
4. **Diataxis Adoption**: Users willing to learn 4 Diataxis types (not overwhelming)

---

## 8. Risks & Mitigation

### Risk 1: Diataxis Confusion

**Risk**: Users confused by 4 types, write wrong type for content

**Likelihood**: High
**Impact**: Medium (doc quality suffers)

**Mitigation**:
- Provide clear decision tree (Protocol Spec)
- Include examples of each type (Adoption Blueprint)
- Agent validation of type vs. content
- Templates for each type reduce confusion

### Risk 2: Frontmatter Neglect

**Risk**: Users skip frontmatter or provide incomplete metadata

**Likelihood**: Medium
**Impact**: Medium (breaks automation)

**Mitigation**:
- Automated validation in pre-commit hooks (SAP-006)
- Templates include frontmatter by default
- Clear error messages for missing fields
- Agents auto-generate frontmatter

### Risk 3: Test Extraction Underuse

**Risk**: Only 20% of How-Tos use test extraction (baseline)

**Likelihood**: Medium
**Impact**: Medium (missed value)

**Mitigation**:
- Document test extraction clearly (Adoption Blueprint)
- Provide concrete examples (Protocol Spec)
- Agents auto-add extraction markers
- Track extraction rate, improve patterns

### Risk 4: Doc-Code Drift

**Risk**: Docs become outdated as code changes

**Likelihood**: High (without test extraction)
**Impact**: High (incorrect docs)

**Mitigation**:
- Test extraction ensures docs stay current (tests fail if docs wrong)
- DDD encourages doc-first workflow (SAP-012)
- Automated validation catches obvious drift
- Regular doc review cycles

---

## 9. Related Documents

**SAP Framework**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root protocol
- [sap-framework/](../sap-framework/) - SAP-000 (framework SAP, uses Diataxis)
- [INDEX.md](../INDEX.md) - SAP registry
- [document-templates.md](../document-templates.md) - SAP templates (follow Diataxis)

**chora-base Core**:
- [README.md](/README.md) - Project overview
- [AGENTS.md](/AGENTS.md) - Agent guidance (Explanation type)
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - Meta-SAP (Section 3.2.3)

**Documentation Components**:
- [DOCUMENTATION_STANDARD.md](/static-template/DOCUMENTATION_STANDARD.md) - Complete framework spec (~700 lines)
- [scripts/extract_tests.py](/static-template/scripts/extract_tests.py) - Test extraction script
- [docs/user-docs/](/static-template/docs/user-docs/) - User-facing documentation (Tutorials, How-Tos)
- [docs/dev-docs/](/static-template/docs/dev-docs/) - Developer documentation (Reference, Explanation)
- [docs/project-docs/](/static-template/docs/project-docs/) - Project documentation (governance, process)

**Related SAPs**:
- [sap-framework/](../sap-framework/) - SAP-000 (framework foundation)
- [chora-base/](../chora-base/) - SAP-002 (meta-SAP references documentation)
- [project-bootstrap/](../project-bootstrap/) - SAP-003 (generates docs/ structure)
- [testing-framework/](../testing-framework/) - SAP-004 (receives extracted tests)
- [quality-gates/](../quality-gates/) - SAP-006 (validates frontmatter)
- [agent-awareness/](../agent-awareness/) - SAP-009 (AGENTS.md follows Diataxis)
- [development-lifecycle/](../development-lifecycle/) - SAP-012 (DDD writes docs first)

**Diataxis Resources**:
- [Diataxis Framework](https://diataxis.fr/) - Official Diataxis documentation

---

## 10. Approval

**Sponsor**: Victor (chora-base owner)
**Approval Date**: 2025-10-28
**Review Cycle**: Quarterly (align with template releases)

**Next Review**: 2026-01-31 (end of Phase 3)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial charter for documentation-framework SAP
- **1.0.1** (2025-11-04): Added trade-offs section, expanded Problem Statement, removed Lifecycle section
