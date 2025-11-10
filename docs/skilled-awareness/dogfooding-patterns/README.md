# SAP-027: Dogfooding Patterns

**Version:** 1.1.0 | **Status:** Pilot | **Maturity:** Pilot

> 6-week methodology for validating patterns through internal use—research (Week 0, ≥30% Level A evidence), build (Weeks 1-3), validate (Week 4, ≥2 adoption cases), GO/NO-GO decision (time savings ≥5x, satisfaction ≥85%, bugs = 0), and formalization (Week 5 if GO).

---

## 🚀 Quick Start (3 minutes)

```bash
# Week -1: Pre-pilot discovery (select candidate from intention inventory)
python scripts/score-pilot-candidates.py \
  --inventory .chora/memory/knowledge/notes/intention-inventory-2025-11-05.md \
  --output pilot-candidates-2025-11-05.md

# Week 0: Research phase (gather evidence)
just research "database migration best practices for Python"
# Output: docs/research/database-migrations-research.md (10-20 pages)

# Weeks 1-3: Build phase (implement pattern)
# Use research to inform implementation decisions

# Week 4: Validation phase (2+ real uses)
# Document time saved, satisfaction (0-10), bugs

# Week 4 End: GO/NO-GO decision
just pilot-decide pilot-2025-11-05-sap-030
# Output: Decision document with recommendation

# Week 5: Formalization (if GO)
# Complete artifact TODOs, mark production-ready
```

**First time?** → Read [adoption-blueprint.md](adoption-blueprint.md) for complete 6-week workflow (25-min read)

---

## 📖 What Is SAP-027?

SAP-027 provides a **6-week dogfooding pilot methodology** for validating patterns through internal use before ecosystem adoption. Reduces risk of investing months in low-ROI patterns by validating fit, evidence, and user demand through structured pilot phases with GO/NO-GO criteria.

**Key Innovation**: **GO/NO-GO criteria framework** (time savings ≥5x, satisfaction ≥85%, bugs = 0, adoption ≥2 cases)—data-driven decision making eliminates guesswork and prevents premature ecosystem adoption.

### How It Works

1. **Week -1 (Pre-Pilot Discovery)**: Score pilot candidates from intention inventory using weighted criteria (evidence 40%, alignment 30%, demand 20%, feasibility 10%)
2. **Week 0 (Research Phase)**: Gather evidence (≥30% Level A citations), generate 10-20 page research report with principles, practices, anti-patterns
3. **Weeks 1-3 (Build Phase)**: Implement pattern to minimum viable state, informed by research
4. **Week 4 (Validation Phase)**: Use pattern in ≥2 real cases, collect metrics (time saved, satisfaction 0-10, bugs)
5. **Week 4 End (Decision Phase)**: Review metrics against GO/NO-GO criteria, calculate ROI, write decision document
6. **Week 5 (Formalization, if GO)**: Complete artifact TODOs, mark production-ready, broadcast adoption

---

## 🎯 When to Use

Use SAP-027 when you need to:

1. **Validate new patterns** - Test feasibility and ROI before ecosystem adoption (avoid months of wasted effort)
2. **Data-driven decisions** - GO/NO-GO criteria eliminate guesswork (objective metrics, not subjective opinions)
3. **Evidence-based design** - Research phase (≥30% Level A evidence) informs implementation
4. **Risk reduction** - Catch low-ROI patterns early (Week 4 NO-GO prevents further investment)
5. **ROI tracking** - Measure time savings, satisfaction, bugs for continuous improvement

**Not needed for**: Trivial patterns (< 5 hours implementation), well-established practices (Redux, TDD), or exploratory spikes (use prototyping instead)

---

## ✨ Key Features

- ✅ **6-Week Methodology** - Structured phases (Research → Build → Validate → Decide → Formalize)
- ✅ **GO/NO-GO Criteria** - Objective decision framework (time ≥5x, satisfaction ≥85%, bugs = 0, adoption ≥2)
- ✅ **Evidence-Based Research** - ≥30% Level A citations (standards, peer-reviewed papers)
- ✅ **ROI Analysis** - Break-even calculation (hours invested vs hours saved)
- ✅ **Metrics Collection** - Time tracking, satisfaction surveys, bug counts
- ✅ **Pilot Documentation** - Weekly metrics, final summary, decision rationale
- ✅ **Template Refinement** - TODO completion workflow for production readiness

---

## 📚 Quick Reference

### 6-Week Pilot Timeline

| Phase | Duration | Activities | Deliverables |
|-------|----------|------------|--------------|
| **Week -1** | Pre-Pilot Discovery | Score intention inventory, select candidate | pilot-candidates-{date}.md |
| **Week 0** | Research Phase | Gather evidence (≥30% Level A), WebSearch | {topic}-research.md (10-20 pages) |
| **Weeks 1-3** | Build Phase | Implement to minimum viable state | Working pattern implementation |
| **Week 4** | Validation Phase | Use in ≥2 real cases, collect metrics | Validation reports with time/satisfaction/bugs |
| **Week 4 End** | Decision Phase | Review GO/NO-GO criteria, calculate ROI | go-no-go-decision.md with recommendation |
| **Week 5** | Formalization (if GO) | Complete artifacts, mark production | Production-ready SAP |

**Total Time**: 6 weeks (42 days) from research to decision

---

### GO/NO-GO Criteria

**GO Decision Requirements** (all 4 criteria must be met):

| Criterion | Target | Measurement | Rationale |
|-----------|--------|-------------|-----------|
| **Time Savings** | ≥5.0x | Hours saved / hours invested | ROI breakeven (1 hour invested → 5+ hours saved) |
| **Satisfaction** | ≥85% | Avg survey score / 10 * 100% | User happiness threshold (8.5/10 or higher) |
| **Bugs Introduced** | = 0 | Count of new bugs caused by pattern | Quality guarantee (no regressions) |
| **Adoption Cases** | ≥ 2 | Real-world uses during Week 4 | Viability proof (pattern works in practice) |

**Example** (GO decision):
```
Time Savings: 5.6x (67 min saved / 12 min invested)
Satisfaction: 92% (9.2/10 avg from 3 uses)
Bugs: 0 (no issues reported)
Adoption: 3 cases (COORD-2025-008, COORD-2025-009, COORD-2025-010)
→ Decision: ✅ GO (all criteria met)
```

**Example** (NO-GO decision):
```
Time Savings: 3.2x (38 min saved / 12 min invested)  ❌ Below 5.0x threshold
Satisfaction: 78% (7.8/10 avg from 2 uses)  ❌ Below 85% threshold
Bugs: 0 (no issues)
Adoption: 2 cases (minimum met)
→ Decision: ❌ NO-GO (2 criteria not met)
```

---

### Week -1: Pre-Pilot Discovery

**Purpose**: Select high-value pilot candidate from intention inventory

**Workflow**:

```bash
# 1. Query intention inventory
cat .chora/memory/knowledge/notes/intention-inventory-2025-11-05.md | \
  grep -A 5 "^## "

# 2. Score candidates (weighted criteria)
python scripts/score-pilot-candidates.py \
  --inventory intention-inventory-2025-11-05.md \
  --output pilot-candidates-2025-11-05.md

# 3. Review top 3-5 candidates
cat pilot-candidates-2025-11-05.md
```

**Scoring Criteria** (weighted):
- **Evidence availability (40%)**: Level A/B sources exist for research
  - 10 points: Multiple Level A (standards, peer-reviewed)
  - 7 points: Mix of Level A + B (case studies)
  - 4 points: Primarily Level B
  - 1 point: Limited to Level C (blogs)

- **Strategic alignment (30%)**: Fits Wave 1/2 vision
  - 10 points: Wave 1 committed feature
  - 7 points: Wave 2 exploratory
  - 4 points: Wave 3 future
  - 1 point: Not in vision

- **User demand (20%)**: Evidence of need
  - 10 points: ≥10 requests
  - 7 points: 5-9 requests
  - 4 points: 1-4 requests
  - 1 point: Internal hypothesis

- **Feasibility (10%)**: Effort estimate
  - 10 points: 1-2 week build, low risk
  - 7 points: 2-3 week build, moderate risk
  - 4 points: 3-4 week build, high risk
  - 1 point: >4 week build, very high risk

**Threshold**: ≥7.0 score to proceed with pilot

---

### Week 0: Research Phase

**Purpose**: Gather evidence to inform implementation (≥30% Level A citations)

**Workflow**:

```bash
# 1. Execute research workflow
just research "database migration best practices for Python"

# 2. Use WebSearch to gather evidence
# - Level A: Standards, peer-reviewed papers
# - Level B: Industry case studies, official docs
# - Level C: Expert opinion, blog posts

# 3. Generate research report (10-20 pages)
# Output: docs/research/{topic}-research.md
```

**Research Report Structure**:

1. **Executive Summary** (12 bullets)
   - Adopt now vs defer decisions
   - Key takeaways

2. **Principles** (The Why)
   - Modularity, SOLID, 12-factor
   - Level A/B/C citations

3. **Practices** (The How)
   - Architecture patterns
   - Code examples, configs

4. **Anti-Patterns** (What to Avoid)
   - Common mistakes
   - Why these fail

5. **Decision Playbooks**
   - "Choose X when..." guidance
   - Trade-off tables

6. **Appendix**
   - Annotated bibliography (Level A/B/C labeled)
   - Glossary

**Requirements**:
- ≥30% Level A evidence citations
- 10-20 pages (2,000-4,000 words)
- Research informs Weeks 1-3 build phase

---

### Weeks 1-3: Build Phase

**Purpose**: Implement pattern to minimum viable state

**Workflow**:

```bash
# 1. Design informed by Week 0 research
# - Reference research report for architectural decisions
# - Cite research in code comments (e.g., "Per X research, using Y pattern")

# 2. Implement to minimum viable state
# - Focus on core functionality (80% of value, 20% of effort)
# - Document TODOs for production readiness

# 3. Test internally
# - Use pattern in real tasks
# - Collect feedback continuously

# 4. Iterate based on feedback
# - Refine patterns, update docs
```

**Build Phase Goals**:
- Working implementation (not production-ready)
- Core use cases functional
- Documentation for validation phase

**Not Required in Build Phase**:
- Complete edge case handling
- Comprehensive testing
- Production optimization

---

### Week 4: Validation Phase

**Purpose**: Use pattern in ≥2 real cases, collect metrics

**Workflow**:

```bash
# 1. Use pattern in real tasks (≥2 cases)
# Document each use with metrics

# 2. Collect metrics for each use:
```

**Validation Metrics Template**:

```markdown
## Validation Case 1: {Task Description}

**Coordinator**: {Your Name}
**Date**: 2025-11-05
**Trace ID**: COORD-2025-008

### Metrics
- **Setup Time**: 12 minutes (one-time cost)
- **Time Saved**: 67 minutes (vs manual baseline)
- **Satisfaction**: 9/10 (very satisfied)
- **Bugs Introduced**: 0
- **Would Use Again**: Yes

### Qualitative Feedback
- Strength: Clear workflow, saved significant time
- Weakness: Initial setup confusing
- Suggestion: Add quick start guide

### ROI Calculation
- Hours Invested: 0.2 hours (12 minutes)
- Hours Saved: 1.1 hours (67 minutes)
- ROI: 5.5x
```

**Requirements**:
- ≥2 validation cases (minimum)
- Real tasks (not synthetic demos)
- Complete metrics for each case

---

### Week 4 End: Decision Phase

**Purpose**: Review metrics, make GO/NO-GO decision

**Workflow**:

```bash
# 1. Aggregate metrics from all validation cases
# Calculate: avg time savings, avg satisfaction, total bugs, adoption count

# 2. Review against GO/NO-GO criteria
# All 4 criteria must be met for GO decision

# 3. Generate decision document
just pilot-decide pilot-2025-11-05-sap-030
# Output: go-no-go-decision.md
```

**Decision Document Template**:

```markdown
# GO/NO-GO Decision: SAP-030 (Database Migrations)

## Metrics Summary
- **Setup Time**: 12 minutes (one-time)
- **Validation Uses**: 3
- **Avg Time Saved**: 67 minutes (5.6x ROI)
- **Avg Satisfaction**: 9.2/10 (92%)
- **Bugs Introduced**: 0
- **Adoption Cases**: 3 (COORD-2025-008, COORD-2025-009, COORD-2025-010)

## Decision: ✅ GO

## Criteria Review
✅ Time Savings: 5.6x ≥ 5.0 (target met)
✅ Satisfaction: 92% ≥ 85% (target met)
✅ Bugs: 0 = 0 (target met)
✅ Adoption: 3 ≥ 2 (target met)

## Rationale
All 4 criteria met with strong margins. Pattern demonstrates clear value
(5.6x time savings), high user satisfaction (92%), zero quality issues,
and proven viability (3 adoption cases).

## Next Steps
1. Week 5: Complete formalization checklist
2. Mark SAP-030 as production-ready
3. Broadcast adoption via SAP-001
```

---

### Week 5: Formalization (if GO)

**Purpose**: Complete artifacts, mark production-ready

**Workflow**:

```bash
# 1. Complete artifact TODOs
# Review capability-charter, protocol-spec, awareness-guide, adoption-blueprint
# Fill in placeholders, add examples, update status

# 2. Update ledger with pilot metrics
# Add adoption cases, time savings, satisfaction

# 3. Mark SAP as production-ready
# Update sap-catalog.json status: pilot → active

# 4. Broadcast adoption via SAP-001
# Create coordination request for ecosystem awareness
```

**Formalization Checklist**:

- [ ] capability-charter.md complete (problem, solution, scope)
- [ ] protocol-spec.md complete (technical contracts, data models)
- [ ] awareness-guide.md / AGENTS.md complete (workflows, examples)
- [ ] adoption-blueprint.md complete (installation steps, validation)
- [ ] ledger.md updated (pilot metrics, adoption cases)
- [ ] sap-catalog.json updated (status: pilot → active)
- [ ] Coordination request created (SAP-001 broadcast)

---

## 🔗 Integration with Other SAPs

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-010** (Memory System) | Intention Inventory | Pilot candidates sourced from intention-inventory-{date}.md in knowledge notes |
| **SAP-001** (Inbox) | Coordination Tracking | Adoption cases tracked via coordination trace IDs (COORD-2025-XXX) |
| **SAP-013** (Metrics Tracking) | ROI Analysis | Time savings, satisfaction, bugs collected with ClaudeROICalculator |
| **SAP-015** (Task Tracking) | Pilot Tracking | Pilot tasks managed via beads CLI (bd create, bd update, bd close) |
| **SAP-029** (SAP Generation) | Formalization | Generate SAP artifacts from templates during Week 5 formalization |

---

## 🏆 Success Metrics

- **Pilot Success Rate**: 70-80% of pilots meet GO criteria (quality bar for candidate selection)
- **Time Savings**: 5.0x average ROI across all GO pilots (breakeven threshold)
- **Satisfaction**: 85%+ average satisfaction (8.5/10 or higher)
- **Bug Rate**: 0 bugs introduced (quality guarantee)
- **Research Quality**: ≥30% Level A evidence citations (research rigor)
- **Formalization Time**: Week 5 completion within 5 business days (efficiency)

---

## 🔧 Troubleshooting

### Problem: Pilot Candidate Score Below Threshold (<7.0)

**Symptom**: Weighted score <7.0, pilot not recommended

**Common Causes**:
1. Low evidence availability (Level C sources only)
2. Poor strategic alignment (not in Wave 1/2 vision)
3. No user demand (internal hypothesis)

**Solutions**:

```bash
# Option 1: Defer pilot, wait for better evidence
# - Continue research, gather Level A/B sources
# - Revisit in next intention inventory review

# Option 2: Adjust candidate
# - Narrow scope to increase feasibility score
# - Align with Wave 1 priorities to boost strategic score

# Option 3: Validate user demand
# - Create coordination request (SAP-001) to gauge interest
# - Collect user feedback before committing to pilot
```

**Validation**: Re-score candidate after adjustments, verify ≥7.0 threshold

---

### Problem: Week 0 Research Report Lacks Level A Evidence (<30%)

**Symptom**: Research report primarily Level B/C sources

**Common Causes**:
1. Domain lacks formal standards (emerging technology)
2. WebSearch results dominated by blog posts
3. Insufficient search depth

**Solutions**:

```bash
# Option 1: Expand search to academic sources
# - Use Google Scholar, ACM Digital Library
# - Search for peer-reviewed papers, conference proceedings

# Option 2: Consult official specifications
# - W3C, IETF, ISO standards
# - Official framework documentation (React, Next.js)

# Option 3: Accept higher Level B ratio (document rationale)
# - For emerging domains, 20-30% Level A may be acceptable
# - Document why Level A sources limited
```

**Validation**: Re-count evidence citations, verify ≥30% Level A

---

### Problem: Week 4 Validation Only 1 Adoption Case (Need ≥2)

**Symptom**: Only 1 real use during validation phase

**Common Causes**:
1. Pattern too niche (limited use cases)
2. Validation phase too short (need more time)
3. Pattern difficult to adopt (high friction)

**Solutions**:

```bash
# Option 1: Extend validation phase by 1 week
# - Allow more time for additional use cases
# - Document extension in pilot timeline

# Option 2: Use pattern in synthetic task (with caveat)
# - Create realistic task that requires pattern
# - Note in decision document: 1 real + 1 synthetic use

# Option 3: NO-GO decision (pivot or defer)
# - If pattern truly has limited demand, make NO-GO decision
# - Document lessons learned, revisit later
```

**Validation**: Ensure ≥2 adoption cases before Week 4 End decision

---

### Problem: GO/NO-GO Criteria Not Met (1+ Criteria Below Threshold)

**Symptom**: Time savings 3.2x (< 5.0x) or satisfaction 78% (< 85%)

**Common Causes**:
1. Pattern overhead too high (setup time reduces ROI)
2. Incomplete implementation (missing core features)
3. Poor user experience (confusing workflow)

**Solutions**:

```bash
# Option 1: NO-GO decision with lessons learned
# - Document why pattern failed criteria
# - Capture insights for future iteration
# - Example: "Pattern setup too complex (12 min), need <5 min for 5x ROI"

# Option 2: Extend pilot 1 week, iterate on feedback
# - Address user experience issues
# - Simplify setup, improve documentation
# - Re-validate with improved pattern

# Option 3: Pivot pattern scope
# - Narrow to highest-ROI use case
# - Remove low-value features increasing overhead
```

**Validation**: Re-calculate metrics after iteration, verify criteria met

---

### Problem: Week 5 Formalization Taking >5 Business Days

**Symptom**: Artifact TODOs incomplete after Week 5 deadline

**Common Causes**:
1. Too many placeholder TODOs in artifacts
2. Missing examples or code snippets
3. Production readiness gaps (testing, docs)

**Solutions**:

```bash
# Option 1: Prioritize critical artifacts
# - Focus on protocol-spec, adoption-blueprint (minimum viable)
# - Defer nice-to-have polish for post-formalization

# Option 2: Use templates for rapid completion
# - Copy structure from similar SAPs (e.g., SAP-015 for task tracking)
# - Fill in domain-specific content

# Option 3: Document incomplete artifacts as known limitations
# - Mark SAP status: pilot (not production)
# - Create follow-up tasks (SAP-015) for completion
```

**Validation**: Review sap-catalog.json, verify status marked appropriately

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete dogfooding specification (52KB, 26-min read)
- **[AGENTS.md](AGENTS.md)** - Agent dogfooding workflows (21KB, 11-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude Code patterns (18KB, 9-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - 6-week setup guide (48KB, 24-min read)
- **[capability-charter.md](capability-charter.md)** - Problem statement and solution design
- **[ledger.md](ledger.md)** - Pilot success metrics and adoption history

### Related Patterns

- [SAP-010 (Memory System)](../memory-system/) - Intention inventory sourcing
- [SAP-001 (Inbox)](../inbox/) - Coordination tracking for adoption cases
- [SAP-013 (Metrics Tracking)](../metrics-tracking/) - ROI calculation and time tracking
- [SAP-015 (Task Tracking)](../task-tracking/) - Pilot task management with beads
- [SAP-029 (SAP Generation)](../sap-generation/) - Artifact generation for formalization

---

**Version History**:
- **1.1.0** (2025-11-05) - Added Week -1 pre-pilot discovery, refined GO/NO-GO criteria thresholds
- **1.0.0** (2025-10-15) - Initial dogfooding patterns with 6-week methodology

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
