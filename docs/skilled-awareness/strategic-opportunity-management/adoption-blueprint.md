# Strategic Opportunity Management - Adoption Blueprint

**Pattern ID**: SAP-060
**Pattern Name**: strategic-opportunity-management
**Version**: 1.0.0
**Status**: Pilot
**Last Updated**: 2025-11-21

## Overview

This blueprint defines the 4-level adoption path for Strategic Opportunity Management, from basic capture (L1) through portfolio intelligence (L4).

**Adoption Maturity Levels**:
- **Level 1**: Manual Capture & VERA Prioritization (2-3 hours setup)
- **Level 2**: Portfolio Management & Automation (8-12 hours cumulative)
- **Level 3**: Strategic Planning & Multi-Team Coordination (20-30 hours cumulative)
- **Level 4**: Organizational Intelligence & Predictive Analytics (40-60 hours cumulative)

**Progressive adoption**: Start with L1 (template-driven capture), evolve to L2 when ANY 2 of 5 triggers occur, continue to L3/L4 as organization matures.

---

## Level 1: Manual Capture & VERA Prioritization

### Capabilities

1. **Rapid Opportunity Capture** (<15 min)
   - Template-driven documentation
   - VERA scoring (Value, Effort, Risk, Alignment)
   - Priority calculation and band assignment
   - Waypoint definition for high-risk/high-effort work

2. **Intention Tracking**
   - Log opportunity_identified A-MEM event
   - Capture intended impact (quantified benefits)
   - Manual retrospective tracking

3. **Basic Integration**
   - SAP-001 inbox routing (opportunities/ directory)
   - SAP-015 beads linking (opportunity_id metadata)
   - Manual promotion workflow (Priority ≥ 25 → CORD)

### Artifacts

**Template** (required):
- `inbox/opportunities/STRATEGIC-OPPORTUNITY-MANAGEMENT-L1.md` - Capture template

**Opportunities** (created during use):
- `inbox/opportunities/OPP-YYYY-NNN-short-name.md` - Captured opportunities

**Events** (manual logging):
- `.chora/memory/events/YYYY-MM.jsonl` - A-MEM lifecycle events

**Knowledge** (post-delivery):
- `.chora/memory/knowledge/notes/YYYY-MM-DD-pattern-name.md` - Extracted patterns

### Setup (2-3 hours)

**Prerequisites**:
- SAP-001 (Inbox) at L1+
- SAP-010 (Memory System) at L1+
- SAP-015 (Beads) at L1+ (optional but recommended)

**Installation**:

```bash
# 1. Verify prerequisites (5 min)
ls inbox/opportunities/                    # SAP-001 inbox exists
ls .chora/memory/events/                   # SAP-010 memory exists
bd list                                    # SAP-015 beads works (optional)

# 2. Create template (10 min)
# Copy from SAP-060 awareness-guide.md or create from scratch
cat > inbox/opportunities/STRATEGIC-OPPORTUNITY-MANAGEMENT-L1.md << 'EOF'
# Opportunity: [SHORT NAME]

**ID**: OPP-YYYY-NNN
**Created**: YYYY-MM-DD
**Status**: captured | promoted | delivered | learned
**Priority**: [calculated from VERA]

## Problem Statement
[What problem does this solve? 2-3 sentences]

## Solution Overview
[What is the proposed solution? 2-3 sentences]

## VERA Scoring
value: [1-5]        # Quantified benefits (time savings, adoption, ROI)
effort: [1-5]       # Hours required (INVERTED: 1=80+ hrs, 5=<4 hrs)
risk: [1-5]         # Technical/adoption risks (INVERTED: 1=high, 5=low)
alignment: [1-5]    # Strategic fit (1=misaligned, 5=critical)

priority: [calculated]  # (V × 2.0) + (E × 1.5) + (R × 1.0) + (A × 2.5)
priority_band: [Critical | High | Medium | Low | Defer]

## Intended Impact
- Time savings: [quantified]
- Adoption increase: [quantified]
- ROI: [quantified]

## Waypoint (if R ≤ 2 or E ≤ 2)
goal: [What uncertainty are we resolving?]
deliverable: [What artifact answers it?]
success_criteria: [What validates the approach?]
estimated_time: 3-4 hours

## A-MEM Events
- ✅ opportunity_identified: [date]
- ⏳ opportunity_promoted: [when CORD created]
- ⏳ opportunity_delivered: [when work complete]
- ⏳ outcome_validated: [6-8 weeks post-delivery]
EOF

# 3. Test template (30 min - create pilot opportunity)
cp inbox/opportunities/STRATEGIC-OPPORTUNITY-MANAGEMENT-L1.md \
   inbox/opportunities/OPP-2025-999-test-opportunity.md

# Edit OPP-2025-999-test-opportunity.md:
#  - Fill in problem, solution
#  - Score VERA dimensions (5 min)
#  - Calculate priority
#  - Log opportunity_identified event

# 4. Validate workflow (1 hour)
# - Create 1 real opportunity
# - VERA score should match actual urgency
# - If Priority ≥ 25, promote to CORD
# - Verify Beads linking (opportunity_id metadata)

# 5. Document L1 adoption (15 min)
# Create ledger.md (see ledger template below)
```

### Validation Criteria

**L1 adoption complete when**:
- [ ] Template exists and is usable
- [ ] At least 1 opportunity captured in <15 min
- [ ] VERA scoring produces priority band
- [ ] Priority band matches actual resourcing (80%+ accuracy target)
- [ ] Waypoint defined for High Risk (R ≤ 2) or High Effort (E ≤ 2) opportunity
- [ ] opportunity_identified event logged to .chora/memory/events/
- [ ] Integration with SAP-001 (opportunity routing) works
- [ ] Integration with SAP-015 (Beads linking) works (optional)

### Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Capture time | <15 min | Time from discovery to saved OPP file |
| VERA accuracy | 80%+ | Priority band vs actual resourcing decision |
| Waypoint ROI | ≥1 pivot prevented | Hours saved by waypoint validation |
| Event logging | 100% | All opportunities have opportunity_identified event |

### Common Issues

**Issue 1: VERA scores seem arbitrary**
- **Symptom**: Value = 5 without quantified benefits
- **Fix**: Require time savings, adoption metrics, or ROI calculations for Value scores

**Issue 2: Capture takes >15 min**
- **Symptom**: Spending 30-60 min writing comprehensive charter
- **Fix**: Use template, aim for 10-15 min, refine during execution

**Issue 3: Priority doesn't match urgency**
- **Symptom**: Priority 28 (High) but not starting for 4 weeks
- **Fix**: Re-score Alignment dimension (likely overestimated strategic fit)

**Issue 4: Waypoint unclear**
- **Symptom**: Can't define concrete deliverable or success criteria
- **Fix**: Start with "What question do I need answered?" then work backward to deliverable

---

## Level 2: Portfolio Management & Automation

### Evolution Triggers

Adopt L2 when **ANY 2** of these 5 criteria occur:

1. **Automation value**: >20 opportunities captured (manual tracking painful)
2. **Portfolio scale**: >30% opportunities have dependencies
3. **VERA accuracy gap**: <70% accuracy (need historical data to improve)
4. **Reporting burden**: Stakeholders request portfolio dashboards
5. **Template fragmentation**: 3+ custom templates emerge (specialization by type)

### New Capabilities

1. **Portfolio Dashboard**
   - Visual overview of all opportunities (by status, priority band, owner)
   - Dependency graph visualization
   - Progress tracking (captured → promoted → delivered → learned)

2. **Automated VERA Calculation**
   - Historical accuracy analysis (intended vs actual impact)
   - Calibrated scoring rubrics (adjust based on variance)
   - Suggested scores based on past similar opportunities

3. **Beads API Integration**
   - Auto-create Beads tasks when CORD promoted
   - Sync task status back to opportunity
   - Completion triggers opportunity_delivered event

4. **Custom VERA Weights**
   - Different weights per opportunity type (technical vs strategic vs research)
   - Team-specific calibration (different teams, different priorities)

### New Artifacts

**Automation**:
- `justfile` recipes for opportunity management
- `scripts/opportunity-manager.py` - Portfolio dashboard + VERA automation
- `scripts/opportunity-promote.py` - Auto-promotion when Priority ≥ 25

**Configuration**:
- `opportunity-config.yaml` - Custom VERA weights, automation settings

**Reports**:
- `reports/opportunity-dashboard.html` - Interactive portfolio view
- `reports/vera-accuracy-report.md` - Historical accuracy analysis

### Setup (8-12 hours cumulative from L1)

**Prerequisites**:
- L1 adoption complete
- At least 5 opportunities with outcome_validated events (for calibration)
- Python 3.11+ or TypeScript/Deno runtime

**Installation**:

```bash
# 1. Install automation scripts (4 hours)
# scripts/opportunity-manager.py
#   - Portfolio dashboard generation
#   - VERA auto-calculation with historical data
#   - Dependency graph rendering

# 2. Add justfile recipes (2 hours)
# just opportunity-create "Short name"
# just opportunity-score OPP-YYYY-NNN
# just opportunity-promote OPP-YYYY-NNN
# just opportunity-dashboard
# just opportunity-metrics

# 3. Configure custom VERA weights (1 hour)
# opportunity-config.yaml

# 4. Integrate with Beads API (3 hours)
# Auto-create tasks on CORD promotion
# Sync task completion → opportunity_delivered event

# 5. Validate automation (2 hours)
# Test dashboard generation
# Test auto-promotion workflow
# Verify VERA calibration
```

### Validation Criteria

**L2 adoption complete when**:
- [ ] Portfolio dashboard shows all opportunities (status, priority, dependencies)
- [ ] Automated VERA calculation using historical data (calibration)
- [ ] justfile recipes functional (create, score, promote, dashboard)
- [ ] Beads API integration working (auto-create tasks, sync status)
- [ ] Custom VERA weights configurable per opportunity type
- [ ] VERA accuracy >70% (improved from L1 with calibration)

### Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| VERA accuracy | >70% | Priority band vs actual resourcing (with calibration) |
| Dashboard usage | Weekly | Stakeholders review dashboard at least weekly |
| Automation ROI | 50%+ time savings | Portfolio management time vs L1 manual tracking |
| Dependency visibility | 100% | All dependencies captured and visualized |

---

## Level 3: Strategic Planning & Multi-Team Coordination

### Evolution Triggers

Adopt L3 when **ANY 2** of these criteria occur:

1. **Multi-team adoption**: 3+ teams using opportunity management
2. **Quarterly planning**: Organization requires portfolio-level roadmap
3. **Resource contention**: Opportunities compete for shared resources
4. **Strategic alignment**: Need to validate work aligns with OKRs/strategy

### New Capabilities

1. **Quarterly Pipeline Planning**
   - Portfolio-level roadmap generation
   - Resource allocation optimization
   - Strategic alignment validation

2. **Multi-Team Coordination**
   - Cross-team dependency management
   - Shared opportunity pools
   - Team capacity planning

3. **Portfolio-Level ROI Projections**
   - Expected value of opportunity pipeline
   - Risk-adjusted ROI forecasting
   - Investment prioritization

4. **Strategic Alignment Tracking**
   - OKR/goal linkage for all opportunities
   - Alignment scoring automation
   - Misalignment alerts

### New Artifacts

**Planning**:
- `plans/quarterly-opportunity-pipeline-YYYY-QN.md` - Quarterly roadmap
- `plans/team-capacity-allocation.yaml` - Resource planning

**Coordination**:
- `coordination/cross-team-dependencies.yaml` - Dependency graph
- `coordination/shared-opportunity-pool.md` - Multi-team opportunities

**Analytics**:
- `analytics/portfolio-roi-projection.md` - Expected value analysis
- `analytics/strategic-alignment-report.md` - OKR linkage

### Setup (20-30 hours cumulative from L2)

**Prerequisites**:
- L2 adoption complete
- Multiple teams (3+) using opportunity management
- Quarterly planning process established

### Validation Criteria

**L3 adoption complete when**:
- [ ] Quarterly pipeline planning established (roadmap generation)
- [ ] Multi-team coordination workflows active (cross-team dependencies)
- [ ] Portfolio-level ROI projections generated
- [ ] Strategic alignment tracked for all opportunities
- [ ] Resource allocation optimized across teams

---

## Level 4: Organizational Intelligence & Predictive Analytics

### Evolution Triggers

Adopt L4 when organization reaches maturity:

1. **Scale**: 10+ teams, 100+ opportunities/year
2. **Data richness**: 2+ years of historical data
3. **Executive sponsorship**: C-level champions opportunity management
4. **AI readiness**: ML infrastructure available

### New Capabilities

1. **Cross-Project Pattern Extraction**
   - Automated pattern mining from historical data
   - Best practice identification
   - Anti-pattern detection

2. **VERA Scoring ML Model**
   - Machine learning improves VERA accuracy to 90%+
   - Predictive scoring based on opportunity characteristics
   - Continuous improvement with feedback loop

3. **Predictive Opportunity Identification**
   - AI suggests opportunities based on organizational context
   - Proactive gap analysis
   - Strategic opportunity generation

4. **Strategic Roadmap Auto-Generation**
   - AI-driven portfolio optimization
   - Multi-quarter planning automation
   - Scenario modeling

### New Artifacts

**AI Models**:
- `models/vera-scorer-v1.0.pkl` - ML model for VERA scoring
- `models/opportunity-recommender-v1.0.pkl` - Opportunity suggestion model

**Intelligence**:
- `intelligence/pattern-library.md` - Extracted organizational patterns
- `intelligence/predictive-roadmap-YYYY-QN.md` - AI-generated roadmap

### Setup (40-60 hours cumulative from L3)

**Prerequisites**:
- L3 adoption complete
- 2+ years historical data (100+ opportunities with outcomes)
- ML infrastructure (model training, serving)
- Data science expertise

### Validation Criteria

**L4 adoption complete when**:
- [ ] Pattern extraction automated (monthly updates)
- [ ] VERA ML model deployed (90%+ accuracy)
- [ ] Predictive opportunity identification active
- [ ] Strategic roadmap auto-generation working
- [ ] Executive dashboards show organizational intelligence

---

## Adoption Roadmap

### Typical Timeline

**L1 (Manual)**: 2-3 hours setup, 1-2 weeks validation
**L2 (Portfolio)**: +8-12 hours, 1-2 months validation
**L3 (Strategic)**: +20-30 hours, 3-6 months validation
**L4 (Intelligence)**: +40-60 hours, 12-18 months validation

**Total investment** (L1 → L4): 70-105 hours over 18-24 months

### Decision Tree

```
Start → L1 (Manual Capture)
         ├─ <20 opportunities captured? → Stay at L1
         ├─ <70% VERA accuracy? → Stay at L1 (refine scoring)
         └─ ANY 2 L2 triggers? → Adopt L2

L2 (Portfolio Management)
         ├─ Single team? → Stay at L2
         ├─ No quarterly planning? → Stay at L2
         └─ ANY 2 L3 triggers? → Adopt L3

L3 (Strategic Planning)
         ├─ <100 opportunities/year? → Stay at L3
         ├─ <2 years historical data? → Stay at L3
         └─ Mature at scale + ML ready? → Adopt L4

L4 (Organizational Intelligence)
         └─ Continuous improvement
```

### Recommended Path

**Month 1-2**: L1 adoption (2-3 hours setup, validate with 2-5 opportunities)
**Month 3-6**: Stay at L1, capture 10-20 opportunities, refine VERA scoring
**Month 7-9**: Adopt L2 when ANY 2 triggers occur (8-12 hours automation)
**Year 2**: Stay at L2, mature portfolio management, multi-team adoption
**Year 2-3**: Adopt L3 when multi-team coordination needed (20-30 hours)
**Year 3+**: Adopt L4 when scale + data maturity + ML readiness achieved (40-60 hours)

---

## Anti-Patterns

### Anti-Pattern 1: Skipping L1 Validation

**Symptom**: Jump directly to L2 automation without L1 validation
**Risk**: Automating broken process (VERA scoring not calibrated, template not validated)
**Remedy**: Always validate L1 with 5+ opportunities before L2 automation

### Anti-Pattern 2: Over-Engineering L1

**Symptom**: Adding dashboard/automation at L1 before validating manual workflow
**Risk**: Wasted effort on features you don't need yet
**Remedy**: Stay at L1 until ANY 2 L2 triggers occur (don't prematurely optimize)

### Anti-Pattern 3: Forcing L3 Adoption

**Symptom**: Implementing multi-team coordination when only 1 team uses opportunity management
**Risk**: Coordination overhead with no benefit
**Remedy**: L3 only when 3+ teams actively using L2

### Anti-Pattern 4: L4 Without Data Maturity

**Symptom**: ML models with <2 years historical data
**Risk**: Models overfit, poor predictions, wasted ML investment
**Remedy**: L4 requires 2+ years + 100+ opportunities with outcomes

---

## Support & Resources

**L1 Resources**:
- Template: `inbox/opportunities/STRATEGIC-OPPORTUNITY-MANAGEMENT-L1.md`
- Awareness guide: [awareness-guide.md](awareness-guide.md)
- Protocol spec: [protocol-spec.md](protocol-spec.md)

**L2 Resources** (Future):
- Automation scripts: `scripts/opportunity-manager.py`
- justfile recipes: `just opportunity-*`
- Dashboard templates: `templates/opportunity-dashboard.html`

**Community**:
- GitHub Discussions: Share VERA scoring rubrics, lessons learned
- Monthly office hours: L2+ adopters share best practices

---

**Created**: 2025-11-21
**Version**: 1.0.0
**Next Review**: After 10 L1 adoptions (validate L1 → L2 evolution triggers)
**Trace ID**: sap-060-adoption-blueprint-2025-11-21
