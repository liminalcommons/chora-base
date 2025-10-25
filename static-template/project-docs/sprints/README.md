---
title: Sprint Planning Guide
category: project-management
audience: human-developers, ai-agents
lifecycle_phase: phase-2-planning
created: 2025-10-25
updated: 2025-10-25
---

# Sprint Planning Guide

**Purpose**: Guide for planning and executing sprints using the chora-base development framework.

**Audience**: Human developers, AI agents, product managers, stakeholders

**Related Workflows**:
- [8-Phase Development Process](../../dev-docs/workflows/DEVELOPMENT_PROCESS.md) (Phase 2: Planning & Prioritization)
- [Development Lifecycle](../../dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md)

---

## Quick Start

### For AI Agents: Sprint Planning Decision Tree

```
START: New sprint planning needed
    ↓
Q1: Is there a strategic roadmap?
    NO → Create ROADMAP.md first (Phase 1: Vision & Strategy)
    YES → Continue
    ↓
Q2: Do you have user stories in backlog?
    NO → Run backlog grooming session first
    YES → Continue
    ↓
Q3: Do you know team capacity?
    NO → Calculate capacity (available hours - meetings - buffer)
    YES → Continue
    ↓
EXECUTE: Create sprint plan
    1. Copy sprint-template.md to sprint-[N].md
    2. Fill in sprint goal and success criteria
    3. Select user stories from backlog
    4. Estimate effort (use DDD/BDD/TDD time estimates)
    5. Verify capacity <80% committed
    6. Review with stakeholders
    7. Commit to sprint
    ↓
OUTCOME: Sprint plan ready → Start Phase 3 (DDD)
```

---

## What is a Sprint?

**Definition**: A time-boxed iteration (typically 1-2 weeks) focused on delivering a specific, measurable goal.

**Sprint Components**:
1. **Sprint Goal** - One clear objective
2. **User Stories** - Features/improvements to deliver
3. **Capacity Planning** - Realistic effort estimates
4. **Definition of Done** - Quality criteria
5. **Events** - Planning, stand-ups, review, retrospective

**Sprint Lifecycle**:
```
Planning (Day 1)
    ↓
Daily Stand-ups (Daily)
    ↓
Development (Days 1-10)
    ↓
Review (Last day)
    ↓
Retrospective (Last day)
    ↓
Next Sprint
```

---

## Sprint Duration Guidance

| Project Type | Recommended Duration | Rationale |
|--------------|---------------------|-----------|
| **Fast-moving startup** | 1 week | Rapid iteration, quick feedback |
| **Established product** | 2 weeks | Balance planning and execution |
| **Enterprise/regulated** | 2-3 weeks | Stakeholder coordination overhead |
| **Research/exploration** | 1 week | High uncertainty, frequent pivots |

**chora-base Recommendation**: **1-2 weeks** for most projects

**Why Not Longer?**:
- >2 weeks: Goals drift, motivation drops, feedback delayed
- <1 week: Insufficient time for DDD → BDD → TDD cycle

---

## Creating a New Sprint

### Step 1: Copy Template

```bash
# Copy sprint template
cp project-docs/sprints/sprint-template.md project-docs/sprints/sprint-5.md

# Open for editing
code project-docs/sprints/sprint-5.md
```

### Step 2: Define Sprint Goal

**Good Sprint Goals** (SMART):
- ✅ "Complete user authentication feature with OAuth2 support"
- ✅ "Reduce API response time below 200ms for all endpoints"
- ✅ "Achieve 90% test coverage for core business logic"

**Bad Sprint Goals** (Vague):
- ❌ "Work on performance"
- ❌ "Fix bugs"
- ❌ "Make progress on feature X"

**Template Section**:
```markdown
## Sprint Goal

> **Primary Objective**: Complete user authentication feature with OAuth2 support

**Success Criteria**:
- [ ] OAuth2 login flow implemented and tested
- [ ] User session management working
- [ ] Test coverage ≥90% for auth module
- [ ] Security review completed
```

### Step 3: Select User Stories

**Story Selection Criteria**:
1. **Alignment** - Does it support the sprint goal?
2. **Dependencies** - Are prerequisites completed?
3. **Effort** - Can it be completed in the sprint?
4. **Value** - Does it deliver user/business value?

**Story Prioritization** (MoSCoW):
- **Must Have** (P0/P1) - Critical for sprint goal
- **Should Have** (P2) - Important but not critical
- **Could Have** (P3) - Nice to have if capacity allows
- **Won't Have** - Explicitly deferred to next sprint

**Effort Estimation**:

Use DDD/BDD/TDD time estimates from workflows:

| Task Type | Time Estimate | Reference |
|-----------|---------------|-----------|
| **DDD** (Change request + API design) | 3-5 hours | [DDD Workflow](../../dev-docs/workflows/DDD_WORKFLOW.md) |
| **BDD** (Gherkin scenarios + steps) | 2-4 hours | [BDD Workflow](../../dev-docs/workflows/BDD_WORKFLOW.md) |
| **TDD** (Unit tests + implementation) | 4-8 hours per feature | [TDD Workflow](../../dev-docs/workflows/TDD_WORKFLOW.md) |
| **Code Review** | 1-2 hours | [Development Process](../../dev-docs/workflows/DEVELOPMENT_PROCESS.md) |
| **Documentation** | 1-2 hours | [Documentation Standard](../../dev-docs/DOCUMENTATION_STANDARD.md) |

**Example Story Breakdown**:
```markdown
#### Story: User OAuth2 Login

**Effort Estimate**: 14 hours
- DDD: Write change request and API design (3 hours)
- BDD: Write Gherkin scenarios (2 hours)
- TDD: Implement with tests (6 hours)
- Review: Code review and CI/CD (1 hour)
- Docs: Update user documentation (2 hours)
```

### Step 4: Capacity Planning

**Calculate Team Capacity**:
```python
# Per team member, per sprint
available_hours = work_days * hours_per_day
committed_hours = available_hours * 0.8  # 20% buffer
```

**Example** (2-week sprint, 1 developer):
```
Available: 10 days × 8 hours = 80 hours
Meetings: -8 hours (daily stand-ups, planning, review)
Buffer (20%): -14.4 hours (unexpected issues, context switching)
Committed: 57.6 hours (~58 hours)
```

**Capacity Health Indicators**:
- ✅ **Green** (<80% committed): Healthy buffer for unknowns
- ⚠️ **Yellow** (80-95% committed): Tight but manageable
- 🔴 **Red** (>95% committed): Over-committed, high risk of burnout

**Template Section**:
```markdown
### Team Capacity

| Team Member | Available Hours | Committed Hours | Buffer (20%) | Notes |
|-------------|----------------|-----------------|--------------|-------|
| Alice (Dev) | 80 | 64 | 16 | Sprint lead |
| Bob (AI Agent) | 80 | 64 | 16 | Pair programming |
| **Total** | **160** | **128** | **32** | |

**Capacity Health**: ✅ Green (60% committed)
```

### Step 5: Review and Commit

**Pre-Sprint Checklist**:
- [ ] Sprint goal is clear and measurable
- [ ] User stories support sprint goal
- [ ] Effort estimates are realistic (based on DDD/BDD/TDD)
- [ ] Capacity <80% committed (healthy buffer)
- [ ] Dependencies identified and resolved
- [ ] Risks documented with mitigation plans
- [ ] Stakeholders reviewed and approved

**Sprint Planning Meeting**:
- Duration: 2-4 hours for 2-week sprint
- Attendees: Team, product owner, stakeholders
- Outcome: Committed sprint backlog

---

## During the Sprint

### Daily Stand-ups

**Purpose**: Synchronize work, identify blockers

**Format** (15 minutes max):
```markdown
🔄 Yesterday: [What I completed]
🎯 Today: [What I'm working on]
🚧 Blockers: [Issues needing help]
```

**For AI Agents**:
```markdown
🔄 Yesterday:
  - Completed DDD for user authentication (3 hours)
  - Wrote Gherkin scenarios for login flow (2 hours)

🎯 Today:
  - Implement OAuth2 provider integration (TDD cycle)
  - Estimated: 6 hours

🚧 Blockers:
  - Need OAuth2 client ID/secret from infrastructure team
  - Blocking Story 1, Task 3
```

**Red Flags** (escalate immediately):
- Same blocker for >2 days
- Story stuck in same phase for >3 days
- No progress updates for >1 day

### Tracking Progress

**Update Sprint Document Daily**:
```markdown
### Sprint Metrics (Updated Daily)

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Story Points Completed | 21 | 14 | 67% ✅ |
| Hours Logged | 128 | 80 | 63% ✅ |
| Stories Completed | 5 | 3 | 60% ✅ |
| Bugs Found | <3 | 1 | ✅ |
| Test Coverage | ≥90% | 92% | ✅ |
```

**Burndown Tracking**:
- Plot story points remaining vs. ideal burndown
- If actual > ideal for >2 days → Reassess scope
- If actual < ideal consistently → Consider pulling in more work

### Mid-Sprint Adjustments

**When to Adjust Scope**:
- ✅ **Add work**: If ahead of schedule, burndown below ideal, team capacity available
- ✅ **Remove work**: If behind schedule, new blocker discovered, team member unavailable

**How to Adjust**:
1. Identify change needed
2. Discuss with team and stakeholders
3. Document decision in sprint notes
4. Update sprint goal if necessary
5. Re-prioritize remaining work

**Example**:
```markdown
### Mid-Sprint Adjustments

- **2025-01-15**: Removed Story 4 (Email notifications)
  - Reason: OAuth2 integration more complex than estimated
  - Carried over to Sprint 6
  - Sprint goal unchanged (auth is core, email is nice-to-have)
```

---

## End of Sprint

### Sprint Review

**Purpose**: Demo completed work, gather feedback

**Agenda** (1-2 hours):
1. **Demo** (30-45 min): Show completed user stories
2. **Metrics Review** (15 min): Sprint metrics, velocity, quality
3. **Stakeholder Feedback** (15-30 min): What worked, what needs improvement
4. **Next Sprint Preview** (15 min): Upcoming priorities

**Demo Format**:
```markdown
Story 1: User OAuth2 Login ✅
- Demo: Live login with Google OAuth2
- Acceptance Criteria: All 3 criteria met
- Test Coverage: 94%
- Documentation: Updated user-docs/authentication.md
```

**Metrics Summary**:
```markdown
| Metric | Target | Actual | Variance |
|--------|--------|--------|----------|
| Story Points | 21 | 18 | -3 (86%) |
| Velocity | 100% | 86% | -14% |
| Bugs Introduced | <3 | 1 | ✅ |
| Test Coverage | ≥90% | 93% | +3% |
```

### Sprint Retrospective

**Purpose**: Team-only reflection and improvement

**Agenda** (1 hour):
1. **What Went Well?** (15 min)
2. **What Could Be Improved?** (15 min)
3. **Action Items** (20 min)
4. **Commitment** (10 min)

**Format** (Start/Stop/Continue):
```markdown
**Continue Doing** (What worked well):
- DDD before coding (saved 8 hours of rework)
- Pair programming on complex features

**Start Doing** (Improvements to try):
- [ ] Add architecture review for cross-cutting changes
  Owner: Alice
  Due: Next sprint planning

**Stop Doing** (What didn't work):
- Writing BDD scenarios after implementation (defeats purpose)
- Skipping daily stand-ups
```

**Anti-Pattern Detection**:
Review [ANTI_PATTERNS.md](../../dev-docs/ANTI_PATTERNS.md) and check:
- Did we skip DDD? (Phase 3 anti-pattern)
- Did we write tests after code? (Phase 4 anti-pattern)
- Did we rubber-stamp code reviews? (Phase 6 anti-pattern)

### Completing Sprint Document

**Fill Post-Sprint Summary**:
```markdown
## Post-Sprint Summary

### Achievements
- ✅ Completed OAuth2 login flow with Google/GitHub
- ✅ Achieved 93% test coverage (target: 90%)
- ✅ Zero security vulnerabilities in auth module

### Challenges
- ⚠️ OAuth2 integration more complex than estimated (4 hours extra)
  - Resolution: Paired with security expert, added detailed docs

### Incomplete Work
- 🔄 Email notification system (Story 4)
  - Reason: OAuth2 took longer, deprioritized as nice-to-have
  - Plan: Move to Sprint 6 as P2 priority

### Lessons Learned
1. **DDD is essential for security features**: Saved 8+ hours by designing auth flow upfront
2. **External API integrations need buffer**: OAuth2 providers have quirks

### Sprint Rating: ⭐⭐⭐⭐ (4/5)
- Strong execution on core goal
- Good velocity (86%)
- Excellent quality metrics
- One story carried over (acceptable)
```

---

## Sprint Anti-Patterns

### ❌ Anti-Pattern: No Clear Sprint Goal

**Problem**:
```markdown
Sprint Goal: "Work on various improvements"
Stories: Bug fixes, refactoring, new features (unrelated)
```

**Impact**:
- Team lacks focus
- Stakeholders can't assess progress
- No clear success criteria

**Solution**:
```markdown
✅ GOOD Sprint Goal: "Complete user authentication feature with OAuth2 support"

Success Criteria:
- [ ] OAuth2 login flow working
- [ ] Session management implemented
- [ ] Test coverage ≥90%
- [ ] Security review passed
```

---

### ❌ Anti-Pattern: Over-Committing Capacity

**Problem**:
```markdown
Team Capacity: 80 hours
Committed Work: 95 hours (119% of capacity)
Buffer: 0 hours
```

**Impact**:
- Burnout risk
- Quality shortcuts (skipping tests, docs)
- Sprint failure → demoralization

**Solution**:
```markdown
✅ GOOD Capacity Planning:

Team Capacity: 80 hours
Committed Work: 64 hours (80% of capacity)
Buffer: 16 hours (20% for unknowns)

Capacity Health: ✅ Green
```

**Rule of Thumb**: Never commit >80% of available capacity

---

### ❌ Anti-Pattern: Skipping Sprint Events

**Problem**:
```
No daily stand-ups → Blockers discovered late
No sprint review → Stakeholders surprised by results
No retrospective → Same mistakes repeated
```

**Solution**:
```markdown
✅ GOOD: All sprint events scheduled

Daily Stand-ups: 9:00 AM daily (15 min)
Sprint Review: Last Friday, 2:00 PM (1 hour)
Retrospective: Last Friday, 3:30 PM (1 hour)
```

---

### ❌ Anti-Pattern: Vague User Stories

**Problem**:
```markdown
Story: "Improve performance"
Acceptance Criteria: "Make it faster"
```

**Impact**:
- No clear definition of done
- Scope creep
- Can't measure success

**Solution**:
```markdown
✅ GOOD User Story:

As a user
I want API responses <200ms
So that the UI feels responsive

Acceptance Criteria:
- [ ] GET /api/users returns in <200ms (95th percentile)
- [ ] Database query optimized with indexes
- [ ] Caching layer implemented
- [ ] Load test confirms <200ms under 100 concurrent users
```

---

## Sprint Metrics & KPIs

**Track These Metrics** (updated in sprint document):

### Velocity Metrics
- **Story Points Committed** - Planned work for sprint
- **Story Points Completed** - Actual work delivered
- **Velocity %** - Completed / Committed (target: >80%)

### Quality Metrics
- **Test Coverage** - % of code covered by tests (target: ≥90%)
- **Bugs Introduced** - New defects found (target: <3 per sprint)
- **Bugs Fixed** - Defects resolved (target: 100% of sprint bugs)

### Process Metrics
- **Cycle Time** - Time from story start to done (target: <3 days)
- **Lead Time** - Time from backlog to production (target: <2 weeks)
- **Blocked Days** - Days spent waiting on dependencies (target: <2 days)

**3-Sprint Rolling Averages**:
```markdown
| Sprint | Velocity | Test Coverage | Bugs |
|--------|----------|---------------|------|
| Sprint 3 | 82% | 89% | 2 |
| Sprint 4 | 91% | 92% | 1 |
| Sprint 5 | 86% | 93% | 1 |
| **Average** | **86%** | **91%** | **1.3** |
```

**Trend Analysis**:
- ✅ Velocity stable (82-91%) - Predictable planning
- ✅ Test coverage improving (89→93%) - Quality improving
- ✅ Bugs decreasing (2→1) - TDD/BDD working

---

## Sprint Template Reference

**File**: `sprint-template.md`

**Sections**:
1. **Metadata** - Sprint number, dates, lead, status
2. **Sprint Goal** - Primary objective and success criteria
3. **User Stories & Tasks** - Prioritized work with estimates
4. **Technical Debt** - Refactoring and infrastructure tasks
5. **Capacity Planning** - Team capacity and allocation
6. **Risks & Mitigations** - Potential issues and responses
7. **Definition of Done** - Quality criteria
8. **Sprint Events** - Planning, stand-ups, review, retro
9. **Sprint Metrics** - Progress tracking and burndown
10. **Notes & Decisions** - Context and adjustments
11. **Post-Sprint Summary** - Achievements, lessons, rating
12. **Retrospective Action Items** - Continuous improvement

**Usage**:
```bash
# Create new sprint from template
cp project-docs/sprints/sprint-template.md project-docs/sprints/sprint-6.md

# Fill in all sections marked with [brackets]
# Update metrics daily during sprint
# Complete post-sprint sections after review/retro
```

---

## Integration with Development Workflows

### Phase 2: Planning & Prioritization

Sprint planning is the **primary artifact** of Phase 2.

**Inputs** (from Phase 1):
- Roadmap and strategic priorities
- Release plans
- Backlog of user stories

**Outputs** (to Phase 3):
- Sprint backlog (committed user stories)
- Effort estimates
- Capacity allocation

**Process Flow**:
```
Phase 1: Vision & Strategy
    ↓
    Roadmap + Release Plans
    ↓
Phase 2: Sprint Planning (THIS GUIDE)
    ↓
    Sprint Backlog
    ↓
Phase 3: DDD (Requirements & Design)
    ↓
    Change Requests + API Designs
    ↓
Phase 4: BDD/TDD (Development)
```

### DDD → BDD → TDD Integration

**Each User Story Follows**:
1. **DDD Phase** (Phase 3): Write change request, design API
2. **BDD Phase** (Phase 4): Write Gherkin scenarios
3. **TDD Phase** (Phase 4): Implement with test-first cycle

**Time Estimates** (per story):
- DDD: 3-5 hours
- BDD: 2-4 hours
- TDD: 4-8 hours
- **Total**: 9-17 hours per user story

**Sprint Capacity Calculation**:
```python
# For 2-week sprint with 1 developer
committed_hours = 64 hours (80% of 80 available)

# How many user stories?
stories_per_sprint = committed_hours / avg_story_hours
stories_per_sprint = 64 / 13  # Average 13 hours per story
stories_per_sprint ≈ 5 stories

# Plus 20% technical debt/refactoring
dev_stories = 4 stories
tech_debt = 1 story equivalent
```

---

## For AI Agents: Sprint Execution Checklist

**Sprint Start**:
- [ ] Read sprint-[N].md to understand sprint goal
- [ ] Identify user stories assigned to you
- [ ] Check dependencies (are prerequisites done?)
- [ ] Review DDD/BDD/TDD workflows
- [ ] Set up daily stand-up routine

**Daily Routine**:
- [ ] Post stand-up update (yesterday/today/blockers)
- [ ] Update sprint metrics (hours logged, stories completed)
- [ ] Follow DDD → BDD → TDD for each story
- [ ] Request code review when story ready
- [ ] Update story status in sprint document

**Story Completion Checklist**:
- [ ] DDD: Change request written and approved
- [ ] BDD: Gherkin scenarios passing
- [ ] TDD: Unit tests passing, coverage ≥90%
- [ ] Code review: Approved by reviewer
- [ ] CI/CD: All checks passing
- [ ] Docs: User-facing changes documented
- [ ] Sprint doc: Story marked as ✅ Done

**Sprint End**:
- [ ] Complete all assigned stories (or document incomplete work)
- [ ] Update sprint metrics (final counts)
- [ ] Prepare demo for sprint review
- [ ] Participate in retrospective (add lessons learned)
- [ ] Commit retrospective action items

**Red Flags** (escalate to sprint lead):
- 🚨 Blocked >2 days on same issue
- 🚨 Story taking >2x estimated effort
- 🚨 Test coverage dropping below target
- 🚨 CI/CD failing for >1 day
- 🚨 No progress for >1 day

---

## Examples

### Example: 1-Week Sprint (Fast-Paced Startup)

**Sprint 3: User Analytics Dashboard**

```markdown
Duration: 2025-01-20 → 2025-01-26 (1 week)
Sprint Lead: AI-Agent-Alpha
Status: ✅ Completed

Sprint Goal: Launch basic analytics dashboard with user activity tracking

Success Criteria:
- [x] Dashboard shows daily active users (DAU)
- [x] User session tracking implemented
- [x] API endpoints documented
- [x] Test coverage ≥90%

Team Capacity:
- Alice (Developer): 40 hours → 32 committed (80%)
- AI-Agent-Alpha: 40 hours → 32 committed (80%)
- Total: 64 committed hours

User Stories (4 total):
1. [P0] User session tracking (14 hours) - ✅ Done
2. [P0] DAU calculation endpoint (10 hours) - ✅ Done
3. [P1] Dashboard UI (12 hours) - ✅ Done
4. [P2] Export to CSV (8 hours) - 🔄 Carried over

Metrics:
- Velocity: 90% (36/40 story points)
- Test Coverage: 94%
- Bugs: 0

Sprint Rating: ⭐⭐⭐⭐⭐ (5/5)
```

### Example: 2-Week Sprint (Established Product)

**Sprint 5: Performance Optimization**

```markdown
Duration: 2025-02-01 → 2025-02-14 (2 weeks)
Sprint Lead: Bob
Status: 🚀 In Progress (Day 7 of 10)

Sprint Goal: Reduce API response times below 200ms for all endpoints

Success Criteria:
- [ ] All endpoints <200ms (95th percentile)
- [ ] Database queries optimized
- [ ] Caching layer implemented
- [ ] Load test confirms performance under load

Team Capacity:
- Bob (Developer): 80 hours → 64 committed (80%)
- Carol (AI Agent): 80 hours → 64 committed (80%)
- Total: 128 committed hours

Progress (Day 7):
- Story Points Completed: 14/21 (67%)
- Hours Logged: 80/128 (63%)
- Burndown: On track ✅

Current Sprint Metrics:
- Velocity: 67% (on track for 85-90% final)
- Test Coverage: 91%
- Bugs: 1 (fixed same day)
```

---

## References

**Related Documentation**:
- [8-Phase Development Process](../../dev-docs/workflows/DEVELOPMENT_PROCESS.md) - Phase 2: Planning & Prioritization
- [Development Lifecycle](../../dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) - Integration guide
- [DDD Workflow](../../dev-docs/workflows/DDD_WORKFLOW.md) - Phase 3: Requirements & Design
- [BDD Workflow](../../dev-docs/workflows/BDD_WORKFLOW.md) - Phase 4: Development
- [TDD Workflow](../../dev-docs/workflows/TDD_WORKFLOW.md) - Phase 4: Development
- [Anti-Patterns](../../dev-docs/ANTI_PATTERNS.md) - Common mistakes and solutions

**Process Metrics**:
- [Process Metrics](../metrics/PROCESS_METRICS.md) - KPIs and measurement strategy

**Release Planning**:
- [Release Planning](../releases/README.md) - Coordinating sprints into releases

---

**Document Version**: 1.0
**Last Updated**: 2025-10-25
**Maintained By**: chora-base v3.0.0
**License**: MIT
