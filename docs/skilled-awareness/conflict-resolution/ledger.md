# SAP-053: Conflict Resolution - Adoption Ledger

**Document Type**: Adoption Ledger
**SAP ID**: SAP-053
**SAP Name**: Conflict Resolution
**Version**: 1.0.0 (Phase 1 - Design)
**Repository**: {{REPOSITORY_NAME}}
**Last Updated**: {{DATE}}
**Maintained By**: {{MAINTAINER}}

---

## Document Purpose

This ledger tracks **SAP-053 adoption progress, metrics, and ROI** for {{REPOSITORY_NAME}}.

**Update Frequency**: Weekly during adoption (Phases 1-4), then quarterly for maintenance

**Sections**:
1. Adoption Status (L0 → L4)
2. Baseline Metrics (pre-SAP-053)
3. Current Metrics (post-SAP-053)
4. Milestone Tracking
5. Knowledge Note Inventory
6. ROI Calculation

---

## 1. Adoption Status

### Adoption Level: L{{CURRENT_LEVEL}}

| Level | Description | Status | Date Achieved |
|-------|-------------|--------|---------------|
| **L0: Aware** | SAP-053 artifacts read, understanding established | ⏳ / ✅ | {{DATE_L0}} |
| **L1: Planned** | Phase 1 (Design) complete, adoption approved | ⏳ / ✅ | {{DATE_L1}} |
| **L2: Implemented** | Phase 2 (Infrastructure) complete, tools installed | ⏳ / ✅ | {{DATE_L2}} |
| **L3: Validated** | Phase 3 (Pilot) complete, metrics meet targets | ⏳ / ✅ | {{DATE_L3}} |
| **L4: Distributed** | Phase 4 complete, SAP-053 production-ready | ⏳ / ✅ | {{DATE_L4}} |

**Current Status**: {{STATUS_DESCRIPTION}}

**Next Milestone**: {{NEXT_MILESTONE}}

**Blockers**: {{BLOCKERS_LIST}}

---

## 2. Baseline Metrics (Pre-SAP-053)

**Measurement Period**: {{BASELINE_START_DATE}} to {{BASELINE_END_DATE}} ({{BASELINE_DAYS}} days)

**Data Source**: A-MEM events (`.chora/memory/events/*.jsonl`) OR manual tracking

### Conflict Frequency

| Metric | Value | Calculation |
|--------|-------|-------------|
| Total PRs | {{TOTAL_PRS}} | Count of merged PRs in baseline period |
| PRs with conflicts | {{PRS_WITH_CONFLICTS}} | Count of PRs that had merge conflicts |
| **Conflict rate** | **{{CONFLICT_RATE}}%** | (PRs with conflicts / Total PRs) × 100 |
| Total conflicts | {{TOTAL_CONFLICTS}} | Sum of all conflicts across all PRs |
| Conflicts per week | {{CONFLICTS_PER_WEEK}} | Total conflicts / (Baseline days / 7) |

**Expected Range**: 20-30% conflict rate (from SAP-053 charter)

---

### Resolution Time

| Metric | Value | Calculation |
|--------|-------|-------------|
| Avg resolution time | {{AVG_RESOLUTION_TIME}} min | Total resolution time / Total conflicts |
| Min resolution time | {{MIN_RESOLUTION_TIME}} min | Fastest conflict resolved |
| Max resolution time | {{MAX_RESOLUTION_TIME}} min | Slowest conflict resolved |
| **Total time wasted** | **{{TOTAL_TIME_WASTED}} hours** | Total resolution time / 60 |

**Expected Range**: 15-30 min/conflict (from SAP-053 charter)

---

### Conflict Types (Baseline)

| Type | Count | Percentage | Avg Resolution Time |
|------|-------|------------|---------------------|
| Documentation (.md) | {{DOC_CONFLICTS}} | {{DOC_PERCENTAGE}}% | {{DOC_AVG_TIME}} min |
| Code (.py, .ts, .js) | {{CODE_CONFLICTS}} | {{CODE_PERCENTAGE}}% | {{CODE_AVG_TIME}} min |
| Configuration (.yaml, .json) | {{CONFIG_CONFLICTS}} | {{CONFIG_PERCENTAGE}}% | {{CONFIG_AVG_TIME}} min |
| Lockfiles | {{LOCKFILE_CONFLICTS}} | {{LOCKFILE_PERCENTAGE}}% | {{LOCKFILE_AVG_TIME}} min |
| Metadata (.DS_Store, etc.) | {{METADATA_CONFLICTS}} | {{METADATA_PERCENTAGE}}% | {{METADATA_AVG_TIME}} min |
| Other | {{OTHER_CONFLICTS}} | {{OTHER_PERCENTAGE}}% | {{OTHER_AVG_TIME}} min |

---

### Recurring Conflicts (Baseline)

**Definition**: Files with ≥2 conflicts in baseline period

| File | Conflict Count | Avg Resolution Time | Total Time Wasted |
|------|----------------|---------------------|-------------------|
| {{FILE_1}} | {{COUNT_1}} | {{AVG_TIME_1}} min | {{TOTAL_TIME_1}} min |
| {{FILE_2}} | {{COUNT_2}} | {{AVG_TIME_2}} min | {{TOTAL_TIME_2}} min |
| {{FILE_3}} | {{COUNT_3}} | {{AVG_TIME_3}} min | {{TOTAL_TIME_3}} min |
| ... | ... | ... | ... |

**Total recurring conflicts**: {{RECURRING_COUNT}} ({{RECURRING_PERCENTAGE}}% of all conflicts)

---

### Escalation Rate (Baseline)

**Note**: Only measurable if escalations were tracked before SAP-053. Otherwise, mark as "Unknown".

| Level | Count | Percentage |
|-------|-------|------------|
| Level 1 (Developer) | {{L1_COUNT}} | {{L1_PERCENTAGE}}% |
| Level 2 (Pair/Owner) | {{L2_COUNT}} | {{L2_PERCENTAGE}}% |
| Level 3 (Project Lead) | {{L3_COUNT}} | {{L3_PERCENTAGE}}% |

---

## 3. Current Metrics (Post-SAP-053)

**Measurement Period**: {{CURRENT_START_DATE}} to {{CURRENT_END_DATE}} ({{CURRENT_DAYS}} days)

**Data Source**: A-MEM events (`conflict_detected`, `conflict_resolved`)

### Conflict Frequency

| Metric | Baseline | Current | Change | Target |
|--------|----------|---------|--------|--------|
| Conflict rate | {{BASELINE_CONFLICT_RATE}}% | {{CURRENT_CONFLICT_RATE}}% | {{CONFLICT_RATE_CHANGE}}% | No target (detection, not prevention) |
| Conflicts per week | {{BASELINE_CONFLICTS_PER_WEEK}} | {{CURRENT_CONFLICTS_PER_WEEK}} | {{CONFLICTS_PER_WEEK_CHANGE}}% | N/A |

**Note**: SAP-053 focuses on **resolution speed**, not conflict prevention (that's SAP-052 multi-developer coordination).

---

### Resolution Time

| Metric | Baseline | Current | Improvement | Target |
|--------|----------|---------|-------------|--------|
| **Avg resolution time** | **{{BASELINE_AVG_TIME}} min** | **{{CURRENT_AVG_TIME}} min** | **{{RESOLUTION_TIME_IMPROVEMENT}}%** | **50-70% reduction** |
| Auto-resolved conflicts | 0 | {{AUTO_RESOLVED_COUNT}} | +{{AUTO_RESOLVED_PERCENTAGE}}% | 30-40% of conflicts |
| Avg auto-resolution time | N/A | {{AUTO_AVG_TIME}} min | N/A | 1-3 min |
| Avg manual resolution time | {{BASELINE_AVG_TIME}} min | {{MANUAL_AVG_TIME}} min | {{MANUAL_TIME_IMPROVEMENT}}% | 30-50% reduction |

**Status**: {{RESOLUTION_TIME_STATUS}} (✅ Meets target / ⚠️ Partial / ❌ Below target)

---

### Conflict Types (Current)

| Type | Count | Auto-Resolved | Manual | Avg Time (Auto) | Avg Time (Manual) |
|------|-------|---------------|--------|-----------------|-------------------|
| Documentation | {{DOC_CONFLICTS_CURRENT}} | 0 | {{DOC_CONFLICTS_CURRENT}} | N/A | {{DOC_AVG_TIME_CURRENT}} min |
| Code | {{CODE_CONFLICTS_CURRENT}} | {{CODE_AUTO}} | {{CODE_MANUAL}} | {{CODE_AUTO_TIME}} min | {{CODE_MANUAL_TIME}} min |
| Configuration | {{CONFIG_CONFLICTS_CURRENT}} | {{CONFIG_AUTO}} | {{CONFIG_MANUAL}} | {{CONFIG_AUTO_TIME}} min | {{CONFIG_MANUAL_TIME}} min |
| Lockfiles | {{LOCKFILE_CONFLICTS_CURRENT}} | {{LOCKFILE_AUTO}} | 0 | {{LOCKFILE_AUTO_TIME}} min | N/A |
| Metadata | {{METADATA_CONFLICTS_CURRENT}} | {{METADATA_AUTO}} | 0 | {{METADATA_AUTO_TIME}} min | N/A |
| Other | {{OTHER_CONFLICTS_CURRENT}} | {{OTHER_AUTO}} | {{OTHER_MANUAL}} | {{OTHER_AUTO_TIME}} min | {{OTHER_MANUAL_TIME}} min |

---

### Resolution Strategies (Current)

| Strategy | Count | Percentage | Avg Time |
|----------|-------|------------|----------|
| MANUAL_REVIEW | {{MANUAL_REVIEW_COUNT}} | {{MANUAL_REVIEW_PERCENTAGE}}% | {{MANUAL_REVIEW_AVG_TIME}} min |
| MANUAL_REVIEW_WITH_OWNERSHIP | {{OWNERSHIP_COUNT}} | {{OWNERSHIP_PERCENTAGE}}% | {{OWNERSHIP_AVG_TIME}} min |
| AUTO_RESOLVE_FORMATTING | {{FORMATTING_COUNT}} | {{FORMATTING_PERCENTAGE}}% | {{FORMATTING_AVG_TIME}} min |
| SCHEMA_DRIVEN_MERGE | {{SCHEMA_COUNT}} | {{SCHEMA_PERCENTAGE}}% | {{SCHEMA_AVG_TIME}} min |
| REGENERATE_FROM_SOURCE | {{REGENERATE_COUNT}} | {{REGENERATE_PERCENTAGE}}% | {{REGENERATE_AVG_TIME}} min |
| DELETE_AND_REGENERATE | {{DELETE_COUNT}} | {{DELETE_PERCENTAGE}}% | {{DELETE_AVG_TIME}} min |

---

### Recurring Conflicts (Current)

**Definition**: Files with ≥2 conflicts in current period

| File | Conflict Count | Knowledge Note Created? | Avg Resolution Time | Reduction vs Baseline |
|------|----------------|------------------------|---------------------|----------------------|
| {{FILE_1_CURRENT}} | {{COUNT_1_CURRENT}} | ✅ / ⏳ | {{AVG_TIME_1_CURRENT}} min | {{REDUCTION_1}}% |
| {{FILE_2_CURRENT}} | {{COUNT_2_CURRENT}} | ✅ / ⏳ | {{AVG_TIME_2_CURRENT}} min | {{REDUCTION_2}}% |
| {{FILE_3_CURRENT}} | {{COUNT_3_CURRENT}} | ✅ / ⏳ | {{AVG_TIME_3_CURRENT}} min | {{REDUCTION_3}}% |
| ... | ... | ... | ... | ... |

**Total recurring conflicts**: {{RECURRING_COUNT_CURRENT}} ({{RECURRING_REDUCTION}}% reduction vs baseline)

**Target**: 80-90% reduction in recurring conflicts (from SAP-053 charter)

**Status**: {{RECURRING_STATUS}} (✅ Meets target / ⚠️ Partial / ❌ Below target)

---

### Escalation Rate (Current)

| Level | Count | Percentage | Baseline | Change |
|-------|-------|------------|----------|--------|
| Level 1 (Developer) | {{L1_COUNT_CURRENT}} | {{L1_PERCENTAGE_CURRENT}}% | {{L1_PERCENTAGE}}% | {{L1_CHANGE}}% |
| Level 2 (Pair/Owner) | {{L2_COUNT_CURRENT}} | {{L2_PERCENTAGE_CURRENT}}% | {{L2_PERCENTAGE}}% | {{L2_CHANGE}}% |
| Level 3 (Project Lead) | {{L3_COUNT_CURRENT}} | {{L3_PERCENTAGE_CURRENT}}% | {{L3_PERCENTAGE}}% | {{L3_CHANGE}}% |

**Expected**: 80-90% resolved at Level 1 (developer), 10-20% escalated to Level 2, <5% escalated to Level 3

**Status**: {{ESCALATION_STATUS}} (✅ Meets target / ⚠️ Partial / ❌ Below target)

---

## 4. Milestone Tracking

### Phase 1: Design

| Milestone | Target Date | Actual Date | Status | Notes |
|-----------|-------------|-------------|--------|-------|
| Read SAP-053 proposal | {{P1_M1_TARGET}} | {{P1_M1_ACTUAL}} | ✅ / ⏳ / ❌ | {{P1_M1_NOTES}} |
| Draft capability-charter.md | {{P1_M2_TARGET}} | {{P1_M2_ACTUAL}} | ✅ / ⏳ / ❌ | {{P1_M2_NOTES}} |
| Draft protocol-spec.md | {{P1_M3_TARGET}} | {{P1_M3_ACTUAL}} | ✅ / ⏳ / ❌ | {{P1_M3_NOTES}} |
| Draft awareness-guide.md | {{P1_M4_TARGET}} | {{P1_M4_ACTUAL}} | ✅ / ⏳ / ❌ | {{P1_M4_NOTES}} |
| Draft adoption-blueprint.md | {{P1_M5_TARGET}} | {{P1_M5_ACTUAL}} | ✅ / ⏳ / ❌ | {{P1_M5_NOTES}} |
| Draft ledger.md (this file) | {{P1_M6_TARGET}} | {{P1_M6_ACTUAL}} | ✅ / ⏳ / ❌ | {{P1_M6_NOTES}} |
| Create CORD request | {{P1_M7_TARGET}} | {{P1_M7_ACTUAL}} | ✅ / ⏳ / ❌ | {{P1_M7_NOTES}} |
| Stakeholder review | {{P1_M8_TARGET}} | {{P1_M8_ACTUAL}} | ✅ / ⏳ / ❌ | {{P1_M8_NOTES}} |

**Phase 1 Status**: {{PHASE_1_STATUS}} ({{PHASE_1_PERCENTAGE}}% complete)

**Phase 1 Effort**: {{PHASE_1_ACTUAL_EFFORT}} days (target: 2-3 days)

---

### Phase 2: Infrastructure

| Milestone | Target Date | Actual Date | Status | Notes |
|-----------|-------------|-------------|--------|-------|
| Implement conflict-checker.py | {{P2_M1_TARGET}} | {{P2_M1_ACTUAL}} | ⏳ / ✅ / ❌ | {{P2_M1_NOTES}} |
| Implement conflict-resolver.py | {{P2_M2_TARGET}} | {{P2_M2_ACTUAL}} | ⏳ / ✅ / ❌ | {{P2_M2_NOTES}} |
| Implement conflict-auto-resolver.py | {{P2_M3_TARGET}} | {{P2_M3_ACTUAL}} | ⏳ / ✅ / ❌ | {{P2_M3_NOTES}} |
| Implement conflict-predictor.py | {{P2_M4_TARGET}} | {{P2_M4_ACTUAL}} | ⏳ / ✅ / ❌ | {{P2_M4_NOTES}} |
| Implement conflict-pattern-detector.py | {{P2_M5_TARGET}} | {{P2_M5_ACTUAL}} | ⏳ / ✅ / ❌ | {{P2_M5_NOTES}} |
| Implement conflict-stats.py | {{P2_M6_TARGET}} | {{P2_M6_ACTUAL}} | ⏳ / ✅ / ❌ | {{P2_M6_NOTES}} |
| Write test suite (100+ tests) | {{P2_M7_TARGET}} | {{P2_M7_ACTUAL}} | ⏳ / ✅ / ❌ | {{P2_M7_NOTES}} |
| Create justfile recipes | {{P2_M8_TARGET}} | {{P2_M8_ACTUAL}} | ⏳ / ✅ / ❌ | {{P2_M8_NOTES}} |
| Integrate SAP-051 (pre-push hook) | {{P2_M9_TARGET}} | {{P2_M9_ACTUAL}} | ⏳ / ✅ / ❌ | {{P2_M9_NOTES}} |
| Code review and approval | {{P2_M10_TARGET}} | {{P2_M10_ACTUAL}} | ⏳ / ✅ / ❌ | {{P2_M10_NOTES}} |

**Phase 2 Status**: {{PHASE_2_STATUS}} ({{PHASE_2_PERCENTAGE}}% complete)

**Phase 2 Effort**: {{PHASE_2_ACTUAL_EFFORT}} days (target: 4-6 days)

---

### Phase 3: Pilot

| Milestone | Target Date | Actual Date | Status | Notes |
|-----------|-------------|-------------|--------|-------|
| Set up pilot environment | {{P3_M1_TARGET}} | {{P3_M1_ACTUAL}} | ⏳ / ✅ / ❌ | {{P3_M1_NOTES}} |
| Generate 10+ test conflicts | {{P3_M2_TARGET}} | {{P3_M2_ACTUAL}} | ⏳ / ✅ / ❌ | {{P3_M2_NOTES}} |
| Measure resolution metrics | {{P3_M3_TARGET}} | {{P3_M3_ACTUAL}} | ⏳ / ✅ / ❌ | {{P3_M3_NOTES}} |
| Create knowledge notes | {{P3_M4_TARGET}} | {{P3_M4_ACTUAL}} | ⏳ / ✅ / ❌ | {{P3_M4_NOTES}} |
| Generate pilot report | {{P3_M5_TARGET}} | {{P3_M5_ACTUAL}} | ⏳ / ✅ / ❌ | {{P3_M5_NOTES}} |
| Stakeholder review (metrics) | {{P3_M6_TARGET}} | {{P3_M6_ACTUAL}} | ⏳ / ✅ / ❌ | {{P3_M6_NOTES}} |

**Phase 3 Status**: {{PHASE_3_STATUS}} ({{PHASE_3_PERCENTAGE}}% complete)

**Phase 3 Effort**: {{PHASE_3_ACTUAL_EFFORT}} days (target: 2-3 days)

---

### Phase 4: Distribution

| Milestone | Target Date | Actual Date | Status | Notes |
|-----------|-------------|-------------|--------|-------|
| Distribute artifacts to chora-base | {{P4_M1_TARGET}} | {{P4_M1_ACTUAL}} | ⏳ / ✅ / ❌ | {{P4_M1_NOTES}} |
| Create public README | {{P4_M2_TARGET}} | {{P4_M2_ACTUAL}} | ⏳ / ✅ / ❌ | {{P4_M2_NOTES}} |
| Integrate with chora-compose | {{P4_M3_TARGET}} | {{P4_M3_ACTUAL}} | ⏳ / ✅ / ❌ | {{P4_M3_NOTES}} |
| Adopt in ≥2 additional repos | {{P4_M4_TARGET}} | {{P4_M4_ACTUAL}} | ⏳ / ✅ / ❌ | {{P4_M4_NOTES}} |
| Establish feedback loop | {{P4_M5_TARGET}} | {{P4_M5_ACTUAL}} | ⏳ / ✅ / ❌ | {{P4_M5_NOTES}} |

**Phase 4 Status**: {{PHASE_4_STATUS}} ({{PHASE_4_PERCENTAGE}}% complete)

**Phase 4 Effort**: {{PHASE_4_ACTUAL_EFFORT}} days (target: 2-3 days)

---

## 5. Knowledge Note Inventory

**Purpose**: Track knowledge notes created from recurring conflict patterns

**Update Frequency**: After each recurring conflict (≥2 in 90 days)

| Note ID | File Pattern | Created Date | Conflict Count | Avg Resolution Time | Prevention Strategy |
|---------|--------------|--------------|----------------|---------------------|---------------------|
| {{NOTE_1_ID}} | {{NOTE_1_FILE}} | {{NOTE_1_DATE}} | {{NOTE_1_COUNT}} | {{NOTE_1_AVG_TIME}} min | {{NOTE_1_PREVENTION}} |
| {{NOTE_2_ID}} | {{NOTE_2_FILE}} | {{NOTE_2_DATE}} | {{NOTE_2_COUNT}} | {{NOTE_2_AVG_TIME}} min | {{NOTE_2_PREVENTION}} |
| {{NOTE_3_ID}} | {{NOTE_3_FILE}} | {{NOTE_3_DATE}} | {{NOTE_3_COUNT}} | {{NOTE_3_AVG_TIME}} min | {{NOTE_3_PREVENTION}} |
| ... | ... | ... | ... | ... | ... |

**Total Knowledge Notes**: {{TOTAL_KNOWLEDGE_NOTES}}

**Expected Benefit**: 30-50% reduction in recurring conflict resolution time (from SAP-053 charter)

---

### Knowledge Note Template

**Location**: `.chora/memory/knowledge/notes/conflict-pattern-{file}.md`

**Generation**: Automatic via `just conflict-patterns` (runs weekly)

**Example**:
```markdown
---
title: "Conflict Pattern: project-docs/sprints/sprint-13.md"
created: 2025-11-20
tags: [conflict-pattern, recurring-conflict, sap-053]
related: [trace-id-1, trace-id-2, trace-id-3]
---

# Conflict Pattern: project-docs/sprints/sprint-13.md

**Conflict Frequency**: 5 conflicts in last 90 days
**Average Resolution Time**: 18.3 minutes

## Analysis

**Common Conflict Types**: content (semantic changes)
**Resolution Strategies**: MANUAL_REVIEW_WITH_OWNERSHIP

## Prevention Recommendations

1. **Coordinate before editing** (SAP-052 multi-developer pattern)
2. **Use feature branches for major updates**
3. **Split sprint plan into separate files** (future enhancement)

## Related Events

- [[trace-id-1]] (2025-11-05, 22 min resolution)
- [[trace-id-2]] (2025-11-12, 15 min resolution)
- [[trace-id-3]] (2025-11-19, 18 min resolution)
```

---

## 6. ROI Calculation

### Investment

| Category | Effort (Days) | Cost (@ ${{HOURLY_RATE}}/hr) | Notes |
|----------|---------------|------------------------------|-------|
| **Phase 1: Design** | {{P1_EFFORT}} | ${{P1_COST}} | SAP artifacts (charter, spec, guide, blueprint, ledger) |
| **Phase 2: Infrastructure** | {{P2_EFFORT}} | ${{P2_COST}} | Scripts, tests, justfile, hooks |
| **Phase 3: Pilot** | {{P3_EFFORT}} | ${{P3_COST}} | Validation, metrics, knowledge notes |
| **Phase 4: Distribution** | {{P4_EFFORT}} | ${{P4_COST}} | chora-base distribution, chora-compose integration |
| **Total Development** | **{{TOTAL_DEV_EFFORT}}** | **${{TOTAL_DEV_COST}}** | One-time investment |
| **Annual Maintenance** | {{MAINTENANCE_EFFORT}} days/year | ${{MAINTENANCE_COST}}/year | Ongoing cost |

**Development Cost Range**: $12,000-$18,000 (target: 10-15 days @ $150/hr)

**Actual Development Cost**: ${{ACTUAL_DEV_COST}} ({{ACTUAL_DEV_EFFORT}} days)

**Variance**: {{COST_VARIANCE}}% ({{OVER_UNDER}} budget)

---

### Benefits (Annual)

**Team Size**: {{TEAM_SIZE}} developers

**Conflict Frequency**: {{CONFLICTS_PER_YEAR}} conflicts/year

**Baseline Resolution Time**: {{BASELINE_AVG_TIME}} min/conflict

**Current Resolution Time**: {{CURRENT_AVG_TIME}} min/conflict

**Time Saved per Conflict**: {{TIME_SAVED_PER_CONFLICT}} min

**Annual Time Saved**: {{ANNUAL_TIME_SAVED}} hours/year

**Annual Cost Saved**: ${{ANNUAL_COST_SAVED}} (@ ${{HOURLY_RATE}}/hr)

---

### ROI Summary

| Metric | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|--------|--------|--------|--------|--------|--------|
| **Investment** | ${{Y1_INVESTMENT}} | ${{Y2_INVESTMENT}} | ${{Y3_INVESTMENT}} | ${{Y4_INVESTMENT}} | ${{Y5_INVESTMENT}} |
| **Benefits** | ${{Y1_BENEFITS}} | ${{Y2_BENEFITS}} | ${{Y3_BENEFITS}} | ${{Y4_BENEFITS}} | ${{Y5_BENEFITS}} |
| **Net Benefit** | ${{Y1_NET}} | ${{Y2_NET}} | ${{Y3_NET}} | ${{Y4_NET}} | ${{Y5_NET}} |
| **ROI** | **{{Y1_ROI}}%** | **{{Y2_ROI}}%** | **{{Y3_ROI}}%** | **{{Y4_ROI}}%** | **{{Y5_ROI}}%** |
| **Cumulative ROI** | {{Y1_CUMULATIVE_ROI}}% | {{Y2_CUMULATIVE_ROI}}% | {{Y3_CUMULATIVE_ROI}}% | {{Y4_CUMULATIVE_ROI}}% | {{Y5_CUMULATIVE_ROI}}% |

**Break-Even**: {{BREAK_EVEN_MONTHS}} months

**5-Year Net Benefit**: ${{FIVE_YEAR_NET_BENEFIT}}

---

### ROI Calculation Formulas

**Year 1 ROI**:
```
Year 1 ROI = (Benefits - Development Cost - Maintenance) / (Development Cost + Maintenance)
           = (${{Y1_BENEFITS}} - ${{TOTAL_DEV_COST}} - ${{MAINTENANCE_COST}}) / (${{TOTAL_DEV_COST}} + ${{MAINTENANCE_COST}})
           = {{Y1_ROI}}%
```

**Year 2+ ROI**:
```
Year N ROI = (Benefits - Maintenance) / Maintenance
           = (${{Y2_BENEFITS}} - ${{MAINTENANCE_COST}}) / ${{MAINTENANCE_COST}}
           = {{Y2_ROI}}%
```

**Cumulative ROI** (as of Year {{CURRENT_YEAR}}):
```
Cumulative ROI = (Total Benefits - Total Investment) / Total Investment
               = (${{TOTAL_BENEFITS}} - ${{TOTAL_INVESTMENT}}) / ${{TOTAL_INVESTMENT}}
               = {{CUMULATIVE_ROI}}%
```

---

### ROI Sensitivity Analysis

**Variables**:
- Conflict frequency: {{CONFLICTS_PER_YEAR_LOW}}-{{CONFLICTS_PER_YEAR_HIGH}} conflicts/year
- Resolution time reduction: {{REDUCTION_LOW}}-{{REDUCTION_HIGH}}%
- Hourly rate: ${{HOURLY_RATE_LOW}}-${{HOURLY_RATE_HIGH}}/hr

| Scenario | Conflict Frequency | Time Reduction | Year 1 ROI | Year 2+ ROI | Break-Even |
|----------|-------------------|----------------|------------|-------------|------------|
| **Best Case** | {{HIGH_CONFLICTS}} | {{HIGH_REDUCTION}}% | {{BEST_Y1_ROI}}% | {{BEST_Y2_ROI}}% | {{BEST_BREAK_EVEN}} months |
| **Expected** | {{MED_CONFLICTS}} | {{MED_REDUCTION}}% | {{EXP_Y1_ROI}}% | {{EXP_Y2_ROI}}% | {{EXP_BREAK_EVEN}} months |
| **Worst Case** | {{LOW_CONFLICTS}} | {{LOW_REDUCTION}}% | {{WORST_Y1_ROI}}% | {{WORST_Y2_ROI}}% | {{WORST_BREAK_EVEN}} months |

---

## 7. Adoption Health

### Health Score: {{HEALTH_SCORE}}/100

**Calculation**:
```
Health Score = (
    0.3 × Resolution Time Improvement (0-100) +
    0.2 × Auto-Resolution Rate (0-100) +
    0.2 × Recurring Conflict Reduction (0-100) +
    0.2 × Tool Adoption Rate (0-100) +
    0.1 × Knowledge Note Creation Rate (0-100)
)
```

**Component Scores**:

| Component | Score | Weight | Contribution | Target |
|-----------|-------|--------|--------------|--------|
| Resolution Time Improvement | {{RESOLUTION_SCORE}}/100 | 30% | {{RESOLUTION_CONTRIBUTION}} | ≥50% improvement |
| Auto-Resolution Rate | {{AUTO_SCORE}}/100 | 20% | {{AUTO_CONTRIBUTION}} | ≥30% of conflicts |
| Recurring Conflict Reduction | {{RECURRING_SCORE}}/100 | 20% | {{RECURRING_CONTRIBUTION}} | ≥80% reduction |
| Tool Adoption Rate | {{TOOL_SCORE}}/100 | 20% | {{TOOL_CONTRIBUTION}} | ≥80% of conflicts use tools |
| Knowledge Note Creation | {{KNOWLEDGE_SCORE}}/100 | 10% | {{KNOWLEDGE_CONTRIBUTION}} | ≥1 note per recurring pattern |

**Health Status**: {{HEALTH_STATUS}}
- 80-100: ✅ Excellent (SAP-053 fully adopted, targets exceeded)
- 60-79: ✅ Good (SAP-053 adopted, targets met)
- 40-59: ⚠️ Fair (SAP-053 partially adopted, some targets missed)
- 20-39: ⚠️ Poor (SAP-053 minimally adopted, most targets missed)
- 0-19: ❌ Failing (SAP-053 not adopted, consider rollback)

---

## 8. Action Items (Next Steps)

**Updated**: {{ACTION_ITEMS_UPDATED_DATE}}

### High Priority

1. {{ACTION_1}} - **Owner**: {{OWNER_1}}, **Due**: {{DUE_1}}, **Status**: {{STATUS_1}}
2. {{ACTION_2}} - **Owner**: {{OWNER_2}}, **Due**: {{DUE_2}}, **Status**: {{STATUS_2}}
3. {{ACTION_3}} - **Owner**: {{OWNER_3}}, **Due**: {{DUE_3}}, **Status**: {{STATUS_3}}

### Medium Priority

4. {{ACTION_4}} - **Owner**: {{OWNER_4}}, **Due**: {{DUE_4}}, **Status**: {{STATUS_4}}
5. {{ACTION_5}} - **Owner**: {{OWNER_5}}, **Due**: {{DUE_5}}, **Status**: {{STATUS_5}}

### Low Priority / Future Enhancements

6. {{ACTION_6}} - **Owner**: {{OWNER_6}}, **Due**: {{DUE_6}}, **Status**: {{STATUS_6}}
7. {{ACTION_7}} - **Owner**: {{OWNER_7}}, **Due**: {{DUE_7}}, **Status**: {{STATUS_7}}

---

## 9. Notes and Observations

**Updated**: {{NOTES_UPDATED_DATE}}

### What's Working Well

- {{WORKING_WELL_1}}
- {{WORKING_WELL_2}}
- {{WORKING_WELL_3}}

### What Needs Improvement

- {{NEEDS_IMPROVEMENT_1}}
- {{NEEDS_IMPROVEMENT_2}}
- {{NEEDS_IMPROVEMENT_3}}

### Blockers and Risks

- {{BLOCKER_1}} - **Mitigation**: {{MITIGATION_1}}
- {{BLOCKER_2}} - **Mitigation**: {{MITIGATION_2}}

### Lessons Learned

- {{LESSON_1}}
- {{LESSON_2}}
- {{LESSON_3}}

---

## Document Metadata

**Template Version**: 1.0.0
**Repository**: {{REPOSITORY_NAME}}
**Last Updated**: {{LAST_UPDATED_DATE}}
**Updated By**: {{UPDATED_BY}}
**Next Review**: {{NEXT_REVIEW_DATE}}

**Related Documents**:
- [capability-charter.md](capability-charter.md) - SAP-053 charter
- [protocol-spec.md](protocol-spec.md) - Technical specification
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - 4-phase adoption plan
- [Pilot Report]({{PILOT_REPORT_PATH}}) - Validation metrics (after Phase 3)

**SAP Dependencies**:
- SAP-051 (Git Workflow) - ✅ Complete
- SAP-052 (Ownership Zones) - ✅ Complete
- SAP-010 (A-MEM) - ✅ Complete (L4)

---

## Usage Instructions

### For Project Maintainers

1. **Copy this template** to your repository:
   ```bash
   cp packages/chora-base/docs/skilled-awareness/conflict-resolution/ledger.md \
      project-docs/sap-053-ledger.md
   ```

2. **Replace template variables** ({{REPOSITORY_NAME}}, {{DATE}}, etc.) with actual values

3. **Establish baseline metrics** (Section 2):
   - Query A-MEM events OR manually track conflicts for 4-8 weeks
   - Calculate conflict rate, avg resolution time, recurring files
   - Document baseline before SAP-053 adoption

4. **Update weekly during adoption** (Phases 1-4):
   - Mark milestones as complete (Section 4)
   - Update effort tracking
   - Note blockers and action items

5. **Update monthly post-adoption** (L4):
   - Refresh current metrics (Section 3)
   - Calculate ROI (Section 6)
   - Review health score (Section 7)
   - Update action items (Section 8)

6. **Quarterly review**:
   - Generate conflict stats: `just conflict-stats days=90`
   - Create knowledge notes: `just conflict-patterns`
   - Recalculate ROI sensitivity
   - Present findings to stakeholders

---

### For AI Agents

**Query metrics from A-MEM**:
```bash
# Total conflicts (last 90 days)
grep '"type": "conflict_resolved"' .chora/memory/events/*.jsonl | wc -l

# Average resolution time
grep '"type": "conflict_resolved"' .chora/memory/events/*.jsonl | \
  jq -r '.resolution_time_minutes' | \
  awk '{sum+=$1; count++} END {print sum/count}'

# Auto-resolution rate
TOTAL=$(grep '"type": "conflict_resolved"' .chora/memory/events/*.jsonl | wc -l)
AUTO=$(grep '"auto_resolved": true' .chora/memory/events/*.jsonl | wc -l)
echo "scale=1; $AUTO / $TOTAL * 100" | bc

# Most frequent files
grep '"type": "conflict_resolved"' .chora/memory/events/*.jsonl | \
  jq -r '.resolved_files[]' | \
  sort | uniq -c | sort -rn | head -10
```

**Update ledger template variables programmatically**:
```python
# scripts/update-sap-053-ledger.py

import re
from datetime import datetime

def update_ledger(ledger_path, variables):
    """Replace {{VAR}} placeholders with actual values."""
    with open(ledger_path, 'r') as f:
        content = f.read()

    for var, value in variables.items():
        content = re.sub(r'\{\{' + var + r'\}\}', str(value), content)

    with open(ledger_path, 'w') as f:
        f.write(content)

# Example usage
variables = {
    'REPOSITORY_NAME': 'chora-workspace',
    'DATE': datetime.now().strftime('%Y-%m-%d'),
    'CURRENT_LEVEL': '3',
    'BASELINE_CONFLICT_RATE': '25',
    'CURRENT_CONFLICT_RATE': '24',
    'BASELINE_AVG_TIME': '22',
    'CURRENT_AVG_TIME': '9',
    # ... etc
}

update_ledger('project-docs/sap-053-ledger.md', variables)
```

---

**Created**: 2025-11-18
**Template Author**: Claude (AI peer) + Victor Piper
**Trace ID**: sap-053-phase1-design-2025-11-18
