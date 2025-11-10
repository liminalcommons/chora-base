# SAP-012: Development Lifecycle

**Version:** 1.2.0 | **Status:** Active | **Maturity:** Production

> 8-phase development lifecycle integrating DDD → BDD → TDD—40-80% defect reduction through Documentation-First → Gherkin scenarios → Red-Green-Refactor cycles.

---

## 🚀 Quick Start (2 minutes)

```bash
# Phase 2: Create sprint plan
just create-sprint-plan $(date +%Y-%m-%d)

# Phase 3: Write how-to guide BEFORE implementation (Documentation-First)
cat > docs/user-docs/how-to/feature-name.md <<'EOF'
# How to Use Feature Name
[Step-by-step user instructions with expected behaviors]
EOF

# Phase 3: Extract BDD scenarios from how-to (L3 pattern)
just doc-to-bdd docs/user-docs/how-to/feature-name.md

# Phase 4: Implement using BDD → TDD
just bdd-scenario features/feature-name.feature  # Confirm RED
just tdd-cycle tests/test_feature.py              # Red → Green → Refactor

# Phase 5: Quality gates
just quality-gates                                # Coverage, linting, types

# Phase 7: Release
just bump-version minor                           # 1.2.0 → 1.3.0
just prepare-release                              # Changelog, tag, build
```

**First time?** → Read [protocol-spec.md](protocol-spec.md) for complete 8-phase lifecycle (20-min read)

---

## 📖 What Is SAP-012?

SAP-012 provides the **8-phase development lifecycle** from Vision (months) → Planning (weeks) → Requirements (days) → Development (days-weeks) → Testing (hours-days) → Review (hours-days) → Release (hours) → Monitoring (continuous). It integrates **DDD → BDD → TDD** methodologies into a unified workflow, achieving 40-80% defect reduction through Documentation-First development.

**Key Innovation**: **L3 Documentation-First Pattern** - Write executable how-to guides BEFORE implementation, extract BDD scenarios from docs, then implement using TDD. This ensures user-facing behavior is defined first, with automated tests verifying documentation accuracy.

---

## 🎯 When to Use

Use SAP-012 when you need to:

1. **Reduce defects** - 40-80% defect reduction through BDD + TDD (research-backed)
2. **Align on requirements** - Documentation-First ensures stakeholder agreement before coding
3. **Maintain velocity** - Structured lifecycle prevents rework and technical debt
4. **Quality-first development** - Built-in quality gates at every phase
5. **Continuous improvement** - Phase 8 monitoring feeds back into planning

**Not needed for**: Quick prototypes (<1 day), throwaway code, or experimental work

---

## ✨ Key Features

- ✅ **8-Phase Lifecycle** - Vision → Planning → Requirements → Development → Testing → Review → Release → Monitoring
- ✅ **40-80% Defect Reduction** - Research-backed from BDD + TDD integration
- ✅ **Documentation-First (L3)** - Write how-to guides → Extract BDD → Implement with TDD
- ✅ **BDD → TDD Integration** - Gherkin scenarios (behavior) → pytest tests (implementation)
- ✅ **Quality Gates** - ≥85% coverage, ruff linting, mypy types, security scanning
- ✅ **LIGHT+ Planning** - Sprint templates with 4 planning constructs
- ✅ **Semantic Versioning** - Automated version bumping (major.minor.patch)
- ✅ **Continuous Monitoring** - Metrics, feedback, iteration planning

---

## 📚 Quick Reference

### 8 Lifecycle Phases

#### **Phase 1: Vision & Strategy** (Months)
- **Purpose**: Define long-term strategic roadmap
- **Artifacts**: ROADMAP.md, vision statements
- **Duration**: 3-12 months per cycle
- **Skip in**: Interactive sessions (vision usually pre-defined)

---

#### **Phase 2: Planning & Prioritization** (Weeks)
- **Purpose**: Break vision into sprint-sized tasks
- **Artifacts**: Sprint plans (sprint-template.md), backlog
- **Duration**: 1-2 weeks per sprint
- **Commands**:
```bash
just create-sprint-plan $(date +%Y-%m-%d)  # Generate sprint plan
bd create "Feature task" --priority high   # Add to .beads/issues.jsonl (SAP-015)
```

**LIGHT+ Planning Constructs** (4 types):
1. **LIGHT** - Default planning construct (80% of work)
2. **WAVE** - Coordinated multi-repo feature (cross-SAP work)
3. **CAMPAIGN** - Multi-month strategic initiative
4. **EXPEDITION** - High-risk, high-reward exploration

See [LIGHT_PLUS_REFERENCE.md](LIGHT_PLUS_REFERENCE.md) for complete details.

---

#### **Phase 3: Requirements & Design** (Days)

**L3 Documentation-First Pattern** (Recommended):

```bash
# 1. Write executable how-to guide BEFORE implementation
cat > docs/user-docs/how-to/user-authentication.md <<'EOF'
---
audience: [end-users, developers]
time: 5 minutes
prerequisites: [Account]
difficulty: beginner
---

# How to Authenticate Users

## Quick Start
1. User navigates to /login
2. User enters email and password
3. System validates credentials
4. System redirects to dashboard on success
5. System shows error message on failure

## Expected Behaviors
- Valid credentials → Dashboard
- Invalid credentials → Error "Invalid email or password"
- Missing fields → Error "Email and password required"
EOF

# 2. Extract BDD scenarios from how-to (automated)
just doc-to-bdd docs/user-docs/how-to/user-authentication.md

# 3. Output: features/user-authentication.feature with Gherkin scenarios
cat features/user-authentication.feature
# Feature: User Authentication
#   Scenario: Successful login
#     Given user is on /login
#     When user enters valid email and password
#     Then user is redirected to dashboard
```

**L2 Manual BDD** (Alternative):
Write Gherkin scenarios manually if docs don't exist or for non-user-facing features.

**Artifacts**:
- Diátaxis how-to guides (user-facing behavior)
- BDD .feature files (Gherkin scenarios)
- API specs (technical contracts)

---

#### **Phase 4: Development (BDD + TDD)** (Days-Weeks)

**BDD → TDD Workflow**:

```bash
# 1. Confirm BDD scenarios are RED (not implemented)
pytest features/user-authentication.feature --gherkin
# ❌ FAILED: Scenario "Successful login" (steps not implemented)

# 2. Implement using TDD cycles
just tdd-cycle tests/test_authentication.py

# TDD Cycle (repeat until BDD scenarios GREEN):
# Step 1: Write test (RED)
def test_validate_credentials_success():
    assert validate_credentials("user@example.com", "password123") == True

# Step 2: Implement minimal code (GREEN)
def validate_credentials(email, password):
    # Minimal implementation
    return email and password

# Step 3: Refactor (stay GREEN)
def validate_credentials(email, password):
    # Production-quality implementation
    user = db.query(User).filter_by(email=email).first()
    return user and user.check_password(password)

# 3. Confirm BDD scenarios turn GREEN
pytest features/user-authentication.feature --gherkin
# ✅ PASSED: Scenario "Successful login"
```

**Artifacts**:
- .feature files (BDD scenarios)
- tests/ (unit tests)
- src/ (implementation code)

---

#### **Phase 5: Testing & Quality** (Hours-Days)

**4 Testing Layers**:
1. **Unit Tests** - Isolated component testing
2. **Smoke Tests** - Critical path validation (5-10 seconds)
3. **Integration Tests** - Multi-component workflows
4. **E2E Tests** - Full user journey (optional, for web apps)

**Quality Gates**:
```bash
just quality-gates                        # Run all gates
# 1. Coverage: ≥85% (pytest --cov)
# 2. Linting: ruff check (200x faster than flake8)
# 3. Type checking: mypy (strict mode)
# 4. Security: bandit scan (SAP-005)
# 5. BDD scenarios: All GREEN
```

**Artifacts**: Coverage reports, test results, quality metrics

---

#### **Phase 6: Review & Integration** (Hours-Days)

**Review Checklist**:
- ✅ Code review (GitHub PR)
- ✅ Documentation review (Diátaxis completeness)
- ✅ CI/CD passes (all quality gates GREEN)
- ✅ BDD scenarios pass (user-facing behavior verified)
- ✅ Security scan passes (0 critical vulnerabilities)

**Commands**:
```bash
git push origin feature-branch           # Push to GitHub
# CI runs automatically (SAP-005):
# - pytest with coverage
# - ruff linting
# - mypy type checking
# - security scanning (bandit)
```

**Artifacts**: PR reviews, CI logs, approval sign-offs

---

#### **Phase 7: Release & Deployment** (Hours)

**Release Workflow**:
```bash
# 1. Bump version (semantic versioning)
just bump-version minor                  # 1.2.0 → 1.3.0 (new features)
just bump-version patch                  # 1.2.0 → 1.2.1 (bug fixes)
just bump-version major                  # 1.2.0 → 2.0.0 (breaking changes)

# 2. Prepare release
just prepare-release                     # Generate changelog, create git tag, build packages

# 3. Publish to PyPI
just publish-test                        # Test PyPI (validate first)
just publish-prod                        # Production PyPI

# 4. Deploy to production (if applicable)
just deploy-prod                         # Platform-specific deployment
```

**Artifacts**: Git tags, PyPI packages, deployment artifacts

---

#### **Phase 8: Monitoring & Feedback** (Continuous)

**Monitoring Activities**:
```bash
# Track metrics (SAP-013)
just track-claude-session                # ROI tracking
just metrics-summary                     # Quality, velocity, process

# Review feedback
cat .chora/memory/events/errors.jsonl   # Error patterns (SAP-010)
gh issue list --state open              # Bug reports

# Plan next iteration
just create-sprint-plan $(date +%Y-%m-%d)  # Phase 2 planning
```

**Artifacts**:
- PROCESS_METRICS.md
- Retrospective notes
- Bug reports and feature requests
- Iteration plans

---

## 🔗 Integration with Other SAPs

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-015** (Task Tracking) | Phase 2 | Sprint plans → `.beads/issues.jsonl` tasks |
| **SAP-007** (Documentation) | Phase 3 | Diátaxis how-to guides → BDD extraction |
| **SAP-004** (Testing) | Phase 4-5 | pytest framework for TDD + BDD |
| **SAP-006** (Quality Gates) | Phase 5 | Pre-commit hooks enforce quality |
| **SAP-005** (CI/CD) | Phase 6 | GitHub Actions automate testing + deployment |
| **SAP-013** (Metrics) | Phase 8 | Track development velocity and quality |
| **SAP-010** (A-MEM) | Phase 8 | Event-sourced development history |

**Cross-SAP Workflow Example**:
```bash
# Phase 2: Planning (SAP-015)
bd create "Add user authentication" --priority high --trace-id SPRINT-W45

# Phase 3: Requirements (SAP-007)
cat > docs/user-docs/how-to/user-authentication.md
just doc-to-bdd docs/user-docs/how-to/user-authentication.md

# Phase 4: Development (SAP-004, SAP-012)
just bdd-scenario features/user-authentication.feature
just tdd-cycle tests/test_authentication.py

# Phase 5: Quality (SAP-006)
git add . && git commit -m "Add authentication"  # Pre-commit hooks run

# Phase 6: Review (SAP-005)
git push origin feature-auth
# GitHub Actions CI runs tests, linting, type checking

# Phase 7: Release (SAP-012)
just bump-version minor
just prepare-release
just publish-prod

# Phase 8: Monitoring (SAP-013, SAP-010)
just track-claude-session
echo '{"timestamp":"'$(date -Iseconds)'","event_type":"milestone","description":"Shipped authentication"}' >> .chora/memory/events/development.jsonl
```

---

## 🏆 Success Metrics

- **Defect Reduction**: 40-80% fewer bugs (research-backed from BDD + TDD)
- **Velocity Maintenance**: No slowdown vs pure TDD (L3 pattern eliminates doc debt)
- **Coverage**: ≥85% test coverage (sweet spot for cost/benefit)
- **Documentation Quality**: 100% of features have executable how-to guides
- **BDD Adherence**: ≥80% of user-facing features use BDD scenarios
- **TDD Adherence**: ≥90% of implementation follows Red-Green-Refactor

---

## 🔧 Troubleshooting

**Problem**: BDD scenarios failing even though unit tests pass

**Solution**: This is expected during TDD implementation. BDD scenarios test user-facing behavior (integration level), while unit tests verify components. Continue TDD cycles until BDD scenarios turn GREEN:
```bash
pytest features/ --gherkin -v            # Show which BDD steps fail
pytest tests/ -v                         # Verify unit tests pass

# Focus TDD on missing behavior until BDD GREEN
just tdd-cycle tests/test_integration.py
```

---

**Problem**: Documentation-First feels slow (Phase 3)

**Solution**: L3 pattern saves 60% time overall despite upfront documentation cost. Benefits:
- **Stakeholder alignment** - Catch requirement issues before coding
- **Automated BDD** - `doc-to-bdd` extracts scenarios automatically
- **Zero doc debt** - Documentation never falls behind implementation
- **Onboarding** - New developers read how-to guides to understand features

**Shortcut for internal/technical features**: Use L2 Manual BDD (skip how-to, write Gherkin directly)

---

**Problem**: TDD cycles take too long (Phase 4)

**Solution**: Use smoke tests for fast feedback during development:
```bash
just smoke                               # Run only critical path tests (5-10s)
just tdd-cycle tests/test_feature.py     # Full TDD cycle when ready

# Optimize pytest:
pytest tests/test_feature.py -v          # Run single test file
pytest tests/test_feature.py::test_name  # Run single test
pytest --lf                              # Re-run last failures only
```

**Expected**: Smoke tests <10s, full test suite <60s

---

**Problem**: Phase 5 quality gates blocking commits

**Solution**: Fix issues locally before committing:
```bash
just quality-gates                       # Identify all issues at once

# Fix each gate:
just lint-fix                            # Auto-fix linting (ruff)
just format                              # Auto-format code
just type-check                          # Show type errors (fix manually)
pytest --cov=src --cov-report=term-missing  # Identify uncovered lines

# Retry commit
git add . && git commit -m "Add feature"
```

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete 8-phase lifecycle specification (72KB, 40-min read)
- **[AGENTS.md](AGENTS.md)** - Agent-specific lifecycle workflows (18KB, 10-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude Code patterns for lifecycle (16KB, 8-min read)
- **[LIGHT_PLUS_REFERENCE.md](LIGHT_PLUS_REFERENCE.md)** - LIGHT+ planning constructs (12KB, 6-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Lifecycle setup guide (20KB, 10-min read)
- **[capability-charter.md](capability-charter.md)** - Problem statement and solution design
- **[ledger.md](ledger.md)** - Production adoption metrics

---

**Version History**:
- **1.2.0** (2025-11-08) - Added L3 Documentation-First pattern, doc-to-bdd extraction
- **1.1.0** (2025-10-28) - Added LIGHT+ planning constructs
- **1.0.0** (2025-06-15) - Initial 8-phase lifecycle with DDD → BDD → TDD

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
