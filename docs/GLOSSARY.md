# Chora-base Ecosystem Glossary

**Purpose**: Comprehensive terminology index for the chora-base ecosystem. Enables discovery of concepts, understanding of relationships, and translation between natural language and formal ontology.

**Usage**:
```bash
# Search for a term
python scripts/chora-search.py "coordination request"

# Reverse lookup (description → term)
python scripts/chora-search.py --reverse "I want to suggest a big change"

# Find related terms
python scripts/chora-search.py --related "strategic proposal"

# List all terms in a category
python scripts/chora-search.py --category "Intake System"
```

**Structure**: Terms organized by category with aliases, related concepts, SAP references, and examples.

---

## Intake System

### Strategic Proposal
Type 1 intake for proposing major strategic directions reviewed quarterly by leadership and product teams.

**Aliases:** Type 1 intake, prop-NNN
**Related:** RFC, ADR, Coordination Request
**SAP:** SAP-001
**File:** inbox/ecosystem/proposals/
**Example:** Proposing health monitoring framework across entire ecosystem
**Example:** Suggesting move from monorepo to multi-repo architecture

### RFC
Request for Comments - formal discussion document for strategic proposals after initial triage approval.

**Aliases:** Request for Comments, RFCNNNN
**Related:** Strategic Proposal, ADR, Decision Record
**SAP:** SAP-001
**File:** inbox/ecosystem/rfcs/
**Example:** RFC-0001 proposing health check format standardization

### ADR
Architecture Decision Record - documents final decision made after RFC discussion period.

**Aliases:** Architecture Decision Record, Decision Record
**Related:** RFC, Strategic Proposal
**SAP:** SAP-001
**File:** inbox/ecosystem/adrs/
**Example:** ADR-0001 adopting JSON-based health check format

### Coordination Request
Type 2 intake for cross-repo dependencies or blocking work reviewed during sprint planning (every 2 weeks).

**Aliases:** Type 2 intake, coord-NNN
**Related:** Strategic Proposal, Implementation Task
**SAP:** SAP-001
**File:** inbox/incoming/coordination/
**Example:** Coordinating testing improvements between chora-base and chora-compose
**Example:** Requesting feature X from chora-base to unblock chora-compose development

### Implementation Task
Type 3 intake for ready-to-implement features or bug fixes reviewed continuously by engineers.

**Aliases:** Type 3 intake, task-NNN
**Related:** Coordination Request
**SAP:** SAP-001
**File:** inbox/incoming/tasks/
**Example:** Implementing configuration validation function
**Example:** Fixing bug in link validator script

### Triage
Process of reviewing and scoring intake items (proposals, coordination requests, tasks) to determine priority and acceptance.

**Aliases:** Intake triage, priority scoring
**Related:** Strategic Proposal, Coordination Request, Priority
**SAP:** SAP-001
**File:** docs/dev-docs/workflows/INTAKE_TRIAGE_GUIDE.md
**Example:** Scoring proposal 42/50 points → Accept this quarter

---

## Development Lifecycle

### DDD
Documentation Driven Design - Phase 3 of development lifecycle where requirements are captured as documentation before coding.

**Aliases:** Documentation Driven Design, Docs-first, Phase 3
**Related:** BDD, TDD, Change Request
**SAP:** SAP-012
**File:** docs/dev-docs/workflows/DDD_WORKFLOW.md
**Example:** Writing API reference documentation before implementing validate_config() function

### BDD
Behavior Driven Development - Phase 4a where acceptance criteria are converted to executable Gherkin scenarios.

**Aliases:** Behavior Driven Development, Gherkin, Phase 4a
**Related:** DDD, TDD, Scenario
**SAP:** SAP-012
**File:** docs/dev-docs/workflows/BDD_WORKFLOW.md
**Example:** Writing .feature file with "Given valid config, When validating, Then success"

### TDD
Test Driven Development - Phase 4b using RED-GREEN-REFACTOR cycles to implement features.

**Aliases:** Test Driven Development, Red-Green-Refactor, Phase 4b
**Related:** DDD, BDD
**SAP:** SAP-012
**File:** docs/dev-docs/workflows/TDD_WORKFLOW.md
**Example:** Writing failing unit test, implementing minimal code to pass, refactoring

### Change Request
DDD Phase 3 output document specifying problem, solution, API design, and acceptance criteria.

**Aliases:** DDD output, requirements document
**Related:** DDD, Acceptance Criteria
**SAP:** SAP-012
**File:** inbox/active/{item}/change-request.md
**Example:** Document specifying validate_config() API and success criteria

### Acceptance Criteria
Given-When-Then format requirements that define feature success conditions.

**Aliases:** Success criteria, Given-When-Then
**Related:** BDD, Scenario
**SAP:** SAP-012
**Example:** Given valid config, When validating, Then return success with no errors

### Gherkin Scenario
BDD executable specification in Given-When-Then format stored in .feature files.

**Aliases:** BDD scenario, .feature file, executable specification
**Related:** BDD, Acceptance Criteria
**SAP:** SAP-012
**File:** features/*.feature
**Example:** Scenario in config_validation.feature testing happy path

### RED-GREEN-REFACTOR
TDD cycle: write failing test (RED), implement minimal code (GREEN), improve design (REFACTOR).

**Aliases:** TDD cycle, red green refactor
**Related:** TDD
**SAP:** SAP-012
**Example:** Write test_validate_config (fails), implement return ValidationResult(True, []), refactor with actual logic

---

## SAP Framework

### SAP
Skilled Awareness Package - portable capability package containing 5 core artifacts defining a reusable development pattern.

**Aliases:** Skilled Awareness Package, Capability Package
**Related:** Capability Charter, Protocol Spec, Awareness Guide
**SAP:** SAP-000
**Example:** SAP-004 (testing-framework) providing pytest infrastructure
**Example:** SAP-012 (development-lifecycle) defining 8-phase workflow

### Capability Charter
SAP artifact 1 of 5 - defines what the capability is, why it exists, and what value it provides.

**Aliases:** Charter, SAP charter
**Related:** SAP, Protocol Spec
**SAP:** SAP-000
**File:** docs/skilled-awareness/{sap-name}/capability-charter.md
**Example:** testing-framework charter explaining pytest adoption benefits

### Protocol Spec
SAP artifact 2 of 5 - technical contract specifying how the capability works (architecture, APIs, workflows).

**Aliases:** Protocol Specification, Technical Spec
**Related:** SAP, Capability Charter
**SAP:** SAP-000
**File:** docs/skilled-awareness/{sap-name}/protocol-spec.md
**Example:** testing-framework protocol defining test structure and pytest configuration

### Awareness Guide
SAP artifact 3 of 5 - agent-facing documentation explaining how to use the capability with examples and common pitfalls.

**Aliases:** Agent Guide, SAP awareness
**Related:** SAP, AGENTS.md
**SAP:** SAP-000
**File:** docs/skilled-awareness/{sap-name}/awareness-guide.md
**Example:** testing-framework awareness guide showing how agents should write tests

### Adoption Blueprint
SAP artifact 4 of 5 - step-by-step guide for installing and integrating the capability into a project.

**Aliases:** Installation Guide, Blueprint
**Related:** SAP
**SAP:** SAP-000
**File:** docs/skilled-awareness/{sap-name}/adoption-blueprint.md
**Example:** testing-framework blueprint with 8-step installation checklist

### Ledger
SAP artifact 5 of 5 - tracks adopters, versions, and lessons learned across projects.

**Aliases:** SAP ledger, adoption ledger
**Related:** SAP
**SAP:** SAP-000
**File:** docs/skilled-awareness/{sap-name}/ledger.md
**Example:** testing-framework ledger showing chora-compose adopted v1.2.0 on 2025-10-15

### SAP Set
Curated bundle of SAPs designed for specific use cases with estimated installation time.

**Aliases:** SAP bundle, capability set
**Related:** SAP
**SAP:** SAP-000
**Example:** minimal-entry set (5 SAPs, 3-5 hours) for ecosystem coordination
**Example:** mcp-server set (10 SAPs, ~1 day) for MCP server development

### Adoption Level
Maturity scale (0-3) indicating depth of SAP integration: 0=not installed, 1=basic, 2=integrated, 3=optimized.

**Aliases:** SAP level, integration level
**Related:** SAP, SAP Evaluation
**SAP:** SAP-019
**Example:** SAP-004 at Level 2 means tests configured and passing but not yet optimized

---

## Event Traceability

### Event Log
Append-only JSONL file recording all significant actions for timeline reconstruction and cross-repo correlation.

**Aliases:** events.jsonl, JSONL log
**Related:** CHORA_TRACE_ID, Event Timeline
**SAP:** SAP-001
**File:** inbox/coordination/events.jsonl
**Example:** Log entry recording coordination_request_accepted event

### CHORA_TRACE_ID
Environment variable or event field enabling correlation of related events across repositories and sessions.

**Aliases:** Trace ID, correlation ID
**Related:** Event Log
**SAP:** SAP-001
**Example:** trace_id: "ecosystem-w3-health-monitoring" linking 47 events across 4 repos

### Event Timeline
Chronological reconstruction of events filtered by trace ID, task ID, or date range.

**Aliases:** Timeline, event history
**Related:** Event Log, CHORA_TRACE_ID
**SAP:** SAP-001
**Example:** Showing all events for coord-003 from submission to completion

---

## Quality & Testing

### Coverage
Percentage of code lines executed by test suite, with target ≥85% for chora-base projects.

**Aliases:** Test coverage, code coverage
**Related:** pytest, Quality Gates
**SAP:** SAP-004
**Example:** pytest --cov=src reports 92% coverage

### Quality Gates
Automated checks (linting, type checking, coverage, security) that must pass before merging code.

**Aliases:** Pre-commit hooks, quality checks
**Related:** Coverage, CI/CD
**SAP:** SAP-006
**File:** .pre-commit-config.yaml
**Example:** Ruff, mypy, pytest hooks running before git commit

### Test Pyramid
Testing strategy with 60% unit tests, 20% integration, 10% smoke, 10% E2E tests.

**Aliases:** Testing pyramid, test distribution
**Related:** Coverage
**SAP:** SAP-004
**Example:** Project with 120 unit tests, 40 integration, 20 smoke, 20 E2E

---

## Priority & Planning

### Priority
Classification of work items: P0 (critical blocker), P1 (high priority), P2 (medium priority).

**Aliases:** P0, P1, P2, priority level
**Related:** Triage, Sprint Planning
**SAP:** SAP-001
**Example:** P0 coordination request blocking current sprint
**Example:** P2 enhancement deferred to future sprint

### Sprint
2-week development cycle with committed work items, goals, and retrospective.

**Aliases:** Sprint cycle, iteration
**Related:** Sprint Planning, Velocity
**SAP:** SAP-012
**File:** docs/project-docs/sprints/sprint-{NN}.md
**Example:** Wave 2 sprint with 18 SAP audits committed

### Sprint Planning
Bi-weekly meeting to select work items, estimate effort, and commit to sprint goals.

**Aliases:** Planning meeting, sprint kickoff
**Related:** Sprint, Capacity
**SAP:** SAP-012
**Example:** Reviewing coordination requests and committing to 84 hours of work

### Velocity
Average story points or hours completed per sprint over last 6 sprints.

**Aliases:** Sprint velocity, team velocity
**Related:** Sprint, Capacity
**SAP:** SAP-012
**Example:** Team velocity of 80 hours per sprint ±20%

### Capacity
Available developer time per sprint calculated as (team size × days × 6h) × 0.7 for buffer.

**Aliases:** Sprint capacity, available time
**Related:** Sprint Planning, Velocity
**SAP:** SAP-012
**Example:** 2 engineers × 10 days × 6h × 0.7 = 84 hours capacity

### Waypoint
Major milestone marking completion of significant capability or wave of work.

**Aliases:** Milestone, checkpoint
**Related:** Wave
**SAP:** SAP-001
**Example:** Waypoint W3 completing health monitoring across ecosystem

### Wave
Large initiative spanning multiple sprints focused on cohesive set of improvements.

**Aliases:** Initiative, wave of work
**Related:** Waypoint, Sprint
**SAP:** SAP-012
**Example:** Wave 2 completing SAP content audit (96 hours, 18 SAPs)

---

## Documentation Framework

### Diátaxis
Documentation framework with 4 types: Tutorials (learning), How-To (task), Reference (information), Explanation (understanding).

**Aliases:** Diataxis, documentation quadrant
**Related:** Tutorial, How-To, Reference, Explanation
**SAP:** SAP-007
**Example:** Reference doc for validate_config() API, How-To for adding validation

### Tutorial
Diátaxis learning-oriented documentation guiding user through first experience.

**Aliases:** Getting started, tutorial guide
**Related:** Diátaxis, How-To
**SAP:** SAP-007
**File:** docs/user-docs/tutorials/
**Example:** "Your First SAP Installation" tutorial

### How-To
Diátaxis task-oriented documentation showing steps to accomplish specific goal.

**Aliases:** Guide, how-to guide, cookbook
**Related:** Diátaxis, Tutorial
**SAP:** SAP-007
**File:** docs/user-docs/how-to/
**Example:** "How to Create a Coordination Request" guide

### Reference
Diátaxis information-oriented documentation describing APIs, configurations, or specifications.

**Aliases:** API reference, technical reference
**Related:** Diátaxis, Protocol Spec
**SAP:** SAP-007
**File:** docs/user-docs/reference/
**Example:** validate_config() function signature and parameters

### Explanation
Diátaxis understanding-oriented documentation explaining concepts, decisions, and architectures.

**Aliases:** Conceptual docs, background
**Related:** Diátaxis, ADR
**SAP:** SAP-007
**File:** docs/user-docs/explanation/
**Example:** "Why Documentation Driven Design?" explanation

### 4-Domain Architecture
Universal documentation structure: user-docs/, dev-docs/, project-docs/, skilled-awareness/.

**Aliases:** Four-domain structure, documentation domains
**Related:** Diátaxis
**SAP:** SAP-007
**Example:** All chora-base projects use docs/ with these 4 subdirectories

---

## Link Validation & Traceability

### Link Validation
Automated checking of markdown links (internal and external) to prevent broken references.

**Aliases:** Link checking, broken link detection
**Related:** Traceability
**SAP:** SAP-016
**File:** scripts/validate-links.sh
**Example:** Wave 2 discovery of 220 broken links across 15 SAPs

### Traceability
Ability to track relationships between requirements, design, tests, and code bidirectionally.

**Aliases:** Requirements traceability, traceability matrix
**Related:** Link Validation, Impact Analysis
**SAP:** SAP-016
**Example:** Tracing REQ-042 → Scenario 15 → test_validate_config() → validate_config()

### Impact Analysis
Analysis of what files/components would be affected by changing or moving a specific file.

**Aliases:** Change impact, reverse link lookup
**Related:** Traceability
**SAP:** SAP-016
**Example:** "20 files link to protocol-spec.md" warning before refactoring

---

## Metrics & ROI

### ROI
Return on Investment - ratio of time/cost saved to time/cost invested in a capability or process.

**Aliases:** Return on Investment, cost-benefit
**Related:** ClaudeROICalculator, Metrics
**SAP:** SAP-013
**Example:** Wave 1 achieved 79x ROI (0.5h actual vs 40h projected)

### ClaudeROICalculator
Tool for tracking time saved, costs, and quality metrics when using Claude Code or AI-assisted development.

**Aliases:** ROI calculator, metrics tracker
**Related:** ROI, Process Metrics
**SAP:** SAP-013
**File:** src/{package}/utils/claude_metrics.py
**Example:** Calculating 2.5x ROI from coord-003 effort tracking

### Process Metrics
Dashboard tracking quality (defects, coverage), velocity (story points), and adherence (DDD/BDD/TDD adoption).

**Aliases:** Metrics dashboard, process KPIs
**Related:** ROI, Quality Gates
**SAP:** SAP-013
**File:** docs/project-docs/metrics/PROCESS_METRICS.md
**Example:** Tracking defect rate reduction from 15/release to 3/release

---

## Agent Awareness

### AGENTS.md
Generic agent awareness file providing context and guidance for AI assistants working in a directory.

**Aliases:** Agent awareness file
**Related:** CLAUDE.md, SAP-009
**SAP:** SAP-009
**File:** AGENTS.md (nested in directories)
**Example:** tests/AGENTS.md explaining testing conventions and patterns

### CLAUDE.md
Claude-specific optimizations supplementing AGENTS.md with token budgets and performance tips.

**Aliases:** Claude awareness file
**Related:** AGENTS.md, SAP-009
**SAP:** SAP-009
**File:** CLAUDE.md
**Example:** Specifying 15-30k token budget for feature development tasks

### Nearest File Wins
Pattern where agents read the awareness file closest to the code being worked on for context.

**Aliases:** Hierarchical awareness, nested AGENTS.md
**Related:** AGENTS.md, SAP-009
**SAP:** SAP-009
**Example:** Agent in tests/integration/ reads tests/AGENTS.md before root AGENTS.md

### Token Budget
Recommended context size for different task types to optimize Claude performance.

**Aliases:** Context budget, token allocation
**Related:** CLAUDE.md
**SAP:** SAP-009
**Example:** Bug fix: 5-10k tokens, feature: 15-30k, refactor: 20-40k

---

## Repository Structure

### Clone-Based Workflow
Development pattern where projects clone chora-base and pull structural updates while customizing content.

**Aliases:** Clone not generate, upstream updates
**Related:** Merge Model
**SAP:** SAP-003
**Example:** Project clones chora-base, customizes docs/, merges structure updates quarterly

### Merge Model
Ability to pull chora-base structural improvements without losing project-specific customizations.

**Aliases:** Upstream merge, pull updates
**Related:** Clone-Based Workflow
**SAP:** SAP-003
**Example:** Merging chora-base v4.2.0 blueprint improvements into existing project

### Blueprint
Template file or directory structure that projects customize after cloning chora-base.

**Aliases:** Template, project template
**Related:** SAP-003
**File:** blueprints/ (deprecated in v3.6.0, migrated to static-template/)
**Example:** pyproject.toml.blueprint customized per project

---

## Ecosystem Coordination

### Ecosystem
Collection of related repositories coordinating through shared inbox protocol and SAP framework.

**Aliases:** Liminal Commons ecosystem, chora ecosystem
**Related:** Coordination Hub
**SAP:** SAP-001
**Example:** chora-base, chora-compose, ecosystem-manifest coordinating via inbox protocol

### Coordination Hub
Central repository (typically chora-base) managing ecosystem-wide coordination and strategic proposals.

**Aliases:** Hub repository
**Related:** Ecosystem
**SAP:** SAP-001
**Example:** chora-base receiving proposals and coordinating releases across ecosystem

### Capability
Reusable development pattern packaged as a SAP and adopted across ecosystem repositories.

**Aliases:** SAP capability, portable capability
**Related:** SAP
**SAP:** SAP-000
**Example:** Testing Framework capability (SAP-004) adopted by chora-base and chora-compose

---

## Glossary Metadata

**Version**: 1.0.0
**Last Updated**: 2025-10-31
**Total Terms**: 75
**Categories**: 14
**SAP References**: 10 SAPs

**Usage Stats**: (Will be populated after usage tracking is implemented)
- Most searched terms: (TBD)
- Most common reverse lookups: (TBD)
- Fuzzy match success rate: (TBD)

**Contributing**: To add or update terms, edit this file following the existing format:
```markdown
### Term Name
Definition sentence explaining the concept clearly.

**Aliases:** Comma-separated alternative names
**Related:** Comma-separated related terms
**SAP:** SAP-XXX if applicable
**File:** Path to canonical file if applicable
**Example:** Real-world usage example
**Example:** Additional example if helpful
```

**Search Tool**: `python scripts/chora-search.py --help`
