---
title: Intake Triage Guide
description: Decision criteria and frameworks for triaging incoming proposals, coordination requests, and tasks
type: reference
audience: [product-leads, engineering-leads, maintainers]
updated: 2025-10-27
related:
  - INBOX_PROTOCOL.md
  - incoming/coordination/README.md
  - ecosystem/proposals/README.md
---

# Intake Triage Guide

**Purpose**: Provide clear decision criteria for triaging strategic proposals, coordination requests, and implementation tasks.

**Audience**: Product leads, engineering leads, maintainers who review and prioritize incoming work.

---

## Table of Contents

1. [Overview](#overview)
2. [Type 1: Strategic Proposals](#type-1-strategic-proposals-quarterly-review)
3. [Type 2: Coordination Requests](#type-2-coordination-requests-sprint-planning)
4. [Type 3: Implementation Tasks](#type-3-implementation-tasks-continuous)
5. [Priority Frameworks](#priority-frameworks)
6. [Capacity Planning](#capacity-planning)
7. [Rejection Patterns](#rejection-patterns)
8. [Escalation](#escalation)

---

## Overview

### Three-Level Intake

```
Type 1: Strategic Proposals
├── Review: Quarterly
├── Decision: Accepted / Deferred / Rejected
└── Output: RFC → ADR → Coordination Requests

Type 2: Coordination Requests
├── Review: Sprint Planning (every 2 weeks)
├── Decision: this_sprint / next_sprint / backlog / rejected
└── Output: Implementation Tasks

Type 3: Implementation Tasks
├── Review: Continuous
├── Decision: Assign / Backlog / Reject
└── Output: DDD → BDD → TDD → Completion
```

### Triage Cadence

| Type | Review Frequency | Decision Makers | SLA |
|------|-----------------|-----------------|-----|
| Type 1 | Quarterly | Product + Engineering Leads | 2 weeks |
| Type 2 | Sprint Planning | Engineering Leads | 1 sprint |
| Type 3 | Continuous | Engineers + Claude Code | 1 day |

---

## Type 1: Strategic Proposals (Quarterly Review)

### Review Schedule

**When**: Quarterly planning sessions (Jan, Apr, Jul, Oct)
**Duration**: 2-4 hours per session
**Participants**: Product leads, engineering leads, key stakeholders

### Triage Framework

#### 1. Strategic Alignment (0-10 points)

**Question**: Does this align with our strategic goals?

- **10 points**: Directly enables strategic goal (e.g., "production-ready ecosystem")
- **7-8 points**: Strongly supports strategic goal
- **4-6 points**: Somewhat related to strategic goals
- **1-3 points**: Tangentially related
- **0 points**: No clear strategic alignment

**Examples**:
- Health monitoring (W3) → 10 points (production-ready blocker)
- Add new MCP server template → 7 points (supports ecosystem growth)
- Refactor internal CI → 4 points (nice to have, not strategic)

#### 2. Business Value (0-10 points)

**Question**: What's the business impact?

- **10 points**: Critical blocker for revenue/users (P0)
- **7-8 points**: High value, but not blocking (P1)
- **4-6 points**: Medium value, long-term benefit
- **1-3 points**: Low value, nice to have
- **0 points**: No clear business value

**Examples**:
- Health monitoring → 10 points (blocks production deployments)
- Performance optimization → 8 points (improves user experience)
- Documentation improvements → 5 points (long-term maintainability)

#### 3. Effort vs Impact (0-10 points)

**Question**: Is the ROI reasonable?

- **10 points**: High impact, low effort (quick win)
- **7-8 points**: High impact, medium effort
- **4-6 points**: Medium impact, medium effort
- **1-3 points**: Medium impact, high effort
- **0 points**: Low impact, high effort (avoid)

**Calculation**:
```
Effort: S (1-2 weeks), M (3-6 weeks), L (7-12 weeks), XL (>12 weeks)
Impact: High / Medium / Low

ROI Score:
High Impact + S Effort = 10
High Impact + M Effort = 8
High Impact + L Effort = 6
Medium Impact + S Effort = 7
Medium Impact + M Effort = 5
Low Impact + * = 0-3
```

#### 4. Risk Assessment (0-10 points)

**Question**: What are the risks?

- **10 points**: Low risk, clear path
- **7-8 points**: Moderate risk, mitigations identified
- **4-6 points**: High risk, but manageable
- **1-3 points**: High risk, unclear how to mitigate
- **0 points**: Unacceptable risk

**Risk Factors**:
- Technical complexity
- Dependencies on external teams/systems
- Regulatory/compliance concerns
- Timeline uncertainty
- Resource availability

#### 5. Readiness (0-10 points)

**Question**: Are we ready to execute?

- **10 points**: All dependencies met, resources available
- **7-8 points**: Most dependencies met, resources likely available
- **4-6 points**: Some blockers, but addressable in Q
- **1-3 points**: Major blockers, unlikely to resolve in Q
- **0 points**: Not ready, missing critical dependencies

### Decision Matrix

**Total Score** = Strategic Alignment + Business Value + Effort vs Impact + Risk + Readiness (max 50)

| Score | Decision | Action |
|-------|----------|--------|
| 40-50 | **Accept** | Move to RFC phase this quarter |
| 30-39 | **Accept (Conditional)** | Address open questions, then RFC |
| 20-29 | **Defer** | Revisit next quarter |
| 10-19 | **Defer (Low Priority)** | Revisit in 2-3 quarters |
| 0-9   | **Reject** | Does not align with strategy |

### Examples

#### Example 1: Health Monitoring (W3)
```
Strategic Alignment:  10  (production-ready blocker)
Business Value:       10  (enables production deployments)
Effort vs Impact:      6  (High impact, L effort: 16 weeks)
Risk:                  8  (Moderate risk, clear mitigations)
Readiness:             9  (Dependencies met, resources available)
Total:                43  → Accept
```

#### Example 2: AI-Powered Code Review
```
Strategic Alignment:   4  (Nice to have, not strategic)
Business Value:        5  (Long-term productivity gain)
Effort vs Impact:      3  (Medium impact, L effort: 12 weeks)
Risk:                  5  (High risk: AI reliability unclear)
Readiness:             3  (No AI expertise on team)
Total:                20  → Defer (revisit when AI expertise available)
```

### Rejection Patterns

**Reject if**:
- No clear strategic alignment (score < 5 on Strategic Alignment)
- No measurable business value (score < 3 on Business Value)
- Effort >> Impact (score < 3 on Effort vs Impact)
- Unacceptable risk (score < 3 on Risk)
- Not ready and unlikely to be ready in next 2 quarters (score < 3 on Readiness)

---

## Type 2: Coordination Requests (Sprint Planning)

### Review Schedule

**When**: Sprint planning (every 2 weeks)
**Duration**: 30-60 minutes
**Participants**: Engineering leads, repo maintainers

### Triage Framework

#### 1. Priority Classification

**P0 (Critical)**:
- Blocks active sprint or waypoint
- Security vulnerability
- Production outage
- Dependency for P0 work in another repo

**Decision**: this_sprint (must be done)

**P1 (High)**:
- Blocks next sprint or waypoint
- Enables critical feature
- High user impact
- Dependency for P1 work in another repo

**Decision**: this_sprint or next_sprint (depends on capacity)

**P2 (Medium)**:
- No immediate blocking
- Medium user impact
- Nice to have improvement
- Technical debt

**Decision**: next_sprint or backlog (depends on capacity)

#### 2. Urgency Assessment

**blocks_sprint**: Blocks active sprint → this_sprint (if capacity)
**next_sprint**: Blocks next sprint → next_sprint
**backlog**: No immediate blocking → backlog

#### 3. Capacity Check

**Question**: Do we have capacity this sprint?

**Calculate Available Hours**:
```
Sprint Capacity = (Team Size × Sprint Length in Days × 6 hours/day) × 0.7

Example:
2 engineers × 10 days × 6 hours/day × 0.7 = 84 hours available

Current Commitments: 60 hours
Available: 24 hours
Incoming Request: 16 hours

Decision: Can accept (24 - 16 = 8 hours buffer)
```

**Buffer Rule**: Keep 20% buffer for unexpected work

#### 4. Dependency Check

**Question**: Are dependencies met?

**Check**:
1. Review `dependencies` field in coordination request
2. Query capability registry:
   ```bash
   yq '.provides[] | select(.id == "required_capability")' \
     inbox/coordination/CAPABILITIES/*.yaml
   ```
3. Verify version compatibility

**Decision**:
- All dependencies met → Can accept
- Dependencies pending → Schedule after dependencies complete
- Dependencies unavailable → Reject or defer

#### 5. Impact Assessment

**Question**: What's the impact if we defer?

- **High**: Blocks other teams, production issues, user-facing problems → this_sprint
- **Medium**: Delays non-critical work, affects internal tools → next_sprint
- **Low**: No immediate impact → backlog

### Decision Matrix

| Priority | Urgency | Capacity | Dependencies | Decision |
|----------|---------|----------|--------------|----------|
| P0 | blocks_sprint | Yes | Met | **this_sprint** |
| P0 | blocks_sprint | No | Met | **this_sprint** (re-prioritize) |
| P0 | blocks_sprint | * | Not met | Escalate |
| P1 | blocks_sprint | Yes | Met | **this_sprint** |
| P1 | next_sprint | Yes | Met | **this_sprint** or **next_sprint** |
| P1 | next_sprint | No | Met | **next_sprint** |
| P1 | backlog | * | Met | **backlog** |
| P2 | * | * | Met | **backlog** |
| * | * | * | Not met | **defer** (until dependencies met) |

### Examples

#### Example 1: Health Endpoint Template (coord-001)
```
Priority:     P0 (blocks W3)
Urgency:      blocks_sprint (blocks coord-002, coord-003)
Capacity:     Yes (24 hours available, 8 hours estimated)
Dependencies: ADR 0001 (met)
Decision:     this_sprint
```

#### Example 2: Documentation Update (coord-042)
```
Priority:     P2 (nice to have)
Urgency:      backlog (no blocking)
Capacity:     Yes (24 hours available, 4 hours estimated)
Dependencies: None
Decision:     backlog (prioritize P0/P1 work first)
```

### Rejection Patterns

**Reject if**:
- No capacity for next 2 sprints and not P0
- Dependencies unavailable with no clear path
- Duplicates existing work
- Out of scope for this repo (check CAPABILITIES.yaml)
- Insufficient detail (can't estimate effort)

**Defer if**:
- Dependencies not met yet (revisit when met)
- Capacity full for 2 sprints but work is valuable (revisit in Sprint+2)

---

## Type 3: Implementation Tasks (Continuous)

### Review Schedule

**When**: Continuous (as tasks arrive)
**Duration**: 5-15 minutes per task
**Participants**: Engineers, Claude Code

### Triage Framework

#### 1. Ready Check

**Question**: Is this task ready to start?

**Checklist**:
- [ ] Clear deliverables defined
- [ ] Acceptance criteria specified
- [ ] Estimated effort provided
- [ ] Dependencies identified (and met)
- [ ] Related coordination request (if any) accepted
- [ ] Fits within DDD → BDD → TDD workflow

**Decision**:
- All boxes checked → Ready (assign)
- Missing items → Send back for clarification

#### 2. Category Classification

**Categories**:
- `feature`: New functionality
- `bug`: Fix broken behavior
- `refactor`: Code improvement (no behavior change)
- `docs`: Documentation only
- `test`: Test coverage improvement
- `chore`: Maintenance (dependencies, CI, etc.)

**Priority by Category**:
- `bug` (P0 if production) → High priority
- `feature` (if linked to coordination request) → Medium priority
- `refactor`, `docs`, `test`, `chore` → Low priority (backlog)

#### 3. Effort Assessment

**Question**: Can we complete this in 1-2 days?

- **2-8 hours**: Ideal task size → Assign
- **8-16 hours**: Large task → Consider breaking down
- **16+ hours**: Too large → Break into smaller tasks

**Breaking Down Large Tasks**:
```
Original: "Implement Health Monitoring Service" (24 hours)

Break into:
1. "Implement Health Checker (polling logic)" (8 hours)
2. "Implement Recovery Manager (auto-recovery)" (8 hours)
3. "Implement Event Emission (trace context)" (4 hours)
4. "Integration Tests (recovery flows)" (4 hours)
```

#### 4. Sprint Fit

**Question**: Does this fit current sprint?

**Check**:
- Sprint capacity remaining
- Sprint goals (does this align?)
- Dependencies on other sprint work

**Decision**:
- Fits sprint → Assign
- Doesn't fit → Backlog for next sprint

### Decision Tree

```
Is task ready? (all fields filled, dependencies met)
├─ Yes → Is effort 2-16 hours?
│   ├─ Yes → Is there sprint capacity?
│   │   ├─ Yes → Assign to engineer/Claude Code
│   │   └─ No → Backlog for next sprint
│   └─ No → Break into smaller tasks
└─ No → Send back with missing items list
```

### Assignment Strategy

**Assign to Claude Code if**:
- Well-defined deliverables
- Clear acceptance criteria
- Fits DDD → BDD → TDD workflow
- No ambiguous decisions required
- Estimated < 8 hours

**Assign to Human if**:
- Requires architectural decisions
- Needs user research/feedback
- Involves external dependencies
- High ambiguity
- Estimated > 8 hours (pair with Claude)

### Examples

#### Example 1: Health Endpoint Template (task-001)
```
Ready:     ✅ (deliverables, acceptance criteria, effort, dependencies)
Category:  feature
Effort:    6-8 hours (ideal size)
Sprint:    Sprint 4 (capacity available)
Decision:  Assign to Claude Code
```

#### Example 2: Refactor Monitoring Service (task-099)
```
Ready:     ❌ (missing acceptance criteria)
Category:  refactor
Effort:    Unknown
Sprint:    N/A
Decision:  Send back for clarification
```

### Rejection Patterns

**Reject if**:
- Out of scope (not in repo's responsibility, check CAPABILITIES.yaml)
- Duplicates existing work
- No clear acceptance criteria after clarification
- Violates architectural standards (suggest alternative approach)

**Backlog if**:
- Ready but no sprint capacity
- Ready but dependencies not met
- Low priority (docs, chore) and higher priority work available

---

## Priority Frameworks

### RICE Framework (Reach × Impact × Confidence / Effort)

**Use for**: Strategic proposals, large coordination requests

**Calculation**:
```
Reach:      How many users/repos affected? (1-10)
Impact:     How much does this help? (1=minimal, 3=high, 10=massive)
Confidence: How sure are we? (0.1-1.0)
Effort:     How many weeks? (1-16+)

RICE Score = (Reach × Impact × Confidence) / Effort

Example: Health Monitoring
Reach:      10 (all 4 repos, all users)
Impact:     10 (enables production use)
Confidence: 0.8 (some unknowns in implementation)
Effort:     16 weeks

RICE = (10 × 10 × 0.8) / 16 = 5.0 (high priority)
```

**Interpretation**:
- RICE > 5.0 → High priority
- RICE 2.0-5.0 → Medium priority
- RICE < 2.0 → Low priority

### MoSCoW (Must Have / Should Have / Could Have / Won't Have)

**Use for**: Sprint planning, backlog prioritization

**Must Have (P0)**:
- Blocks sprint/waypoint
- Critical bug
- Security issue
- Contractual obligation

**Should Have (P1)**:
- High value
- Important but not critical
- Can defer 1-2 sprints if needed

**Could Have (P2)**:
- Nice to have
- Low impact if omitted
- Can defer indefinitely

**Won't Have**:
- Out of scope
- Low ROI
- Not aligned with strategy

### Eisenhower Matrix (Urgent vs Important)

**Use for**: Daily triage, task prioritization

```
              Urgent       Not Urgent
Important     Do First     Schedule
Not Important Delegate     Eliminate
```

**Do First** (P0): Urgent + Important
- Production outages
- Security vulnerabilities
- Blocking dependencies

**Schedule** (P1): Not Urgent + Important
- Strategic work
- Architecture improvements
- Technical debt

**Delegate** (P2): Urgent + Not Important
- Interruptions
- Requests from other teams
- Low-impact bugs

**Eliminate**: Not Urgent + Not Important
- Busywork
- Nice-to-haves
- Low ROI improvements

---

## Capacity Planning

### Sprint Capacity Calculation

```
Nominal Capacity = Team Size × Sprint Days × 6 hours/day

Adjusted Capacity = Nominal × Availability Factor

Availability Factors:
- 1.0 = Dedicated team, no meetings, no interruptions (ideal)
- 0.8 = Some meetings, minimal interruptions
- 0.7 = Normal team, regular meetings (typical)
- 0.5 = High meeting load, many interruptions
- 0.3 = Part-time team, heavy meeting load

Example:
2 engineers × 10 days × 6 hours/day × 0.7 = 84 hours available
```

### Buffer Allocation

**Reserve 20% for**:
- Bug fixes
- Urgent requests
- Blockers
- Estimation errors

**Effective Capacity** = Adjusted Capacity × 0.8

### Overcommitment Warning

**If Committed Hours > Effective Capacity**:
1. Re-prioritize (move P2 to backlog)
2. Negotiate timelines (defer non-critical work)
3. Add resources (if critical P0 work)
4. Push back (reject if out of scope)

---

## Rejection Patterns

### Common Rejection Reasons

#### 1. Strategic Misalignment
**Pattern**: Proposal doesn't align with strategic goals

**Response Template**:
```
Thank you for the proposal. After review, we've determined this doesn't
align with our current strategic priorities (production-ready ecosystem,
MCP server standardization). We're deferring this to [Q+2] for
reconsideration. If strategic priorities change, we'll revisit.

Alternative: Consider [alternative approach that does align]
```

#### 2. Insufficient Capacity
**Pattern**: Coordination request is valuable but no capacity

**Response Template**:
```
Thank you for the coordination request. This aligns well with our goals,
but we don't have capacity in the next 2 sprints (Sprint N, Sprint N+1).
We're adding this to the backlog for Sprint N+2 (Week X).

We'll notify you when we schedule this work.
```

#### 3. Dependencies Not Met
**Pattern**: Task depends on unavailable capability

**Response Template**:
```
Thank you for the task request. This depends on [capability] from [repo],
which is not yet available (blocks: [list dependencies]).

We're deferring this until dependencies are met. Expected: [date/sprint].
We'll revisit when [dependency] is released.
```

#### 4. Out of Scope
**Pattern**: Request doesn't match repo capabilities

**Response Template**:
```
Thank you for the request. After reviewing our CAPABILITIES.yaml, this is
outside our repository's scope. This would be better handled by:
- [repo name] (capability: [id])

We're closing this request. Please submit to [correct repo].
```

#### 5. Unclear Requirements
**Pattern**: Task missing critical details

**Response Template**:
```
Thank you for the task submission. Before we can proceed, we need:
- [ ] Acceptance criteria (what defines "done"?)
- [ ] Effort estimate (rough hours?)
- [ ] Dependencies (what must be done first?)

Please update the task and resubmit.
```

### Deferral Patterns

**Defer to Next Quarter** (Strategic Proposals):
- Valuable but not urgent
- Dependencies not ready
- Capacity constraints

**Defer to Next Sprint** (Coordination Requests):
- Capacity full this sprint
- Lower priority than committed work
- Dependencies completing soon

**Defer to Backlog** (Implementation Tasks):
- Ready but no capacity
- P2 priority
- Can be done anytime

---

## Escalation

### When to Escalate

**Escalate to Product Lead if**:
- Strategic decision needed
- Cross-team coordination required
- Resource allocation dispute
- Priority conflict (two P0s, not enough capacity)

**Escalate to Engineering Lead if**:
- Technical feasibility question
- Architecture decision needed
- Resource allocation within engineering

**Escalate to Ecosystem Team if**:
- Cross-repo conflict (two repos both claim capability)
- Ecosystem standard change
- Quality gate modification

### Escalation Process

1. **Document the issue**:
   - What's the conflict?
   - What are the options?
   - What's your recommendation?

2. **Identify stakeholders**:
   - Who needs to decide?
   - Who needs to be informed?

3. **Set deadline**:
   - When do we need a decision?
   - What's the impact of delay?

4. **Present options**:
   - Option A: [description, pros, cons]
   - Option B: [description, pros, cons]
   - Recommendation: [which and why]

5. **Document decision**:
   - Decision: [A or B]
   - Rationale: [why]
   - Next steps: [action items]

---

## Decision Templates

### Strategic Proposal Acceptance

```yaml
proposal_id: prop-XXX
decision:
  date: YYYY-MM-DD
  outcome: accepted
  decision_makers: [Name 1, Name 2]
  rationale: |
    [Why this was accepted - strategic alignment, business value, etc.]
  next_steps:
    - Create RFC [RFC number]
    - Target FCP: [date range]
    - Expected completion: [Q]
```

### Strategic Proposal Deferral

```yaml
proposal_id: prop-XXX
decision:
  date: YYYY-MM-DD
  outcome: deferred
  next_review: YYYY-MM-DD
  decision_makers: [Name 1, Name 2]
  rationale: |
    [Why deferred - capacity, dependencies, strategic timing, etc.]
  conditions_for_acceptance:
    - [What needs to change for this to be accepted]
```

### Strategic Proposal Rejection

```yaml
proposal_id: prop-XXX
decision:
  date: YYYY-MM-DD
  outcome: rejected
  decision_makers: [Name 1, Name 2]
  rationale: |
    [Why rejected - strategic misalignment, infeasible, etc.]
  alternatives:
    - [Alternative approaches that would align better]
```

### Coordination Request Triage

```yaml
request_id: coord-XXX
decision:
  date: YYYY-MM-DD
  outcome: this_sprint | next_sprint | backlog | rejected
  sprint: Sprint N
  decision_makers: [Name]
  rationale: |
    [Why this scheduling decision - capacity, priority, dependencies]
  assigned_to: [Engineer name or "Claude Code"]
  estimated_completion: YYYY-MM-DD
```

---

## Metrics to Track

### Type 1 (Strategic Proposals)

- **Acceptance rate**: Accepted / Total
- **Time to decision**: Created → Decision (target: 2 weeks)
- **Deferral reasons**: Why deferred? (patterns)
- **RFC success rate**: Accepted proposals → Completed RFCs

### Type 2 (Coordination Requests)

- **Fulfillment rate**: Fulfilled / Total
- **Time to triage**: Created → Triaged (target: 1 sprint)
- **Time to fulfillment**: Created → Fulfilled (track by priority)
- **Rejection reasons**: Why rejected? (patterns)

### Type 3 (Implementation Tasks)

- **Assignment rate**: Assigned / Total
- **Completion rate**: Completed / Assigned
- **Time to completion**: Created → Completed (track by category)
- **Backlog size**: Tasks in backlog (monitor for growth)

### Capacity Metrics

- **Utilization**: Actual Hours / Available Hours (target: 70-80%)
- **Overcommitment**: Committed Hours / Available Hours (target: <100%)
- **Throughput**: Tasks completed per sprint
- **Cycle time**: Created → Completed (average)

---

## Related Documentation

- [INBOX_PROTOCOL.md](INBOX_PROTOCOL.md) - Complete protocol documentation
- [CLAUDE.md](CLAUDE.md) - Claude Code patterns for inbox
- [incoming/coordination/README.md](incoming/coordination/README.md) - Type 2 intake
- [ecosystem/proposals/README.md](ecosystem/proposals/README.md) - Type 1 intake
- [incoming/tasks/README.md](incoming/tasks/README.md) - Type 3 intake
- [examples/health-monitoring-w3/](examples/health-monitoring-w3/) - Complete example
