# Week 6 Verification Plan: Tier 2 Continuation

**Date**: 2025-11-09
**Focus**: Tier 2 (Development Support) - Continue after Tier 1 completion
**Target SAPs**: 2 SAPs (SAP-010 + 1 more)
**Goal**: Advance Tier 2 from 40% → 60-80%

---

## Context

### Campaign Status (End of Week 5)
- **Overall Progress**: 32% (10/31 SAPs)
- **Tier 1 (Core Infrastructure)**: 100% (9/9) ✅ **COMPLETE**
- **Tier 2 (Development Support)**: 40% (2/5) ⏳
  - ✅ SAP-007: documentation-framework (Week 4)
  - ✅ SAP-009: agent-awareness (Week 4)
  - ⏳ SAP-010: memory-system
  - ⏳ SAP-011: docker-operations OR SAP-013: metrics-framework
  - ⏳ One more TBD

### Week 5 Results
- **SAPs Verified**: 2 (SAP-008, SAP-012)
- **Decisions**: 1 CONDITIONAL GO, 1 GO
- **Time**: 3.9 hours (233 min)
- **Key Achievement**: Tier 1 100% complete

---

## Week 6 Target SAPs

### Primary Target: SAP-010 (memory-system)

**Why SAP-010**:
- Part of Tier 2 (Development Support)
- Listed in PROGRESS_SUMMARY as Week 6 target
- A-MEM (Agent Memory) system
- SAP directory exists: `docs/skilled-awareness/memory-system/`

**Categorization Check**:
```bash
python -c "import json; cat=json.load(open('sap-catalog.json')); sap=next(s for s in cat['saps'] if s['id']=='SAP-010'); print(f\"Included by default: {sap.get('included_by_default')}\"); print(f\"Status: {sap.get('status')}\"); print(f\"Version: {sap.get('version')}\")"
```

**Expected**: `included_by_default: false` (incremental SAP)

**Verification Method**: Incremental adoption (post-bootstrap)

---

### Secondary Target: SAP-011 vs SAP-013

**Option A: SAP-011 (docker-operations)**
- Listed in PROGRESS_SUMMARY as Week 6 target
- Directory exists: `docs/skilled-awareness/docker-operations/`
- Docker containerization for MCP servers

**Option B: SAP-013 (metrics-framework)**
- Already partially verified in Week 2 (8-minute L1 adoption)
- May need L2/L3 verification
- Directory exists: `docs/skilled-awareness/metrics-framework/`

**Decision Strategy**: Check both during pre-flight, choose based on:
1. Which is actually Tier 2
2. Which has clearer L1 criteria
3. Which complements SAP-010 better

---

## Pre-Flight Checks

### Check 1: SAP-010 Categorization

**Commands**:
```bash
# Check if included by default
python -c "import json; cat=json.load(open('sap-catalog.json')); sap=next(s for s in cat['saps'] if s['id']=='SAP-010'); print(sap.get('included_by_default', 'NOT SET'))"

# Check SAP directory structure
ls -la docs/skilled-awareness/memory-system/

# Check for adoption blueprint
test -f docs/skilled-awareness/memory-system/adoption-blueprint.md && echo "BLUEPRINT EXISTS" || echo "BLUEPRINT MISSING"
```

**Expected Results**:
- `included_by_default: false` → Incremental SAP
- 5 SAP artifacts present (charter, protocol, awareness, adoption, ledger)
- Adoption blueprint exists with L1 criteria

---

### Check 2: Fast-Setup Inclusion

**Commands**:
```bash
# Check if memory system files in generated project
cd docs/project-docs/verification/verification-runs/2025-11-09-week3-sap-005-006/generated-project
test -d .chora/memory && echo "MEMORY DIR EXISTS" || echo "MEMORY DIR MISSING"
ls -la .chora/memory/ 2>/dev/null || echo "No memory directory"
```

**Expected Results**:
- `.chora/memory/` directory may or may not exist
- If exists: SAP-010 partially included (verify existing files)
- If missing: SAP-010 needs incremental adoption (copy from template)

---

### Check 3: SAP-011 vs SAP-013 Decision

**SAP-011 Check**:
```bash
# Check categorization
python -c "import json; cat=json.load(open('sap-catalog.json')); sap=next((s for s in cat['saps'] if s['id']=='SAP-011'), None); print(f'SAP-011: {sap}' if sap else 'SAP-011 NOT FOUND')"

# Check directory
ls -la docs/skilled-awareness/docker-operations/
```

**SAP-013 Check** (already partially verified):
```bash
# Review Week 2 verification results
ls -la docs/project-docs/verification/verification-runs/2025-11-09-sap-013-l1-validation/

# Check if L2/L3 adoption needed
cat docs/skilled-awareness/metrics-framework/adoption-blueprint.md | grep -A 5 "Level 2"
```

**Decision Criteria**:
1. If SAP-011 doesn't exist in catalog → Use SAP-013 (L2 adoption)
2. If SAP-011 is Tier 3+ → Use SAP-013 (stay in Tier 2)
3. If both are Tier 2 → Choose based on time estimate (prefer faster)

---

## Inferred L1 Criteria

### SAP-010 (memory-system) - Inferred L1 Criteria

Based on A-MEM architecture pattern:

| Criterion | Target | Verification Method |
|-----------|--------|---------------------|
| `.chora/memory/` directory exists | Required | Directory check |
| Event log present | `.chora/memory/events/` | Directory + sample file check |
| Knowledge graph present | `.chora/memory/knowledge/` | Directory + sample file check |
| Trace context present | `.chora/memory/traces/` | Directory + sample file check |
| README or index file | `.chora/memory/README.md` | File check |

**Total L1 Criteria**: ~5 (directory + 3 subsystems + documentation)

---

### SAP-011 (docker-operations) - Inferred L1 Criteria

Based on Docker standardization pattern:

| Criterion | Target | Verification Method |
|-----------|--------|---------------------|
| Dockerfile exists | Required | File check |
| docker-compose.yml exists | Required | File check |
| .dockerignore exists | Required | File check |
| Docker builds successfully | No errors | `docker build` execution |

**Total L1 Criteria**: ~4 (3 files + build test)

---

### SAP-013 (metrics-framework) - L2 Criteria

If choosing SAP-013 L2 adoption:

| Criterion | Target | Verification Method |
|-----------|--------|---------------------|
| L1 already verified | ✅ Week 2 | Review previous verification |
| Metrics collection automated | Script/justfile integration | Integration check |
| Baseline metrics established | Initial data points | Metrics file check |
| Reporting mechanism | Dashboard or export | Verification check |

**Total L2 Criteria**: ~4 (assuming L1 complete)

---

## Verification Strategy

### Approach 1: SAP-010 + SAP-011 (Both Incremental)

**Estimated Time**:
- SAP-010 incremental adoption: 1.5-2 hours
- SAP-011 incremental adoption: 1-1.5 hours
- Cross-validation: 30 minutes
- Reporting: 30 minutes
- **Total**: 3.5-4.5 hours

**Pros**:
- Both new SAPs verified
- Completes more of Tier 2
- Docker + Memory are complementary

**Cons**:
- Longer time commitment
- Two full adoptions

---

### Approach 2: SAP-010 + SAP-013 L2 (Incremental + Enhancement)

**Estimated Time**:
- SAP-010 incremental adoption: 1.5-2 hours
- SAP-013 L2 adoption: 1 hour
- Cross-validation: 30 minutes
- Reporting: 30 minutes
- **Total**: 3.5-4 hours

**Pros**:
- SAP-013 L1 already done (Week 2)
- L2 adoption faster than new SAP
- Memory + Metrics are highly complementary

**Cons**:
- Only 1 new SAP verified (but 2 SAPs advanced overall)

---

## Recommended Approach

**RECOMMENDATION**: **Approach 2** (SAP-010 + SAP-013 L2)

**Rationale**:
1. **Efficiency**: SAP-013 L1 done, L2 faster than new SAP
2. **Integration**: Memory + Metrics are highly complementary (SAP-010 generates events, SAP-013 measures usage)
3. **ROI Continuity**: SAP-013 Week 2 demonstrated $550 ROI, L2 builds on that
4. **Time**: Slightly faster (3.5-4h vs 3.5-4.5h)
5. **Value**: Advances 2 SAPs (1 new, 1 enhancement)

---

## Week 6 Execution Plan

### Day 1: SAP-010 (memory-system)

**Morning** (1.5-2 hours):
1. ✅ Pre-flight checks (15 min)
2. ✅ Read adoption blueprint (20 min)
3. ✅ Incremental adoption (45-60 min)
   - Create `.chora/memory/` directory structure
   - Copy template files
   - Verify L1 criteria
4. ✅ Document verification results (20-30 min)

**Output**: SAP-010-VERIFICATION.md

---

### Day 2: SAP-013 L2 (metrics-framework)

**Afternoon** (1 hour):
1. ✅ Review Week 2 L1 verification (10 min)
2. ✅ Read L2 adoption blueprint (15 min)
3. ✅ L2 incremental adoption (20-30 min)
   - Automate metrics collection
   - Establish baseline
   - Create reporting
4. ✅ Document L2 verification (10-15 min)

**Output**: SAP-013-L2-VERIFICATION.md

---

### Day 3: Cross-Validation + Reporting

**Evening** (1 hour):
1. ✅ Cross-validation: SAP-010 ↔ SAP-013 (30 min)
   - Check if memory events feed into metrics
   - Verify integration points
2. ✅ Week 6 comprehensive report (30 min)
3. ✅ Update PROGRESS_SUMMARY.md (10 min)

**Output**: CROSS_VALIDATION.md, WEEK_6_REPORT.md

---

## Success Criteria

### SAP-010 (memory-system)

**L1 GO Criteria**:
- ✅ All 5 L1 criteria met (100%)
- ✅ `.chora/memory/` directory structure created
- ✅ All 3 subsystems present (events, knowledge, traces)
- ✅ Documentation present
- ✅ Integration with existing SAPs documented

**Acceptable**: CONDITIONAL GO if 4/5 criteria met

---

### SAP-013 L2 (metrics-framework)

**L2 GO Criteria**:
- ✅ L1 verified (Week 2 ✅)
- ✅ All 4 L2 criteria met (100%)
- ✅ Metrics collection automated
- ✅ Baseline metrics established
- ✅ Reporting mechanism working

**Acceptable**: CONDITIONAL GO if 3/4 L2 criteria met

---

## Contingency Plans

### Contingency 1: SAP-010 Takes Longer Than Expected

**If SAP-010 takes >2 hours**:
- Defer SAP-013 L2 to Week 7
- Complete SAP-010 thoroughly
- Do lightweight cross-validation
- **Result**: Week 6 verifies 1 SAP (SAP-010)

---

### Contingency 2: SAP-013 L2 Criteria Unclear

**If L2 criteria not well-defined**:
- Infer L2 criteria from ledger
- Use SAP-000 (sap-framework) as guide
- Document assumptions
- **Result**: CONDITIONAL GO with documented assumptions

---

### Contingency 3: Both SAPs Blocked

**If both SAPs have blocking issues**:
- Pivot to SAP-011 (docker-operations)
- OR defer Week 6 and fix blockers
- Document blockers for future resolution

---

## Time Budget

| Activity | Estimated | Contingency | Total |
|----------|-----------|-------------|-------|
| Pre-flight checks | 15 min | 10 min | 25 min |
| SAP-010 verification | 1.5-2h | 30 min | 2.5h max |
| SAP-013 L2 verification | 1h | 20 min | 1h 20min max |
| Cross-validation | 30 min | 15 min | 45 min max |
| Reporting | 30 min | 15 min | 45 min max |
| **Total** | **3.5-4h** | **1.5h** | **5.5h max** |

**Target**: Complete in 3.5-4 hours (no contingency needed)
**Buffer**: 1.5 hours for unexpected issues

---

## Expected Outcomes

### Campaign Progress After Week 6

| Metric | Before Week 6 | After Week 6 (Expected) | Change |
|--------|---------------|-------------------------|--------|
| **Total Progress** | 32% (10/31) | **35-39%** (11-12/31) | +3-6% |
| **Tier 2 Progress** | 40% (2/5) | **60-80%** (3-4/5) | +20-40% |
| **Total Time** | 19h | **22-23h** | +3-4h |

### Decisions Expected

**SAP-010**: GO or CONDITIONAL GO ✅
**SAP-013 L2**: GO or CONDITIONAL GO ✅

**Target**: 0 NO-GO decisions

---

## Next Steps After Week 6

### If Tier 2 Reaches 60% (3/5 SAPs)

**Week 7 Focus**: Complete Tier 2
- Remaining 2 Tier 2 SAPs
- OR start Tier 3

### If Tier 2 Reaches 80% (4/5 SAPs)

**Week 7 Focus**: Finish Tier 2 + Start Tier 3
- 1 remaining Tier 2 SAP
- 1-2 Tier 3 SAPs

---

## References

- **Week 5 Report**: `docs/project-docs/verification/verification-runs/2025-11-09-week5-sap-008-012/WEEK_5_REPORT.md`
- **Progress Summary**: `docs/project-docs/verification/PROGRESS_SUMMARY.md`
- **SAP Catalog**: `sap-catalog.json`
- **Generated Project**: `docs/project-docs/verification/verification-runs/2025-11-09-week3-sap-005-006/generated-project/`

---

**Plan Status**: DRAFT
**Ready to Execute**: After pre-flight checks confirm SAP-010 + SAP-013 L2 approach
**Estimated Start**: 2025-11-09
**Estimated Duration**: 3.5-4 hours

---

**End of Week 6 Plan**
