# Capability Charter: Actionable Quality Infrastructure

**Capability ID**: SAP-054
**Modern Namespace**: chora.quality.actionable_infrastructure
**Type**: Meta-Pattern
**Status**: Draft
**Version**: 1.0.0
**Created**: 2025-11-20
**Last Updated**: 2025-11-20

---

## Executive Summary

**SAP-054: Actionable Quality Infrastructure** defines a foundational meta-pattern for complete quality feedback loops that eliminate toil and prevent bypass culture. It establishes the principle "Detection without action is noise" by specifying a 5-phase feedback loop (DETECT → CLASSIFY → REMEDIATE → TRACK → PREVENT) with progressive adoption levels (L0→L4) that enable systematic quality improvement.

**Key Benefits**:
- ✅ **Complete Feedback Loops**: Transform L0 (DETECT-only) quality checks into L2-L4 actionable systems
- 🎯 **Toil Elimination**: Reduce quality check triage time by 60-70% at L1, 85-90% at L2
- 🚫 **Prevent Bypass Culture**: Auto-fix 60-80% of common patterns, reducing `--no-verify` temptation
- 📊 **Trend Detection**: Track quality degradation over time with L3 metrics
- 🔄 **Pre-commit Integration**: Block new issues at source with L4 prevention hooks
- 🏗️ **Meta-Pattern Foundation**: Applies to ALL quality infrastructure (SAP verification, testing, linting, traceability, link validation, etc.)

**Estimated Impact**:
- L0→L1: 2x reduction in triage time (manual categorization becomes automated)
- L1→L2: 5x reduction via automation (60-80% of fixes become one-command operations)
- L2→L3: 1.2x improvement via trend detection (identify degrading metrics early)
- L3→L4: 1.3x improvement via prevention (block new issues before commit)
- **Overall L0→L4: 15-20x improvement over 12 months**

---

## Problem Statement

### Current Challenges

The chora-workspace quality infrastructure has 4 incomplete quality feedback loops creating 2-3 hours/week toil and driving bypass behavior:

1. **Manifest Discovery** (12 results → 6 false positives)
   - **Toil**: Manual verification every week that 6 SAPs are already documented
   - **Pattern**: Discovery matches commits/events but doesn't cross-reference manifest
   - **Status**: L0 (DETECT-only)

2. **Script Refactoring Audit** (147 scripts, 3 metrics)
   - UTF-8 compliance: 65% (84/128) - stagnant for months
   - JSONExporter usage: 24% (34/137)
   - Emoji removal: 38% (57/147)
   - **Toil**: No systematic refactoring workflow, manual script-by-script updates
   - **Status**: L0 (DETECT-only)

3. **Link Validation** (>100 broken links)
   - **Toil**: Manual link fixing or ignoring warnings
   - **Pattern**: Files moved/renamed, no automated link rewriting
   - **Status**: L0 (DETECT-only)

4. **Traceability Validation** (60% pass rate)
   - Pre-existing violations block commits
   - **Pattern**: `--no-verify` bypass becoming normalized
   - Missing vision_ref, missing tests (auto-fixable for many cases)
   - **Status**: L0 (DETECT-only)

**Quantified Toil**:
- Weekly health check triage: 45-60 min
- False positive verification: 20-30 min
- Manual link fixes: 30-45 min
- Pre-commit bypasses: 15-20 min
- **Total: 2-3 hours/week**

**Root Cause**: Quality infrastructure stuck at L0 (DETECT-only), missing:
- CLASSIFY: Auto-fixable? Investigation required? False positive?
- REMEDIATE: Automated fixes for 60-80% of common patterns
- TRACK: Health trends over time to detect degradation
- PREVENT: Integration into pre-commit/save hooks

### Business Impact

- **Ongoing Toil**: 2-3 hours/week (104-156 hours/year) spent on manual triage and fixes
- **Bypass Culture**: `--no-verify` becoming normalized due to pre-existing violations blocking commits
- **Quality Degradation**: Stagnant metrics (65% UTF-8 for months) indicate no systematic improvement
- **False Positive Fatigue**: 50% of manifest discovery results are false positives, creating noise
- **No ROI Path**: Cannot calculate automation ROI without classification and remediation infrastructure

### User Stories

**As a developer**, I want to:
- Automatically filter false positives from quality check results
- Run `just health-fix-*` to auto-fix 60-80% of common violations
- See quality metrics trend over time (improving or degrading?)
- Have pre-commit hooks block NEW issues only (not pre-existing)

**As a project maintainer**, I want:
- Weekly health check results showing: auto-fixable (green), investigate (yellow), false-positive (filtered)
- One-command remediation for batch operations (e.g., add UTF-8 headers to 44 scripts)
- Trend analysis showing if quality is improving or degrading month-over-month
- Quality gates that prevent regressions without blocking on pre-existing issues

**As a quality infrastructure creator**, I want:
- Meta-pattern defining complete feedback loop requirements
- Reference implementations showing L0→L4 progression
- ROI calculation framework for evaluating automation investment
- Guidance on when to build quality infrastructure vs manual process

---

## Solution Design

### Approach

SAP-054 defines a **5-phase feedback loop** that transforms detection-only quality checks into actionable quality improvement systems:

**Phase 1: DETECT** (L0 - Current State)
- Find issues via automated scripts/tools
- Output: List of violations (e.g., "12 untracked features")
- Human action: Manual triage every time

**Phase 2: CLASSIFY** (L1 - 2x Toil Reduction)
- Categorize each violation:
  - ✅ **Auto-fixable**: Can be scripted (e.g., add UTF-8 header)
  - 🔍 **Requires investigation**: Manual analysis needed (e.g., complex refactor)
  - ⚠️ **False positive**: Filter in future runs (e.g., SAP already in manifest)
- Output: JSON with `classification`, `auto_action`, `suggestion` fields
- Human action: Review classifications, focus on investigation items only

**Phase 3: REMEDIATE** (L2 - 5x Toil Reduction via Automation)
- Auto-fix scripts for 60-80% of common patterns
- Justfile recipes: `just health-fix-manifest-discovery`, `just health-fix-scripts`, etc.
- Batch operations (e.g., add UTF-8 headers to 44 scripts in one command)
- Output: Diff showing proposed fixes, confirmation prompt
- Human action: Review and approve auto-fixes

**Phase 4: TRACK** (L3 - 1.2x Improvement via Trend Detection)
- Time-series metrics tracking quality over time
- Trend analysis: improving, degrading, or stable?
- Health dashboards showing week-over-week/month-over-month changes
- Output: Grafana/dashboard showing quality trends
- Human action: Investigate degrading metrics proactively

**Phase 5: PREVENT** (L4 - 1.3x Improvement via Pre-commit Hooks)
- Pre-commit hooks block NEW violations (not pre-existing)
- Auto-fixes run on save/commit (IDE integration)
- Quality baseline maintained automatically
- Output: Git commit blocked if new violations introduced
- Human action: Fix violations before commit

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│          Quality Check (SAP Verification, Testing,          │
│           Linting, Traceability, Link Validation)           │
└─────────────────────────────────────────────────────────────┘
                             │
                             │ SAP-054 5-Phase Feedback Loop
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  L0: DETECT                                                  │
│    - Run quality check script                                │
│    - Output: List of violations                              │
│    - Status: Manual triage required                          │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  L1: CLASSIFY                                                │
│    - Categorize: auto-fixable / investigate / false-positive │
│    - Output: JSON with classification metadata               │
│    - Status: Reduced triage time (60-70%)                    │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  L2: REMEDIATE                                               │
│    - Auto-fix scripts for common patterns                    │
│    - Justfile recipes: just health-fix-*                     │
│    - Status: 85-90% toil reduction                           │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  L3: TRACK                                                   │
│    - Time-series metrics storage                             │
│    - Trend analysis (improving/degrading/stable)             │
│    - Status: Proactive quality monitoring                    │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  L4: PREVENT                                                 │
│    - Pre-commit hooks block NEW violations                   │
│    - Auto-fixes run on save/commit                           │
│    - Status: Quality baseline maintained automatically       │
└─────────────────────────────────────────────────────────────┘
```

### Core Principle

**"Detection without action is noise"**

Any automated quality check must support the full feedback loop:
1. **DETECT** → Find issues (what we have)
2. **CLASSIFY** → Categorize: auto-fixable? investigate? false-positive?
3. **REMEDIATE** → Automated fix for common patterns
4. **TRACK** → Trend analysis to measure improvement
5. **PREVENT** → Block new issues at source (pre-commit hooks)

**Quality checks stuck at L0 (DETECT-only)**:
- Create ongoing toil (2-3 hours/week for 4 checks)
- Drive bypass culture (`--no-verify` becoming normalized)
- Provide no ROI path (cannot automate without classification)
- Generate false positive fatigue (50% of results ignored)

**Quality checks at L2-L4 (Complete feedback loop)**:
- Toil reduced by 85-90% (auto-fix 60-80% of violations)
- Bypass culture prevented (clear fix path eliminates temptation)
- Positive ROI (400-500% ROI typical for L2 adoption)
- False positives filtered (classification eliminates noise)

### Adoption Levels

**L0: Detection Only** (Current state for 3/4 checks)
- Script finds issues
- Human triages manually every time
- Issues recur, quality degrades
- **Time**: 2-3 hours/week per check

**L1: Classification Added** (2x toil reduction)
- Script categorizes violations (auto-fixable / investigate / false-positive)
- Reduced triage time (focus on investigation items only)
- Human still does fixes manually
- **Time**: 1-1.5 hours/week per check (40-50% reduction)

**L2: Remediation Added** (5x reduction via automation) ← **Target for 400-500% ROI**
- Auto-fix scripts for 60-80% of common patterns
- `just health-fix-*` recipes (one-command remediation)
- Human handles edge cases only
- **Time**: 20-30 min/week per check (85-90% reduction)

**L3: Tracking Added** (1.2x improvement via trend detection)
- Health metrics over time (stored in .chora/memory/ or metrics DB)
- Trend detection (improving or degrading?)
- VERA-based prioritization for non-auto-fixable items
- **Time**: 15-20 min/week per check (dashboard review)

**L4: Prevention Integrated** (1.3x improvement via pre-commit)
- Pre-commit hooks prevent NEW issues (not pre-existing)
- Auto-fixes run on save/commit (IDE integration)
- Quality baseline maintained automatically
- **Time**: 10-15 min/week per check (only new edge cases)

---

## Success Metrics

### Adoption Metrics

- **Number of quality checks at each level**:
  - Baseline: 4 checks at L0 (100%)
  - Target (3 months): 4 checks at L1 (100%), 2 checks at L2 (50%)
  - Target (6 months): 4 checks at L2 (100%), 2 checks at L3 (50%)
  - Target (12 months): 4 checks at L3-L4 (100%)

- **Ecosystem distribution**:
  - chora-workspace: Testbed for SAP-054 patterns (4 quality checks)
  - chora-base: SAP-054 specification distributed
  - chora-compose: Generate projects with SAP-054 quality infrastructure

### Quality Metrics

**L1 Adoption Metrics** (Classification Phase):
- Percentage of violations auto-classified: >80% target
- Classification accuracy: >90% target (false positive rate <10%)
- Triage time reduction: 40-70% (from 2-3h/week → 1-1.5h/week)

**L2 Adoption Metrics** (Remediation Phase):
- Percentage of violations auto-fixable: 60-80% target
- Auto-fix success rate: >95% target (failures require investigation)
- Toil reduction: 85-90% (from 2-3h/week → 20-30min/week)

**L3 Adoption Metrics** (Tracking Phase):
- Quality metrics tracked over time: 100% of checks
- Trend detection accuracy: >85% (correctly identify improving/degrading metrics)
- Proactive fix rate: >70% (degrading metrics fixed before becoming critical)

**L4 Adoption Metrics** (Prevention Phase):
- New violations blocked by pre-commit: >95%
- Pre-commit bypass rate: <5% (only for documented exceptions)
- Quality baseline maintained: >90% (metrics stable or improving)

### Business Metrics

**ROI Metrics**:
- L0→L1 investment: 2-3 hours per quality check
- L0→L1 savings: 1-1.5 hours/week × 52 weeks = 52-78 hours/year
- L0→L1 payback: 2-3 weeks
- **L0→L1 ROI**: 1,700-2,600% (12 months)

- L1→L2 investment: 4-6 hours per quality check
- L1→L2 savings: 1.5-2 hours/week × 52 weeks = 78-104 hours/year
- L1→L2 payback: 3-4 weeks
- **L1→L2 ROI**: 1,300-2,600% (12 months)

- **Overall L0→L4 ROI**: 430-650% (12 months, conservative estimate)

**Developer Experience Metrics**:
- Bypass culture reduction: `--no-verify` usage <5% (from 20-30%)
- False positive fatigue: User reports of "noisy" quality checks <10% (from 50%)
- Quality confidence: Developer survey rating >4/5 for "quality checks are helpful, not burdensome"

**Meta-Pattern Adoption**:
- Number of new quality checks created using SAP-054 pattern
- Percentage of quality checks following 5-phase feedback loop
- Time to create new quality check (target: <4 hours with SAP-054 guidance)

---

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Classification logic too complex** | High | Medium | Start with simple rules (e.g., "missing vision_ref" = auto-fixable), iterate based on feedback |
| **Auto-fix scripts introduce bugs** | High | Low | Require review/confirmation before applying fixes, comprehensive test suite for fix scripts |
| **L0→L4 adoption too slow** | Medium | Medium | Target L2 first (highest ROI), defer L3-L4 until L2 proven |
| **False positive classification** | Medium | Medium | Allow manual override, track classification accuracy, refine rules |
| **Pre-commit hooks block productivity** | High | Low | Only block NEW violations (not pre-existing), allow `--no-verify` for documented emergencies |
| **Metrics tracking overhead** | Low | Low | Use existing A-MEM infrastructure, minimal storage/compute required |

---

## Integration Points

### Prerequisites

**Framework Dependencies**:
- **SAP-000 (SAP Framework)**: Defines SAP structure and governance
- **SAP-009 (Agent Awareness)**: AGENTS.md patterns for quality infrastructure workflows

**Quality Infrastructure Dependencies**:
- **SAP-006 (Quality Gates)**: Pre-commit hooks framework for L4 prevention phase
- **SAP-004 (Testing Framework)**: Test coverage for auto-fix scripts
- **SAP-056 (Lifecycle Traceability)**: Traceability validation as reference implementation

### Dependents

**Quality Checks Adopting SAP-054**:
1. **Manifest Discovery**: L0→L1 (classify false positives) → L2 (auto-add to manifest)
2. **Script Refactoring**: L0→L1 (classify by fix pattern) → L2 (batch UTF-8/emoji fixes)
3. **Link Validation**: L0→L1 (classify moved/renamed/deleted) → L2 (auto-rewrite links)
4. **Traceability Validation**: L0→L1 (classify missing vision_ref) → L2 (auto-add vision_ref)

**Future Quality Checks**:
- SAP structure validation (SAP-050)
- Code ownership verification
- Documentation completeness checks
- Commit message validation

### Complements

- **SAP-008 (Automation Scripts)**: Justfile recipes for `just health-fix-*` commands
- **SAP-010 (Memory System)**: A-MEM events for quality check execution tracking
- **SAP-019 (SAP Self-Evaluation)**: VERA framework for prioritizing non-auto-fixable items
- **SAP-050 (SAP Adoption Verification)**: Meta-SAP that should itself adopt SAP-054 pattern

---

## Open Questions

1. **Classification Rule Format**: Should classification rules be code (Python functions) or config (YAML/JSON)?
   - **Proposed**: Start with Python functions for flexibility, extract to config when patterns stabilize

2. **Auto-fix Confirmation UX**: Always prompt for confirmation, or allow `--auto-approve` flag?
   - **Proposed**: Default to confirmation prompt, add `--auto-approve` for CI/CD pipelines

3. **Metrics Storage**: Store in A-MEM events, separate metrics DB, or both?
   - **Proposed**: Start with A-MEM events (reuse infrastructure), migrate to metrics DB at scale

4. **Pre-commit Hook Scope**: Block ALL violations, or only violations in changed files?
   - **Proposed**: Only violations in changed files (prevents blocking on pre-existing issues)

5. **L3 vs L4 Priority**: Should we defer L3 (tracking) until L4 (prevention) is in place?
   - **Proposed**: No - L3 enables proactive fixes, L4 enables prevention. Both valuable independently.

---

## References

**Quality Infrastructure SAPs**:
- [SAP-006: Quality Gates](../quality-gates/protocol-spec.md) - Pre-commit hooks for L4 prevention
- [SAP-050: SAP Adoption Verification](../sap-adoption-verification/protocol-spec.md) - Quality verification patterns (should adopt SAP-054)
- [SAP-056: Lifecycle Traceability](../lifecycle-traceability/protocol-spec.md) - Traceability validation (reference implementation)

**Supporting Infrastructure**:
- [SAP-008: Automation Scripts](../automation-scripts/protocol-spec.md) - Justfile recipes for remediation
- [SAP-010: Memory System](../memory-system/protocol-spec.md) - A-MEM for metrics tracking
- [SAP-019: SAP Self-Evaluation](../sap-self-evaluation/protocol-spec.md) - VERA prioritization framework

**Meta-Framework**:
- [SAP-000: SAP Framework](../sap-framework/protocol-spec.md) - Defines SAP governance and structure

---

**Version**: 1.0.0
**Status**: Draft
**Next Review**: After L1 adoption validation (OPP-2025-040 completion)
