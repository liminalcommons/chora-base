---
title: Development Anti-Patterns and Solutions
type: reference
status: current
audience: developers, ai-agents
last_updated: 2025-10-25
version: 1.0.0
---

# Development Anti-Patterns and Solutions

**Purpose:** Catalog common mistakes in software development and provide evidence-based solutions.

**How to Use:** When facing a decision or problem, check this guide to avoid known pitfalls.

**Evidence:** These anti-patterns are compiled from real-world projects, research, and the Agentic Coding Best Practices study.

---

## Table of Contents

1. [Phase 1: Vision & Strategy](#phase-1-vision--strategy)
2. [Phase 2: Planning & Prioritization](#phase-2-planning--prioritization)
3. [Phase 3: Requirements & Design](#phase-3-requirements--design)
4. [Phase 4: Development](#phase-4-development)
5. [Phase 5: Testing & Quality](#phase-5-testing--quality)
6. [Phase 6: Review & Integration](#phase-6-review--integration)
7. [Phase 7: Release & Deployment](#phase-7-release--deployment)
8. [Phase 8: Monitoring & Feedback](#phase-8-monitoring--feedback)
9. [Cross-Cutting Anti-Patterns](#cross-cutting-anti-patterns)
10. [Quick Reference](#quick-reference)

---

## Phase 1: Vision & Strategy

### ❌ Anti-Pattern: No Strategic Direction

**Problem:**
```markdown
Team approach: "Let's just build whatever seems useful"
No roadmap, no vision, no success metrics
```

**Impact:**
- Features don't align with user needs
- Wasted effort on low-value work
- No way to measure success
- Team lacks focus and direction

**Solution:**
```markdown
✅ GOOD:
- Define clear product vision (1-2 sentences)
- Create roadmap with quarterly milestones
- Establish measurable success metrics
- Get stakeholder alignment on priorities

Example:
**Vision:** Transform X from prototype to production-grade Y
**Q1 2026 Milestone:** Feature A with 90% user satisfaction
**Success Metric:** 10,000 monthly active users
```

**Reference:** [DEVELOPMENT_PROCESS.md - Phase 1](workflows/DEVELOPMENT_PROCESS.md#phase-1-vision--strategy)

---

### ❌ Anti-Pattern: Ignoring Ecosystem

**Problem:**
```markdown
Build in isolation, discover integration conflicts later
No research on existing solutions or patterns
```

**Impact:**
- Reinvent the wheel (waste 2-3 weeks)
- Incompatible with ecosystem tools
- Miss opportunities for collaboration
- Poor adoption due to friction

**Solution:**
```markdown
✅ GOOD:
- Survey ecosystem landscape before building
- Identify integration patterns (what exists?)
- Coordinate with related projects
- Document architectural decisions (ADRs)

Example:
Research Phase:
- Survey 10 similar tools in ecosystem
- Identify 3 common integration patterns
- Choose pattern used by 70% of ecosystem
- Document decision in ADR-001
```

---

### ❌ Anti-Pattern: No Release Planning

**Problem:**
```markdown
No version strategy, no deprecation timeline
Breaking changes without warning
```

**Impact:**
- Users surprised by breaking changes
- No clear upgrade path
- Loss of user trust
- Support burden increases 3x

**Solution:**
```markdown
✅ GOOD:
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Plan releases quarterly
- Deprecate features with 90-day notice
- Provide migration guides

Example Timeline:
v1.0.0 (Oct 2025) → v1.1.0 (Nov) → v2.0.0 (Feb 2026)
                                      ↑ Breaking changes documented in upgrade guide
```

---

## Phase 2: Planning & Prioritization

### ❌ Anti-Pattern: No Clear Sprint Goals

**Problem:**
```markdown
Sprint planning: "Work on whatever tasks are in backlog"
No focus, no success criteria
```

**Impact:**
- Team works on unrelated tasks
- No coherent deliverable at sprint end
- Difficult to measure progress
- Low morale (no sense of accomplishment)

**Solution:**
```markdown
✅ GOOD:
Sprint goal: One sentence describing deliverable

Example:
❌ BAD:  "Sprint 15: Fix bugs and add features"
✅ GOOD: "Sprint 15: Production-ready config validation (v1.1.0)"

Success Criteria:
- ✅ Users can validate YAML/JSON configs
- ✅ 90% of errors caught before deployment
- ✅ All tests pass, ready to release
```

---

### ❌ Anti-Pattern: Over-Committing

**Problem:**
```markdown
Plan 40 hours of work for 1-week sprint
No buffer for unknowns, context switching, meetings
```

**Impact:**
- Consistent sprint failures
- Team burnout
- Rushed, low-quality work
- Technical debt accumulates

**Solution:**
```markdown
✅ GOOD:
Plan 60-70% of available capacity

Example (1-week sprint, 5 people):
Total capacity: 200 hours (5 people × 40 hours)
Planned work: 120-140 hours (60-70%)
Buffer: 60-80 hours (meetings, unknowns, support)

Rule: If sprint consistently completes early, increase capacity.
      If sprint consistently fails, decrease capacity.
```

---

### ❌ Anti-Pattern: No Stakeholder Alignment

**Problem:**
```markdown
Engineers plan sprint, build features
Product sees results: "This isn't what we wanted"
```

**Impact:**
- Wasted 1-2 weeks of development
- Team morale drops
- Rework consumes next sprint
- Loss of trust between teams

**Solution:**
```markdown
✅ GOOD:
Sprint planning meeting with all stakeholders

Agenda:
1. Review roadmap and priorities (Product)
2. Propose sprint goal (Engineering)
3. Review acceptance criteria (Product + Engineering)
4. Get explicit approval (All stakeholders)
5. Commit to sprint (Engineering)

Outcome: Signed-off sprint plan
```

---

## Phase 3: Requirements & Design

### ❌ Anti-Pattern: Skipping DDD (Coding First)

**Problem:**
```markdown
Start coding → Realize design issue → Throw away code → Redesign
Cycle repeats 2-3 times per feature
```

**Impact:**
- 40-60% of development time wasted on rework
- Frustration and low morale
- Inconsistent APIs
- Poor documentation (written as afterthought)

**Solution:**
```markdown
✅ GOOD:
DDD Process (3-5 hours upfront):
1. Write change request (Explanation + How-to)
2. Design API (Reference documentation)
3. Extract acceptance criteria
4. Review with stakeholders
5. Get approval BEFORE coding

ROI: 3-5 hours upfront saves 8-15 hours of rework
```

**Reference:** [DDD_WORKFLOW.md](workflows/DDD_WORKFLOW.md)

---

### ❌ Anti-Pattern: Vague Requirements

**Problem:**
```markdown
Requirement: "Build a better error handling system"
What does "better" mean? No success criteria.
```

**Impact:**
- Engineers guess at requirements
- 60% chance of building wrong thing
- Multiple rework cycles
- Stakeholder dissatisfaction

**Solution:**
```markdown
✅ GOOD:
Specific, measurable requirements

❌ BAD:  "Build better error handling"
✅ GOOD:
**Problem:** 90% of error messages don't suggest fixes
            (causes 80% of support tickets)
**Solution:** Errors include suggestions for correction
**Success:** Support tickets reduced by 60%
**API:** ErrorFormatter.not_found(entity, id, similar_ids)
**Example:** "Server 'githbu' not found. Did you mean 'github'?"
```

---

### ❌ Anti-Pattern: No Design Review

**Problem:**
```markdown
Write API documentation → Skip review → Start coding
Product sees implementation: "Not what we discussed"
```

**Impact:**
- Build wrong API
- 1-2 weeks wasted
- Breaking changes required
- User confusion

**Solution:**
```markdown
✅ GOOD:
Design review with explicit approval

Review Checklist:
- [ ] Product validates business value
- [ ] Engineering validates technical feasibility
- [ ] Technical writer validates clarity
- [ ] Examples are complete and correct

Approval Format:
**Approved by:**
- Product: @alice (2025-10-25)
- Engineering: @bob (2025-10-25)
- Tech Writer: @charlie (2025-10-25)

**Ready for Implementation:** ✅ YES
```

---

## Phase 4: Development

### ❌ Anti-Pattern: Writing Tests After Code

**Problem:**
```markdown
1. Write implementation
2. Write tests that match implementation
3. Tests don't catch bugs (just document what code does)
```

**Impact:**
- Tests don't drive design
- Poor test coverage (only happy paths)
- Tests are coupled to implementation
- Refactoring breaks tests

**Solution:**
```markdown
✅ GOOD:
TDD Process (RED-GREEN-REFACTOR)

1. Write test FIRST (RED)
   - Test describes desired behavior
   - Test fails (code doesn't exist)

2. Write minimal code (GREEN)
   - Just enough to pass test
   - Don't worry about perfection

3. Refactor (improve design)
   - Tests stay GREEN
   - Code becomes better designed

Evidence: 40-80% fewer defects with TDD
```

**Reference:** [TDD_WORKFLOW.md](workflows/TDD_WORKFLOW.md)

---

### ❌ Anti-Pattern: Large, Untested Commits

**Problem:**
```markdown
1500-line PR with no tests
"I'll add tests later" (never happens)
```

**Impact:**
- Review takes 4+ hours
- Bugs slip through
- Hard to debug failures
- Technical debt accumulates

**Solution:**
```markdown
✅ GOOD:
Small, incremental commits with tests

Guidelines:
- PRs < 500 lines (ideally < 300)
- Every commit includes tests
- One behavior per commit
- Tests written BEFORE implementation

Example:
Commit 1: Add validate_config (RED test)
Commit 2: Implement validation (GREEN)
Commit 3: Add error handling (RED test)
Commit 4: Implement errors (GREEN)
Commit 5: Refactor validation logic
```

---

### ❌ Anti-Pattern: Skipping REFACTOR Phase

**Problem:**
```markdown
Test 1 (RED → GREEN) → immediately write Test 2
Code becomes duplicated, messy, hard to maintain
```

**Impact:**
- Technical debt grows exponentially
- Velocity decreases over time
- Bugs increase (complex code)
- Refactoring becomes "big rewrite"

**Solution:**
```markdown
✅ GOOD:
Refactor after every 2-3 tests

Cycle:
Test 1 (RED → GREEN → REFACTOR)
Test 2 (RED → GREEN → REFACTOR)
Test 3 (RED → GREEN → REFACTOR)

Refactoring Targets:
- Remove duplication
- Improve naming
- Extract helper functions
- Optimize performance
- Add documentation

Rule: Tests must stay GREEN during refactoring
```

---

### ❌ Anti-Pattern: Testing Implementation Details

**Problem:**
```markdown
Test internal state, private methods
Tests break when refactoring (even though behavior unchanged)
```

**Impact:**
- Refactoring becomes expensive
- Tests are brittle
- False failures (tests fail, behavior correct)
- Developers avoid refactoring

**Solution:**
```markdown
✅ GOOD:
Test behavior through public API

❌ BAD:  assert object._internal_state == "valid"
✅ GOOD: assert object.is_valid() is True

❌ BAD:  Test private method directly
✅ GOOD: Test public method that uses private method

Principle: Tests should verify WHAT, not HOW
```

---

## Phase 5: Testing & Quality

### ❌ Anti-Pattern: "Tests Pass, Ship It"

**Problem:**
```markdown
Run unit tests only
Linting? Type checking? Security? "We'll do it later"
```

**Impact:**
- Production bugs (integration failures)
- Security vulnerabilities
- Style inconsistencies
- Type errors in production

**Solution:**
```markdown
✅ GOOD:
Test pyramid + quality gates

Quality Checklist (all must pass):
- ✅ Unit tests pass
- ✅ Smoke tests pass (<30s critical paths)
- ✅ Integration tests pass
- ✅ BDD scenarios pass
- ✅ Test coverage ≥85%
- ✅ Linting (ruff): 0 errors
- ✅ Type checking (mypy): 0 errors
- ✅ Security scan (bandit): 0 critical issues
- ✅ Pre-commit hooks pass

Automation: CI/CD enforces all checks
```

---

### ❌ Anti-Pattern: Ignoring Flaky Tests

**Problem:**
```markdown
Test fails randomly
Team reaction: "Just re-run CI" or "Skip that test"
```

**Impact:**
- Tests lose credibility
- Real bugs masked by flaky tests
- CI becomes unreliable
- Test suite degrades over time

**Solution:**
```markdown
✅ GOOD:
Fix flaky tests immediately (P1 priority)

Common Causes:
1. Race conditions (async/timing)
   Fix: Use proper async patterns, await all operations

2. Shared state between tests
   Fix: Isolate tests, use fixtures

3. External dependencies
   Fix: Mock external calls, use test doubles

4. Non-deterministic data
   Fix: Freeze time, seed random generators

Rule: Flaky test = broken test = must fix
```

---

### ❌ Anti-Pattern: Low Test Coverage Accepted

**Problem:**
```markdown
Coverage is 45%
"Good enough, ship it"
```

**Impact:**
- 55% of code untested
- Production bugs in uncovered code
- Fear of refactoring (might break things)
- Technical debt

**Solution:**
```markdown
✅ GOOD:
Coverage gates enforced

Targets:
- Overall: ≥85%
- New code: ≥90%
- Critical modules: ≥95%

Exceptions (explicit approval required):
- Generated code
- Legacy code (with plan to improve)
- Experimental features (with timeline)

CI Enforcement:
- PR blocked if coverage decreases
- Coverage report in PR comment
- Annotate uncovered lines in diff
```

---

## Phase 6: Review & Integration

### ❌ Anti-Pattern: Rubber-Stamp Reviews

**Problem:**
```markdown
Reviewer: "LGTM" without reading code
Approve in 2 minutes for 500-line PR
```

**Impact:**
- Bugs slip through
- Design issues not caught
- No knowledge sharing
- Code quality degrades

**Solution:**
```markdown
✅ GOOD:
Thorough review with checklist

Review Checklist:
**Functionality:**
- [ ] Code matches acceptance criteria
- [ ] Edge cases handled
- [ ] Error handling appropriate

**Design:**
- [ ] Design is clear and maintainable
- [ ] No unnecessary complexity
- [ ] Follows project patterns

**Tests:**
- [ ] Test coverage adequate (≥90% new code)
- [ ] Tests are meaningful (not just coverage)
- [ ] Edge cases tested

**Documentation:**
- [ ] API docs complete
- [ ] CHANGELOG updated
- [ ] Examples provided

Time: Allocate 1-2 hours for thorough review
```

---

### ❌ Anti-Pattern: Skipping CI/CD

**Problem:**
```markdown
Merge PR without waiting for CI
"It passed locally, it'll be fine"
```

**Impact:**
- Broken main branch
- Blocks other developers
- Production deployment fails
- Rollback required (wasted hours)

**Solution:**
```markdown
✅ GOOD:
CI/CD gates enforced

Merge Requirements (ALL must pass):
- ✅ CI/CD pipeline GREEN
- ✅ 1+ code review approval
- ✅ All comments addressed
- ✅ Branch up to date with main
- ✅ No merge conflicts
- ✅ Coverage not decreased

Automation: GitHub branch protection rules
```

---

### ❌ Anti-Pattern: No PR Template

**Problem:**
```markdown
PR description: "Fixed stuff"
No context, no testing info, no checklist
```

**Impact:**
- Reviewers waste time asking questions
- Important checks skipped
- Inconsistent PR quality
- Knowledge loss (no documentation)

**Solution:**
```markdown
✅ GOOD:
PR template with required sections

Template:
## Summary
Brief description of changes

## Related Issues
Closes #XX

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] All tests passing locally

## Documentation
- [ ] API docs updated
- [ ] CHANGELOG.md updated

## Quality Checklist
- [ ] Code follows style guide
- [ ] Type hints complete
- [ ] Coverage ≥90% for new code
```

---

## Phase 7: Release & Deployment

### ❌ Anti-Pattern: Manual, Error-Prone Releases

**Problem:**
```markdown
15 manual steps to release
Easy to forget step, make typo, push to wrong branch
```

**Impact:**
- Broken releases (forget changelog)
- Wrong version tags
- Incomplete deploys
- Rollback required (2-4 hours wasted)

**Solution:**
```markdown
✅ GOOD:
Automated release pipeline

One-Command Release:
```bash
just release minor  # Automates all steps
```

What it does:
1. Bump version (pyproject.toml)
2. Update CHANGELOG.md
3. Run pre-release checks
4. Create release commit
5. Create git tag
6. Push to GitHub
7. Trigger CI/CD
8. Build package
9. Publish to PyPI
10. Create GitHub release

Time: 5 minutes (vs 30 minutes manual)
Error rate: 0% (vs 15% manual)
```

---

### ❌ Anti-Pattern: No Rollback Plan

**Problem:**
```markdown
Deploy to production and hope for the best
When things break: "How do we roll back?!"
```

**Impact:**
- Extended downtime (30+ minutes)
- Data loss
- User frustration
- Revenue impact

**Solution:**
```markdown
✅ GOOD:
Rollback procedure tested in advance

Deployment Checklist:
- [ ] Rollback procedure documented
- [ ] Rollback tested in staging
- [ ] Database migrations reversible
- [ ] Feature flags enable/disable
- [ ] Monitoring alerts configured
- [ ] On-call team notified

Rollback Procedure:
```bash
# Revert to previous version
kubectl rollout undo deployment/app

# Verify rollback
kubectl rollout status deployment/app

# Monitor metrics
watch kubectl get pods
```

Practice: Monthly rollback drills
```

---

### ❌ Anti-Pattern: No Version Strategy

**Problem:**
```markdown
Version numbers: 1.0, 1.1, 2.0, 1.5 (out of order?)
Breaking changes in patch releases
No deprecation warnings
```

**Impact:**
- Users surprised by breaking changes
- No clear upgrade path
- Adoption resistance
- Support burden increases

**Solution:**
```markdown
✅ GOOD:
Semantic versioning (MAJOR.MINOR.PATCH)

Rules:
- MAJOR (1.0.0 → 2.0.0): Breaking changes
  - Requires migration guide
  - Deprecated features removed
  - 90-day warning period

- MINOR (1.0.0 → 1.1.0): New features (backward-compatible)
  - Additive changes only
  - Deprecations announced (removed in next MAJOR)

- PATCH (1.0.0 → 1.0.1): Bug fixes only
  - No behavior changes
  - No new features
  - No API changes

Enforcement: CI checks version bump type matches changes
```

---

## Phase 8: Monitoring & Feedback

### ❌ Anti-Pattern: "Deploy and Forget"

**Problem:**
```markdown
Deploy to production
No monitoring, no alerts, no feedback loop
First notice of issues: User complaint
```

**Impact:**
- Extended downtime (no alerts)
- Data loss (no monitoring)
- User churn (poor experience)
- Reputation damage

**Solution:**
```markdown
✅ GOOD:
Active monitoring and alerting

Monitoring Checklist:
- [ ] Metrics dashboard (Grafana)
  - Request rate
  - Latency (p50, p95, p99)
  - Error rate
  - Resource usage

- [ ] Alerts configured (Prometheus)
  - Error rate >1%
  - Latency p95 >500ms
  - Service down
  - Resource exhaustion

- [ ] Logs aggregated (ELK/Loki)
  - Error logs
  - Performance logs
  - Audit logs

- [ ] On-call rotation
  - 24/7 coverage
  - Escalation procedures
  - Runbooks for common issues

Daily: Review metrics (15 min)
Weekly: Deep dive (1-2 hours)
Monthly: Health report
```

---

### ❌ Anti-Pattern: Ignoring User Feedback

**Problem:**
```markdown
Bug reports pile up on GitHub
No response, no triage, no prioritization
Users give up and leave
```

**Impact:**
- User frustration
- Reputation damage
- Missed improvement opportunities
- Community loses trust

**Solution:**
```markdown
✅ GOOD:
Systematic feedback management

Triage Process:
1. Acknowledge within 24 hours
2. Prioritize within 48 hours
3. Update weekly on progress

Priority Framework:
| Priority | Criteria | Response Time |
|----------|----------|---------------|
| P0 (Critical) | Outage, data loss, security | Immediate (hours) |
| P1 (High) | Severe degradation | 1-2 days |
| P2 (Medium) | Moderate impact | 1-2 weeks |
| P3 (Low) | Minor issue | Next sprint |

Template Response:
```markdown
Thanks for reporting this!

**Priority:** P1 (High)
**Estimated Fix:** 1-2 days
**Workaround:** Use X instead of Y
**Tracking:** Issue #123

Updates will be posted here.
```
```

---

### ❌ Anti-Pattern: No Iteration Planning

**Problem:**
```markdown
Release features
Never review what worked/didn't work
Repeat same mistakes in next sprint
```

**Impact:**
- Same bugs recur
- Process doesn't improve
- Team doesn't learn
- Velocity stagnates

**Solution:**
```markdown
✅ GOOD:
Feedback loop drives iteration

Sprint Retrospective (weekly):
1. What went well?
2. What didn't go well?
3. What should we change?

Metrics Review (monthly):
- Velocity trend
- Defect rate
- Cycle time
- Test coverage

Process Updates:
- Document learnings
- Update workflows
- Adjust estimates
- Improve tooling

Example:
Issue: 40% of bugs in error handling
Action: Add error handling checklist to PR template
Result: 60% reduction in error bugs next sprint
```

---

## Cross-Cutting Anti-Patterns

### ❌ Anti-Pattern: No Documentation

**Problem:**
```markdown
Code with no comments, no API docs, no README
"The code is self-documenting" (it's not)
```

**Impact:**
- Onboarding takes 2-3 weeks
- Same questions asked repeatedly
- Knowledge loss when people leave
- AI agents can't understand codebase

**Solution:**
```markdown
✅ GOOD:
Documentation as first-class deliverable

Documentation Checklist:
- [ ] README.md (project overview)
- [ ] AGENTS.md (machine-readable instructions)
- [ ] API reference (user-docs/reference/)
- [ ] How-to guides (user-docs/how-to/)
- [ ] Architecture docs (dev-docs/)
- [ ] Code comments (why, not what)

Enforcement:
- PR blocked if docs missing
- CI extracts and tests code examples
- Quarterly docs review for staleness
```

**Reference:** [DOCUMENTATION_STANDARD.md](../DOCUMENTATION_STANDARD.md)

---

### ❌ Anti-Pattern: Copy-Paste Programming

**Problem:**
```markdown
Copy code from Stack Overflow
Paste without understanding
Works (maybe), but introduces vulnerabilities/bugs
```

**Impact:**
- Security vulnerabilities
- Licensing violations
- Bugs propagate across codebase
- No learning

**Solution:**
```markdown
✅ GOOD:
Understand before using

Process:
1. Read and understand code
2. Verify license compatibility
3. Test in isolation
4. Adapt to your use case
5. Document source (attribution)
6. Write tests

For AI-generated code:
- Review ALL generated code
- Test thoroughly
- Verify no hallucinations
- Check for security issues
```

---

### ❌ Anti-Pattern: No Error Handling

**Problem:**
```markdown
Code assumes happy path
No try-catch, no validation, no fallbacks
```

**Impact:**
- Crashes in production
- Poor user experience
- Data loss
- Security vulnerabilities

**Solution:**
```markdown
✅ GOOD:
Defensive programming

Error Handling Checklist:
- [ ] Validate all inputs
- [ ] Handle all exceptions
- [ ] Provide helpful error messages
- [ ] Log errors with context
- [ ] Fail gracefully (fallbacks)

Example:
```python
def validate_config(path: str) -> ValidationResult:
    """Validate configuration file."""
    try:
        # Validate input
        if not path:
            raise ValueError("config_path cannot be empty")

        # Load file
        with open(path) as f:
            config = yaml.safe_load(f)

        # Validate schema
        errors = _validate_schema(config)

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors
        )

    except FileNotFoundError:
        return ValidationResult(
            valid=False,
            errors=[f"Configuration file not found: {path}"]
        )

    except yaml.YAMLError as e:
        return ValidationResult(
            valid=False,
            errors=[f"Invalid YAML syntax: {e}"]
        )

    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error validating {path}", exc_info=e)
        return ValidationResult(
            valid=False,
            errors=["An unexpected error occurred. Please check logs."]
        )
```
```

---

### ❌ Anti-Pattern: Premature Optimization

**Problem:**
```markdown
Optimize before measuring
"This might be slow" → spend 1 week optimizing
Turns out it wasn't a bottleneck
```

**Impact:**
- Wasted 1 week
- Code more complex
- Harder to maintain
- Actual bottlenecks not fixed

**Solution:**
```markdown
✅ GOOD:
Measure first, optimize second

Process:
1. Make it work (correctness)
2. Make it right (design)
3. Make it fast (optimization)

Optimization Workflow:
1. Measure performance (profiling)
2. Identify bottlenecks (data-driven)
3. Optimize hot paths only
4. Measure again (verify improvement)

Example:
```python
# Step 1: Make it work
def process_items(items):
    results = []
    for item in items:
        results.append(expensive_operation(item))
    return results


# Step 2: Measure
import cProfile
cProfile.run('process_items(data)')
# Result: expensive_operation takes 95% of time


# Step 3: Optimize bottleneck
def process_items(items):
    # Cache expensive operation results
    cache = {}
    results = []
    for item in items:
        if item not in cache:
            cache[item] = expensive_operation(item)
        results.append(cache[item])
    return results


# Step 4: Measure again
# Result: 10x faster
```

Rule: Profile before optimizing
```

---

## Quick Reference

### Decision Tree: Is This an Anti-Pattern?

```
Are you about to...?
│
├─ Start coding without documentation?
│  └─ ❌ ANTI-PATTERN: Skipping DDD
│     Solution: Write API docs first
│
├─ Write tests after implementation?
│  └─ ❌ ANTI-PATTERN: Test-after development
│     Solution: Use TDD (test-first)
│
├─ Skip code review to ship faster?
│  └─ ❌ ANTI-PATTERN: Rubber-stamp reviews
│     Solution: Thorough review with checklist
│
├─ Deploy without monitoring?
│  └─ ❌ ANTI-PATTERN: Deploy and forget
│     Solution: Set up metrics and alerts
│
├─ Copy-paste code without understanding?
│  └─ ❌ ANTI-PATTERN: Copy-paste programming
│     Solution: Understand, adapt, test
│
└─ Optimize without measuring?
   └─ ❌ ANTI-PATTERN: Premature optimization
      Solution: Measure first, optimize second
```

---

### Most Impactful Anti-Patterns to Avoid

**Top 5 by Cost:**

1. **Skipping DDD** (Coding before design)
   - Cost: 40-60% of dev time wasted on rework
   - Solution: 3-5 hours DDD upfront

2. **No Test Strategy** (Test-after or no tests)
   - Cost: 40-80% more defects, 2x maintenance time
   - Solution: TDD + BDD + test pyramid

3. **No Code Review** (Rubber-stamp approvals)
   - Cost: 3x more production bugs
   - Solution: Thorough review with checklist

4. **Manual Releases** (Error-prone deployment)
   - Cost: 15% failed releases, 2-4 hours each
   - Solution: Automated release pipeline

5. **Deploy and Forget** (No monitoring)
   - Cost: Extended outages, user churn
   - Solution: Metrics, alerts, on-call

---

### Red Flags Checklist

**Warning signs you're in anti-pattern territory:**

- [ ] "We'll add tests/docs later" (never happens)
- [ ] "Just ship it, we'll fix bugs in production"
- [ ] "Code review? Just LGTM it"
- [ ] "Let's skip the planning and start coding"
- [ ] "Copy this from Stack Overflow" (without understanding)
- [ ] "This might be slow, let's optimize first" (no data)
- [ ] "Users will figure it out" (no error messages)
- [ ] "It works on my machine" (no CI/CD)
- [ ] "We don't have time for refactoring"
- [ ] "The code is self-documenting" (no docs)

**If you hear these phrases, STOP and review this guide.**

---

## Summary

**Anti-patterns are expensive:**
- 40-60% of development time wasted
- 3-10x more defects
- Lower team morale
- Technical debt accumulates

**Solutions are evidence-based:**
- DDD reduces rework by 40-60%
- TDD reduces defects by 40-80%
- Code review catches 60% of bugs
- Automated releases: 0% error rate vs 15% manual

**Key Principle:**
> Prevention is cheaper than cure. Invest upfront in process, save 10x on fixes.

---

## Related Documentation

- [DEVELOPMENT_PROCESS.md](workflows/DEVELOPMENT_PROCESS.md) - 8-phase process
- [DDD_WORKFLOW.md](workflows/DDD_WORKFLOW.md) - Documentation-first design
- [BDD_WORKFLOW.md](workflows/BDD_WORKFLOW.md) - Behavior-driven development
- [TDD_WORKFLOW.md](workflows/TDD_WORKFLOW.md) - Test-driven development
- [DEVELOPMENT_LIFECYCLE.md](workflows/DEVELOPMENT_LIFECYCLE.md) - Integration guide

---

**Version:** 1.0.0
**Created:** 2025-10-25
**Last Updated:** 2025-10-25
**Maintained By:** Project team
**Next Review:** Quarterly

---

**Remember:** Anti-patterns are patterns that appear useful but lead to negative consequences. Avoid them to save time, reduce defects, and improve team effectiveness.
