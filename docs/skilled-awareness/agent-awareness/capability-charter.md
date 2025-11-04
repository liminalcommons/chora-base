# Capability Charter: Agent Awareness

**SAP ID**: SAP-009
**Version**: 1.0.0
**Status**: Draft (Phase 3)
**Owner**: Victor (chora-base maintainer)
**Created**: 2025-10-28
**Last Updated**: 2025-10-28

---

## 1. Problem Statement

### Current Challenge

chora-base provides **AGENTS.md + CLAUDE.md patterns with nested awareness files**, but the agent awareness system lacks:

1. **Explicit Awareness Contracts** - No documented structure for AGENTS.md/CLAUDE.md content, layout, sections
2. **Nesting Rationale** - Why nested awareness files (tests/AGENTS.md, scripts/AGENTS.md) exist, when to use them
3. **Context Optimization** - Progressive loading patterns, token budgets not standardized across projects
4. **Claude-Specific Patterns** - What makes CLAUDE.md different from AGENTS.md, when to use which file
5. **Discovery Mechanism** - How agents find and prioritize awareness files not explicit

**Result**:
- **Adopters**: Write inconsistent awareness files, unsure what content belongs where
- **AI Agents**: Miss domain-specific guidance, load unnecessary context, inefficient token usage
- **Maintainers**: Can't enforce awareness file standards, duplicated content across files
- **Projects**: Context loading varies 10-30k tokens for same task due to lack of optimization

### Evidence

**From adopter feedback**:
- "Should I put testing guidance in root AGENTS.md or tests/AGENTS.md?" - No clear guidance
- "What's the difference between AGENTS.md and CLAUDE.md?" - Structure unclear
- "How do agents know which awareness file to read?" - Discovery mechanism not documented
- "My AGENTS.md is 1500 lines, is that too big?" - No size guidelines

**From agent behavior**:
- Agents read root AGENTS.md even when working in tests/ (inefficient)
- Claude-specific patterns duplicated in both AGENTS.md and CLAUDE.md
- Context loading inconsistent (10k-30k tokens for same task)
- Nested awareness files (tests/AGENTS.md) often ignored

**From maintenance burden**:
- Awareness file structure varies widely across projects
- Updates require changing multiple files (root + nested)
- No validation for awareness file quality
- Duplicated guidance (same content in AGENTS.md and tests/AGENTS.md)

### Business Impact

Without structured agent awareness:
- **Context Inefficiency**: 10-30k token variance for same task (should be 5-10k consistent)
- **Agent Confusion**: 30-60 min per session finding right guidance (should be <10 min)
- **Maintenance Overhead**: 2-4 hours to write awareness files (should be 30-60 min)
- **Missed Guidance**: 40% of domain-specific patterns missed by agents

---

## 2. Proposed Solution

### Agent Awareness SAP

A **comprehensive SAP describing AGENTS.md/CLAUDE.md structure, nesting patterns, and context optimization** to provide explicit contracts for agent guidance files.

This SAP documents:
1. **What awareness files contain** - Structure, sections, content guidelines for AGENTS.md and CLAUDE.md
2. **How nesting works** - When to create nested files (tests/AGENTS.md, scripts/AGENTS.md), discovery mechanism
3. **What's guaranteed** - Awareness file contracts (max size, required sections, optimization patterns)
4. **How agents use them** - Loading strategy, context budgets, progressive loading
5. **How to write them** - Templates, patterns, validation

### Key Principles

1. **Dual-File Pattern** - AGENTS.md (generic agent guidance) + CLAUDE.md (Claude-specific patterns and context)
2. **Nested Awareness** - Domain-specific files in subdirectories (tests/AGENTS.md for testing, scripts/AGENTS.md for automation)
3. **Nearest File Wins** - Agents read awareness file nearest to working code (tests/AGENTS.md overrides root AGENTS.md)
4. **Progressive Loading** - Essential → Extended → Full context phases to optimize token usage
5. **Context Budgets** - Token budgets by task type (setup: 5-10k, feature: 10-15k, debug: 5-10k)

### Design Trade-offs and Rationale

**Why dual-file pattern (AGENTS.md + CLAUDE.md) instead of single AGENTS.md?**
- **Trade-off**: Simplicity (single file) vs. specificity (separate generic + Claude-specific files)
- **Decision**: Dual files allow Claude-specific optimizations (context window, artifacts, tool calling) without cluttering generic guidance for other agents
- **Alternative considered**: Single AGENTS.md with Claude sections → rejected because it makes generic guidance harder to find for non-Claude agents

**Why nested awareness files instead of single root AGENTS.md?**
- **Trade-off**: Single source of truth (root only) vs. domain-specific guidance (nested files)
- **Decision**: Nested files reduce context loading by 50-70% for domain-specific tasks (testing, Docker, scripts) and prevent root AGENTS.md from growing >2000 lines
- **Alternative considered**: Single root AGENTS.md with all guidance → rejected due to token inefficiency and poor maintainability

**Why "nearest file wins" instead of merging all awareness files?**
- **Trade-off**: Comprehensive context (merge all files) vs. focused context (nearest only)
- **Decision**: Nearest-file strategy prevents context pollution and reduces token usage by 40-60%, while still allowing progressive loading if needed
- **Alternative considered**: Merge root + nested awareness files → rejected because it loads unnecessary context (e.g., Docker guidance when writing tests)

**Why progressive loading (Essential → Extended → Full) instead of all-at-once?**
- **Trade-off**: Simplicity (load everything) vs. efficiency (load incrementally)
- **Decision**: Progressive loading reduces initial context by 60-80% and enables agents to request more context only when needed, optimizing token budgets
- **Alternative considered**: Load all context upfront → rejected due to token waste and slower agent response times

**Why context budgets (5-15k tokens) instead of unlimited context?**
- **Trade-off**: Complete information (no limits) vs. efficient loading (budgets)
- **Decision**: Context budgets force awareness files to be concise and well-organized, preventing bloat and ensuring fast agent context loading
- **Alternative considered**: No token budgets → rejected because awareness files tend to grow indefinitely without constraints

---

## 3. Scope

### In Scope

**Agent Awareness SAP Artifacts**:
- ✅ Capability Charter (this document) - Problem, scope, outcomes
- ✅ Protocol Specification - AGENTS.md structure, CLAUDE.md structure, nesting rules, context optimization
- ✅ Awareness Guide - Agent workflows for reading awareness files, progressive loading
- ✅ Adoption Blueprint - How to write awareness files, validate structure
- ✅ Traceability Ledger - Projects using awareness patterns, compliance tracking

**Components Covered**:
1. **AGENTS.md Blueprint** (~900 lines) - Generic agent guidance structure
2. **CLAUDE.md Blueprint** (~450 lines) - Claude-specific patterns and context
3. **Nested Awareness Files** - tests/AGENTS.md, scripts/AGENTS.md, docker/AGENTS.md, .chora/memory/AGENTS.md
4. **Discovery Mechanism** - How agents find and prioritize awareness files (nearest file wins)
5. **Context Management** - Progressive loading, token budgets, optimization patterns
6. **Validation Rules** - Max size, required sections, quality standards

### Out of Scope (for v1.0)

- ❌ Agent-specific integrations (non-Claude agents like Cursor, Copilot)
- ❌ Automated awareness file generation (future Phase 4)
- ❌ Real-time context optimization (static guidance only)
- ❌ Cross-repository awareness file sharing (future consideration)

---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Phase 3):
- ✅ SAP-009 complete (all 5 artifacts)
- ✅ AGENTS.md and CLAUDE.md blueprints documented with required sections
- ✅ Nesting pattern explained (nearest file wins, discovery mechanism)
- ✅ Context optimization patterns catalogued (progressive loading, budgets)
- ✅ Agents use SAP-009 to read awareness files efficiently

**Quality Success** (Phase 3-4):
- ✅ 100% of generated projects have compliant awareness files
- ✅ Context loading consistent (5-10k tokens for setup, 10-15k for features)
- ✅ Single source of truth for awareness file standards
- ✅ Nested awareness files used appropriately (tests/, scripts/, docker/)

**Maintenance Success** (Phase 4):
- ✅ Automated awareness file validation
- ✅ Context usage tracking across projects
- ✅ Awareness file quality metrics (token efficiency, coverage)
- ✅ Continuous improvement of patterns

### Key Metrics

| Metric | Baseline | Target (Phase 3) | Target (Phase 4) |
|--------|----------|------------------|------------------|
| Context Loading Variance | 10-30k tokens | 5-15k tokens | 5-10k tokens |
| Agent Guidance Discovery | ~60% found | 90% found | 95% found |
| Awareness File Compliance | ~50% | 80% | 95% |
| Awareness File Writing Time | 2-4 hours | 30-60 min | 15-30 min |
| Context Efficiency | ~40% relevant | 80% relevant | 90% relevant |

**Measurement**:
- **Context Loading**: Measure token usage by task type (setup, feature, debug)
- **Guidance Discovery**: % of domain-specific patterns agents find
- **Compliance**: % of projects with valid AGENTS.md + CLAUDE.md structure
- **Writing Time**: Survey adopters on awareness file creation time
- **Efficiency**: % of loaded context actually used by agents

---

## 5. Stakeholders

### Primary Stakeholders

**Template Maintainer**:
- Victor (chora-base owner)
- Maintains AGENTS.md and CLAUDE.md blueprints
- Updates SAP-009 when awareness patterns change

**AI Agents** (Read Awareness Files):
- Claude Code (primary agent)
- Cursor Composer
- Other LLM-based agents
- Use SAP-009 to understand how to read and prioritize awareness files

**Project Developers** (Write Awareness Files):
- chora-compose maintainer
- mcp-n8n maintainer
- Example project maintainers
- External adopters
- Use SAP-009 to write compliant AGENTS.md/CLAUDE.md files

### Secondary Stakeholders

**Domain Specialists**:
- Testing specialists (maintain tests/AGENTS.md)
- DevOps engineers (maintain docker/AGENTS.md, scripts/AGENTS.md)
- Memory system maintainers (maintain .chora/memory/AGENTS.md)
- Write nested awareness files for their domains

**Documentation Reviewers**:
- Code reviewers
- Quality gatekeepers
- Use SAP-009 standards for awareness file review

---

## 6. Dependencies

### Internal Dependencies

**Framework Dependencies**:
- ✅ SAP-000 (sap-framework) - Provides SAP structure
- ✅ SAP-002 (chora-base-meta) - References SAP-009 as capability
- ✅ SAP-003 (project-bootstrap) - Generates initial AGENTS.md/CLAUDE.md

**Capability Dependencies**:
- SAP-007 (documentation-framework) - Awareness files are documentation, follow Diataxis
- SAP-010 (memory-system) - .chora/memory/AGENTS.md describes memory patterns
- SAP-004 (testing-framework) - tests/AGENTS.md describes testing patterns
- SAP-011 (docker-operations) - docker/AGENTS.md describes Docker patterns

**Documentation Dependencies**:
- [blueprints/AGENTS.md.blueprint](/blueprints/AGENTS.md.blueprint) - Template for generic guidance
- [blueprints/CLAUDE.md.blueprint](/blueprints/CLAUDE.md.blueprint) - Template for Claude-specific guidance

### External Dependencies

**Tooling**:
- Git (version control for awareness files)
- Markdown parsers (for agent reading)
- AI agents with file system access

**Standards**:
- Markdown format (awareness files are .md)
- Diataxis principles (awareness files are "Explanation" documents)
- Token budget conventions (5-15k tokens by task type)

---

## 7. Constraints & Assumptions

### Constraints

1. **Markdown Format**: Awareness files must be markdown (human-readable, git-friendly)
2. **File-Based Discovery**: Agents discover awareness files via file system, not database
3. **Context Window Limits**: Claude has 200k token context window, awareness files must fit within budget
4. **Backward Compatibility**: Changes to awareness file structure must not break existing agents

### Assumptions

1. **Agent File Access**: Agents can read local file system (awareness files)
2. **Nearest-File Logic**: Agents understand directory hierarchy and can find nearest awareness file
3. **Progressive Loading**: Agents can request additional context if Essential context insufficient
4. **Markdown Parsing**: Agents can parse markdown structure (headings, sections, code blocks)

---

## 8. Risks & Mitigation

### Risk 1: Awareness File Bloat

**Risk**: Awareness files grow too large (>2000 lines), slowing context loading

**Likelihood**: Medium
**Impact**: High (defeats purpose of context optimization)

**Mitigation**:
- Enforce max size guidelines (root AGENTS.md <1500 lines, CLAUDE.md <800 lines)
- Use nested awareness files to distribute content
- Progressive loading reduces impact of large files
- Automated size validation (Phase 4)

### Risk 2: Nested File Confusion

**Risk**: Agents confused by multiple awareness files, load wrong one

**Likelihood**: Low
**Impact**: Medium (missed guidance)

**Mitigation**:
- Document "nearest file wins" clearly in Protocol
- Provide agent decision tree for file selection
- Test with multiple agents (Claude, Cursor)
- Include examples in Awareness Guide

### Risk 3: Duplication Between Files

**Risk**: Same guidance duplicated in AGENTS.md and CLAUDE.md

**Likelihood**: Medium
**Impact**: Medium (maintenance burden)

**Mitigation**:
- Clear separation: AGENTS.md (generic), CLAUDE.md (Claude-specific only)
- Review checklist for duplication
- Document what belongs in each file (Protocol)
- Automated duplication detection (Phase 4)

### Risk 4: Context Budget Violations

**Risk**: Awareness files exceed token budgets, waste context

**Likelihood**: Low
**Impact**: Medium (inefficient)

**Mitigation**:
- Document budgets clearly (5k setup, 10-15k feature, 5-10k debug)
- Progressive loading enables exceeding budgets when necessary
- Track actual token usage (Ledger)
- Optimize patterns based on usage data

---

## 9. Related Documents

**SAP Framework**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root protocol
- [sap-framework/](../sap-framework/) - SAP-000 (framework SAP)
- [INDEX.md](../INDEX.md) - SAP registry
- [document-templates.md](../document-templates.md) - SAP templates

**chora-base Core**:
- [README.md](/README.md) - Project overview
- [AGENTS.md](/AGENTS.md) - Root agent guidance
- [CLAUDE.md](/CLAUDE.md) - Root Claude-specific guidance
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - Meta-SAP (Section 3.2.5)

**Awareness File Components**:
- [blueprints/AGENTS.md.blueprint](/blueprints/AGENTS.md.blueprint) - Generic guidance template (~900 lines)
- [blueprints/CLAUDE.md.blueprint](/blueprints/CLAUDE.md.blueprint) - Claude-specific template (~450 lines)
- [static-template/tests/AGENTS.md](/static-template/tests/AGENTS.md) - Nested awareness example (testing)
- [static-template/scripts/AGENTS.md](/static-template/scripts/AGENTS.md) - Nested awareness example (scripts)

**Related SAPs**:
- [sap-framework/](../sap-framework/) - SAP-000 (framework foundation)
- [chora-base/](../chora-base/) - SAP-002 (meta-SAP references agent awareness)
- [project-bootstrap/](../project-bootstrap/) - SAP-003 (generates awareness files)
- [documentation-framework/](../documentation-framework/) - SAP-007 (awareness files are docs)
- [memory-system/](../memory-system/) - SAP-010 (.chora/memory/AGENTS.md)

---

## 10. Approval

**Sponsor**: Victor (chora-base owner)
**Approval Date**: 2025-10-28
**Review Cycle**: Quarterly (align with template releases)

**Next Review**: 2026-01-31 (end of Phase 3)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial charter for agent-awareness SAP
- **1.0.1** (2025-11-04): Added trade-offs section, expanded Problem Statement, removed Lifecycle section
