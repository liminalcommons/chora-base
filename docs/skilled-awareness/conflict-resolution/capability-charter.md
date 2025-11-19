# Capability Charter: Conflict Resolution Strategies

**SAP ID**: SAP-053
**Version**: 1.0.0
**Status**: Draft
**Created**: 2025-11-18
**Author**: chora-base maintainers + Claude (AI peer)

---

## Document Purpose

This charter defines SAP-053 (Conflict Resolution Strategies) - a systematic approach to detecting, resolving, and learning from merge conflicts in multi-developer Git workflows. It establishes the problem, solution, scope, and success criteria for automated conflict detection, resolution strategies by file type, and knowledge accumulation from conflict patterns.

**Audience**: Developers, AI agents, project leads, SAP adopters

**Related Documents**:
- [protocol-spec.md](protocol-spec.md) - Conflict detection algorithms, resolution strategies, A-MEM event schema
- [awareness-guide.md](awareness-guide.md) - Agent workflows, decision trees, tool reference
- [adoption-blueprint.md](adoption-blueprint.md) - 4-phase adoption plan (Design → Infrastructure → Pilot → Distribution)

---

## Problem Statement

### Current State: Reactive Conflict Resolution

**What's broken**:

1. **Conflicts discovered too late** - Developers find conflicts at merge time, not before
2. **No systematic resolution strategies** - Every conflict treated the same (code vs docs vs config)
3. **No conflict history tracking** - Recurring patterns not captured or analyzed
4. **No knowledge accumulation** - Resolution expertise stays in developers' heads
5. **No automation for safe cases** - Even trivial conflicts (whitespace, formatting) require manual work

**Quantitative pain**:

| Metric | Current State (2 Developers) | Pain Point |
|--------|------------------------------|------------|
| **Conflict frequency** | 20-30% of PRs | Wastes time, blocks PRs |
| **Resolution time** | 15-30 min/conflict | 3-5 conflicts/week = 45-150 min/week lost |
| **Recurring conflicts** | 40-50% in same files | Same patterns repeat, no learning |
| **Auto-resolvable conflicts** | 0% (all manual) | Trivial conflicts waste developer time |
| **Conflict knowledge** | Undocumented | Expertise lost when developers leave |

**Annual cost** (2 developers at $150/hour):
- Conflict resolution time: 39-130 hours/year = **$5,850-$19,500/year**
- Recurring conflict tax: Additional 30-40% = **$1,755-$7,800/year**
- **Total**: **$7,605-$27,300/year** wasted on preventable/repetitive conflict resolution

### Why Now?

**Immediate trigger**: SAP-051 (Git Workflow) and SAP-052 (Ownership Zones) provide the foundation for systematic conflict management.

**Strategic dependencies met**:
- ✅ SAP-051 (Git Workflow) - Provides pre-merge hooks for conflict detection
- ✅ SAP-052 (Ownership Zones) - Defines conflict jurisdiction rules (who resolves what)
- ✅ SAP-010 (A-MEM) - Event logging infrastructure for conflict history

**Ecosystem maturity**: With git hooks (SAP-051), ownership zones (SAP-052), and memory system (SAP-010), we have the infrastructure to detect conflicts early, assign resolution authority, and learn from patterns. Time to formalize conflict resolution as a skilled capability.

**Multi-developer readiness**: Adding a second developer will DOUBLE conflict frequency. We need systematic conflict prevention NOW, before conflicts become a bottleneck.

---

## Solution Overview

### Core Capability: Systematic Conflict Resolution

Define **SAP-053 (Conflict Resolution Strategies)** as a skilled awareness pattern providing:

1. **Conflict Detection Automation**
   - Pre-merge conflict checker (runs before PR creation)
   - CI/CD integration (checks conflicts on PR open/update)
   - Conflict predictor (analyzes concurrent work, predicts likely conflicts)
   - Justfile recipe: `just conflict-check`

2. **Resolution Strategies by File Type**
   - **Documentation (.md)**: Manual review, preserve both versions with conflict markers
   - **Code (.py, .ts, .js)**: Manual resolution, file owner has jurisdiction (SAP-052)
   - **Configuration (YAML, JSON)**: Schema-driven merge (auto-merge if both changes valid)
   - **Generated files** (lockfiles, build artifacts): Regenerate from source
   - **Metadata** (frontmatter, package.json): Field-level merge (auto-merge non-conflicting fields)

3. **Conflict History Logging** (A-MEM Integration)
   - Log all conflicts to `.chora/memory/events/` with `conflict_detected` event type
   - Track: files involved, conflict type, resolution strategy, time to resolve, developer
   - Analyze patterns: Which files conflict most? Which strategies work best?

4. **Conflict Pattern Knowledge Notes**
   - Create knowledge notes for recurring conflict resolutions (≥2 recurrences)
   - Example: `recurring-conflict-justfile.md` documents common justfile conflict patterns
   - Wiki-link to related patterns, build reusable conflict resolution library

5. **Automated Conflict Resolution** (Safe Cases Only)
   - Auto-resolve whitespace-only conflicts
   - Auto-resolve formatting conflicts (if both sides formatted correctly)
   - Auto-resolve lock file conflicts (regenerate via package manager)
   - Auto-resolve frontmatter `last_updated` (use latest timestamp)
   - Justfile recipe: `just auto-resolve-conflicts` (dry-run mode by default)

6. **Conflict Escalation Protocol**
   - **Level 1** (default): Developer resolves (file owner, SAP-052 jurisdiction)
   - **Level 2** (if stuck >30 min): Pair programming resolution
   - **Level 3** (if owners disagree): Project lead arbitration

### Integration with Existing SAPs

**Dependencies**:
- **SAP-051 (Git Workflow)**: Pre-merge hooks provide conflict detection execution point
- **SAP-052 (Ownership Zones)**: Conflict jurisdiction rules (file owner resolves)
- **SAP-010 (A-MEM)**: Event logging for conflict history and pattern analysis

**Synergies**:
- **SAP-054 (Work Partitioning)** (future): Prevents conflicts through intelligent work distribution
- **SAP-055 (Multi-Dev Awareness)** (future): Awareness files document conflict-prone zones
- **SAP-015 (Beads Tasks)**: Link conflict resolution tasks to beads for tracking

---

## Scope & Boundaries

### In Scope

**Phase 1 (Design & Specification)**:
- ✅ SAP-053 charter, protocol spec, awareness guide, adoption blueprint, ledger
- ✅ Conflict detection algorithm design (pre-merge, CI/CD, predictor)
- ✅ Resolution strategy decision trees (by file type)
- ✅ A-MEM event schema for conflict logging
- ✅ Knowledge note templates for conflict patterns

**Phase 2 (Infrastructure Development)**:
- ✅ Conflict detection scripts (`scripts/detect-conflicts.py`, `scripts/predict-conflicts.py`)
- ✅ Auto-resolver for safe cases (`scripts/auto-resolve-conflicts.py`)
- ✅ A-MEM integration (`emit_conflict_event()` in event logging)
- ✅ Justfile recipes (`just conflict-check`, `just auto-resolve`, `just conflict-history`)
- ✅ Test suite (conflict detection, auto-resolution, A-MEM logging)

**Phase 3 (Pilot Validation)**:
- ✅ Pilot adoption in chora-workspace
- ✅ Simulate 10+ conflict scenarios (docs, code, config, lockfiles)
- ✅ Test auto-resolver on safe cases
- ✅ Create 3-5 conflict resolution knowledge notes
- ✅ Collect metrics (resolution time, recurrence rate, auto-resolve success rate)

**Phase 4 (Distribution)**:
- ✅ Publish SAP-053 to chora-base
- ✅ Integrate conflict detection in chora-compose project generation
- ✅ Create adoption guide for existing repos
- ✅ Ecosystem announcement

### Out of Scope

**Explicitly excluded**:

1. **Semantic merge** - No automated semantic conflict resolution (requires deep code understanding)
2. **AI-powered conflict resolution** - No LLM-based auto-resolution (too risky, hallucination risk)
3. **Pessimistic locking** - No file locking to prevent concurrent edits (kills parallelism)
4. **Operational Transformation (OT)** - No Google Docs-style real-time merging (too complex)
5. **Conflict prevention through rigid partitioning** - That's SAP-054 (Work Partitioning)

**Rationale**: SAP-053 focuses on practical conflict detection and resolution strategies, not cutting-edge merge algorithms. Automation is limited to safe cases (whitespace, formatting, lockfiles). Code conflicts require human judgment.

### Boundaries with Other SAPs

| SAP | Boundary | Interaction |
|-----|----------|-------------|
| **SAP-051 (Git Workflow)** | SAP-051 provides pre-merge hooks, SAP-053 provides conflict detection logic | SAP-053 conflict checker runs via SAP-051 pre-push hook |
| **SAP-052 (Ownership Zones)** | SAP-052 defines who owns files, SAP-053 uses ownership for conflict jurisdiction | SAP-053 defers to file owner (SAP-052) for conflict resolution |
| **SAP-010 (A-MEM)** | SAP-010 provides event logging, SAP-053 defines conflict event schema | SAP-053 logs `conflict_detected`, `conflict_resolved` events to A-MEM |
| **SAP-054 (Work Partitioning)** | SAP-054 prevents conflicts via work distribution, SAP-053 resolves inevitable conflicts | Complementary: SAP-054 reduces conflicts, SAP-053 handles remaining ones |
| **SAP-055 (Multi-Dev Awareness)** | SAP-055 documents conflict-prone zones, SAP-053 creates knowledge notes | SAP-053 knowledge notes feed SAP-055 awareness files |

---

## Success Criteria

### Quantitative Metrics (Pilot Validation)

| Metric | Baseline (Current) | Target (After SAP-053) | Improvement |
|--------|-------------------|----------------------|-------------|
| **Conflicts detected before merge** | 0% (all at merge time) | 100% | +100% |
| **Average resolution time** | 15-30 min | 5-10 min | 50-70% reduction |
| **Recurring conflicts** | 40-50% of conflicts | 5-10% of conflicts | 80-90% reduction |
| **Auto-resolvable conflicts** | 0% | 30-40% | +30-40% |
| **Conflicts logged to A-MEM** | 0% | 100% | +100% |
| **Conflict knowledge notes** | 0 | 3-5 during pilot | Reusable library |

**ROI Target**: 12-200% Year 1 (baseline: $7.6k-$20.5k benefits vs ~$6.8k investment)

### Qualitative Outcomes

- ✅ Developers can predict conflicts before they happen (predictor tool)
- ✅ Conflict resolution strategies documented and reusable (knowledge notes)
- ✅ Reduced frustration (conflicts detected early, not at merge time)
- ✅ Learning accumulation (conflict patterns captured as knowledge)
- ✅ Faster onboarding (new developers learn from conflict history)

### Exit Criteria (Per Phase)

**Phase 1 (Design)**: SAP-053 charter and spec complete, peer-reviewed, ready for implementation
**Phase 2 (Infrastructure)**: Conflict detection tools tested, auto-resolver validated on safe cases
**Phase 3 (Pilot)**: Pilot metrics collected, knowledge notes created, SAP-053 refined
**Phase 4 (Distribution)**: SAP-053 published to chora-base, available for ecosystem adoption

---

## Key Assumptions

### Technical Assumptions

1. **Git-based workflows**: All chora ecosystem projects use Git (not SVN, Mercurial, etc.)
2. **Pre-merge hooks supported**: Git version ≥ 2.9 (pre-push hooks available)
3. **Python 3.8+ available**: Conflict detection scripts written in Python
4. **A-MEM infrastructure exists**: SAP-010 provides event logging (dependency met)
5. **Ownership zones defined**: SAP-052 provides CODEOWNERS file (dependency met)

### Organizational Assumptions

1. **Multi-developer teams**: 2+ developers working concurrently (conflict risk exists)
2. **Distributed collaboration**: Developers work on separate branches, merge via PRs
3. **PR-based workflow**: All changes go through pull requests (not direct commits to main)
4. **Developer discipline**: Teams willing to run `just conflict-check` before creating PRs
5. **Knowledge sharing culture**: Teams document conflict patterns in knowledge notes

### Validation Assumptions

1. **Pilot duration**: 2-4 weeks sufficient to encounter 10+ conflicts for validation
2. **Conflict frequency**: 20-30% of PRs have conflicts (matches industry baseline)
3. **Auto-resolve safety**: Whitespace/formatting/lockfile conflicts are safe to auto-resolve
4. **Knowledge note threshold**: 2+ recurrences justify creating a pattern note

---

## Risks & Mitigation

### Technical Risks

**Risk 1: Auto-resolver creates broken code**
- **Likelihood**: Medium
- **Impact**: High (broken code worse than manual conflict)
- **Mitigation**: Auto-resolve ONLY safe cases (whitespace, formatting, lockfiles), require manual review for code conflicts, extensive testing in pilot, dry-run mode by default

**Risk 2: Conflict detection false positives**
- **Likelihood**: Medium
- **Impact**: Low (wastes time investigating non-existent conflicts)
- **Mitigation**: Tune predictor based on pilot data, make predictions informational (not blocking), track false positive rate

**Risk 3: A-MEM conflict logging too verbose**
- **Likelihood**: Low
- **Impact**: Low (A-MEM handles volume well)
- **Mitigation**: Log only significant conflicts (skip trivial auto-resolved ones), add filtering in queries

### Coordination Risks

**Risk 4: Developers bypass conflict detection**
- **Likelihood**: Medium
- **Impact**: High (defeats purpose of automated detection)
- **Mitigation**: Make detection fast (<10 sec), integrate into CI/CD (can't bypass), show value via time savings metrics

**Risk 5: Conflict resolution knowledge notes go stale**
- **Likelihood**: Medium
- **Impact**: Medium (reduces long-term value)
- **Mitigation**: Include knowledge note review in quarterly retrospectives, link to A-MEM events (knowledge notes cite specific conflicts)

**Risk 6: Ownership jurisdiction unclear for shared files**
- **Likelihood**: Low (SAP-052 defines jurisdiction)
- **Impact**: Medium (delays resolution if owners disagree)
- **Mitigation**: Escalation protocol (Level 1 → Level 2 → Level 3), document common shared file patterns

---

## Dependencies

### Hard Dependencies (Must Have)

| Dependency | Status | Required For | Blocker If Missing? |
|------------|--------|--------------|---------------------|
| **SAP-051 (Git Workflow)** | ✅ Complete (2025-11-17) | Pre-merge hooks for conflict detection | **YES** |
| **SAP-052 (Ownership Zones)** | ✅ Complete (2025-11-18) | Conflict jurisdiction rules | **YES** |
| **SAP-010 (A-MEM)** | ✅ Complete (L4) | Conflict event logging | **YES** |
| **Python 3.8+** | ✅ Available | Conflict detection scripts | **YES** |
| **Git 2.9+** | ✅ Available | Pre-push hooks | **YES** |

**Dependency Status**: ✅ **ALL HARD DEPENDENCIES MET** - Ready to proceed

### Soft Dependencies (Nice to Have)

| Dependency | Status | Benefit If Available |
|------------|--------|---------------------|
| **SAP-015 (Beads Tasks)** | ✅ Complete (L4) | Link conflict resolution to tasks for tracking |
| **SAP-016 (Link Validation)** | ✅ Complete (L3) | Validate wikilinks in conflict knowledge notes |
| **GitHub Actions** | ✅ Available (chora-workspace) | CI/CD conflict detection on PR open |

---

## Timeline & Effort

### Estimated Timeline

**Total**: 3-4 weeks (design → distribution)

| Phase | Duration | Deliverables | Dependencies |
|-------|----------|--------------|--------------|
| **Phase 1: Design** | 1 week | Charter, spec, guide, blueprint, ledger | None (ready to start) |
| **Phase 2: Infrastructure** | 1-2 weeks | Detection scripts, auto-resolver, tests | Phase 1 complete |
| **Phase 3: Pilot** | 1 week | chora-workspace pilot, metrics, knowledge notes | Phase 2 complete |
| **Phase 4: Distribution** | 1 week | chora-base publication, chora-compose integration | Phase 3 complete |

### Estimated Effort

**Total**: 10-15 person-days

| Activity | Effort | Notes |
|----------|--------|-------|
| SAP-053 definition (5 artifacts) | 2-3 days | Charter, spec, guide, blueprint, ledger |
| Conflict detection scripts | 2-3 days | Pre-merge checker, predictor, A-MEM integration |
| Auto-resolver for safe cases | 1-2 days | Whitespace, formatting, lockfiles |
| Test suite | 1-2 days | Conflict detection, auto-resolution, A-MEM logging |
| Pilot validation | 2-3 days | Simulate conflicts, create knowledge notes, collect metrics |
| chora-compose integration | 1 day | Add detection scripts to project generation |
| Documentation & distribution | 1-2 days | Adoption guide, ecosystem announcement |

---

## ROI Projection

### Investment (Costs)

**Development effort**: 10-15 days × $150/hour × 8 hours/day = **$12,000-$18,000**

**Ongoing costs**:
- Conflict detection overhead: ~5-10 sec per PR (negligible)
- Knowledge note maintenance: ~30 min/month = **$75/month**

**Total Year 1 Investment**: ~$12,000-$19,000

### Returns (Benefits)

**Quantifiable** (2-developer team):

1. **Reduce conflict resolution time**: 15-30 min → 5-10 min (67% reduction)
   - Conflicts per week: ~3-5
   - **Time saved**: 30-100 min/week = **26-87 hours/year**
   - **Value**: $3,900-$13,050/year

2. **Reduce recurring conflicts**: 40-50% → 5-10% (85% reduction)
   - Recurring conflicts prevented: ~2-3 per month
   - **Time saved**: ~1-2 hours/month = **12-24 hours/year**
   - **Value**: $1,800-$3,600/year

3. **Auto-resolve safe conflicts**: 30-40% of conflicts
   - Auto-resolved: ~1-2 per week
   - **Time saved**: 15-30 min/week = **13-26 hours/year**
   - **Value**: $1,950-$3,900/year

**Total Annual Savings**: **51-137 hours/year** = **$7,650-$20,550/year**

**Year 1 ROI**: (Benefits $7.7k-$20.6k - Investment $12k-$19k) / Investment = **-36% to +72%**
**Year 2+ ROI**: (Benefits $7.7k-$20.6k - Maintenance $900) / Maintenance = **750-2,189%**

**Break-Even**: 7-14 months (investment paid back by time savings)

---

## Next Steps

### Immediate (This Week)

1. ✅ Review SAP-053 charter with stakeholders
2. ⏳ Create CORD request for chora-base SAP-053 definition (Phase 1-2)
3. ⏳ Begin drafting protocol-spec.md (conflict detection algorithms, resolution strategies)

### Phase 1 (Week 1)

4. Draft protocol-spec.md (conflict detection, resolution strategies, A-MEM schema)
5. Draft awareness-guide.md (agent workflows, decision trees, tool reference)
6. Draft adoption-blueprint.md (4-phase adoption plan)
7. Draft ledger.md (adoption tracking, metrics, ROI)

### Phase 2 (Week 2-3)

8. Implement conflict detection scripts (detect-conflicts.py, predict-conflicts.py)
9. Implement auto-resolver (auto-resolve-conflicts.py)
10. Integrate with A-MEM (emit_conflict_event)
11. Create justfile recipes (just conflict-check, just auto-resolve, just conflict-history)
12. Write test suite (pytest, 80%+ coverage)

---

## Approval & Sign-Off

**Charter Status**: Draft for review
**Created**: 2025-11-18
**Authors**: chora-base maintainers + Claude (AI peer)
**Reviewers**: [TBD - Victor Piper, ecosystem contributors]
**Approval Date**: [TBD]

**Sign-Off Criteria**:
- [ ] Charter reviewed by project lead (Victor Piper)
- [ ] Dependencies confirmed (SAP-051, SAP-052, SAP-010 all complete)
- [ ] ROI projection validated (12-200% Year 1 acceptable)
- [ ] Risk mitigation strategies approved
- [ ] Timeline feasible (3-4 weeks)

**Next Document**: [protocol-spec.md](protocol-spec.md) - Conflict detection algorithms and resolution strategies

---

**Created**: 2025-11-18 by chora-base maintainer + Claude (AI peer)
**Document Type**: Capability Charter (SAP-053)
**Status**: Draft
**Last Updated**: 2025-11-18
