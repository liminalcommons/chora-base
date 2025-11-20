# FEAT-002 Discovery Validation Analysis Report

**Date**: 2025-11-19
**Benchmark**: 31 queries (15 real-world + 15 edge cases + 1 coverage)
**Accuracy**: 61.3% (19/31 matches)
**Target**: 90%+ accuracy
**Gap**: -28.7 percentage points

---

## Executive Summary

The comprehensive validation benchmark revealed **61.3% routing accuracy**, falling **28.7 percentage points short** of the 90% target. While AUTOMATION_RECIPE queries achieved 100% accuracy, PATTERN_CONCEPT (42.9%), HISTORICAL_EVENT (50%), and UNKNOWN (0%) queries showed significant routing issues.

**Key Findings**:
1. **AUTOMATION_RECIPE**: Perfect (100%) - justfile routing works flawlessly
2. **CODE_FEATURE**: Strong (77.8%) - feature manifest routing mostly reliable
3. **HISTORICAL_EVENT**: Moderate (50%) - past tense detection inconsistent
4. **PATTERN_CONCEPT**: Weak (42.9%) - conflicts with automation keywords
5. **UNKNOWN fallback**: Broken (0%) - no proper fallback for ambiguous queries

**Performance**:
- Average discovery time: 0.087 seconds ✅ (target: <30s)
- Average token estimate: 7,016 tokens (baseline for comparison)

---

## Detailed Mismatch Analysis

### Category 1: PATTERN vs AUTOMATION Confusion (6 cases)

**Pattern**: "how do we X" and "workflow for X" queries incorrectly route to AUTOMATION instead of PATTERN.

| Query ID | Query | Expected | Got | Reason |
|----------|-------|----------|-----|--------|
| RW-002 | how do we write tests for Python scripts | PATTERN | AUTOMATION | "write tests" triggered automation |
| RW-014 | how do we handle fuzzy matching for query typos | PATTERN | AUTOMATION | "handle" + "fuzzy matching" triggered automation |
| EC-002 | workflow for testing | PATTERN | AUTOMATION | "testing" keyword tipped to automation |
| EC-011 | explain testing workflow and show test files | PATTERN | AUTOMATION | Compound query, last part ("show files") won |
| RW-005 | show me git workflow patterns documentation | CODE | AUTOMATION | "workflow" + "patterns" triggered automation fallback |
| EC-010 | show me SAP adoption patterns and run metrics | CODE | AUTOMATION | Compound query, "run metrics" won |

**Root Cause**: Automation keywords (test, run, execute, workflow) have higher weight than "how do we" pattern signals.

**Recommendation**:
- Increase weight of "how do we" and "explain" patterns
- Add disambiguation: "how do we X" → PATTERN (unless "run" or "execute" present)
- Handle compound queries by prioritizing first intent

---

### Category 2: HISTORICAL Misrouting (3 cases)

**Pattern**: Past tense and temporal queries don't consistently trigger historical routing.

| Query ID | Query | Expected | Got | Reason |
|----------|-------|----------|-----|--------|
| RW-011 | when was the script refactoring phase completed | HISTORICAL | AUTOMATION | "script" keyword triggered automation |
| RW-015 | when did we deliver OPP-2025-002 knowledge indexes | HISTORICAL | PATTERN | "deliver" + "knowledge" triggered pattern |
| EC-007 | fix bug in parser | HISTORICAL | PATTERN | Interpreted as "how to fix bugs" (pattern) not past event |

**Root Cause**: "when did/was" signals compete with domain keywords (script, knowledge, fix).

**Recommendation**:
- Increase weight of temporal signals ("when did", "when was", past tense verbs)
- Add past tense verb detection (completed, delivered, fixed → HISTORICAL)
- Prioritize temporal signals over domain keywords

---

### Category 3: UNKNOWN Fallback Failure (3 cases)

**Pattern**: Queries with no clear codebase intent incorrectly route to CODE or AUTOMATION instead of UNKNOWN.

| Query ID | Query | Expected | Got | Reason |
|----------|-------|----------|-----|--------|
| EC-013 | random gibberish query xyz123 | UNKNOWN | AUTOMATION | No confidence threshold, defaulted to automation |
| EC-014 | delete everything now | UNKNOWN | CODE | "delete" matched code patterns somehow |
| EC-015 | what is the meaning of life | UNKNOWN | CODE | No confidence threshold, defaulted to code |

**Root Cause**: No UNKNOWN fallback logic - every query routes to one of 4 types regardless of confidence.

**Recommendation**:
- Add confidence score threshold (e.g., if all pattern scores < 0.3, route to UNKNOWN)
- Add negative pattern matching (philosophical questions, destructive commands → UNKNOWN)
- Implement "no clear intent" detection

---

## Accuracy by Query Type

| Query Type | Correct | Total | Accuracy | Target | Gap |
|------------|---------|-------|----------|--------|-----|
| AUTOMATION_RECIPE | 6 | 6 | 100.0% | 90%+ | +10.0pp ✅ |
| CODE_FEATURE | 7 | 9 | 77.8% | 90%+ | -12.2pp |
| HISTORICAL_EVENT | 3 | 6 | 50.0% | 90%+ | -40.0pp ❌ |
| PATTERN_CONCEPT | 3 | 7 | 42.9% | 90%+ | -47.1pp ❌ |
| UNKNOWN | 0 | 3 | 0.0% | 90%+ | -90.0pp ❌ |
| **Overall** | **19** | **31** | **61.3%** | **90%+** | **-28.7pp** ❌ |

---

## Performance Metrics

### Discovery Time

- **Average**: 0.087 seconds ✅
- **Range**: 0.060s - 0.128s
- **Target**: <30 seconds
- **Status**: **EXCEEDS target by 344x** (0.087s vs 30s)

### Token Estimates

- **Average**: 7,016 tokens
- **Range**: 500 - 16,000 tokens
- **Breakdown by method**:
  - Justfile (AUTOMATION): 5,000 tokens avg
  - Event logs (HISTORICAL): 7,500 tokens avg
  - Knowledge graph (PATTERN): 10,000 tokens avg
  - Feature manifest (CODE): 7,556 tokens avg

**Baseline Comparison** (Traditional Discovery):
- Traditional grep: 20,000-40,000 tokens (estimate)
- Discovery system: 7,016 tokens avg
- **Estimated savings**: 65-82% (meets 60-73% target) ✅

---

## Fuzzy Matching & Synonym Expansion Validation

**Typo Queries** (3 tested):
- EC-004: "authentiction code" → CODE_FEATURE ✅ (fuzzy match worked)
- EC-005: "wokflow patterns" → PATTERN_CONCEPT ✅ (fuzzy match worked)
- EC-006: "validaton script" → AUTOMATION_RECIPE ✅ (fuzzy match worked)

**Accuracy**: 100% (3/3)
**Conclusion**: Fuzzy matching (OPP-2025-003) is working as expected ✅

**Synonym Queries** (3 tested):
- EC-007: "fix bug in parser" → PATTERN (expected HISTORICAL) ❌
- EC-008: "execute coverage report" → AUTOMATION ✅
- EC-009: "locate code for authentication" → CODE ✅

**Accuracy**: 66.7% (2/3)
**Conclusion**: Synonym expansion works for most cases, EC-007 is ambiguous

---

## Root Causes Summary

1. **Pattern Weight Imbalance**: Automation keywords (test, run, execute) override "how do we" patterns
2. **Temporal Signal Weakness**: "when did/was" signals lose to domain keywords
3. **No UNKNOWN Fallback**: Missing confidence threshold and negative pattern matching
4. **Compound Query Handling**: Last keywords override first intent in multi-part queries

---

## Recommendations (Priority Order)

### Priority 1: Fix UNKNOWN Fallback (Critical)

**Impact**: Prevents 0% → 90%+ on negative queries (+90pp improvement)

**Changes**:
1. Add confidence score calculation to QueryClassifier
2. If all pattern scores < 0.3 threshold, route to UNKNOWN
3. Add negative pattern list (gibberish, philosophical, destructive commands)

**Effort**: 1-2 hours
**Expected Improvement**: +9pp overall (3/31 queries fixed)

---

### Priority 2: Strengthen PATTERN vs AUTOMATION Disambiguation (High)

**Impact**: Improves PATTERN accuracy from 42.9% → 85%+ (+42pp improvement)

**Changes**:
1. Increase weight of "how do we", "explain", "what patterns" from 2.0 → 3.0 (strong signal)
2. Add disambiguation rule: "how do we X" → PATTERN (unless "run" or "execute" in same sentence)
3. Prioritize first intent in compound queries ("show patterns and run metrics" → CODE not AUTOMATION)

**Effort**: 2-3 hours
**Expected Improvement**: +19pp overall (6/31 queries fixed)

---

### Priority 3: Improve HISTORICAL Temporal Detection (Medium)

**Impact**: Improves HISTORICAL accuracy from 50% → 80%+ (+30pp improvement)

**Changes**:
1. Increase weight of "when did", "when was" from 2.0 → 3.0 (strong signal)
2. Add past tense verb detection (completed, delivered, fixed, deployed → +1.0 weight)
3. Prioritize temporal signals over domain keywords in disambiguation

**Effort**: 1-2 hours
**Expected Improvement**: +10pp overall (3/31 queries fixed)

---

### Projected Impact After All Fixes

| Query Type | Current | After Fixes | Improvement |
|------------|---------|-------------|-------------|
| UNKNOWN | 0.0% | 90%+ | +90pp |
| PATTERN_CONCEPT | 42.9% | 85%+ | +42pp |
| HISTORICAL_EVENT | 50.0% | 80%+ | +30pp |
| CODE_FEATURE | 77.8% | 85%+ | +7pp |
| AUTOMATION_RECIPE | 100.0% | 100% | 0pp |
| **Overall** | **61.3%** | **88-92%** | **+27-31pp** ✅ |

**Projected Accuracy**: 88-92% (meets 90%+ target)

---

## Go/No-Go Decision on FEAT-002 Promotion

### Current State
- ✅ Discovery time: 0.087s (exceeds target)
- ✅ Token savings: 65-82% (meets 60-73% target)
- ❌ Routing accuracy: 61.3% (below 90% target)

### Recommendation: **NO-GO** (Fix routing accuracy first)

**Rationale**:
1. **Routing accuracy critical**: 61.3% means 4 in 10 queries route incorrectly (poor UX)
2. **Easy fixes available**: 4-6 hours to implement Priority 1-3 recommendations
3. **High confidence in projections**: Fixes target known root causes (UNKNOWN fallback, PATTERN weight, HISTORICAL signals)
4. **Quality gate justification**: chora-base promotion requires validated claims (90%+ routing accuracy)

### Next Steps
1. Implement Priority 1-3 fixes (4-6 hours)
2. Re-run validation benchmark (31 queries + existing 39 = 70 total)
3. Validate 88-92% accuracy achieved
4. Make new go/no-go decision

**Estimated Time to Promotion**: 1-2 days (4-6 hours fixes + re-validation)

---

## Validation Artifacts

- **Queries**: `scripts/fixtures/feat-002-validation/queries.csv` (31 queries)
- **Results**: `scripts/fixtures/feat-002-validation/benchmark-results.csv` (raw data)
- **Analysis**: `scripts/fixtures/feat-002-validation/analysis-report.md` (this report)
- **Benchmark Script**: `scripts/run-discovery-benchmark.py`

---

## Lessons Learned

1. **Small validation sets hide issues**: OPP-2025-001's 34 curated queries showed 100% accuracy, but real-world queries revealed 61.3%
2. **Edge cases critical**: Ambiguous, compound, and negative queries exposed 3 major failure modes
3. **Confidence thresholds needed**: Without UNKNOWN fallback, system tries to route everything (creates false confidence)
4. **Pattern weights need tuning**: Initial weights worked for curated queries, failed on diverse real-world queries

---

**Report Generated**: 2025-11-19
**Author**: Claude Sonnet 4.5 (OPP-2025-004 Validation)
**Status**: Validation Complete - Awaiting Fixes Before Promotion
