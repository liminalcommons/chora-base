# Development Examples

This directory contains complete feature development walkthroughs following the 8-phase development lifecycle.

## Purpose

**Goal:** Demonstrate real-world application of chora-base workflows with actual time data, metrics, and outcomes.

**What You'll Find:**
- Complete feature implementations from start to finish
- Actual time spent (not just estimates)
- Real defects found and when
- ROI calculations and efficiency gains
- Lessons learned and what to do differently

---

## Available Examples

### [FEATURE_WALKTHROUGH.md](FEATURE_WALKTHROUGH.md) - OAuth2 Authentication Implementation

**Scope:** Add OAuth2 authentication to MCP server
**Duration:** 14 days (56 hours total) across all 8 phases
**Team:** 1 developer
**Outcome:** Production-ready feature with 95% test coverage, zero production bugs

#### Phases Covered

1. **Vision & Strategy** (4 hours)
   - Business justification and strategic fit
   - Stakeholder alignment
   - Success criteria definition

2. **Planning** (8 hours)
   - Sprint planning with capacity allocation
   - Task breakdown and estimation
   - Dependency identification

3. **Requirements & Design** (12 hours)
   - DDD: Complete documentation first
   - API design and data models
   - Integration points identified

4. **Development** (16 hours)
   - BDD: Acceptance tests with Gherkin scenarios
   - TDD: Test-driven implementation
   - RED-GREEN-REFACTOR cycles

5. **Testing & Quality** (8 hours)
   - Integration test suite
   - Coverage validation (achieved 95%)
   - Security testing

6. **Review & Integration** (4 hours)
   - PR review with feedback cycles
   - CI/CD pipeline execution
   - Merge to main branch

7. **Release & Deployment** (2 hours)
   - Release candidate testing
   - Production deployment
   - Rollback plan validation

8. **Monitoring & Feedback** (2 hours)
   - Metrics collection
   - Post-mortem analysis
   - Process improvements identified

#### Key Learnings

**What Worked Well:**
- **DDD upfront saved 10 hours** - Writing docs first prevented 2 major rework cycles
- **BDD prevented 3 acceptance issues** - Gherkin scenarios caught misalignments early
- **TDD caught 5 bugs before PR** - Unit tests found issues during development (40% defect reduction)

**Challenges:**
- OAuth2 provider integration took 3 hours longer than estimated (poor external API docs)
- Security testing revealed token expiration edge case (caught in phase 5, not production)

**Total ROI:**
- **17 hours saved** vs. ad-hoc approach (27% efficiency gain)
- **Zero production bugs** in first 3 months
- **95% test coverage** maintained

**What We'd Do Differently:**
- Allocate more buffer for external API integration (20% → 30%)
- Add security testing earlier (phase 4 instead of phase 5)
- Include token refresh scenario in initial BDD scenarios

---

## How to Use These Examples

### For AI Agents

**Before Starting Similar Work:**
1. Read the example to understand the full lifecycle
2. Use time estimates as baseline for planning
3. Check for similar patterns/challenges
4. Adapt decision trees to your context

**During Development:**
1. Reference specific phase sections as you work
2. Compare your progress to example timelines
3. Look for similar challenges and solutions
4. Track your own time for future estimates

**After Completion:**
1. Compare actual vs. estimated time
2. Calculate your own ROI
3. Document your learnings
4. Consider creating your own walkthrough

### For Human Developers

**Learning:**
- Understand real-world application of workflows
- See evidence-based results (time savings, defect reduction)
- Learn from both successes and mistakes

**Planning:**
- Use time estimates for sprint planning
- Understand where buffer is needed
- Identify risk areas (external dependencies, security)

**Improvement:**
- Adapt patterns to your context
- Share your own walkthroughs
- Contribute learnings back to team

---

## Creating New Walkthrough Examples

When creating a new feature walkthrough, use this template:

### Required Sections

1. **Header**
   - Feature description and scope
   - Duration (calendar days and total hours)
   - Team size and composition
   - Outcome summary

2. **All 8 Phases**
   - Actual time spent (not just estimates)
   - Key activities and deliverables
   - Decisions made and rationale
   - Challenges encountered

3. **Key Learnings**
   - What worked well
   - What didn't work
   - What you'd do differently
   - Evidence (metrics, defects, time saved)

4. **ROI Calculation**
   - Time saved vs. alternative approach
   - Defects prevented
   - Quality improvements
   - Efficiency gains

### Include Real Data

**Time Tracking:**
- Actual hours spent (not estimates)
- Breakdown by phase
- Comparison to initial estimates
- Where time was saved/lost

**Defects:**
- How many found and when
- How many prevented by which practice
- Production bugs (if any)
- Cost of defects (time to fix)

**Quality Metrics:**
- Test coverage achieved
- Code review feedback cycles
- CI/CD pipeline results
- Production stability (first 3 months)

### Show Both Success and Failures

**Don't just document success:**
- Include what didn't work
- Show estimation errors
- Document rework cycles
- Share mistakes and learnings

**Be honest about ROI:**
- Calculate both time saved and time invested
- Show when workflows didn't help
- Identify contexts where to deviate
- Update time estimates based on actuals

---

## Example Template

```markdown
# Feature: [Name] - Complete Walkthrough

**Scope:** [1-2 sentence description]
**Duration:** [X days] ([Y hours total])
**Team:** [Size and roles]
**Outcome:** [Production result with metrics]

---

## Phase 1: Vision & Strategy ([X hours])

**Goal:** [What we wanted to achieve]

**Activities:**
- [Actual activities performed]

**Deliverables:**
- [What we created]

**Time:** [Estimated X hours, Actual Y hours, Variance Z%]

**Learnings:** [What worked, what didn't]

---

[Repeat for all 8 phases]

---

## Key Learnings

**What Worked:**
- [Specific practices with quantified impact]

**Challenges:**
- [Issues encountered with solutions]

**ROI Analysis:**
- Time invested: [X hours]
- Time saved: [Y hours]
- Net gain: [Z hours] ([%] efficiency gain)
- Defects prevented: [N]
- Quality achieved: [coverage %, uptime %, etc.]

**Recommendations:**
- [What to do next time]
```

---

## Contributing Walkthroughs

We encourage teams to contribute their own feature walkthroughs:

1. **Use the template above**
2. **Include real data** (anonymize if needed)
3. **Be honest** about what didn't work
4. **Calculate ROI** with evidence
5. **Submit PR** with your walkthrough

**Benefits of Contributing:**
- Help other teams learn from your experience
- Improve workflow documentation
- Refine time estimates
- Build collective knowledge

---

## Related Documentation

**Workflows:**
- [../workflows/](../workflows/) - Complete process documentation
- [../workflows/DEVELOPMENT_LIFECYCLE.md](../workflows/DEVELOPMENT_LIFECYCLE.md) - How phases connect

**Anti-Patterns:**
- [../ANTI_PATTERNS.md](../ANTI_PATTERNS.md) - Common mistakes to avoid

**Project Management:**
- [../../project-docs/sprints/](../../project-docs/sprints/) - Sprint planning
- [../../project-docs/releases/](../../project-docs/releases/) - Release management
- [../../project-docs/metrics/](../../project-docs/metrics/) - Process metrics

**Root Documentation:**
- [../../../ROADMAP.md](../../../ROADMAP.md) - Project roadmap
- [../../../AGENTS.md](../../../AGENTS.md) - Complete project guide

---

**Questions?** Open an issue or see [../CONTRIBUTING.md](../CONTRIBUTING.md) for how to contribute your own walkthroughs.
