# Skilled Awareness Package (SAP) Protocol

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-10-27
**Scope**: All chora-base capabilities and adopter repositories

---

## Purpose

This protocol defines **Skilled Awareness Packages (SAPs)** — complete, installable capability bundles that enable humans and AI agents to adopt, install, upgrade, and maintain chora-base capabilities with clear contracts and predictable outcomes.

**Core Principle**: Every major capability in chora-base ships as a first-class SAP with protocol, awareness guidance, and agent-executable blueprints.

---

## What is a SAP?

A **Skilled Awareness Package** is a structured capability bundle consisting of:

1. **5 Core Artifacts** (documentation)
2. **Infrastructure** (schemas, templates, directories, configs)
3. **Testing Layer** (optional E2E tests, BDD scenarios)

### 1. Core Artifacts

Every SAP includes five standardized documents:

| Artifact | Purpose | Audience |
|----------|---------|----------|
| **Capability Charter** | Problem, scope, outcomes, stakeholders, lifecycle | Humans + AI (decision-making) |
| **Protocol Specification** | Technical contract, interfaces, guarantees | Humans + AI (implementation) |
| **Awareness Guide** | How to work with this capability | AI agents (execution) |
| **Adoption Blueprint** | Step-by-step installation instructions | AI agents (installation) |
| **Traceability Ledger** | Adopters, versions, status tracking | Humans + AI (governance) |

**Templates**: See [docs/reference/skilled-awareness/document-templates.md](docs/reference/skilled-awareness/document-templates.md)

### 2. Infrastructure

SAPs include all files, directories, and configurations needed:

- **Schemas** (JSON Schema, Pydantic models)
- **Templates** (Jinja2, blueprint files)
- **Directories** (standard structure)
- **Configuration Files** (YAML, JSON, ENV)
- **Scripts** (automation, validation)

**Example** (inbox SAP):
```
inbox/
├── INBOX_PROTOCOL.md              # Protocol
├── CLAUDE.md                      # Awareness
├── schemas/                       # Infrastructure
│   ├── coordination-request.json
│   └── broadcast.json
├── coordination/
│   ├── CAPABILITIES/
│   └── ECOSYSTEM_STATUS.yaml
└── examples/
```

### 3. Testing Layer (Optional)

SAPs may include automated tests:

- **E2E Tests** (test SAP installation)
- **BDD Scenarios** (acceptance criteria validation)
- **Validation Scripts** (check SAP consistency)

**Note**: Executable How-Tos primarily test **adopter-built features**, not SAP installation itself. SAPs may include installation validation but it's not required.

---

## SAP Scope Levels

SAPs operate at three organizational levels:

### 1. Vision & Strategy (Quarterly - 3-6 months)

**Purpose**: Long-term capability evolution, ecosystem coordination

**Deliverables**:
- Capability waves (Wave 1, Wave 2, etc.)
- Waypoints (W1, W2, W3 milestones)
- Quarterly roadmaps
- Strategic proposals
- RFCs (Requests for Comments)
- ADRs (Architecture Decision Records)

**Example**: [inbox/examples/health-monitoring-w3/](inbox/examples/health-monitoring-w3/) - 16-week health monitoring initiative with Wave 1 and Wave 2 structure

**SAP Role**: Charter defines strategic goals, Protocol references RFCs/ADRs

### 2. Planning & Prioritization (Bi-weekly - sprints)

**Purpose**: Sprint planning, capacity allocation, feature prioritization

**Deliverables**:
- Sprint plans
- Coordination requests (cross-repo dependencies)
- Capability backlog
- Resource allocation

**Example**: inbox coordination requests triaged during sprint planning (this_sprint, next_sprint, backlog)

**SAP Role**: Adoption Blueprint includes sprint planning guidance, Ledger tracks adoption status

### 3. Implementation (Continuous - features)

**Purpose**: Day-to-day feature development, bug fixes, maintenance

**Deliverables**:
- DDD change requests
- BDD feature files
- TDD test suites
- Pull requests
- Releases

**Example**: inbox tasks (task-001, task-002, task-003, task-004) following DDD → BDD → TDD

**SAP Role**: Awareness Guide provides execution patterns, Protocol Spec defines interfaces

---

## Installation Pattern: Blueprint-Based Adoption

SAPs are installed via **agent-readable blueprint instructions** (not shell scripts).

### Blueprint Structure

Adoption blueprints are markdown documents with:

1. **Prerequisites** - Dependencies, required versions
2. **Installation Steps** - Numbered, agent-executable steps
3. **Validation Commands** - Verify installation success
4. **Configuration Checklist** - Required customizations
5. **Upgrade Path** - Sequential version adoption

**Format**:
```markdown
## Installation

### Prerequisites
- chora-base v3.0.0+
- Python 3.11+

### Step 1: Create Directory Structure
Create the following directories:
- `inbox/`
- `inbox/coordination/`
- `inbox/coordination/CAPABILITIES/`

### Step 2: Copy Schema Files
Copy from chora-base:
- `inbox/schemas/coordination-request.json` → `inbox/schemas/coordination-request.json`

### Step 3: Update AGENTS.md
Add section "Inbox Coordination" with content from awareness guide.

### Validation
Run: `ls inbox/coordination/CAPABILITIES/ && echo "✅ Inbox installed"`
```

### Agent Execution

Agents read blueprints and:
1. Create directories (via Write tool or Bash)
2. Copy/create files (via Write tool)
3. Update existing files like AGENTS.md (via Edit tool)
4. Run validation commands (via Bash)
5. Confirm installation success

**Not Scripts**: Agents execute instructions directly, not shell scripts. This provides:
- Transparency (agent shows each step)
- Interactivity (user can intervene)
- Cross-platform compatibility (agent adapts to environment)
- Auditability (agent logs all actions)

---

## Upgrade Pattern: Sequential Adoption

Every SAP release includes an **upgrade blueprint** for sequential adoption.

### Versioning

SAPs follow semantic versioning:
- **Major** (2.0.0): Breaking changes, new protocol
- **Minor** (1.1.0): New features, backward-compatible
- **Patch** (1.0.1): Bug fixes, clarifications

### Upgrade Workflow

1. **Check Current Version**: Read ledger entry for adopter
2. **Find Upgrade Path**: Locate upgrade blueprint (e.g., `v1.0-to-v1.1.md`)
3. **Execute Upgrade**: Follow blueprint steps
4. **Validate**: Run upgrade validation commands
5. **Update Ledger**: Record new version

**Example** (inbox SAP):
```
docs/reference/skilled-awareness/inbox/upgrades/
├── v1.0-to-v1.1.md
├── v1.1-to-v2.0.md
└── v2.0-to-v2.1.md
```

**Cumulative Upgrades**: Adopters on v1.0 upgrading to v2.1 follow three blueprints sequentially.

---

## Integration with Development Lifecycle

SAPs integrate with chora-base's DDD → BDD → TDD workflow:

### DDD (Documentation Driven Design)

**SAP Role**: Protocol Spec and Charter are created **before** implementation

**Workflow**:
1. Identify capability need
2. Create Charter (problem, scope, outcomes)
3. Write Protocol Spec (technical contract)
4. Get stakeholder approval
5. → Proceed to BDD

**Output**: ✅ Charter + ✅ Protocol Spec

### BDD (Behavior Driven Development)

**SAP Role**: Acceptance criteria from Charter become BDD scenarios

**Workflow**:
1. Extract acceptance criteria from Charter
2. Write Gherkin scenarios (feature files)
3. Implement step definitions
4. Run tests (RED - all fail)
5. → Proceed to TDD

**Output**: ✅ Executable acceptance tests (failing)

### TDD (Test Driven Development)

**SAP Role**: Awareness Guide and Blueprint created during implementation

**Workflow**:
1. Write unit test (RED)
2. Implement infrastructure (GREEN)
3. Refactor (improve design)
4. Document patterns in Awareness Guide
5. Write installation steps in Blueprint
6. → Complete SAP

**Output**: ✅ Infrastructure + ✅ Awareness Guide + ✅ Blueprint

### Result

Complete SAP with all 5 artifacts + infrastructure + tests, validated through DDD → BDD → TDD.

---

## SAP Governance

### Roles

| Role | Responsibility | Examples |
|------|---------------|----------|
| **Capability Owner** | Defines scope, maintains SAP | Victor (chora-base owner) |
| **Agent Operator** | Executes blueprints, reports issues | Claude Code, Cursor |
| **Adopter Maintainer** | Customizes SAP for project | chora-compose maintainer |
| **Governance Rep** | Reviews proposals, approves changes | TBD (future) |

### Change Management

**Minor Changes** (documentation, clarifications):
- Create PR with changes
- Update SAP version (patch)
- Notify via broadcast (optional)

**Major Changes** (protocol changes, breaking):
- Create RFC (Request for Comments)
- 7-day Final Comment Period (FCP)
- Update SAP version (major)
- Create upgrade blueprint
- Notify via broadcast (required)

**Example**: inbox SAP RFC 0001 (health monitoring) → 7-day FCP → ADR 0001 → implementation

---

## SAP Index

Central registry of all SAPs: [docs/reference/skilled-awareness/INDEX.md](docs/reference/skilled-awareness/INDEX.md)

**Format**:
```markdown
| SAP ID | Capability | Version | Status | Phase | Location |
|--------|------------|---------|--------|-------|----------|
| SAP-001 | inbox-coordination | 1.0.0 | Pilot | Phase 1 | docs/reference/skilled-awareness/inbox/ |
| SAP-002 | project-bootstrap | 0.1.0 | Draft | Phase 2 | docs/reference/skilled-awareness/project-bootstrap/ |
...
```

**Status Values**:
- **Draft**: In development, not ready for adoption
- **Pilot**: Ready for limited adoption, feedback phase
- **Active**: Production-ready, recommended for all adopters
- **Deprecated**: Superseded, upgrade recommended
- **Archived**: No longer maintained

---

## Examples

### Complete SAP: inbox-coordination

Location: [docs/reference/skilled-awareness/inbox/](docs/reference/skilled-awareness/inbox/)

**Artifacts**:
- ✅ [capability-charter.md](docs/reference/skilled-awareness/inbox/capability-charter.md)
- ✅ [protocol-spec.md](docs/reference/skilled-awareness/inbox/protocol-spec.md)
- ✅ [awareness-guide.md](docs/reference/skilled-awareness/inbox/awareness-guide.md)
- ✅ [adoption-blueprint.md](docs/reference/skilled-awareness/inbox/adoption-blueprint.md)
- ✅ [ledger.md](docs/reference/skilled-awareness/inbox/ledger.md)

**Infrastructure**:
- ✅ `inbox/schemas/` (JSON Schema)
- ✅ `inbox/coordination/` (directory structure)
- ✅ `inbox/examples/health-monitoring-w3/` (complete example)

**Testing**:
- ✅ Example trace validation (events, timeline analysis)

**Status**: Pilot (Phase 1)

### Meta-SAP: sap-framework

Location: [docs/reference/skilled-awareness/sap-framework/](docs/reference/skilled-awareness/sap-framework/)

**Purpose**: Defines the SAP pattern itself (this protocol is part of it)

**Status**: Draft (Phase 1)

---

## SAP Lifecycle

```
┌──────────────────────────────────────────────────────────┐
│ 1. IDENTIFICATION                                        │
│    - Capability need identified                          │
│    - Added to SAP Index (status: Draft)                  │
└─────────────────┬────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────────────────────┐
│ 2. CREATION (DDD → BDD → TDD)                            │
│    - Charter + Protocol (DDD)                            │
│    - BDD scenarios (BDD)                                 │
│    - Infrastructure + Awareness + Blueprint (TDD)        │
│    - Ledger initialized                                  │
└─────────────────┬────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────────────────────┐
│ 3. PILOT ADOPTION                                        │
│    - 1-3 adopters install SAP                            │
│    - Feedback collected                                  │
│    - Refinements made                                    │
│    - Status: Pilot                                       │
└─────────────────┬────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────────────────────┐
│ 4. PRODUCTION RELEASE                                    │
│    - SAP validated by pilot adopters                     │
│    - Broadcast sent to ecosystem                         │
│    - Status: Active                                      │
│    - Recommended for all adopters                        │
└─────────────────┬────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────────────────────┐
│ 5. MAINTENANCE                                           │
│    - Bug fixes (patch versions)                          │
│    - Enhancements (minor versions)                       │
│    - Ledger updated with adopter versions                │
│    - Periodic broadcasts                                 │
└─────────────────┬────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────────────────────┐
│ 6. EVOLUTION                                             │
│    - Breaking changes (major versions)                   │
│    - RFC process for major changes                       │
│    - Upgrade blueprints created                          │
│    - Deprecation notices                                 │
└─────────────────┬────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────────────────────┐
│ 7. DEPRECATION (if needed)                               │
│    - Replacement SAP identified                          │
│    - Migration blueprint created                         │
│    - Status: Deprecated                                  │
│    - Grace period for migration                          │
└─────────────────┬────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────────────────────┐
│ 8. ARCHIVAL                                              │
│    - All adopters migrated                               │
│    - Status: Archived                                    │
│    - Docs preserved for reference                        │
└──────────────────────────────────────────────────────────┘
```

---

## Benefits

### For Humans

- **Clear Contracts**: Explicit guarantees, no assumptions
- **Predictable Upgrades**: Sequential adoption path, no surprises
- **Governance**: Versioning, change management, stakeholder alignment
- **Visibility**: Ledger shows who's using what version

### For AI Agents

- **Machine-Readable**: Structured artifacts, consistent format
- **Executable Instructions**: Step-by-step blueprints, validation commands
- **Awareness Guidance**: How to work with capability, common patterns
- **Traceability**: Ledger tracks versions, dependencies

### For Ecosystem

- **Coordination**: Cross-repo capabilities follow same pattern
- **Reusability**: SAPs can be adopted by any chora-base adopter
- **Quality**: DDD → BDD → TDD ensures high quality
- **Discoverability**: SAP Index shows all capabilities

---

## Related Documents

- **SAP Templates**: [docs/reference/skilled-awareness/document-templates.md](docs/reference/skilled-awareness/document-templates.md)
- **SAP Roadmap**: [docs/reference/skilled-awareness/chora-base-sap-roadmap.md](docs/reference/skilled-awareness/chora-base-sap-roadmap.md)
- **SAP Index**: [docs/reference/skilled-awareness/INDEX.md](docs/reference/skilled-awareness/INDEX.md)
- **Inbox SAP** (reference implementation): [docs/reference/skilled-awareness/inbox/](docs/reference/skilled-awareness/inbox/)
- **Executable How-Tos**: [docs/reference/writing-executable-howtos.md](docs/reference/writing-executable-howtos.md)
- **Development Lifecycle**: [static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md](static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md)

---

## Questions & Feedback

**For SAP protocol questions**: Open issue in chora-base repository
**For specific SAP questions**: See SAP's own adoption-blueprint.md or ledger.md
**For ecosystem coordination**: Use inbox system (coordination requests)

---

**Version History**:
- **1.0.0** (2025-10-27): Initial protocol definition
