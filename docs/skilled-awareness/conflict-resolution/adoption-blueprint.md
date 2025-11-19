# SAP-053: Conflict Resolution - Adoption Blueprint

**Document Type**: Adoption Blueprint
**SAP ID**: SAP-053
**SAP Name**: Conflict Resolution
**Version**: 1.0.0 (Phase 1 - Design)
**Status**: Draft
**Created**: 2025-11-18
**Last Updated**: 2025-11-18
**Author**: Claude (AI peer) + Victor Piper

---

## Document Purpose

This adoption blueprint provides a **4-phase implementation plan** for SAP-053 (Conflict Resolution) across chora ecosystem projects.

**Audience**: Project leads, developers, AI agents adopting SAP-053

**What you'll find here**:
1. **Phase-by-phase roadmap** - Detailed steps for each adoption phase
2. **Effort estimates** - Time investment per phase
3. **Success criteria** - How to measure completion
4. **Risk mitigation** - Common blockers and solutions
5. **Rollback strategy** - How to revert if adoption fails

---

## Overview: 4-Phase Adoption Model

SAP-053 follows the standard chora SAP lifecycle:

| Phase | Duration | Effort | Deliverables | Status |
|-------|----------|--------|--------------|--------|
| **Phase 1: Design** | 1 week | 2-3 days | 5 SAP artifacts (charter, spec, guide, blueprint, ledger) | 🔄 IN PROGRESS |
| **Phase 2: Infrastructure** | 1-2 weeks | 4-6 days | Tools, scripts, tests, justfile recipes | ⏳ PENDING |
| **Phase 3: Pilot** | 1 week | 2-3 days | Validation in chora-workspace, metrics, knowledge notes | ⏳ PENDING |
| **Phase 4: Distribution** | 1 week | 2-3 days | chora-base publication, chora-compose integration | ⏳ PENDING |
| **TOTAL** | **3-4 weeks** | **10-15 days** | **15+ artifacts** | **~20% complete** |

**Current Status**: Phase 1 (Design) in progress - 3 of 5 artifacts complete (charter, protocol-spec, awareness-guide)

---

## Phase 1: Design (Week 1)

### Goals

1. Define SAP-053 problem, solution, and scope
2. Design technical implementation (algorithms, schemas, workflows)
3. Document agent workflows and best practices
4. Plan 4-phase adoption roadmap
5. Create adoption tracking template

### Deliverables

| Artifact | Lines | Status | Owner |
|----------|-------|--------|-------|
| capability-charter.md | 319 | ✅ COMPLETE | Claude + Victor |
| protocol-spec.md | 794 | ✅ COMPLETE | Claude + Victor |
| awareness-guide.md | 880 | ✅ COMPLETE | Claude + Victor |
| adoption-blueprint.md | (this file) | 🔄 IN PROGRESS | Claude + Victor |
| ledger.md | ~200 | ⏳ PENDING | Claude + Victor |

**Total**: ~2,400 lines of design documentation

### Tasks

#### Task 1.1: Review SAP-053 Proposal ✅ COMPLETE

**Input**: [inbox/ecosystem/proposals/prop-008-sap-053-conflict-resolution.md](../../../../../../../inbox/ecosystem/proposals/prop-008-sap-053-conflict-resolution.md)

**Output**: Understanding of problem (20-30% of PRs have conflicts, 15-30 min/resolution) and solution (6 components: detection, strategies, history, knowledge notes, auto-resolution, escalation)

**Time**: 30 minutes

---

#### Task 1.2: Draft capability-charter.md ✅ COMPLETE

**Purpose**: Define problem statement, solution overview, scope, dependencies, timeline, ROI

**Key Sections**:
- Problem statement (conflicts waste $7.6k-$27.3k/year)
- Solution overview (6 components)
- Success criteria (100% detection, 50-70% faster resolution)
- Dependencies (SAP-051 ✅, SAP-052 ✅, SAP-010 ✅)
- ROI projection (12-200% Year 1, 750-2,189% Year 2+)

**Time**: 2-3 hours

**Output**: 319-line charter

---

#### Task 1.3: Draft protocol-spec.md ✅ COMPLETE

**Purpose**: Define technical implementation (algorithms, schemas, tool interfaces)

**Key Sections**:
- Conflict detection algorithms (pre-merge checker, CI/CD, predictor)
- Resolution strategies by file type (6 strategies)
- A-MEM integration schema (conflict_detected, conflict_resolved events)
- Auto-resolution logic (safety criteria)
- Escalation protocol (3 levels)
- Tool interfaces (justfile, Python scripts)
- Testing strategy

**Time**: 3-4 hours

**Output**: 794-line specification

---

#### Task 1.4: Draft awareness-guide.md ✅ COMPLETE

**Purpose**: Document agent workflows, decision trees, best practices

**Key Sections**:
- 4 agent workflows (pre-PR check, CI/CD response, pattern detection, risk prediction)
- 4 decision trees (detection, strategy selection, escalation, knowledge notes)
- Tool reference (justfile recipes, scripts, A-MEM queries)
- 5 best practices
- Integration patterns (SAP-051, SAP-052, SAP-010)
- 5 common scenarios with solutions
- Metrics and anti-patterns

**Time**: 3-4 hours

**Output**: 880-line guide

---

#### Task 1.5: Draft adoption-blueprint.md 🔄 IN PROGRESS

**Purpose**: Plan 4-phase adoption roadmap

**Key Sections**:
- Phase-by-phase tasks and deliverables
- Effort estimates and success criteria
- Risk mitigation and rollback strategy
- Multi-repository adoption sequence

**Time**: 2-3 hours

**Output**: This file (~600 lines)

---

#### Task 1.6: Draft ledger.md ⏳ PENDING

**Purpose**: Create adoption tracking template

**Key Sections**:
- Adoption status table (L0 → L4)
- Metrics baseline and targets
- Milestone tracking
- Knowledge note inventory
- ROI calculation template

**Time**: 1-2 hours

**Output**: ~200 lines

---

### Success Criteria (Phase 1)

- [ ] All 5 SAP artifacts created (charter, spec, guide, blueprint, ledger)
- [ ] Total documentation ≥2,000 lines
- [ ] Dependencies verified (SAP-051 ✅, SAP-052 ✅, SAP-010 ✅)
- [ ] Stakeholder review completed (Victor approves design)
- [ ] CORD request created for chora-base SAP-053 definition

**Exit Gate**: Cannot proceed to Phase 2 until all Phase 1 artifacts are approved.

---

## Phase 2: Infrastructure (Weeks 2-3)

### Goals

1. Implement conflict detection tools (checker, predictor)
2. Implement resolution tools (resolver, auto-resolver)
3. Implement A-MEM integration (pattern detector)
4. Write comprehensive test suite (100+ test cases)
5. Create justfile recipes for all workflows
6. Integrate with SAP-051 (pre-push hook)

### Deliverables

| Artifact | Lines | Type | Status |
|----------|-------|------|--------|
| conflict-checker.py | ~300 | Script | ⏳ PENDING |
| conflict-resolver.py | ~400 | Script | ⏳ PENDING |
| conflict-auto-resolver.py | ~250 | Script | ⏳ PENDING |
| conflict-predictor.py | ~350 | Script | ⏳ PENDING |
| conflict-pattern-detector.py | ~300 | Script | ⏳ PENDING |
| conflict-stats.py | ~200 | Script | ⏳ PENDING |
| test_conflict_detection.py | ~200 | Test | ⏳ PENDING |
| test_resolution_strategies.py | ~250 | Test | ⏳ PENDING |
| test_amem_integration.py | ~150 | Test | ⏳ PENDING |
| justfile (SAP-053 recipes) | ~100 | Config | ⏳ PENDING |
| .git/hooks/pre-push (SAP-051) | ~50 | Hook | ⏳ PENDING |

**Total**: ~2,550 lines of implementation code + tests

### Tasks

#### Task 2.1: Implement conflict-checker.py

**Purpose**: Detect conflicts before merge (pre-PR workflow)

**Key Functions**:
- `check_for_conflicts(branch)` - Test merge simulation
- `classify_conflicts(files)` - Determine conflict type
- `generate_report(format)` - Text or JSON output

**Algorithm** (from protocol-spec.md):
1. Fetch latest from remote: `git fetch origin`
2. Test merge (no-commit): `git merge --no-commit --no-ff origin/main`
3. Parse conflict markers from git status
4. Classify conflicts (content, whitespace, lockfile, metadata)
5. Abort test merge: `git merge --abort`
6. Return report

**Exit Codes**:
- `0`: No conflicts
- `1`: Conflicts detected (manual review)
- `2`: Auto-resolvable conflicts
- `3`: Tool error

**Time**: 1-2 days

**Testing**: 20+ test cases (content conflicts, whitespace conflicts, lockfiles, metadata, no conflicts)

---

#### Task 2.2: Implement conflict-resolver.py

**Purpose**: Interactive conflict resolution with strategy guidance

**Key Functions**:
- `select_resolution_strategy(file, conflict_type)` - Choose strategy
- `resolve_manual(file)` - Guided manual resolution
- `resolve_with_ownership(file)` - SAP-052 integration
- `log_resolution(file, strategy, time)` - A-MEM logging

**Workflow**:
1. Analyze file type and conflict type
2. Select resolution strategy (decision tree from awareness-guide)
3. For MANUAL_REVIEW_WITH_OWNERSHIP: Query CODEOWNERS, suggest contacting owner
4. Present options: accept ours, accept theirs, edit manually, escalate
5. Execute resolution
6. Log to A-MEM (conflict_resolved event)
7. Commit (optional)

**Time**: 2 days

**Testing**: 15+ test cases (each resolution strategy, ownership integration, escalation)

---

#### Task 2.3: Implement conflict-auto-resolver.py

**Purpose**: Automatically resolve safe conflicts (formatting, lockfiles, metadata)

**Key Functions**:
- `auto_resolve_formatting(file)` - Accept both, run formatter
- `regenerate_lockfile(file)` - Delete and regenerate
- `delete_and_ignore(file)` - Delete metadata, add to .gitignore
- `verify_safety(file)` - Ensure no semantic changes

**Safety Criteria**:
- Only auto-resolve: whitespace, formatting, lockfile, metadata
- Always validate result (schema check, syntax check, formatter check)
- Rollback on failure (revert to pre-resolution state)

**Time**: 1-2 days

**Testing**: 25+ test cases (each auto-resolvable type, validation failures, rollback)

---

#### Task 2.4: Implement conflict-predictor.py

**Purpose**: Predict conflict risk based on file history and multi-developer activity

**Key Functions**:
- `predict_conflict_risk(files)` - Calculate risk score (0-1)
- `get_edit_frequency(file, days)` - Commit count
- `get_recent_conflicts(file, days)` - A-MEM query
- `get_multi_dev_activity(file, days)` - Contributor count

**Risk Score Calculation**:
```python
risk_score = (
    0.4 * edit_frequency_score +  # How often edited
    0.4 * conflict_history_score + # Past conflicts
    0.2 * multi_dev_score          # Multiple contributors
)

# Classify:
# risk < 0.3 = LOW
# 0.3 ≤ risk < 0.7 = MEDIUM
# risk ≥ 0.7 = HIGH
```

**Time**: 1-2 days

**Testing**: 10+ test cases (low/medium/high risk files, edge cases)

---

#### Task 2.5: Implement conflict-pattern-detector.py

**Purpose**: Query A-MEM for recurring conflicts, create knowledge notes

**Key Functions**:
- `query_conflict_events(days)` - Get conflict_resolved events
- `detect_recurring_patterns(threshold)` - ≥2 conflicts in 90 days
- `create_knowledge_note(file, conflicts)` - Generate note template
- `generate_prevention_recommendations(file, pattern)` - Suggest improvements

**Knowledge Note Template**:
```markdown
---
title: "Conflict Pattern: {file}"
tags: [conflict-pattern, recurring-conflict, sap-053]
related: [{trace_ids}]
---

# Conflict Pattern: {file}

**Frequency**: {count} conflicts in {days} days
**Avg Resolution Time**: {avg_time} minutes

## Analysis

**Common Conflict Types**: {types}
**Resolution Strategies**: {strategies}

## Prevention Recommendations

{recommendations}

## Related Events

{wikilinks to trace_ids}
```

**Time**: 1 day

**Testing**: 8+ test cases (recurring vs one-time, knowledge note generation, wikilink formatting)

---

#### Task 2.6: Implement conflict-stats.py

**Purpose**: Generate conflict metrics dashboard (weekly/monthly/quarterly)

**Key Metrics**:
- Total conflicts (by period)
- Auto-resolved vs manual (percentage)
- Average resolution time (overall, by strategy)
- Most frequent files (top 10)
- Resolution strategies distribution
- Escalation rate (Level 2+, Level 3)
- Time saved vs baseline

**Output Format**: Text (human-readable) or JSON (for automation)

**Time**: 1 day

**Testing**: 5+ test cases (different time periods, edge cases)

---

#### Task 2.7: Write Test Suite

**Test Coverage Target**: ≥80% for all scripts

**Test Suites**:
1. `test_conflict_detection.py` (20+ tests)
   - Content conflicts
   - Whitespace/formatting conflicts
   - Lockfile conflicts
   - Metadata conflicts
   - No conflicts (baseline)
   - Edge cases (empty repo, merge conflicts in tests themselves)

2. `test_resolution_strategies.py` (25+ tests)
   - Each resolution strategy (6 strategies × 3-5 tests each)
   - Strategy selection logic
   - Ownership integration (SAP-052)
   - Escalation triggers

3. `test_amem_integration.py` (15+ tests)
   - Event logging (conflict_detected, conflict_resolved)
   - Event schema validation
   - Query patterns
   - Knowledge note generation

4. `test_auto_resolution.py` (20+ tests)
   - Auto-resolve safety criteria
   - Formatting conflicts
   - Lockfile regeneration
   - Metadata deletion
   - Validation and rollback

**Time**: 2-3 days

**Output**: 100+ test cases, ≥80% coverage

---

#### Task 2.8: Create Justfile Recipes

**Recipe Set**:
```bash
# Conflict detection
conflict-check branch="main"            # Pre-PR conflict check
conflict-check-json branch="main"       # JSON output for CI/CD
conflict-predict                        # Risk prediction for staged files

# Conflict resolution
conflict-resolve file                   # Interactive resolution
conflict-auto-resolve                   # Auto-resolve safe conflicts
conflict-resolve-lockfile file          # Regenerate lockfile

# Pattern detection
conflict-patterns                       # Detect recurring patterns
conflict-history file days="90"         # File-specific history

# Metrics
conflict-stats days="30"                # Weekly/monthly dashboard
```

**Time**: 1 day (includes testing)

---

#### Task 2.9: Integrate with SAP-051 (Pre-Push Hook)

**Hook**: `.git/hooks/pre-push`

**Logic**:
```bash
#!/bin/bash
# SAP-053: Conflict detection before push

just conflict-check-json > /tmp/conflict-report.json

HAS_CONFLICTS=$(jq -r '.has_conflicts' /tmp/conflict-report.json)
AUTO_RESOLVABLE=$(jq -r '.auto_resolvable' /tmp/conflict-report.json)

if [ "$HAS_CONFLICTS" = "true" ]; then
    if [ "$AUTO_RESOLVABLE" = "true" ]; then
        echo "⚠️  Auto-resolvable conflicts detected."
        echo "Run 'just conflict-auto-resolve' before pushing."
        exit 0  # Warn but allow
    else
        echo "❌ Conflicts detected. Resolve before pushing."
        exit 1  # Block push
    fi
fi

echo "✅ No conflicts detected."
exit 0
```

**Installation**: Copy to `.git/hooks/pre-push`, `chmod +x`

**Time**: 2-3 hours (includes testing)

---

### Success Criteria (Phase 2)

- [ ] All 6 scripts implemented (checker, resolver, auto-resolver, predictor, pattern-detector, stats)
- [ ] Test suite ≥100 test cases, ≥80% coverage
- [ ] All tests passing (pytest exit code 0)
- [ ] Justfile recipes created and tested
- [ ] SAP-051 pre-push hook integrated
- [ ] Code review completed (Victor approves implementation)

**Exit Gate**: Cannot proceed to Phase 3 until all tests pass and code is reviewed.

---

## Phase 3: Pilot (Week 3-4)

### Goals

1. Validate SAP-053 tools in chora-workspace (2-developer simulation)
2. Generate 10+ test conflicts across different file types
3. Measure resolution time reduction (target: 50-70% faster)
4. Create 2-3 knowledge notes for recurring patterns
5. Generate pilot report with metrics and findings

### Test Scenarios

| Scenario | File Type | Conflict Type | Expected Strategy | Target Time |
|----------|-----------|---------------|-------------------|-------------|
| **1. Lockfile conflict** | poetry.lock | lockfile | REGENERATE_FROM_SOURCE | 1-2 min |
| **2. Metadata conflict** | .DS_Store | metadata | DELETE_AND_REGENERATE | 30 sec |
| **3. Formatting conflict** | scripts/format.py | whitespace | AUTO_RESOLVE_FORMATTING | 1-2 min |
| **4. Documentation conflict** | docs/README.md | content | MANUAL_REVIEW | 5-10 min |
| **5. Code conflict (owned)** | scripts/validate.py | content | MANUAL_REVIEW_WITH_OWNERSHIP | 10-15 min |
| **6. Sprint plan conflict** | project-docs/sprints/sprint-13.md | content | MANUAL_REVIEW_WITH_OWNERSHIP | 10-15 min |
| **7. Config conflict** | feature-manifest.yaml | content | SCHEMA_DRIVEN_MERGE | 3-5 min |
| **8. Event log conflict** | .chora/memory/events/2025-11.jsonl | content | MANUAL (append both) | 2-3 min |
| **9. Cross-domain conflict** | docs/ + scripts/ + project-docs/ | content | Multi-domain consensus | 20-30 min |
| **10. Recurring pattern** | Same file as scenario 6 | content | Knowledge note trigger | 8-10 min |

**Total Test Time**: 60-90 minutes (vs baseline 150-300 min for 10 conflicts = **50-70% reduction**)

---

### Tasks

#### Task 3.1: Set Up Pilot Environment

**Steps**:
1. Ensure SAP-051, SAP-052, SAP-010 are active in chora-workspace (✅ already met)
2. Install SAP-053 tools (scripts, justfile recipes, pre-push hook)
3. Create baseline metrics:
   - Historical conflict rate (from A-MEM events)
   - Average resolution time (from past 90 days)
   - Most frequent conflict files

**Time**: 1-2 hours

---

#### Task 3.2: Generate Test Conflicts

**Method**: Create 10+ feature branches with intentional conflicts

**Example Workflow** (for scenario 1: lockfile conflict):
```bash
# Branch A: Add dependency X
git checkout -b test-conflict-1a
poetry add requests
git commit -m "Add requests dependency"
git push -u origin test-conflict-1a

# Branch B: Add dependency Y (from main)
git checkout main
git checkout -b test-conflict-1b
poetry add pyyaml
git commit -m "Add pyyaml dependency"
git push -u origin test-conflict-1b

# Attempt merge (will conflict in poetry.lock)
git checkout test-conflict-1a
git merge test-conflict-1b
# → Conflict in poetry.lock

# Test SAP-053 workflow
just conflict-check                    # Detect conflict
just conflict-auto-resolve             # Auto-resolve (regenerate lockfile)
# → Measure time (target: 1-2 min)
```

**Repeat** for all 10 scenarios.

**Time**: 3-4 hours

---

#### Task 3.3: Measure Resolution Metrics

**Metrics to Capture**:
- Conflict detection time (pre-merge check vs discovering during merge)
- Resolution time per conflict type
- Auto-resolution success rate
- Escalation rate (Level 2+)
- Tool errors or false positives

**Method**: Log all resolutions to A-MEM (automatic via tools), then query:

```bash
# Average resolution time by strategy
grep '"type": "conflict_resolved"' .chora/memory/events/2025-11.jsonl | \
  jq -r '[.resolution_strategies[], .resolution_time_minutes] | @tsv'

# Auto-resolution rate
TOTAL=$(grep '"type": "conflict_resolved"' .chora/memory/events/*.jsonl | wc -l)
AUTO=$(grep '"auto_resolved": true' .chora/memory/events/*.jsonl | wc -l)
echo "Auto-resolution rate: $(echo "scale=1; $AUTO / $TOTAL * 100" | bc)%"
```

**Time**: 2 hours (distributed across test scenarios)

---

#### Task 3.4: Create Knowledge Notes

**Trigger**: After 2nd conflict in same file (simulate recurring pattern)

**Method**:
```bash
# Manually trigger pattern detection
just conflict-patterns

# Review generated knowledge note
cat .chora/memory/knowledge/notes/conflict-pattern-sprint-13.md

# Validate content:
# - Frequency accurate?
# - Prevention recommendations relevant?
# - Wikilinks to related events?
```

**Expected Output**: 2-3 knowledge notes for recurring patterns

**Time**: 1-2 hours

---

#### Task 3.5: Generate Pilot Report

**Location**: `project-docs/metrics/sap-053-pilot-validation-report.md`

**Structure** (follow SAP-052 pilot report template):
```markdown
# SAP-053 Pilot Validation Report

**Date**: 2025-11-XX
**Duration**: X hours
**Repository**: chora-workspace
**Status**: ✅ SUCCESS / ⚠️ PARTIAL / ❌ FAILED

## Summary

Validated SAP-053 tools across 10 test scenarios with {metric} resolution time reduction.

## Test Scenarios Executed

| Scenario | File | Strategy | Time | Target | Pass/Fail |
|----------|------|----------|------|--------|-----------|
| 1 | poetry.lock | REGENERATE | 1.5 min | 1-2 min | ✅ PASS |
| ... | ... | ... | ... | ... | ... |

## Key Findings

### Finding 1: {title}
{description}

**Impact**: {impact}
**Recommendation**: {recommendation}

## Metrics Summary

| Metric | Baseline | Pilot | Improvement |
|--------|----------|-------|-------------|
| Avg Resolution Time | 20 min | 8 min | 60% reduction |
| Auto-Resolution Rate | 0% | 40% | +40% |
| Detection Time | N/A | 30 sec | Pre-merge detection |
| Escalation Rate | N/A | 10% | 90% resolved at L1 |

## ROI Projection

{calculation based on metrics}

## Recommendations

{next steps for Phase 4}
```

**Time**: 2-3 hours

---

### Success Criteria (Phase 3)

- [ ] All 10 test scenarios executed and documented
- [ ] Resolution time reduction ≥50% (target: 50-70%)
- [ ] Auto-resolution rate ≥30% (target: 30-40%)
- [ ] ≥2 knowledge notes created for recurring patterns
- [ ] Pilot report generated with metrics and findings
- [ ] Zero blocking issues (all conflicts resolvable within target time)

**Exit Gate**: Cannot proceed to Phase 4 until pilot metrics meet targets.

---

## Phase 4: Distribution (Week 4-5)

### Goals

1. Distribute SAP-053 artifacts to chora-base (template source)
2. Integrate with chora-compose (auto-install in new projects)
3. Create public documentation (README, examples)
4. Monitor adoption metrics across ecosystem
5. Iterate based on feedback

### Deliverables

| Artifact | Location | Type | Status |
|----------|----------|------|--------|
| SAP-053 artifacts | packages/chora-base/docs/skilled-awareness/conflict-resolution/ | Docs | 🔄 IN PROGRESS (Phase 1) |
| Scripts | packages/chora-base/scripts/ | Tools | ⏳ PENDING (Phase 2) |
| Justfile recipes | packages/chora-base/justfile | Config | ⏳ PENDING (Phase 2) |
| Tests | packages/chora-base/tests/ | Tests | ⏳ PENDING (Phase 2) |
| chora-compose integration | packages/chora-compose/templates/ | Integration | ⏳ PENDING (Phase 4) |
| Public README | packages/chora-base/docs/skilled-awareness/conflict-resolution/README.md | Docs | ⏳ PENDING (Phase 4) |

### Tasks

#### Task 4.1: Distribute Artifacts to chora-base

**Steps**:
1. Copy SAP-053 docs from chora-workspace to chora-base:
   ```bash
   # Already in correct location (packages/chora-base/)
   # Commit to chora-base main branch
   cd packages/chora-base
   git add docs/skilled-awareness/conflict-resolution/
   git commit -m "Add SAP-053 (Conflict Resolution) artifacts

   Phase 1 (Design): capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger
   "
   git push
   ```

2. Copy scripts (after Phase 2):
   ```bash
   cd packages/chora-base
   git add scripts/conflict-*.py tests/test_conflict_*.py
   git commit -m "Add SAP-053 implementation (Phase 2)"
   git push
   ```

3. Update chora-base AGENTS.md and CLAUDE.md to reference SAP-053

**Time**: 1 hour

---

#### Task 4.2: Create Public README

**Location**: `packages/chora-base/docs/skilled-awareness/conflict-resolution/README.md`

**Content**:
```markdown
# SAP-053: Conflict Resolution

**Status**: Production-Ready (Phase 4 Complete)
**Version**: 1.0.0
**Pilot Validation**: 2025-11-XX (chora-workspace, 50-70% time reduction)

## Quick Start

### Installation

```bash
# For existing chora projects
just install-sap-053

# For new projects (via chora-compose)
# SAP-053 is auto-installed by default
```

### Usage

```bash
# Before creating PR
just conflict-check

# Auto-resolve safe conflicts
just conflict-auto-resolve

# Interactive resolution
just conflict-resolve <file>
```

## Features

- **Pre-merge conflict detection** (before CI/CD)
- **Auto-resolution** for formatting, lockfiles, metadata (30-40% of conflicts)
- **Risk prediction** (edit high-traffic files safely)
- **Pattern detection** (learn from recurring conflicts)
- **A-MEM integration** (track metrics, build knowledge)

## Documentation

- [capability-charter.md](capability-charter.md) - Problem statement and ROI
- [protocol-spec.md](protocol-spec.md) - Technical implementation
- [awareness-guide.md](awareness-guide.md) - Agent workflows and best practices
- [adoption-blueprint.md](adoption-blueprint.md) - 4-phase adoption plan
- [ledger.md](ledger.md) - Adoption tracking template

## Pilot Results

**Repository**: chora-workspace
**Test Scenarios**: 10
**Resolution Time Reduction**: 50-70%
**Auto-Resolution Rate**: 30-40%
**Status**: ✅ All tests passed

## Dependencies

- SAP-051 (Git Workflow) - Required
- SAP-052 (Ownership Zones) - Required
- SAP-010 (A-MEM) - Required

## Support

- Issues: [chora-base GitHub Issues](https://github.com/chora-ai/chora-base/issues)
- Discussions: [chora-base Discussions](https://github.com/chora-ai/chora-base/discussions)
```

**Time**: 1-2 hours

---

#### Task 4.3: Integrate with chora-compose

**Goal**: Auto-install SAP-053 when creating new chora projects

**Method**:
1. Update chora-compose project template:
   ```yaml
   # packages/chora-compose/templates/project-template.yaml

   saps:
     - SAP-051  # Git Workflow
     - SAP-052  # Ownership Zones
     - SAP-053  # Conflict Resolution (NEW)
     - SAP-010  # A-MEM
   ```

2. Add installation step to `chora-compose init`:
   ```python
   # packages/chora-compose/src/project_generator.py

   def install_sap_053(project_path):
       """Install SAP-053 tools and hooks."""
       # Copy scripts from chora-base
       copy_scripts(
           source=chora_base / "scripts/conflict-*.py",
           dest=project_path / "scripts/"
       )

       # Add justfile recipes
       append_justfile_recipes(
           source=chora_base / "justfile-sap-053.j2",
           dest=project_path / "justfile"
       )

       # Install pre-push hook
       install_git_hook(
           hook_type="pre-push",
           source=chora_base / "hooks/pre-push-sap-053.sh",
           dest=project_path / ".git/hooks/pre-push"
       )
   ```

3. Test new project generation:
   ```bash
   chora-compose init my-new-project
   cd my-new-project

   # Verify SAP-053 installed
   just --list | grep conflict
   # → conflict-check, conflict-auto-resolve, etc.

   ls scripts/conflict-*.py
   # → conflict-checker.py, conflict-resolver.py, etc.
   ```

**Time**: 1-2 days

---

#### Task 4.4: Monitor Adoption Metrics

**Metrics to Track** (via ledger.md in each repo):
- Adoption level (L0 → L4)
- Conflict rate (conflicts/PR)
- Resolution time (average)
- Auto-resolution rate
- Recurring conflict reduction

**Method**: Quarterly review across ecosystem:

```bash
# For each repo (chora-workspace, chora-gateway, chora-orchestration, etc.)
cd repo
just conflict-stats days=90

# Aggregate metrics
# Compare to baseline (pre-SAP-053)
```

**Time**: Ongoing (1 hour/quarter)

---

#### Task 4.5: Iterate Based on Feedback

**Feedback Sources**:
1. GitHub Issues (chora-base repo)
2. A-MEM events (check for tool errors, escalations)
3. Team retros (collect subjective feedback)

**Common Enhancements** (expected in Phase 4):
- Add new resolution strategies (e.g., image conflicts, binary files)
- Improve conflict predictor accuracy (machine learning?)
- Integrate with GitHub API (auto-assign reviewers on conflict)
- Add conflict dashboard (web UI)

**Time**: Ongoing (2-3 hours/month)

---

### Success Criteria (Phase 4)

- [ ] SAP-053 artifacts distributed to chora-base
- [ ] Public README created
- [ ] chora-compose integration complete
- [ ] ≥2 additional repos adopt SAP-053 (e.g., chora-gateway, chora-orchestration)
- [ ] Adoption metrics tracked in ledger.md
- [ ] Feedback loop established (GitHub Issues, team retros)

**Exit Gate**: SAP-053 is production-ready when ≥3 repos achieve L3 adoption.

---

## Multi-Repository Adoption Sequence

### Sequence 1: Foundational Repos (High Priority)

1. **chora-workspace** (meta-repository)
   - Phase 3 pilot ✅
   - Use case: Coordination conflicts across submodules
   - Expected ROI: 50-70% time reduction

2. **chora-base** (template source)
   - Phase 4 distribution ✅
   - Use case: Multi-developer template contributions
   - Expected ROI: 30-50% time reduction

3. **chora-compose** (project generator)
   - Phase 4 integration ✅
   - Use case: Ensure all new projects have SAP-053
   - Expected ROI: N/A (infrastructure)

### Sequence 2: Production Services (Medium Priority)

4. **chora-gateway** (API gateway)
   - Adopt in Q1 2026
   - Use case: Code conflicts in API endpoints
   - Expected ROI: 40-60% time reduction

5. **chora-orchestration** (workflow orchestration)
   - Adopt in Q1 2026
   - Use case: Config conflicts in workflow definitions
   - Expected ROI: 30-50% time reduction

### Sequence 3: Ecosystem Projects (Low Priority)

6. **castalia** (game project)
   - Adopt in Q2 2026
   - Use case: Asset conflicts (JSON, game data)
   - Expected ROI: 20-40% time reduction

7. **chora-n8n** (automation workflows)
   - Adopt in Q2 2026
   - Use case: Workflow definition conflicts
   - Expected ROI: 15-30% time reduction

---

## Risk Mitigation

### Risk 1: Tool Errors During Pilot

**Probability**: Medium (30-40% chance of bugs in Phase 2 implementation)

**Impact**: High (blocks Phase 3 pilot)

**Mitigation**:
- Comprehensive test suite (≥100 test cases, ≥80% coverage) in Phase 2
- Manual testing before automated testing
- Graceful error handling (tool errors don't corrupt git repo)

**Rollback**: Revert scripts, continue manual conflict resolution

---

### Risk 2: Auto-Resolver Introduces Semantic Changes

**Probability**: Low (5-10% if safety criteria are strict)

**Impact**: Critical (could break production code)

**Mitigation**:
- **Conservative safety criteria**: Only auto-resolve whitespace, formatting, lockfiles, metadata
- **Validation step**: Run formatter, schema validator, syntax checker after auto-resolution
- **Rollback on failure**: Revert to pre-resolution state if validation fails

**Rollback**: `git checkout HEAD <file>` to undo auto-resolution

---

### Risk 3: Low Adoption Rate (Developers Bypass Tools)

**Probability**: Medium (20-30% if tools are cumbersome)

**Impact**: Medium (SAP-053 ROI not realized)

**Mitigation**:
- **Make tools fast** (conflict-check in <5 seconds)
- **Integrate with existing workflow** (pre-push hook, not separate command)
- **Show immediate value** (auto-resolve saves 5-10 min)
- **Communicate ROI** (share pilot report metrics)

**Rollback**: N/A (adoption is optional, low risk)

---

### Risk 4: Pilot Metrics Don't Meet Targets

**Probability**: Low (10-15% if design is sound)

**Impact**: Medium (delays Phase 4, requires redesign)

**Mitigation**:
- **Realistic targets**: 50-70% time reduction (not 90%)
- **Multiple test scenarios**: 10+ scenarios cover edge cases
- **Iterate during pilot**: Adjust strategies if early scenarios fail

**Rollback**: Return to Phase 2 (Infrastructure) for fixes, re-run pilot

---

### Risk 5: Dependency SAPs Change (SAP-051, SAP-052, SAP-010)

**Probability**: Low (5-10% in next 6 months)

**Impact**: Medium (SAP-053 integration may break)

**Mitigation**:
- **Monitor dependency SAP updates** (subscribe to chora-base changelog)
- **Version SAP-053 integration** (document which versions of dependencies are compatible)
- **Test integration** during dependency updates

**Rollback**: Pin to known-good versions of dependency SAPs

---

## Rollback Strategy

### Full Rollback (Abandon SAP-053 Adoption)

**Trigger**: Critical issues in Phase 3 pilot (e.g., tool corrupts git repo, >50% of conflicts unresolvable)

**Steps**:
1. Uninstall pre-push hook: `rm .git/hooks/pre-push`
2. Remove justfile recipes: `git checkout justfile`
3. Delete scripts: `rm scripts/conflict-*.py`
4. Continue manual conflict resolution
5. Document lessons learned (post-mortem)

**Time**: 30 minutes

**Impact**: Return to baseline (no SAP-053 benefits, no new risks)

---

### Partial Rollback (Revert to Manual Resolution, Keep Detection)

**Trigger**: Auto-resolver has issues, but conflict-checker is valuable

**Steps**:
1. Disable auto-resolver: Remove `just conflict-auto-resolve` recipe
2. Keep conflict-checker: Continue using `just conflict-check`
3. Resolve all conflicts manually
4. Fix auto-resolver bugs (Phase 2 iteration)
5. Re-pilot auto-resolver separately

**Time**: 15 minutes

**Impact**: Keep detection benefits, reduce auto-resolution risk

---

### Per-Repository Rollback (Rollback in One Repo, Keep in Others)

**Trigger**: SAP-053 works well in chora-workspace but causes issues in chora-gateway

**Steps**:
1. Identify problematic repo (e.g., chora-gateway)
2. Rollback only in that repo (steps above)
3. Continue SAP-053 in other repos (chora-workspace, chora-base)
4. Investigate root cause (repo-specific issue? SAP-053 bug?)
5. Fix and re-adopt in problematic repo later

**Time**: 30 minutes (per repo)

**Impact**: Minimize blast radius, preserve gains in successful repos

---

## Effort Summary

| Phase | Duration | Effort | Key Deliverables | Risk |
|-------|----------|--------|------------------|------|
| Phase 1 | 1 week | 2-3 days | 5 SAP artifacts (2,400+ lines) | Low |
| Phase 2 | 1-2 weeks | 4-6 days | 6 scripts, tests, justfile, hook (2,550+ lines) | Medium |
| Phase 3 | 1 week | 2-3 days | 10 test scenarios, pilot report | Medium |
| Phase 4 | 1 week | 2-3 days | Distribution, integration, monitoring | Low |
| **TOTAL** | **3-4 weeks** | **10-15 days** | **15+ artifacts, 5,000+ lines** | **Low-Medium** |

**vs Original Estimate**: On track (proposal estimated 3-4 weeks, 10-15 days)

**Actual Progress** (as of 2025-11-18):
- Phase 1: 60% complete (3 of 5 artifacts done)
- Phase 2: 0% complete (pending)
- Phase 3: 0% complete (pending)
- Phase 4: 0% complete (pending)
- **Overall**: ~15% complete

**Projected Completion**: Late November / Early December 2025 (if 2-3 hours/day allocation)

---

## ROI Projection

### Investment

| Category | Phase | Effort | Cost (@ $150/hr) |
|----------|-------|--------|------------------|
| Design | Phase 1 | 2-3 days | $2,400-$3,600 |
| Implementation | Phase 2 | 4-6 days | $4,800-$7,200 |
| Validation | Phase 3 | 2-3 days | $2,400-$3,600 |
| Distribution | Phase 4 | 2-3 days | $2,400-$3,600 |
| **Total Development** | **All** | **10-15 days** | **$12,000-$18,000** |
| Annual Maintenance | Ongoing | 0.5 days/month | $900/year |

### Benefits (2-Developer Team)

**Baseline** (pre-SAP-053):
- Conflicts: 3-5/week × 50 weeks = 150-250 conflicts/year
- Resolution time: 15-30 min/conflict
- **Annual time wasted**: 2,250-7,500 min = **37.5-125 hours/year**
- **Annual cost**: $5,625-$18,750

**After SAP-053** (projected):
- Auto-resolution: 30-40% of conflicts (1-2 min each)
- Manual resolution: 50-70% faster (5-10 min vs 15-30 min)
- Recurring conflicts: 80-90% reduction
- **Annual time saved**: 51-137 hours/year
- **Annual savings**: $7,650-$20,550

### ROI Calculation

```
Year 1 ROI = (Benefits - Investment) / Investment
           = ($7,650-$20,550 - $12,000-$18,000) / ($12,000-$18,000)
           = -36% to +72%

Year 2+ ROI = Benefits / Maintenance
            = $7,650-$20,550 / $900
            = 750% to 2,189%

Break-Even: 7-14 months
```

**ROI Sensitivity**:
- **Best case**: High conflict rate, complex conflicts → 72% Year 1, 2,189% Year 2+
- **Worst case**: Low conflict rate, simple conflicts → -36% Year 1, 750% Year 2+
- **Expected**: Medium conflict rate → 12-200% Year 1 (from charter)

---

## Next Steps (Immediate)

### This Week (Phase 1 Completion)

1. ✅ Finish adoption-blueprint.md (this file) - 1 hour remaining
2. ⏳ Draft ledger.md - 1-2 hours
3. ⏳ Create CORD request for chora-base SAP-053 definition - 30 min
4. ⏳ Stakeholder review (Victor approves Phase 1 artifacts) - 1 hour
5. ⏳ Commit Phase 1 artifacts to chora-base - 15 min

**Total Remaining (Phase 1)**: 3-5 hours

---

### Next Week (Phase 2 Start)

1. Implement conflict-checker.py (1-2 days)
2. Write tests for conflict detection (0.5 days)
3. Implement conflict-resolver.py (2 days)
4. Write tests for resolution strategies (0.5 days)

**Goal**: 50% of Phase 2 complete by end of next week

---

## Document Metadata

**Version**: 1.0.0
**Status**: Draft (Phase 1 - Design)
**Last Updated**: 2025-11-18
**Next Review**: After Phase 1 completion (stakeholder review)

**Related Documents**:
- [capability-charter.md](capability-charter.md) - SAP-053 charter
- [protocol-spec.md](protocol-spec.md) - Technical specification
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [ledger.md](ledger.md) - Adoption tracking (to be created)

**SAP Dependencies**:
- SAP-051 (Git Workflow) - ✅ Complete
- SAP-052 (Ownership Zones) - ✅ Complete
- SAP-010 (A-MEM) - ✅ Complete (L4)

---

**Created**: 2025-11-18
**Author**: Claude (AI peer) + Victor Piper
**Trace ID**: sap-053-phase1-design-2025-11-18
