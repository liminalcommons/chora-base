# Roadmap - Example MCP Server

**Status:** Living document (updated with each release)
**Current Version:** 0.1.0

**See Also:**
- [Sprint Planning Guide](project-docs/sprints/README.md) - How to plan and track sprints
- [8-Phase Development Lifecycle](dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) - How to execute features
- [Process Metrics](project-docs/metrics/PROCESS_METRICS.md) - How to measure success

---

## How We Execute This Roadmap

### Sprint Planning

**Process:** [project-docs/sprints/README.md](project-docs/sprints/README.md)

- **Cadence:** 1-2 week sprints with clear goals
- **Capacity Planning:** Never commit >80% of available capacity
- **Tracking:** Velocity and burndown charts in sprint templates
- **Retrospectives:** End of each sprint to refine process

**Example Sprint:**
```
Sprint 2 (Nov 4-17, 2025)
Capacity: 20 hours available
Committed: 16 hours (80%)
  - Tool 2: Search capability (DDD: 3h, BDD: 2h, TDD: 6h) = 11h
  - Error handling improvements (investigation: 2h, implementation: 3h) = 5h
Reserved: 4 hours (20% buffer for unknowns)

Result: 86% velocity (delivered 16 of planned 16 hours)
```

### Development Process

**Complete Workflow:** [dev-docs/workflows/DEVELOPMENT_PROCESS.md](dev-docs/workflows/DEVELOPMENT_PROCESS.md)

- **DDD (Documentation-First):** Write docs before code → saves 8-15 hours of rework
- **BDD (Behavior-Driven):** Define acceptance criteria with Gherkin → prevents 2-5 acceptance issues
- **TDD (Test-Driven):** RED-GREEN-REFACTOR cycle → 40-80% fewer defects (Microsoft Research)

**Time Investment Per Feature:**
- DDD upfront: 3-5 hours
- BDD upfront: 2-4 hours
- TDD continuous: 40% of development time
- Total: 10-19 hours per feature (average 14 hours)

### Quality Gates

**Measured in:** [project-docs/metrics/PROCESS_METRICS.md](project-docs/metrics/PROCESS_METRICS.md)

- **Test Coverage:** ≥85% (enforced in CI/CD)
- **Process Adherence:** ≥90% workflow compliance
- **Defect Rate:** <3 defects per release
- **Sprint Velocity:** 80-90% of committed work delivered

---

## Current Focus

### v0.1.0 (Current) - Core Functionality

**Target:** 2025-11-15
**Status:** In Development (Sprint 2 of 4)

**Goal:** Establish core MCP server with essential tools and robust error handling

**Features:**

- [ ] **Core MCP Server** - Standard protocol implementation
  - [x] FastMCP integration (completed Sprint 1)
  - [x] Basic tool registration (completed Sprint 1)
  - [ ] Error handling framework (in progress Sprint 2)

- [ ] **Essential Tools** - 3-5 high-value tools
  - [x] Tool 1: List resources (Sprint 1 ✅)
    - DDD: 4h, BDD: 2h, TDD: 5h = 11h actual (12h estimated, 92% accuracy)
  - [ ] Tool 2: Search capability (Sprint 2 🔄)
    - DDD: complete (3h), BDD: in progress (2h estimated)
  - [ ] Tool 3: Create artifact (Sprint 3 planned)
    - DDD: not started (4h estimated)

- [ ] **Error Handling** - Robust error reporting and recovery
  - [ ] User-friendly error messages with suggestions (Sprint 2 🔄)
  - [ ] Graceful degradation for tool failures (Sprint 3 planned)

- [ ] **Documentation** - Complete project documentation
  - [x] AGENTS.md (Sprint 1 ✅)
  - [ ] README.md with usage examples (Sprint 4 planned)
  - [ ] 3 how-to guides (Sprint 4 planned)

- [ ] **Testing** - Comprehensive test coverage
  - [x] Unit tests for Tool 1 (Sprint 1 ✅, 92% coverage)
  - [ ] Unit tests for Tool 2 (Sprint 2 in progress)
  - [ ] Integration test suite (Sprint 4 planned)

**Sprint Breakdown:**

| Sprint | Dates | Capacity | Committed | Delivered | Velocity |
|--------|-------|----------|-----------|-----------|----------|
| Sprint 1 | Oct 21-Nov 3 | 14h | 12h (86%) | 12h | 100% ✅ |
| Sprint 2 | Nov 4-17 | 20h | 16h (80%) | _in progress_ | _TBD_ |
| Sprint 3 | Nov 18-Dec 1 | 18h | 14h (78%) | _planned_ | _TBD_ |
| Sprint 4 | Dec 2-15 | 16h | 12h (75%) | _planned_ | _TBD_ |

**Success Criteria:**
- [x] All 3 core tools implemented and tested (1/3 complete)
- [ ] Test coverage ≥85% (currently 92% for completed tools)
- [ ] Documentation complete (README, AGENTS.md, 3 how-tos)
- [ ] Zero high-severity bugs
- [ ] Process adherence ≥90% (currently 95% Sprint 1)

**Metrics (Sprint 1):**
- Velocity: 100% (delivered 12 of 12 committed hours)
- Process adherence: 95% (followed DDD→BDD→TDD for Tool 1)
- Defects: 0 production bugs, 2 caught in TDD (before PR)
- Coverage: 92% (exceeds 85% gate)

---

## Near-Term Roadmap

### v0.2.0 (Planned) - Enhanced Capabilities

**Target:** 2025-12-31
**Status:** Planning (backlog refinement starting Sprint 4)

**Goal:** Expand tool set and add performance optimizations

**Candidate Features:**
- **Advanced Search** - Filters, sorting, pagination
- **Batch Operations** - Process multiple resources at once
- **Caching Layer** - Improve performance for repeated queries
- **Extended Error Recovery** - Auto-retry with exponential backoff

**Planning Process:**
1. Review v0.1.0 metrics in Sprint 4 retrospective
   - Actual velocity vs. estimated (target: 80-90%)
   - Defect rate (target: <3 per release)
   - Process adherence (target: ≥90%)
2. Stakeholder feedback session (mid-December)
3. Capacity planning for Q1 2026
4. Sprint breakdown (estimated 4-6 sprints)

**Estimated Effort:** 48-72 hours (4-6 sprints @ 12-16h each)

---

## Long-Term Vision

### v0.3.0 (Vision) - Enterprise Features

**Target:** Q1 2026
**Status:** Exploratory (non-committed vision)

**Possible Directions:**
- **Multi-tenancy Support** - Isolate data per tenant
- **Advanced Monitoring** - Observability and alerting
- **Plugin System** - Community-contributed extensions
- **Performance Optimization** - Sub-100ms response times

**Decision Points:**
- After v0.2.0 metrics review
- Depends on user adoption and feedback
- Requires dedicated capacity planning session
- Subject to strategic priorities

**Strategic Questions:**
- Do we have 10+ active users requesting multi-tenancy?
- Is observability a top-3 pain point?
- Can we commit 80-120 hours for plugin system?

**See:** [dev-docs/vision/](dev-docs/vision/) for exploratory vision documents

---

## Roadmap Principles

### Commitment Levels

**Current (v0.1.0):**
- ✅ **Committed** - Features have sprint breakdown and capacity allocation
- ✅ **Success criteria defined** - Clear quality gates and metrics
- ✅ **Timeline set** - Target delivery date with confidence

**Planned (v0.2.0):**
- ⚠️ **Candidate features** - Subject to metrics review and feedback
- ⚠️ **Estimated effort** - Rough time ranges, not sprint breakdown
- ⚠️ **Flexible timeline** - Target quarter, may shift

**Vision (v0.3.0+):**
- 💭 **Exploratory** - Possible future directions
- 💭 **Non-committed** - Depends on adoption, feedback, capacity
- 💭 **Strategic questions** - Decision criteria not yet met

### How We Update This Roadmap

**Quarterly Reviews:**
- Review past sprint metrics (velocity, defects, adherence)
- Gather stakeholder feedback
- Refine candidate features based on learnings
- Promote planned → current or defer based on capacity

**Sprint Reviews:**
- Update current sprint status
- Adjust upcoming sprint plans based on velocity
- Document blockers and risks

**Ad-Hoc Updates:**
- Breaking changes or urgent features
- Significant scope changes
- Strategic pivots

---

## How to Use This Roadmap

### For AI Agents

**Finding Current Work:**
- Look at "Current Focus" section for v0.1.0 features
- Check sprint breakdown table for current sprint
- Use sprint planning templates in [project-docs/sprints/](project-docs/sprints/)

**Planning New Work:**
- Follow sprint planning guide for capacity allocation
- Use workflow time estimates (DDD: 3-5h, BDD: 2-4h, TDD: 40%)
- Never commit >80% of capacity
- Reference completed sprints for velocity benchmarks

**Tracking Progress:**
- Update sprint table with actual hours delivered
- Calculate velocity (delivered / committed)
- Update process metrics in [project-docs/metrics/](project-docs/metrics/)
- Document learnings in sprint retrospectives

### For Stakeholders

**Understanding Commitment:**
- **Current** = committed with sprint breakdown
- **Planned** = candidate features, subject to review
- **Vision** = exploratory, non-committed

**Tracking Delivery:**
- Check sprint table for current status
- Review success criteria progress
- See metrics for quality and velocity trends

**Requesting Features:**
- Submit as issue or proposal
- Will be evaluated in quarterly review
- Prioritized based on strategic fit, capacity, and adoption

### For Contributors

**Proposing Features:**
- See [dev-docs/CONTRIBUTING.md](dev-docs/CONTRIBUTING.md) for process
- Use sprint planning templates for effort estimation
- Follow DDD → BDD → TDD workflow for implementation

**Understanding Process:**
- Read [dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md](dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md)
- Check [dev-docs/ANTI_PATTERNS.md](dev-docs/ANTI_PATTERNS.md) for mistakes to avoid
- Reference [dev-docs/examples/FEATURE_WALKTHROUGH.md](dev-docs/examples/FEATURE_WALKTHROUGH.md) for real-world example

---

## Questions?

**Process:** See [dev-docs/workflows/](dev-docs/workflows/)
**Planning:** See [project-docs/sprints/](project-docs/sprints/)
**Contributing:** See [dev-docs/CONTRIBUTING.md](dev-docs/CONTRIBUTING.md)
**Project:** See [AGENTS.md](AGENTS.md)
