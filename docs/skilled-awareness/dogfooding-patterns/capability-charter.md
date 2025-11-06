# Capability Charter: Dogfooding Patterns

**SAP ID**: SAP-027
**Version**: 1.0.0
**Status**: active
**Owner**: Victor
**Created**: 2025-11-03
**Last Updated**: 2025-11-03

---

## 1. Problem Statement

### Current Challenge

New patterns and capabilities lack validation before ecosystem adoption, leading to failed patterns, wasted integration effort, and reduced ecosystem trust.

Current challenge: No formalized methodology for testing patterns internally before recommending them to the ecosystem. Ad-hoc pilots lack structure, success criteria, and ROI analysis.

Developers face: uncertainty about pattern viability, unclear GO/NO-GO thresholds, missing metrics templates, and difficulty reproducing pilot methodology.

### Evidence



- SAP-029 pilot achieved 120x time savings vs 5x target (24x over expectations)

- 5-week dogfooding pilot (3 weeks early completion) validated template generation at scale

- chora-compose achieved 9x efficiency with dogfooding (COORD-2025-009 coordination)

- 100% developer satisfaction (5/5 rating) from structured pilot approach

- Zero critical bugs across 2 generated SAPs (SAP-029, SAP-028)



### Business Impact

Without dogfooding methodology:

- Pattern risk: Untested patterns fail in ecosystem, wasting integration effort (5-10h per adopter)
- Trust erosion: Failed recommendations reduce ecosystem confidence in future patterns
- Missed optimization: No feedback loop to refine patterns before wide adoption
- ROI uncertainty: Unknown break-even point discourages pattern investment
- Methodological debt: Each new pilot reinvents validation approach

---

## 2. Proposed Solution

### Dogfooding Patterns

SAP-027 provides a formalized dogfooding pilot methodology for validating patterns through internal use before ecosystem adoption.

Key capabilities: 4-phase pilot design (research, build, validate, decide), GO/NO-GO criteria framework (≥5x time savings, ≥85% satisfaction, 0 critical bugs, 2+ adoption cases), ROI analysis templates, metrics collection structure, pilot documentation patterns.

Setup time: 6-week pilot (expandable to 9 weeks), research at Week 0, build Weeks 1-3, validate Week 4, GO decision at Week 4, formalization at Week 5.

### Key Principles



- Internal validation first: Test patterns through dogfooding before ecosystem recommendation

- Quantified success criteria: GO/NO-GO thresholds based on time savings, satisfaction, quality

- Progressive validation: Week 4 GO decision (90% confidence) → Week 5 formalization (100% confidence)

- ROI transparency: Break-even analysis shows investment vs savings curve

- Documentation rigor: Weekly metrics + final summary provide reproducible methodology

- Template refinement: TODO completion makes artifacts production-ready before formalization



---

## 3. Scope

### In Scope



- 4-phase pilot framework (research week 0, build weeks 1-3, validate week 4, decide week 5)

- GO/NO-GO criteria (time savings ≥5x, satisfaction ≥85%, bugs = 0, adoption ≥2 cases)

- Metrics templates (time tracking, validation reports, satisfaction surveys)

- ROI analysis method (setup cost, per-use savings, break-even calculation)

- Pilot documentation structure (weekly logs, cross-comparison, final summary)

- TODO completion workflow (P0/P1/P2 prioritization, template refinement)



### Out of Scope



- A/B testing methodology - Different validation approach (comparative)

- User research beyond satisfaction surveys - Requires qualitative methods

- Ecosystem-wide rollout strategy - Covered by SAP-001 (Inbox Coordination)

- Automated pilot execution - Manual methodology, no automation tooling



---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Level 1):
- ✅ SAP-027 installed (5 artifacts present: capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger)
- ✅ First pilot completed using simplified 3-week workflow (skip discovery & research, focus on build + validate)
- ✅ GO/NO-GO decision made based on satisfaction ≥85% (simplified criteria, no time savings requirement)
- ✅ Pilot documentation created: pilot plan + GO/NO-GO decision document
- ✅ Time estimate: 3-4 hours setup + 3-week pilot (20-25 hours total)

**Adoption Success** (Level 2):
- ✅ All Level 1 criteria met
- ✅ Full 6-week pilot completed (Week -1 discovery + Week 0 research + Weeks 1-3 build + Week 4 validation)
- ✅ Evidence-based research conducted (≥30% Level A, ≥40% Level B, ≤30% Level C, 10+ total sources)
- ✅ Weighted candidate scoring used (evidence 40%, alignment 30%, demand 20%, feasibility 10%)
- ✅ GO decision achieved (composite score ≥60%, all hard gates passed: time_savings ≥5x, satisfaction ≥85%, bugs = 0, adoption ≥2)
- ✅ Integration with SAP-010 (A-MEM event logging), SAP-006 (vision promotion/demotion), SAP-015 (beads epic creation)
- ✅ Time estimate: 6-8 hours setup + 6-week pilot (25-50 hours total, depending on build complexity)

**Adoption Success** (Level 3):
- ✅ All Level 2 criteria met
- ✅ Multi-pilot infrastructure operational: pilot dashboard, automated vision sync, candidate scoring scripts
- ✅ 5+ pilots completed (2+ GO decisions, 1+ NO-GO with lessons learned documented)
- ✅ Average pilot setup time reduced to ≤2 hours (vs 6-8 hours at Level 2) via automation
- ✅ Vision document reflects pilot outcomes (Wave 1 promotions for GO, Wave 3 demotions for NO-GO)
- ✅ Beads backlog contains P1 epics for all GO decisions, with pilot metadata (satisfaction, time savings, bugs)
- ✅ Lessons learned notes created for all NO-GO decisions, with root causes and recommendations
- ✅ Time estimate: 12-16 hours one-time infrastructure setup, then 1-2 hours per subsequent pilot

### Key Metrics

| Metric | Baseline (No SAP-027) | Target (Level 2) | Target (Level 3) |
|--------|----------------------|------------------|------------------|
| **Pilot Setup Time** | Ad-hoc (8-12h) | 6-8h (structured) | 1-2h (automated) |
| **GO Decision Confidence** | 50% (gut feel) | 90% (evidence-based) | 95% (multi-pilot data) |
| **Pilot Success Rate** | 40% (2/5 pilots GO) | 60% (3/5 pilots GO) | 70% (7/10 pilots GO) |
| **Failed Pattern Cost** | 50h wasted (unvalidated) | 25h (early NO-GO Week 4) | 10h (Week -1 filtering) |
| **Vision Accuracy** | 50% (untested roadmap) | 80% (pilot-validated) | 90% (5+ pilots inform roadmap) |
| **Lessons Learned Coverage** | 0% (failures undocumented) | 100% (NO-GO → lessons note) | 100% + cross-pilot patterns |

---

## 5. Stakeholders

### Primary Stakeholders

**Dogfooding Patterns Owner**:
- **Owner**: Victor
- **Responsibilities**:
  - Maintain SAP artifacts and documentation
  - Review community feedback
  - Coordinate with related SAP owners
  
  - Coordinate with dependencies: SAP-000, SAP-029
  

**Primary Users**:
- **Product Managers**: Need structured methodology to validate features before roadmap commitment. Use Week -1 discovery scoring to select highest-ROI pilots from 20+ candidates.
- **Engineering Leads**: Need evidence-based GO/NO-GO criteria (not gut feel) to decide which patterns to adopt. Use composite scoring (time savings, satisfaction, bugs, adoption) to justify decisions.
- **AI Agents (Claude, other LLMs)**: Need clear workflows for pilot execution. Use awareness-guide.md decision tree to navigate 3 common workflows (discovery, GO decision, NO-GO decision).
- **Development Teams**: Need pilot templates to dogfood features efficiently. Use Level 1 (simplified) adoption for first pilot, upgrade to Level 2 after 2-3 pilots.
- **Technical Leaders**: Need metrics to track pilot program health. Use pilot dashboard (Level 3) to view active/completed pilots, GO/NO-GO trends, time savings ROI.

### Secondary Stakeholders

**Related SAP Maintainers**:

- **SAP-000 (SAP Framework)**: SAP-027 follows SAP-000 artifact structure (5 artifacts) and uses sap-evaluator.py for validation
- **SAP-010 (Memory System)**: SAP-027 requires A-MEM event logging (dogfooding.jsonl) for pilot metrics tracking and intention inventory for candidate selection
- **SAP-006 (Vision Synthesis)**: SAP-027 integrates with vision document to promote GO decisions to Wave 1, demote NO-GO to Wave 3
- **SAP-015 (Task Tracking)**: SAP-027 integrates with beads to create P1 epics for GO decisions, close tasks for NO-GO decisions



**Community**:
- chora-base adopters
- Ecosystem contributors
- External users

---

## 6. Dependencies

### Required SAP Dependencies

- **SAP-000 (SAP Framework)**: Provides artifact structure (5 files), validation tooling (sap-evaluator.py), and versioning conventions. SAP-027 must follow SAP-000 structure to be discoverable in sap-catalog.json.

- **SAP-010 (Memory System / A-MEM)**: Provides event logging (`.chora/memory/events/dogfooding.jsonl`) for pilot metrics tracking, intention inventory for Week -1 candidate selection, and knowledge notes for lessons learned. Without SAP-010, pilot metrics cannot be tracked systematically.

### Optional SAP Dependencies

- **SAP-006 (Vision Synthesis)**: Enables automatic vision document updates (Wave promotion/demotion) after GO/NO-GO decisions. Without SAP-006, vision updates must be done manually.

- **SAP-015 (Task Tracking / Beads)**: Enables automatic epic creation (GO decisions) and task closure (NO-GO decisions). Without SAP-015, backlog updates must be done manually in existing task tracker (Jira, Linear, GitHub Issues).

- **SAP-019 (Self-Evaluation)**: Enables validation of pilot SAP candidates before piloting. Use `sap-evaluator.py` to check artifact completeness (≥3 of 5 artifacts) before investing in full pilot.

- **SAP-016 (Link Validation)**: Enables validation of links in pilot documentation before GO decision. Ensures adoption blueprints and awareness guides have working cross-references.

### External Dependencies

**Required**:
- **Python 3.9+**: For A-MEM event logging (JSON), scoring scripts (candidate selection), and pilot dashboard (Level 3)
- **jq**: For A-MEM event querying and JSON parsing in validation commands
- **Bash 4.0+**: For pilot automation scripts (sync-to-vision.sh, pilot-dashboard.sh)
- **Git**: For version control of pilot documentation and A-MEM event logs

**Optional**:
- **just (command runner)**: For simplified pilot workflows (e.g., `just research "{query}"` for Week 0 research)
- **bd (beads CLI)**: For SAP-015 integration (epic creation, task management)
- **GitHub CLI (gh)**: For coordination requests (SAP-001 inbox) related to pilot outcomes

---

## 7. Constraints & Assumptions

### Constraints

1. **Time Investment Constraint**: Full pilot (Level 2) requires 25-50 hours over 6 weeks. Teams with <10h/week available should use Level 1 (simplified) instead.

2. **Minimum Adoption Requirement**: GO decisions require ≥2 adoption cases (projects/teams). Single-team pilots cannot achieve GO status, limiting applicability for solo developers.

3. **Evidence Availability Constraint**: Week 0 research requires ≥30% Level A evidence (standards, peer-reviewed). Cutting-edge patterns with no established evidence cannot meet research requirements, forcing Level 1 (skip research) adoption.

4. **Manual Metrics Collection**: Satisfaction surveys and time tracking are manual (not automated). Adds 30-60 minutes overhead per pilot Week 4 validation.

5. **Integration Dependency**: Vision promotion/demotion and epic creation require SAP-006 and SAP-015. Projects without these SAPs must handle vision/backlog updates manually.

### Assumptions

1. **Internal Dogfooding Feasibility**: Assumes teams can dogfood patterns internally before external rollout. Not applicable for patterns requiring external users (e.g., public API adoption).

2. **Quantifiable Metrics**: Assumes time savings, satisfaction, and bugs are measurable. Qualitative benefits (e.g., "improved code clarity") cannot be quantified for GO/NO-GO decision.

3. **Stable Evaluation Criteria**: Assumes GO/NO-GO thresholds (≥5x time savings, ≥85% satisfaction, 0 bugs) are appropriate across all pattern types. Some patterns may require adjusted criteria.

4. **Week 4 Decision Readiness**: Assumes 3 weeks build time is sufficient for meaningful validation. Complex patterns requiring >3 weeks build may need extended pilot timeline.

5. **A-MEM Event Logging Discipline**: Assumes teams will consistently log pilot events to `.chora/memory/events/dogfooding.jsonl`. Inconsistent logging prevents accurate metrics tracking.

6. **Intention Inventory Maintenance**: Assumes project maintains up-to-date intention inventory (SAP-010) with 10-20+ candidates. Without inventory, Week -1 discovery scoring cannot be performed.

---

## 8. Risks & Mitigations

### Risk 1: False Negatives (Good Patterns Rejected by NO-GO)

**Risk**: GO/NO-GO criteria are too strict (≥5x time savings, ≥85% satisfaction, 0 bugs). Valuable patterns that deliver 3x time savings or have 1 minor bug get rejected, missing adoption opportunities.

**Likelihood**: Medium (40% of pilots may fall in "gray zone" between GO and NO-GO)
**Impact**: High (Pattern rejection means 25-50 hours pilot investment wasted, plus opportunity cost of not adopting valuable pattern)

**Mitigation**:
- Use composite score (60% threshold) as primary decision, not just individual hard gates
- Document "near-miss" NO-GO decisions (e.g., 58% composite score) with recommendations for scope reduction and re-pilot
- Create P3 future tasks for NO-GO patterns that show promise (e.g., high satisfaction but low time savings suggests narrower scope pilot)
- Review GO/NO-GO thresholds quarterly based on 5+ pilot outcomes (adjust if <50% GO rate indicates overly strict criteria)

### Risk 2: Pilot Overhead Discourages Adoption

**Risk**: Level 2 full pilot requires 6-8 hours setup + 25-50 hours execution. Teams perceive overhead as too high, skip pilots entirely, return to ad-hoc validation with 40% failure rate.

**Likelihood**: Medium (50% of first-time adopters may abandon after seeing 6-8h setup estimate)
**Impact**: Medium (No pilots = 40% pattern failure rate = 20-50h wasted per failed pattern across ecosystem)

**Mitigation**:
- Promote Level 1 (simplified) as default entry point (3-4h setup vs 6-8h)
- Quantify ROI in adoption blueprint: "6-8h setup investment prevents 25-50h failed pilot cost" (5-10x ROI)
- Provide pilot plan templates (Level 1 template reduces setup to 1h via copy-paste)
- Create pilot dashboard (Level 3) showing cumulative time savings across all pilots (motivates continued investment)

### Risk 3: Inconsistent A-MEM Event Logging

**Risk**: Teams forget to log pilot events (`pilot_started`, `pilot_completed`, `pilot_go_decision`) to `.chora/memory/events/dogfooding.jsonl`. Week 4 evaluation lacks metrics data, forcing manual reconstruction (adds 1-2h overhead).

**Likelihood**: High (70% of first pilots miss ≥1 event due to unfamiliarity)
**Impact**: Low (1-2h manual metrics collection, but doesn't block GO/NO-GO decision)

**Mitigation**:
- Add event logging checklist to pilot plan template (Week 1: log `pilot_started`, Week 4: log `pilot_completed` + decision)
- Create pilot-init script (`scripts/pilot-init.sh`) that auto-logs `pilot_started` event when creating pilot directory
- Add validation command to Week 4 checklist: `grep "pilot_started" .chora/memory/events/dogfooding.jsonl` (catches missing events before evaluation)
- Provide fallback: Manual metrics documentation in `go-no-go-decision.md` if A-MEM events missing (no pilot blocked by logging failure)

---

## 9. Lifecycle

### Development Phase
**Status**: ⏳ **Planned**
**Target Completion**: [Date]

**Milestones**:
- [ ] SAP catalog entry created
- [ ] capability-charter.md (this document)
- [ ] protocol-spec.md (technical contracts)
- [ ] awareness-guide.md (AI agent guidance)
- [ ] adoption-blueprint.md (installation guide)
- [ ] ledger.md (adoption tracking)

### Pilot Phase
**Status**: ⏳ **Planned**
**Target Start**: [Date]
**Duration**: 1-2 weeks

**Activities**:
- Install SAP in 2-3 test projects
- Measure adoption time (target: documented estimates)
- Agent execution validation
- Collect feedback from early adopters
- Iterate on documentation

### Active Phase
**Status**: ⏳ **Planned**
**Target Start**: [Date]

**Ongoing Activities**:
- Quarterly reviews and updates
- Community feedback integration
- Ledger maintenance (adoption tracking)

- Integration with SAP-000, SAP-029


### Maintenance Phase

**Maintenance SLA**:
- Critical issues: 24-48 hours
- Major updates: 1-2 weeks
- Minor updates: Quarterly batch updates
- Documentation improvements: Ad-hoc

---

## 10. Related Documents

### Within chora-base

**SAP Artifacts**:
- [Protocol Specification](./protocol-spec.md) - Technical contracts for Dogfooding Patterns
- [Awareness Guide](./awareness-guide.md) - AI agent quick reference
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step installation
- [Traceability Ledger](./ledger.md) - Version history and adoption tracking

**Related SAPs**:
- [SAP-000: SAP Framework](../sap-framework/capability-charter.md) - Core SAP protocols


- [SAP-000: [Name]](../[directory]/capability-charter.md) - [Relationship]

- [SAP-029: [Name]](../[directory]/capability-charter.md) - [Relationship]



**SAP Catalog**:
- [sap-catalog.json](../../../sap-catalog.json) - Machine-readable SAP registry

### External Documentation

**Official Documentation**:
- [Wikipedia: Eating your own dog food](https://en.wikipedia.org/wiki/Eating_your_own_dog_food) - History and practice of dogfooding
- [Google Research: Dogfooding at Scale](https://research.google/pubs/pub43146/) - Large-scale internal product validation
- [Stage-Gate Process (Robert G. Cooper)](https://www.stage-gate.com/) - Product development gates with GO/KILL decisions
- [Oxford Centre for Evidence-Based Medicine Levels](https://www.cebm.ox.ac.uk/resources/levels-of-evidence) - Evidence quality pyramid (Level A/B/C)
- [Google's HEART Framework](https://www.dtelepathy.com/ux-metrics/#happiness) - Happiness, Engagement, Adoption, Retention, Task Success metrics

**Community Resources**:
- [Atlassian: Team Playbook - Pilot Programs](https://www.atlassian.com/team-playbook/plays/pilot-program) - Internal validation patterns
- [ProductPlan: How to Run a Product Pilot](https://www.productplan.com/glossary/product-pilot/) - Pilot program best practices
- [Amplitude: Product Waves Framework](https://amplitude.com/blog/product-roadmap) - Wave 1/2/3 strategic planning

---

## 11. Approval & Sign-Off

**Charter Author**: Victor
**Date**: 2025-11-03
**Version**: 1.0.0

**Approval Status**: ✅ **Approved**

**Review Cycle**:
- **Next Review**: [Date]
- **Review Frequency**: Quarterly

**Change Log**:
- 2025-11-03: Initial charter (1.0.0) - Victor

---

**Version History**:
- **1.0.0** (2025-11-03): Initial charter for Dogfooding Patterns