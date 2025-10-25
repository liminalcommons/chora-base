---
title: Release Planning Guide
category: project-management
audience: human-developers, ai-agents
lifecycle_phase: phase-7-release
created: 2025-10-25
updated: 2025-10-25
---

# Release Planning Guide

**Purpose**: Guide for planning, executing, and documenting software releases using the chora-base framework.

**Audience**: Human developers, AI agents, release managers, stakeholders

**Related Workflows**:
- [8-Phase Development Process](../../dev-docs/workflows/DEVELOPMENT_PROCESS.md) (Phase 7: Release & Deployment)
- [Development Lifecycle](../../dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md)

---

## Quick Start

### For AI Agents: Release Planning Decision Tree

```
START: Release planning needed
    ↓
Q1: What type of release?
    MAJOR (vX.0.0) → Breaking changes, requires migration
    MINOR (v1.X.0) → New features, backward compatible
    PATCH (v1.1.X) → Bug fixes only
    ↓
Q2: Are all features complete?
    NO → Complete sprints first, ensure feature readiness
    YES → Continue
    ↓
Q3: Are quality gates met?
    NO → Address test coverage, bugs, security issues
    YES → Continue
    ↓
Q4: Is documentation complete?
    NO → Update docs, create upgrade guide, write changelog
    YES → Continue
    ↓
EXECUTE: Create release plan
    1. Copy release-template.md to release-vX.Y.Z.md
    2. Fill in features, changes, metrics
    3. Create deployment plan
    4. Execute pre-release checklist
    5. Deploy to staging (RC testing)
    6. Deploy to production
    7. Monitor and communicate
    ↓
OUTCOME: Release deployed → Start Phase 8 (Monitoring & Feedback)
```

---

## What is a Release?

**Definition**: A packaged version of the software that delivers value to users, marked with a version number and deployed to production.

**Release Types** (Semantic Versioning):
1. **MAJOR** (vX.0.0) - Breaking changes requiring adopter action
2. **MINOR** (v1.X.0) - New features, backward compatible
3. **PATCH** (v1.1.X) - Bug fixes only

**Release Components**:
1. **Code** - Tagged version in git
2. **Documentation** - Updated docs, changelog, upgrade guide
3. **Artifacts** - Built packages (PyPI, Docker, etc.)
4. **Communication** - Release notes, blog post, announcements
5. **Deployment** - Production deployment and monitoring

**Release Lifecycle**:
```
Planning
    ↓
Development (Sprints)
    ↓
Feature Freeze
    ↓
Code Freeze
    ↓
Release Candidate (RC) Testing
    ↓
Production Deployment
    ↓
Monitoring & Communication
    ↓
Retrospective
```

---

## Semantic Versioning

### Version Format: MAJOR.MINOR.PATCH

**MAJOR** (X.0.0):
- Breaking API changes
- Removed deprecated features
- Significant architecture changes
- Requires adopter migration effort

**Examples**:
- v1.0.0 → v2.0.0: Remove deprecated `old_api()`, change config format
- v2.0.0 → v3.0.0: Rewrite core engine, new plugin system

**MINOR** (1.X.0):
- New features (backward compatible)
- Enhanced functionality
- New API endpoints (additive)
- Performance improvements

**Examples**:
- v1.5.0 → v1.6.0: Add new `analytics_dashboard()` feature
- v1.6.0 → v1.7.0: Add OAuth2 authentication option

**PATCH** (1.1.X):
- Bug fixes only
- Security patches
- Documentation corrections
- No new features

**Examples**:
- v1.5.0 → v1.5.1: Fix crash on invalid input
- v1.5.1 → v1.5.2: Security patch for dependency vulnerability

### Pre-Release Versions

**Format**: vX.Y.Z-rc.N (Release Candidate)

**Examples**:
- v2.0.0-rc.1 → First release candidate for v2.0.0
- v2.0.0-rc.2 → Second release candidate (if issues found in RC1)
- v2.0.0 → Final production release

**Alpha/Beta** (optional):
- v2.0.0-alpha.1 → Early development, unstable
- v2.0.0-beta.1 → Feature complete, testing phase
- v2.0.0-rc.1 → Final testing before production

---

## Release Planning

### Step 1: Determine Release Type

**Decision Matrix**:

| Change Type | Impact | Version Bump | Migration Effort |
|-------------|--------|--------------|------------------|
| **Breaking API change** | High | MAJOR | High (hours-days) |
| **Remove deprecated feature** | High | MAJOR | Medium (hours) |
| **Add new feature** | Medium | MINOR | Low (minutes) |
| **Improve performance** | Medium | MINOR | None (automatic) |
| **Fix bug** | Low | PATCH | None (automatic) |
| **Security patch** | Variable | PATCH | None (automatic) |

**Examples**:

```python
# Breaking change → MAJOR
# v1.x: def process(data: dict) -> dict:
# v2.0: def process(data: DataModel) -> Result:  # Type change!

# New feature → MINOR
# v1.5: (no analytics)
# v1.6: def get_analytics() -> AnalyticsReport:  # New function!

# Bug fix → PATCH
# v1.5.0: Bug in error handling
# v1.5.1: Fixed error handling (no API change)
```

### Step 2: Define Release Scope

**Scope Elements**:
1. **Target Sprints** - Which sprints contribute to this release?
2. **Features** - What new capabilities?
3. **Improvements** - What enhancements?
4. **Bug Fixes** - What issues resolved?
5. **Technical Debt** - What refactoring included?

**Scope Matrix**:

| Sprint | Features | Improvements | Bugs Fixed | Included in Release |
|--------|----------|--------------|------------|---------------------|
| Sprint 5 | OAuth2 login | Performance tuning | #123, #124 | ✅ v1.6.0 |
| Sprint 6 | Analytics dashboard | API caching | #125 | ✅ v1.6.0 |
| Sprint 7 | Export to CSV | UI polish | #126, #127 | ❌ v1.7.0 (next) |

**Release Scope Document**:
```markdown
## Release v1.6.0 Scope

**Sprints**: Sprint 5-6 (4 weeks)

**Features** (MINOR):
- OAuth2 authentication (Google, GitHub)
- User analytics dashboard (DAU, sessions, activity)

**Improvements**:
- API response time reduced by 50% (300ms → 150ms)
- Database query optimization with caching

**Bug Fixes**:
- Fixed crash on invalid OAuth token (#123)
- Fixed session timeout handling (#124)
- Fixed dashboard timezone bug (#125)

**Out of Scope** (deferred to v1.7.0):
- Export to CSV feature (Sprint 7)
- Email notifications (Sprint 8)
```

### Step 3: Create Release Plan

**Use Template**:
```bash
# Copy release template
cp project-docs/releases/release-template.md project-docs/releases/release-v1.6.0.md

# Fill in all sections
code project-docs/releases/release-v1.6.0.md
```

**Required Sections to Complete**:
1. **Executive Summary** - High-level overview for stakeholders
2. **Features & Changes** - Detailed list of what's included
3. **Quality & Testing** - Test coverage, performance benchmarks
4. **Documentation** - Updated docs, upgrade guide
5. **Deployment Plan** - Step-by-step deployment process
6. **Communication Plan** - How to announce the release

### Step 4: Quality Gates

**Pre-Release Quality Checklist**:

**Code Quality**:
- [ ] All planned features merged to main
- [ ] Test coverage ≥90% (unit + integration)
- [ ] All CI/CD checks passing
- [ ] Code review backlog cleared (0 pending PRs)
- [ ] Static analysis passing (linting, type checking)

**Testing**:
- [ ] Unit tests passing (100% of tests)
- [ ] Integration tests passing
- [ ] E2E tests passing for critical user flows
- [ ] Performance benchmarks met (response time, throughput)
- [ ] Load testing completed (if applicable)
- [ ] Security scan completed (0 critical/high vulnerabilities)

**Documentation**:
- [ ] CHANGELOG.md updated with all changes
- [ ] Upgrade guide created (docs/upgrades/vX.Y-to-vX.Z.md)
- [ ] API reference updated for new features
- [ ] User documentation updated
- [ ] README.md updated (if needed)

**Bugs**:
- [ ] 0 critical (P0) bugs open
- [ ] 0 high (P1) bugs open
- [ ] <3 medium (P2) bugs open (documented in known issues)

**Stakeholder Approval**:
- [ ] Product owner approval
- [ ] Engineering lead approval
- [ ] QA/Testing sign-off
- [ ] Security review (if applicable)

**Red Flags** (do NOT release if any present):
- 🚨 Critical bug discovered
- 🚨 Test coverage dropped below 85%
- 🚨 Performance regression >10%
- 🚨 Security vulnerability (high/critical)
- 🚨 Incomplete migration guide (for MAJOR release)

---

## Release Candidate (RC) Testing

### What is an RC?

**Definition**: A potentially shippable version of the software, deployed to staging for final validation before production.

**Purpose**:
- Final integration testing
- User acceptance testing (UAT)
- Performance/load testing
- Documentation review
- Go/No-Go decision

**Timeline**: 3-7 days before production release

### RC Testing Process

**Day -7: Deploy RC1 to Staging**

```bash
# 1. Create RC tag
git checkout main
git pull origin main
git tag v1.6.0-rc.1
git push origin v1.6.0-rc.1

# 2. Deploy to staging
just deploy-staging

# 3. Run smoke tests
just test-smoke-staging

# 4. Verify deployment
just verify-staging
```

**Day -7 to -1: RC Testing**

**Test Plan**:
1. **Automated Tests** (Day -7, 2 hours)
   - Run full test suite on staging
   - Performance benchmarks
   - Security scan

2. **Manual Testing** (Day -6 to -4, 1 day)
   - Test new features end-to-end
   - Exploratory testing
   - Cross-browser/platform testing (if applicable)

3. **User Acceptance Testing** (Day -4 to -2, 2 days)
   - Stakeholder testing
   - Beta user testing (if applicable)
   - Feedback collection

4. **Documentation Review** (Day -2, 4 hours)
   - Verify upgrade guide accuracy
   - Test migration steps on example project
   - Review release notes

5. **Go/No-Go Meeting** (Day -1, 1 hour)
   - Review test results
   - Review metrics
   - Decision: Ship or Fix-and-Retest

**RC Test Checklist**:
- [ ] All automated tests passing on staging
- [ ] Manual testing completed (no critical bugs found)
- [ ] UAT completed (stakeholder approval)
- [ ] Performance benchmarks met on staging
- [ ] Security scan passed
- [ ] Documentation verified (upgrade guide tested)
- [ ] Monitoring configured and tested
- [ ] Rollback plan tested

**If Issues Found**:

**Minor Issues** (P2/P3 bugs):
- Document in "Known Issues"
- Plan fix for next PATCH release
- Proceed with release

**Major Issues** (P0/P1 bugs):
- Fix immediately
- Deploy RC2 to staging
- Re-test (3-day cycle)
- New Go/No-Go meeting

---

## Production Deployment

### Pre-Deployment Checklist

**Final Verification** (Day 0, morning):
- [ ] RC testing completed successfully
- [ ] Go/No-Go approval obtained
- [ ] Deployment window scheduled
- [ ] On-call team notified
- [ ] Rollback plan reviewed
- [ ] Communication plan ready

**Deployment Window**:
- **Recommended**: Tuesday-Thursday, 10 AM - 2 PM (local time)
- **Avoid**: Friday, Monday, holidays, end-of-quarter
- **Rationale**: Support team available, time to fix issues, avoid weekend on-call

### Deployment Steps

**Step 1: Tag Final Release** (5 minutes)

```bash
# 1. Tag final release
git checkout main
git pull origin main
git tag v1.6.0
git push origin v1.6.0

# 2. Create GitHub release
gh release create v1.6.0 \
  --title "v1.6.0 - OAuth2 & Analytics" \
  --notes-file project-docs/releases/release-v1.6.0-notes.md
```

**Step 2: Build Artifacts** (10-30 minutes)

```bash
# Python package (PyPI)
just build-package
just publish-package  # Publishes to PyPI

# Docker image
just build-docker
just push-docker  # Pushes to Docker registry

# Verify artifacts
just verify-artifacts
```

**Step 3: Deploy to Production** (15-30 minutes)

```bash
# 1. Deploy to production
just deploy-production

# 2. Run smoke tests
just test-smoke-production

# 3. Verify deployment
just verify-production
```

**Step 4: Monitor** (First 24 hours)

**Immediate Monitoring** (First 1 hour):
- [ ] Error rate <0.1% (baseline: 0.05%)
- [ ] Response time within 10% of baseline (p95 <165ms)
- [ ] No spike in support tickets
- [ ] All critical endpoints responding

**Extended Monitoring** (First 24 hours):
- [ ] Error rate stable
- [ ] Performance metrics stable
- [ ] User feedback positive
- [ ] No critical bug reports

**Monitoring Dashboard**:
```markdown
## Production Health (v1.6.0)

| Metric | Baseline | Current | Alert Threshold | Status |
|--------|----------|---------|-----------------|--------|
| Error Rate | 0.05% | 0.04% | >0.1% | ✅ |
| Response Time (p95) | 150ms | 145ms | >200ms | ✅ |
| Memory Usage | 480MB | 490MB | >550MB | ✅ |
| CPU Usage | 40% | 42% | >70% | ✅ |
| Active Users | 1,200 | 1,250 | <1,000 | ✅ |

**Status**: ✅ Healthy (All metrics within normal range)
```

### Rollback Plan

**When to Rollback**:
- 🚨 Error rate >0.5% (10x baseline)
- 🚨 Critical bug affecting >10% of users
- 🚨 Data loss or corruption detected
- 🚨 Security vulnerability exploited

**Rollback Procedure** (<5 minutes):

```bash
# 1. Rollback to previous version
just rollback-to v1.5.2

# 2. Verify rollback
just verify-production

# 3. Notify stakeholders
just notify-rollback v1.6.0 v1.5.2
```

**Post-Rollback**:
1. Identify root cause of failure
2. Fix in development branch
3. Re-test thoroughly
4. Create new RC (v1.6.1-rc.1)
5. Re-execute RC testing process

---

## Post-Release Activities

### Communication

**Release Announcement** (Day 0, within 1 hour of deployment):

**Channels**:
- [ ] GitHub release (automated by `gh release create`)
- [ ] Blog post (if major release)
- [ ] Email to users/adopters
- [ ] Social media (Twitter, LinkedIn)
- [ ] Slack/Discord announcement (if applicable)

**Example Release Notes** (public-facing):

```markdown
# Release v1.6.0: OAuth2 & Analytics

We're excited to announce v1.6.0, featuring OAuth2 authentication and a new analytics dashboard!

## Highlights

- ✨ **OAuth2 Login**: Sign in with Google or GitHub
- ✨ **Analytics Dashboard**: Track daily active users, sessions, and activity
- 🔧 **50% Faster API**: Reduced response times from 300ms to 150ms

## Upgrading

```bash
pip install --upgrade your-package-name
```

## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete details.

## Questions?

- Documentation: https://docs.example.com
- GitHub Issues: https://github.com/org/repo/issues
```

### Metrics Collection

**Track These Metrics** (1 week post-release):

**Adoption Metrics**:
- Downloads/installs (PyPI, Docker pulls)
- Upgrade rate (% of users on latest version)
- GitHub stars/watchers increase

**Quality Metrics**:
- Error rate (production)
- Support tickets opened
- Bug reports (GitHub issues)
- User satisfaction (feedback, ratings)

**Performance Metrics**:
- Response time (p50, p95, p99)
- Throughput (requests/sec)
- Resource usage (CPU, memory)

**Example Metrics Summary** (1 week post-release):

```markdown
## v1.6.0 Metrics (1 Week Post-Release)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **Downloads (PyPI)** | 500 | 650 | ✅ (+30%) |
| **Upgrade Rate** | 60% | 72% | ✅ |
| **Error Rate** | <0.1% | 0.06% | ✅ |
| **Support Tickets** | <10 | 4 | ✅ |
| **Bug Reports** | <5 | 2 | ✅ |
| **User Satisfaction** | >90% | 94% | ✅ |

**Overall Release Rating**: ⭐⭐⭐⭐⭐ (5/5)
```

### Release Retrospective

**Schedule**: 1 week after release
**Duration**: 1 hour
**Attendees**: Release team + stakeholders

**Agenda**:
1. **What Went Well?** (15 min)
2. **What Could Be Improved?** (15 min)
3. **Metrics Review** (15 min)
4. **Action Items for Next Release** (15 min)

**Retrospective Format**:

```markdown
## v1.6.0 Release Retrospective

### What Went Well ✅

- RC testing caught 2 critical bugs before production
- Deployment was smooth (30 minutes, zero downtime)
- Documentation was comprehensive and accurate
- User feedback overwhelmingly positive

### What Could Be Improved ⚠️

- RC testing took 7 days (target: 5 days)
  - Issue: UAT coordination delays
  - Solution: Schedule UAT testers earlier

- Post-release monitoring was manual
  - Issue: No automated alerts configured
  - Solution: Set up DataDog/New Relic alerts

### Action Items for Next Release

- [ ] Implement automated monitoring alerts (Owner: DevOps, Due: v1.7.0)
- [ ] Schedule UAT testers 2 weeks before RC (Owner: PM, Due: v1.7.0 planning)
- [ ] Create deployment runbook for on-call team (Owner: Eng Lead, Due: Sprint 9)

### Lessons Learned

1. **DDD/BDD/TDD prevented rework**: Zero features had to be reworked after merge
2. **Performance testing early paid off**: No surprises in production
3. **Upgrade guide testing is essential**: Found 2 errors in migration steps during RC
```

---

## Release Cadence

### Recommended Release Frequency

| Project Type | MAJOR | MINOR | PATCH |
|--------------|-------|-------|-------|
| **Fast-moving startup** | 6-12 months | 2-4 weeks | As needed |
| **Established product** | 12-24 months | 4-8 weeks | Weekly |
| **Enterprise/regulated** | 24+ months | 8-12 weeks | Bi-weekly |
| **Library/Framework** | 12-18 months | 8-12 weeks | As needed |

**chora-base Recommendation**: **4-6 week MINOR release cycle** (aligns with 2-3 sprints)

**Why 4-6 Weeks?**:
- ✅ Enough time to deliver meaningful features (2-3 sprints)
- ✅ Frequent enough to get user feedback quickly
- ✅ Manageable overhead for docs, testing, communication

**PATCH Releases**: As needed for critical bugs or security issues

### Release Calendar

**Example 6-Month Release Plan**:

| Version | Type | Planned Date | Sprints | Key Features |
|---------|------|--------------|---------|--------------|
| v1.6.0 | MINOR | 2025-02-15 | 5-6 | OAuth2, Analytics |
| v1.6.1 | PATCH | 2025-02-22 | - | Critical bug fix |
| v1.7.0 | MINOR | 2025-04-01 | 7-9 | Export, Notifications |
| v1.8.0 | MINOR | 2025-05-15 | 10-12 | Advanced search |
| v2.0.0 | MAJOR | 2025-07-01 | 13-16 | New plugin system |

**Communication**:
- Publish release calendar in README.md
- Update quarterly (adjust dates based on actual progress)
- Communicate delays early (better to delay than ship incomplete)

---

## Release Anti-Patterns

### ❌ Anti-Pattern: No Release Planning

**Problem**:
```
"Sprint 6 is done, let's release!"
- No release document
- No changelog
- No upgrade testing
- No communication plan
```

**Impact**:
- Users surprised by breaking changes
- Support tickets flood in
- Rollback required

**Solution**:
```markdown
✅ GOOD: Planned Release

- Release plan created 2 weeks before target date
- All sections completed (features, testing, docs, communication)
- RC testing conducted (7 days)
- Go/No-Go meeting held
- Communication prepared in advance
```

---

### ❌ Anti-Pattern: Skipping RC Testing

**Problem**:
```
"All tests pass in CI, ship directly to production!"
```

**Impact**:
- Integration issues discovered in production
- Data migration fails on real data
- Performance issues under load

**Solution**:
```markdown
✅ GOOD: RC Testing on Staging

- Deploy RC1 to staging (identical to production)
- Run full test suite on staging
- Conduct load testing
- Test upgrade path with real data
- UAT with stakeholders
- Fix issues, deploy RC2 if needed
```

---

### ❌ Anti-Pattern: "It Compiles, Ship It"

**Problem**:
```
Quality Gates:
- [ ] Tests passing (75% coverage)
- [x] CI/CD passing
- [ ] Documentation incomplete
- [ ] 5 critical bugs open
- [ ] No upgrade guide
```

**Impact**:
- Users can't upgrade (no migration guide)
- Bugs discovered in production
- Support team overwhelmed

**Solution**:
```markdown
✅ GOOD: Quality Gates Met

- [x] Tests passing (93% coverage)
- [x] CI/CD passing
- [x] Documentation complete
- [x] 0 critical/high bugs open
- [x] Upgrade guide tested
- [x] Stakeholder approval
```

---

### ❌ Anti-Pattern: Friday Deployments

**Problem**:
```
Deploy v1.6.0 on Friday at 5 PM
→ Critical bug discovered at 6 PM
→ On-call team scrambles over weekend
```

**Impact**:
- Weekend on-call stress
- Delayed rollback (team unavailable)
- User frustration (issue not fixed until Monday)

**Solution**:
```markdown
✅ GOOD: Tuesday-Thursday Deployment

Deploy v1.6.0 on Tuesday at 10 AM
- Support team available all day
- Time to monitor and fix issues same day
- Weekend free for team
- Users get timely support
```

**Exception**: Emergency security patches (deploy immediately, any day)

---

## For AI Agents: Release Execution Checklist

### Pre-Release Phase

**2 Weeks Before Release Date**:
- [ ] Create release plan (release-vX.Y.Z.md)
- [ ] Identify all features/changes for release
- [ ] Review quality gates (tests, coverage, bugs)
- [ ] Start drafting CHANGELOG.md entries

**1 Week Before Release Date**:
- [ ] Complete all planned features (feature freeze)
- [ ] Update all documentation
- [ ] Create upgrade guide (docs/upgrades/)
- [ ] Prepare release notes (public-facing)
- [ ] Schedule RC deployment to staging

### RC Testing Phase

**Day -7** (Deploy RC1):
- [ ] Create RC tag (v1.6.0-rc.1)
- [ ] Deploy to staging
- [ ] Run automated tests on staging
- [ ] Verify deployment successful

**Day -6 to -2** (Testing):
- [ ] Conduct manual testing
- [ ] Coordinate UAT with stakeholders
- [ ] Test upgrade path on example project
- [ ] Monitor staging metrics
- [ ] Document any issues found

**Day -1** (Go/No-Go):
- [ ] Review all test results
- [ ] Check quality gates
- [ ] Hold Go/No-Go meeting
- [ ] Decision: Ship or Fix-and-Retest

### Production Deployment

**Day 0** (Release Day):
- [ ] Tag final release (vX.Y.Z)
- [ ] Build artifacts (PyPI, Docker, etc.)
- [ ] Deploy to production
- [ ] Run smoke tests
- [ ] Verify deployment
- [ ] Publish GitHub release
- [ ] Send release announcement
- [ ] Monitor production metrics (first hour)

### Post-Release

**Day 1-7** (Monitoring):
- [ ] Monitor error rates daily
- [ ] Track adoption metrics
- [ ] Respond to user feedback
- [ ] Triage bug reports
- [ ] Update metrics in release document

**Day 7** (Retrospective):
- [ ] Collect metrics summary
- [ ] Hold release retrospective
- [ ] Document lessons learned
- [ ] Create action items for next release
- [ ] Update release document with final metrics

---

## References

**Related Documentation**:
- [8-Phase Development Process](../../dev-docs/workflows/DEVELOPMENT_PROCESS.md) - Phase 7: Release & Deployment
- [Development Lifecycle](../../dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) - Full lifecycle integration
- [Sprint Planning Guide](../sprints/README.md) - How sprints feed into releases
- [Anti-Patterns](../../dev-docs/ANTI_PATTERNS.md) - Release anti-patterns (Phase 7)

**Process Metrics**:
- [Process Metrics](../metrics/PROCESS_METRICS.md) - Release KPIs and measurement

**Version History**:
- [CHANGELOG.md](../../CHANGELOG.md) - Complete version history
- [Upgrade Guides](README.md) - chora-base version-specific migration guides

---

**Document Version**: 1.0
**Last Updated**: 2025-10-25
**Maintained By**: chora-base v3.0.0
**License**: MIT
