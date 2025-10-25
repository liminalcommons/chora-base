---
sprint_number: [Number]
start_date: YYYY-MM-DD
end_date: YYYY-MM-DD
sprint_lead: [Name/Agent ID]
status: planning | in_progress | completed
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Sprint [Number]: [Sprint Name]

**Duration**: [Start Date] → [End Date] ([N] weeks)
**Sprint Lead**: [Name/Agent ID]
**Status**: 🎯 Planning | 🚀 In Progress | ✅ Completed

---

## Sprint Goal

> **Primary Objective**: [One clear, measurable goal for this sprint]

**Success Criteria**:
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

**Alignment**:
- **Roadmap Phase**: [Phase from Vision & Strategy]
- **Release Target**: [vX.Y.Z]
- **Strategic Theme**: [e.g., "Performance Optimization", "User Experience Enhancement"]

---

## User Stories & Tasks

### High Priority (Must Have)

#### Story 1: [User Story Title]

**As a** [user type]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria**:
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]

**Tasks**:
- [ ] **DDD**: Write change request and API design (2 hours) - [Assignee]
- [ ] **BDD**: Write Gherkin scenarios (1 hour) - [Assignee]
- [ ] **TDD**: Implement with tests (4 hours) - [Assignee]
- [ ] **Review**: Code review and CI/CD (1 hour) - [Assignee]
- [ ] **Docs**: Update user documentation (1 hour) - [Assignee]

**Effort Estimate**: [N] hours
**Priority**: P0 (Blocker) | P1 (High) | P2 (Medium) | P3 (Low)
**Status**: 📝 Not Started | 🚧 In Progress | ✅ Done | ❌ Blocked

**Dependencies**:
- Depends on: [Story ID or external dependency]
- Blocks: [Story ID]

**Notes**:
[Additional context, design decisions, or important considerations]

---

#### Story 2: [User Story Title]

[Repeat structure above for each high-priority story]

---

### Medium Priority (Should Have)

#### Story 3: [User Story Title]

[Same structure as above]

---

### Low Priority (Nice to Have)

#### Story 4: [User Story Title]

[Same structure as above]

---

## Technical Debt & Improvements

### Refactoring Tasks

- [ ] **[Task Title]** - [Description] (Effort: [N] hours) - [Assignee]
  - **Why**: [Technical debt or improvement rationale]
  - **Impact**: [Performance, maintainability, etc.]

### Infrastructure Tasks

- [ ] **[Task Title]** - [Description] (Effort: [N] hours) - [Assignee]
  - **Why**: [Infrastructure improvement rationale]
  - **Impact**: [Deployment, CI/CD, monitoring, etc.]

---

## Capacity Planning

### Team Capacity

| Team Member | Available Hours | Committed Hours | Buffer (20%) | Notes |
|-------------|----------------|-----------------|--------------|-------|
| [Name/Agent] | 40 | 32 | 8 | [e.g., "On-call rotation"] |
| [Name/Agent] | 40 | 32 | 8 | [e.g., "Half-day meetings"] |
| **Total** | **80** | **64** | **16** | |

**Velocity**: [N] story points (based on last 3 sprints average)

### Story Point Allocation

| Priority | Story Points | Hours Estimate | % of Capacity |
|----------|--------------|----------------|---------------|
| High (Must Have) | [N] | [N] | [N]% |
| Medium (Should Have) | [N] | [N] | [N]% |
| Low (Nice to Have) | [N] | [N] | [N]% |
| Technical Debt | [N] | [N] | [N]% |
| **Total** | **[N]** | **[N]** | **[N]%** |

**Capacity Health**:
- ✅ Green: <80% committed (healthy buffer)
- ⚠️ Yellow: 80-95% committed (tight but manageable)
- 🔴 Red: >95% committed (over-committed, risk of burnout)

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation Strategy | Owner |
|------|--------|-------------|---------------------|-------|
| [Risk description] | High/Medium/Low | High/Medium/Low | [How to mitigate] | [Name] |
| [External dependency delay] | High | Medium | [Parallel work, backup plan] | [Name] |
| [Technical complexity unknown] | Medium | High | [Spike/POC first, expert consultation] | [Name] |

---

## Definition of Done

Sprint is considered complete when:

**Code Quality**:
- [ ] All user stories meet acceptance criteria
- [ ] Code review approved by [N] reviewers
- [ ] Test coverage ≥ [N]% (unit + integration)
- [ ] All CI/CD checks passing (linting, type checking, tests)
- [ ] No P0/P1 bugs introduced

**Documentation**:
- [ ] User-facing features documented in user-docs/
- [ ] API changes documented in dev-docs/reference/
- [ ] CHANGELOG.md updated
- [ ] README.md updated if needed

**Testing**:
- [ ] BDD scenarios written and passing
- [ ] Unit tests written (TDD cycle)
- [ ] Integration tests passing
- [ ] Manual testing completed for UI changes

**Deployment**:
- [ ] Changes merged to main branch
- [ ] Release notes drafted (if applicable)
- [ ] Deployment plan reviewed (if production release)

**Sign-off**:
- [ ] Sprint review conducted with stakeholders
- [ ] Demo completed (if applicable)
- [ ] Retrospective scheduled

---

## Sprint Events

### Sprint Planning
**Date**: [YYYY-MM-DD]
**Duration**: [N] hours
**Attendees**: [List]

**Outcomes**:
- Sprint goal agreed
- User stories estimated and committed
- Capacity confirmed

### Daily Stand-ups
**Schedule**: [Time] daily
**Format**: What I did, what I'm doing, blockers

**Stand-up Template**:
```
🔄 Yesterday: [Completed tasks]
🎯 Today: [Planned tasks]
🚧 Blockers: [Issues needing help]
```

### Sprint Review
**Date**: [YYYY-MM-DD]
**Duration**: [N] hours
**Attendees**: [List]

**Agenda**:
1. Demo completed user stories
2. Review sprint metrics
3. Gather stakeholder feedback
4. Discuss next sprint priorities

### Sprint Retrospective
**Date**: [YYYY-MM-DD]
**Duration**: [N] hours
**Attendees**: [Team only]

**Agenda**:
1. What went well?
2. What could be improved?
3. Action items for next sprint

---

## Sprint Metrics (Updated Daily)

### Progress Tracking

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| **Story Points Completed** | [N] | [N] | [%] |
| **Hours Logged** | [N] | [N] | [%] |
| **Stories Completed** | [N] | [N] | [%] |
| **Bugs Found** | <[N] | [N] | ✅/⚠️/🔴 |
| **Bugs Fixed** | [N] | [N] | [%] |
| **Test Coverage** | ≥[N]% | [N]% | ✅/⚠️/🔴 |

### Burndown Chart (Manual Update)

```
Story Points Remaining
[N] │ ●
    │  ╲
    │   ●
    │    ╲
    │     ●
    │      ╲
  0 └───────●
    Day 1  Day 5  Day 10

    ● Actual    ╲ Ideal
```

### Velocity Trend

| Sprint | Committed | Completed | Velocity |
|--------|-----------|-----------|----------|
| Sprint N-2 | [N] | [N] | [N]% |
| Sprint N-1 | [N] | [N] | [N]% |
| **Sprint N** | **[N]** | **[N]** | **[N]%** |

**3-Sprint Average**: [N] story points

---

## Notes & Decisions

### Sprint Planning Notes
- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]

### Mid-Sprint Adjustments
- **[Date]**: [What changed and why]
- **[Date]**: [What changed and why]

### Stakeholder Feedback
- **[Date]**: [Feedback received]
- **[Date]**: [Action taken based on feedback]

---

## Post-Sprint Summary

> **Note**: Fill this section after sprint completion

### Achievements
- ✅ [Completed goal 1]
- ✅ [Completed goal 2]
- ✅ [Completed goal 3]

### Challenges
- ⚠️ [Challenge faced and how resolved]
- ⚠️ [Challenge faced and how resolved]

### Incomplete Work
- 🔄 [User story carried over to next sprint]
  - **Reason**: [Why not completed]
  - **Plan**: [How to complete in next sprint]

### Lessons Learned
1. **[Lesson]**: [Description and action item]
2. **[Lesson]**: [Description and action item]

### Metrics Summary

| Metric | Target | Actual | Variance |
|--------|--------|--------|----------|
| Story Points | [N] | [N] | [+/-N] |
| Velocity | [N]% | [N]% | [+/-N]% |
| Bugs Introduced | <[N] | [N] | [+/-N] |
| Test Coverage | ≥[N]% | [N]% | [+/-N]% |

**Sprint Rating**: ⭐⭐⭐⭐⭐ (5 = Excellent, 1 = Poor)

---

## Retrospective Action Items

> **Note**: Fill this section after retrospective

**Continue Doing** (What worked well):
- [Practice 1]
- [Practice 2]

**Start Doing** (Improvements to try):
- [ ] [Action item 1] - Owner: [Name] - Due: [Date]
- [ ] [Action item 2] - Owner: [Name] - Due: [Date]

**Stop Doing** (What didn't work):
- [Practice to discontinue]
- [Practice to discontinue]

---

## References

**Related Documents**:
- [Vision & Strategy](../project-docs/vision/ROADMAP.md)
- [Previous Sprint](sprint-[N-1].md)
- [Next Sprint](sprint-[N+1].md)
- [Release Plan](../releases/release-vX.Y.Z.md)

**Development Workflows**:
- [8-Phase Development Process](../dev-docs/workflows/DEVELOPMENT_PROCESS.md)
- [DDD Workflow](../dev-docs/workflows/DDD_WORKFLOW.md)
- [BDD Workflow](../dev-docs/workflows/BDD_WORKFLOW.md)
- [TDD Workflow](../dev-docs/workflows/TDD_WORKFLOW.md)

**Process Metrics**:
- [Overall Process Metrics](../metrics/PROCESS_METRICS.md)

---

**Template Version**: 1.0
**Last Updated**: 2025-10-25
**Maintained By**: chora-base v3.0.0
