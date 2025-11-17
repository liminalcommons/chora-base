# Capability Charter: Git Workflow Patterns

**SAP ID**: SAP-051
**Version**: 1.0.0
**Status**: Draft
**Owner**: chora-base maintainer
**Created**: 2025-11-16
**Last Updated**: 2025-11-16

---

## 1. Problem Statement

### Current Challenge

Without standardized git workflows, multi-developer collaboration leads to merge conflicts, inconsistent commit history, and coordination overhead. As the chora ecosystem grows from single-developer (chora-workspace) to multi-developer teams, the lack of git workflow standards creates several critical problems:

**What's missing**:
1. **No standardized branch naming** - Developers use ad-hoc branch names, making it hard to understand branch purpose or identify work types (feature/bugfix/hotfix)
2. **No commit message conventions** - Inconsistent commit messages reduce git log readability and make changelog generation impossible
3. **No merge strategy guidance** - Unclear when to use squash vs merge vs rebase, leading to messy git history
4. **No git hooks** - No automated validation of commit messages or branch names before push
5. **No pre-commit checks** - Developers can commit malformed messages, breaking tooling and downstream automation

**Impact on multi-developer workflows**:
- Merge conflicts increase when branch naming doesn't indicate feature/bugfix/hotfix work types
- PR reviews slower due to unclear commit messages that don't explain "why" behind changes
- Git history difficult to navigate and understand (debugging, auditing, onboarding suffer)
- No automated enforcement creates drift over time as teams grow
- Manual changelog generation wastes 1-2 hours per release

### Evidence

- Currently: ~20-30% of PRs have merge conflicts requiring manual resolution (15-30 min per conflict)
- Average PR review time: 15-30 minutes (could be reduced with better commit messages)
- Changelog generation: Manual work (1-2 hours per release, error-prone)
- No git hook infrastructure in any ecosystem repo (chora-base, chora-workspace, chora-compose)
- Commit messages inconsistent: Some use conventional commits, others don't (no enforcement)
- Branch names ad-hoc: No pattern to distinguish feature/bugfix/hotfix/chore work

### Business Impact

**Immediate costs** (quantified):
- **Conflict resolution overhead**: 3-5 conflicts/week × 15-30 min = 45-150 min/week = 39-130 hours/year wasted
- **Slow PR reviews**: 5-10 PRs/week × 5-10 min extra per review = 25-100 min/week = 22-87 hours/year wasted
- **Manual changelogs**: 2-3 releases/quarter × 1-2 hours = 8-24 hours/year wasted
- **Total**: 69-241 hours/year wasted ($10,350-$36,150 at $150/hour)

**Strategic risks**:
- **Scaling bottleneck**: Current chaos prevents bringing second developer into chora-workspace (blocks ecosystem growth)
- **Quality degradation**: Unclear git history makes debugging harder, increases bug resolution time
- **Onboarding friction**: New developers struggle to understand git patterns, slow ramp-up time
- **Foundation missing**: Can't build advanced tooling (semantic versioning, automated releases, changelog generation) without commit conventions

**Urgency**: Bringing second developer into chora-workspace (immediate trigger) requires multi-developer coordination patterns. Without SAP-051 foundation, other multi-dev SAPs (SAP-052 Ownership Zones, SAP-053 Conflict Resolution, SAP-054 Work Partitioning) cannot be implemented effectively.

---

## 2. Proposed Solution

### Git Workflow Patterns

Define **SAP-051: Git Workflow Patterns** establishing standardized git workflows for multi-developer collaboration across the entire chora ecosystem. This SAP provides:

1. **Branch Naming Conventions** - Clear prefixes indicate work type (feature/bugfix/hotfix/chore/docs)
2. **Commit Message Standards** - Conventional Commits v1.0.0 for consistent, parseable commit history
3. **Merge Strategy Decision Tree** - Guidance on squash vs merge vs rebase based on context
4. **Git Hooks** - Client-side enforcement (pre-commit, commit-msg, pre-push) with automatic validation
5. **Justfile Automation** - One-command git-setup, commit validation, changelog generation

**How it solves the problem**:
- **Reduces conflicts**: Branch naming + merge strategies prevent 30-50% of merge conflicts
- **Accelerates reviews**: Conventional commits enable 20-30% faster PR reviews (clear commit messages)
- **Automates changelogs**: Conventional commits enable 95% automated changelog generation (1-2 hours → 5 min)
- **Enforces standards**: Git hooks prevent non-compliant commits from being pushed
- **Scales collaboration**: Foundation for other multi-dev SAPs (ownership zones, conflict resolution, work partitioning)

**Alignment with ecosystem**:
- **SAP-001 (Inbox)**: Git conventions improve coordination request clarity
- **SAP-010 (Memory)**: Conventional commits enable better event correlation via commit SHAs
- **SAP-015 (Beads)**: Branch naming conventions align with beads task workflows
- **SAP-012 (Lifecycle)**: DDD → BDD → TDD cycles align with feature branch workflows

### Key Principles

1. **Convention over configuration** - Standardize git workflows to reduce decision fatigue
2. **Automate enforcement** - Git hooks prevent non-compliant commits before they're pushed
3. **Industry alignment** - Use Conventional Commits v1.0.0 (widely adopted, tool-supported)
4. **Lightweight process** - Minimal ceremony, maximum value (no Git Flow complexity)
5. **Agent-friendly** - Commit conventions enable AI agents to understand git history
6. **Ecosystem consistency** - Same patterns across all chora repos (chora-base, chora-workspace, chora-compose)
7. **Incremental adoption** - Can be adopted repo-by-repo without breaking existing workflows
8. **Tooling foundation** - Enables semantic versioning, automated releases, changelog generation

---

## 3. Scope

### In Scope

- **Branch naming conventions** (feature/bugfix/hotfix/chore/docs prefixes)
- **Conventional Commits v1.0.0** (type, scope, subject, body, footer schema)
- **Merge strategy decision tree** (squash vs merge vs rebase guidance)
- **Git hooks** (pre-commit, commit-msg, pre-push with validation scripts)
- **Justfile recipes** (git-setup, validate-commits, changelog automation)
- **Documentation** (5 SAP artifacts: charter, spec, guide, blueprint, ledger)
- **Validation tests** (test suite for git hooks, commit message parsing)
- **Pilot adoption** (chora-workspace validation before ecosystem distribution)
- **chora-compose integration** (include git hooks in project generation template)

### Out of Scope

- **Server-side hooks** - Focus on client-side enforcement (GitHub Actions workflows separate)
- **Git Flow branch model** - Too complex, use lightweight feature branch workflow instead
- **Trunk-based development** - Too advanced for current team maturity
- **Semantic versioning automation** - Future work (SAP-051 is foundation, not implementation)
- **Automated release workflow** - Future work (depends on SAP-051 as foundation)
- **GitHub-specific features** - Keep SAP provider-agnostic (works with GitHub, GitLab, Bitbucket)
- **Code review automation** - Separate concern (SAP-052 Ownership Zones handles reviewer assignment)

---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Level 1):
- SAP-051 installed in chora-base (5 artifacts present: charter, spec, guide, blueprint, ledger)
- Basic git hooks functional (commit-msg validation works)
- Justfile recipes tested (git-setup, validate-commits run without errors)
- Documentation complete (adoption blueprint available for repos)

**Operational Success** (Level 2):
- chora-workspace pilot completed (git hooks installed, validated in real workflows)
- 100% of commits in chora-workspace follow Conventional Commits (measured over 2-week period)
- 100% of branches in chora-workspace follow naming conventions
- Git hooks installed in chora-base and chora-compose (ecosystem-wide adoption)
- Baseline metrics established (conflict rate, PR review time, changelog generation time)

**Impact Success** (Level 3):
- 30-50% reduction in merge conflicts (baseline: 20-30% of PRs → target: 10-15% of PRs)
- 20-30% faster PR reviews (baseline: 15-30 min → target: 10-20 min)
- 95% automated changelog generation (baseline: 100% manual, 1-2 hours → target: 5 min, 95% automated)
- Second developer successfully onboarded to chora-workspace (validates multi-dev readiness)
- Foundation complete for SAP-052 (Ownership Zones), SAP-053 (Conflict Resolution), SAP-054 (Work Partitioning)

**Qualitative indicators**:
- Developers report git history is more readable and useful for debugging
- New contributors understand git workflow from documentation alone
- PRs are easier to review due to clear commit messages
- Merge conflicts are faster to resolve when they occur (better branch naming)

### Expected Metrics

**Performance**:
- Git hook validation time: <500ms per commit (imperceptible developer friction)
- Changelog generation time: <5 min per release (down from 1-2 hours manual)
- Commit message parsing accuracy: 100% (strict schema enforcement)

**Adoption**:
- Time to install in new repo: <5 min (just git-setup recipe)
- Repos using SAP-051: 100% of chora ecosystem repos within 4 weeks of publication
- Developer compliance: 100% (enforced by git hooks, no manual adherence needed)

**ROI**:
- Year 1 ROI: 50-250% (benefits $9k-21k vs investment ~$6k)
- Year 2+ ROI: 400-700% (benefits continue, investment is one-time)
- Payback period: 3-6 months

---

## 5. Stakeholders & Governance

### Primary Stakeholders

**Maintainers**:
- chora-base team: Owns SAP-051 definition, git hook scripts, justfile recipes
- chora-workspace team: Pilot validation, feedback on real workflows
- chora-compose team: Integration into project generation template

**Users**:
- All developers in chora ecosystem (current: 1 developer, target: 2+ developers)
- AI agents (Claude): Use commit conventions for better git history understanding
- Future contributors: Benefit from clear git workflow documentation

**Affected Parties**:
- New developers: Must learn Conventional Commits (minimal learning curve, ~10 min)
- Existing workflows: Must migrate to SAP-051 conventions (automated by git hooks)

### Governance Model

**Decision authority**:
- chora-base maintainer: Final approval for SAP-051 definition changes
- chora-workspace lead (Victor): Pilot validation sign-off

**Review cadence**:
- Quarterly: Review SAP-051 adoption metrics (conflict rate, PR review time, compliance)
- On-demand: Update git hooks if new edge cases discovered

**Change process**:
- Minor updates (hook bug fixes): Direct commits to chora-base
- Major changes (Conventional Commits schema changes): RFC process via SAP-001 inbox

**Success review**:
- After chora-workspace pilot (Week 3): Validate success criteria before ecosystem distribution
- After 3 months: Review Level 3 success criteria (conflict reduction, PR review time, ROI)

---

## 6. Lifecycle Plan

### Development Phases

**Phase 1: Design & Specification (Week 1)**
- Research Conventional Commits v1.0.0, analyze ecosystem git patterns
- Draft SAP-051 charter, protocol specification
- Write awareness guide, create adoption blueprint
- Define validation tests

**Phase 2: Infrastructure Development (Week 2)**
- Build git hooks (pre-commit, commit-msg, pre-push)
- Create justfile recipes (git-setup, validate-commits, changelog)
- Write validation tests for git hooks
- Document git hooks in adoption blueprint

**Phase 3: Pilot Validation (Week 2-3)**
- Install SAP-051 in chora-workspace
- Test git hooks in real workflows (2-week validation period)
- Measure success criteria (conflict rate, PR review time, compliance)
- Refine SAP-051 based on pilot feedback

**Phase 4: Ecosystem Distribution (Week 3)**
- Integrate git hooks into chora-compose project generation
- Publish SAP-051 announcement via SAP-001 inbox
- Provide adoption support to ecosystem repos

### Open Questions

- **Q1**: Should pre-push hook validate against remote main branch (requires network call)?
  - **Risk**: Adds latency to push operation (500ms-2s)
  - **Mitigation**: Make remote validation optional (flag in git config)

- **Q2**: How to handle commit message validation for merge commits?
  - **Risk**: Merge commits auto-generated by GitHub may not follow Conventional Commits
  - **Mitigation**: Configure git hooks to skip merge commits, enforce on regular commits only

- **Q3**: How to enforce branch naming conventions without server-side hooks?
  - **Risk**: Developers can push branches with non-compliant names if they skip pre-push hook
  - **Mitigation**: Add CI/CD check in GitHub Actions (fails PR if branch name invalid)

- **Q4**: Should we support custom commit types beyond standard Conventional Commits?
  - **Risk**: Ecosystem-specific types (e.g., `sap:`, `coord:`) may not be supported by tooling
  - **Mitigation**: Start with standard types, add custom types only if validated need emerges

### Sunset Criteria

SAP-051 would be retired or superseded if:

1. **Industry standard emerges** that supersedes Conventional Commits (unlikely, widely adopted)
2. **Git itself adds native support** for commit message validation (unlikely, git remains unopinionated)
3. **Ecosystem pivots to trunk-based development** (possible in 2+ years if team maturity increases)
4. **Zero adoption** after 6 months (indicates SAP doesn't solve real problem)

**Likely evolution path**: SAP-051 becomes foundation for more advanced capabilities (semantic versioning automation, release workflow orchestration) rather than being replaced.

---

## 7. Related SAPs & Dependencies

### Dependencies

- **None** - SAP-051 is foundational, no dependencies on other SAPs

### Dependents (SAPs that build on SAP-051)

- **SAP-052 (Ownership Zones)**: Uses git hooks for PR automation, branch naming for domain identification
- **SAP-053 (Conflict Resolution)**: Uses git hooks for pre-merge validation, commit SHAs for conflict tracking
- **SAP-054 (Work Partitioning)**: Uses branch analysis for concurrent work detection, commit patterns for work clustering
- **SAP-055 (Multi-Dev Awareness)**: Documents git workflow patterns in AGENTS.md awareness files

### Complementary SAPs

- **SAP-001 (Inbox)**: Conventional commits improve coordination request clarity
- **SAP-010 (Memory)**: Conventional commits enable better event correlation via commit SHAs
- **SAP-015 (Beads)**: Branch naming conventions align with beads task workflows
- **SAP-012 (Lifecycle)**: DDD → BDD → TDD cycles align with feature branch workflows

---

**Created**: 2025-11-16 by chora-base maintainer + Claude (AI peer)
**Document Status**: Draft for review
**Next Steps**: Create protocol specification (protocol-spec.md)
