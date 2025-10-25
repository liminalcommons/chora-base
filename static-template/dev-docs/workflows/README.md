# Development Workflows

This directory contains the complete 8-phase development lifecycle for structured, evidence-based software development.

## Overview

**Philosophy:** Evidence-based development process that reduces defect rate by 40-80% (Microsoft Research, Google studies)

**Complete Lifecycle:**
1. **Vision & Strategy** → [ROADMAP.md](../../../ROADMAP.md)
2. **Planning** → [Sprint Planning](../../project-docs/sprints/README.md)
3. **Requirements & Design** → [DDD_WORKFLOW.md](DDD_WORKFLOW.md)
4. **Development** → [BDD_WORKFLOW.md](BDD_WORKFLOW.md) + [TDD_WORKFLOW.md](TDD_WORKFLOW.md)
5. **Testing & Quality** → Built into all workflows
6. **Review & Integration** → [AGENTS.md](../../../AGENTS.md) PR section
7. **Release & Deployment** → [Release Planning](../../project-docs/releases/RELEASE_PLANNING_GUIDE.md)
8. **Monitoring & Feedback** → [Process Metrics](../../project-docs/metrics/PROCESS_METRICS.md)

---

## Workflow Documents

### Core Process (5,115 lines total)

**End-to-End Guides:**
- **[DEVELOPMENT_PROCESS.md](DEVELOPMENT_PROCESS.md)** (1,108 lines) - Complete 8-phase lifecycle from Vision to Monitoring
- **[DEVELOPMENT_LIFECYCLE.md](DEVELOPMENT_LIFECYCLE.md)** (753 lines) - How DDD → BDD → TDD connect and integrate

**Individual Workflows:**
- **[DDD_WORKFLOW.md](DDD_WORKFLOW.md)** (919 lines) - Documentation Driven Design
  - Write docs first (saves 8-15 hours of rework per feature)
  - Time investment: 3-5 hours upfront
  - ROI: Prevents misalignment, enables parallel work

- **[BDD_WORKFLOW.md](BDD_WORKFLOW.md)** (1,148 lines) - Behavior Driven Development
  - Define acceptance criteria with Gherkin scenarios
  - Time investment: 2-4 hours per feature
  - ROI: Prevents 2-5 acceptance issues per feature

- **[TDD_WORKFLOW.md](TDD_WORKFLOW.md)** (1,187 lines) - Test Driven Development
  - RED-GREEN-REFACTOR cycle
  - Time investment: 40% of total development time
  - ROI: 40-80% fewer defects (Microsoft Research)

### Anti-Patterns

- **[../ANTI_PATTERNS.md](../ANTI_PATTERNS.md)** (1,309 lines) - Common mistakes and evidence-based solutions
  - Skip-docs-first anti-pattern (wastes 8-15 hours)
  - Skip-tests anti-pattern (40-80% more defects)
  - Overcommitment anti-pattern (burnout, missed deadlines)
  - 20+ documented patterns with real-world impact

---

## Quick Start for AI Agents

### Decision Trees

**Should I write docs first?**
→ **YES** (DDD saves 8-15 hours of rework)
- Exception: Trivial bug fixes (<30 min)

**Should I write acceptance tests first?**
→ **YES** (BDD prevents 2-5 acceptance issues)
- Exception: Infrastructure changes with no user-facing behavior

**Should I write unit tests first?**
→ **YES** (TDD reduces defects 40-80%)
- Exception: Throwaway prototypes, spikes

**How much to commit in sprint?**
→ **<80% of available capacity**
- Reserve 20% for unknowns, bugs, tech debt
- Target: 80-90% velocity (deliver what you commit)

### Time Estimates for Planning

**Per Feature (average):**
- DDD (Documentation): 3-5 hours
- BDD (Acceptance Tests): 2-4 hours
- TDD (Implementation): 4-8 hours (40% of total dev time)
- Review & Integration: 1-2 hours
- **Total:** 10-19 hours (average 14 hours per feature)

**Sprint Velocity:**
- Target: Deliver 80-90% of committed work
- Commitment: Never exceed 80% of available capacity
- Buffer: 20% reserved for unknowns

**Process Adherence:**
- Target: ≥90% workflow compliance
- Measured in: [../../project-docs/metrics/PROCESS_METRICS.md](../../project-docs/metrics/PROCESS_METRICS.md)
- Review: End of each sprint

---

## Related Documentation

**Examples:**
- [../examples/FEATURE_WALKTHROUGH.md](../examples/FEATURE_WALKTHROUGH.md) - OAuth2 complete walkthrough (14 days, 56 hours, real data)

**Project Management:**
- [../../project-docs/sprints/](../../project-docs/sprints/) - Sprint planning templates and guides
- [../../project-docs/releases/](../../project-docs/releases/) - Release planning and management
- [../../project-docs/metrics/](../../project-docs/metrics/) - Process KPIs and measurement

**Root Documentation:**
- [../../../ROADMAP.md](../../../ROADMAP.md) - Committed features and timelines
- [../../../AGENTS.md](../../../AGENTS.md) - Complete project guide for AI agents
- [../CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines

---

## How to Use These Workflows

### For AI Agents

1. **Before Starting Feature:**
   - Read [DEVELOPMENT_LIFECYCLE.md](DEVELOPMENT_LIFECYCLE.md) for overview
   - Check [../ANTI_PATTERNS.md](../ANTI_PATTERNS.md) for mistakes to avoid
   - Use decision trees above for quick answers

2. **During Feature Development:**
   - Follow DDD → BDD → TDD sequence
   - Reference individual workflow docs for details
   - Track time against estimates

3. **After Feature Completion:**
   - Update process metrics
   - Document learnings in knowledge base
   - Refine time estimates based on actuals

### For Human Developers

1. **Learning:** Start with [DEVELOPMENT_LIFECYCLE.md](DEVELOPMENT_LIFECYCLE.md)
2. **Reference:** Use individual workflow docs (DDD, BDD, TDD) as needed
3. **Planning:** Use time estimates for sprint planning
4. **Improvement:** Review [../ANTI_PATTERNS.md](../ANTI_PATTERNS.md) regularly

### For Teams

1. **Onboarding:** Require reading of DEVELOPMENT_LIFECYCLE.md
2. **Standards:** Enforce ≥90% workflow compliance
3. **Retrospectives:** Review process metrics each sprint
4. **Evolution:** Update workflows based on team learnings

---

## Evidence Base

These workflows are based on:

**Research:**
- Microsoft Research: "Realizing quality improvement through test driven development" (2008)
- Google: "Engineering Practices" internal studies
- IBM: "Maximizing ROI on Software Development" (2003)

**Real-World Validation:**
- OAuth2 Feature Walkthrough: 17 hours saved (27% efficiency gain)
- Sprint velocity tracking: 80-90% predictability with <80% commitment
- Defect tracking: 40-80% reduction with TDD

**Continuous Improvement:**
- Process metrics tracked in each project
- Retrospectives feed workflow refinements
- Evidence-based decision making

---

**Questions?** See [../../../AGENTS.md](../../../AGENTS.md) for project-specific guidance or [../CONTRIBUTING.md](../CONTRIBUTING.md) for how to propose workflow improvements.
