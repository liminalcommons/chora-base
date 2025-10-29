# Protocol Specification: SAP Framework

**SAP ID**: SAP-000
**Version**: 1.0.0
**Status**: Draft → Active (Phase 1)
**Last Updated**: 2025-10-27

---

## 1. Overview

This protocol defines the **technical contract** for the Skilled Awareness Package (SAP) Framework: structure, formats, versioning, installation, and governance.

**Core Guarantee**: Any capability packaged as a SAP can be installed, upgraded, and maintained by humans and AI agents using standardized artifacts and blueprints.

---

## 2. SAP Structure

### 2.1 Required Artifacts

Every SAP MUST include 5 artifacts:

| Artifact | Filename | Format | Purpose |
|----------|----------|--------|---------|
| Capability Charter | `capability-charter.md` | Markdown + YAML frontmatter | Problem, scope, outcomes, stakeholders, lifecycle |
| Protocol Specification | `protocol-spec.md` | Markdown + YAML frontmatter | Technical contract, interfaces, guarantees |
| Awareness Guide | `awareness-guide.md` | Markdown + YAML frontmatter | Agent execution patterns, common workflows |
| Adoption Blueprint | `adoption-blueprint.md` | Markdown + YAML frontmatter | Installation steps, validation, configuration |
| Traceability Ledger | `ledger.md` | Markdown + YAML frontmatter | Adopter tracking, versions, status |

**Location Convention**:
```
docs/reference/skilled-awareness/<capability-name>/
├── capability-charter.md
├── protocol-spec.md
├── awareness-guide.md
├── adoption-blueprint.md
└── ledger.md
```

**Example**: [inbox SAP](../inbox/)

### 2.2 Artifact Schemas

#### 2.2.1 YAML Frontmatter (All Artifacts)

**Required Fields**:
```yaml
---
sap_id: SAP-NNN            # Unique SAP identifier
version: X.Y.Z             # Semantic version
status: <status>           # Draft | Pilot | Active | Deprecated | Archived
last_updated: YYYY-MM-DD   # Last modification date
---
```

**Optional Fields**:
```yaml
owner: <name>              # Capability owner
created: YYYY-MM-DD        # Creation date
phase: <phase>             # Roadmap phase (Phase 1, Phase 2, etc.)
scope: <scope>             # Vision | Planning | Implementation | All
```

#### 2.2.2 Capability Charter Schema

**Required Sections**:
1. Problem Statement (current challenge, evidence, business impact)
2. Proposed Solution (high-level approach, key principles)
3. Scope (in scope, out of scope)
4. Outcomes (success criteria, key metrics)
5. Stakeholders (primary, secondary)
6. Dependencies (framework, external)
7. Constraints & Assumptions
8. Risks & Mitigation
9. Lifecycle (phases, deliverables, success criteria)
10. Related Documents
11. Approval (sponsor, date, review cycle)

**Template**: See [document-templates.md](../document-templates.md#capability-charter)

#### 2.2.3 Protocol Specification Schema

**Required Sections**:
1. Overview (technical summary, core guarantee)
2. SAP Structure (required artifacts, infrastructure)
3. Interfaces (APIs, CLIs, configurations)
4. Data Models (schemas, formats)
5. Behavior (workflows, state machines, error handling)
6. Quality Gates (testing, validation, performance)
7. Dependencies (internal, external)
8. Versioning (semantic versioning, compatibility)
9. Security (if applicable)
10. Examples (reference implementations)

**Template**: See [document-templates.md](../document-templates.md#protocol-specification)

#### 2.2.4 Awareness Guide Schema

**Required Sections**:
1. Quick Reference (common commands, patterns)
2. Agent Context Loading (what to read, what to skip)
3. Common Workflows (step-by-step agent execution)
4. Troubleshooting (common issues, solutions)
5. Integration (with other capabilities, tools)
6. Best Practices (agent-specific patterns)

**Template**: See [document-templates.md](../document-templates.md#awareness-guide)

#### 2.2.5 Adoption Blueprint Schema

**Required Sections**:
1. Prerequisites (versions, dependencies)
2. Installation Steps (numbered, agent-executable)
3. Validation Commands (verify installation)
4. Configuration Checklist (required customizations)
5. Upgrade Path (version-specific blueprints)
6. Troubleshooting (installation issues)

**Template**: See [document-templates.md](../document-templates.md#adoption-blueprint)

#### 2.2.6 Traceability Ledger Schema

**Required Sections**:
1. Adopter Registry (table: adopter, version, status, date)
2. Version History (table: version, date, changes)
3. Active Deployments (production SAPs)
4. Deprecation Notices (if applicable)

**Template**: See [document-templates.md](../document-templates.md#traceability-ledger)

### 2.3 Infrastructure

SAPs MAY include infrastructure files:

**Schemas** (`schemas/`):
- JSON Schema files (`.json`)
- Pydantic models (`.py`)
- OpenAPI specs (`.yaml`)

**Templates** (`templates/`):
- Jinja2 templates (`.jinja2`)
- Blueprint files (`.blueprint`)
- Configuration templates (`.yaml`, `.json`)

**Directories**:
- Standard folder structure
- Example projects
- Test fixtures

**Configurations**:
- YAML configs
- JSON configs
- Environment files (`.env.example`)

**Scripts**:
- Validation scripts
- Migration scripts
- Diagnostic tools

**Location Convention**:
```
<capability-name>/
├── schemas/
│   ├── capability-config.json
│   └── capability-model.py
├── templates/
│   ├── config.yaml.jinja2
│   └── setup.blueprint
├── examples/
│   └── complete-example/
├── scripts/
│   ├── validate.py
│   └── migrate-v1-to-v2.py
└── [5 core artifacts]
```

**Example**: [inbox SAP infrastructure](../inbox/)

---

## 3. Interfaces

### 3.1 Blueprint Interface

Blueprints are **markdown documents** with step-by-step instructions.

**Blueprint Format**:
```markdown
## Installation

### Prerequisites
- Requirement 1
- Requirement 2

### Step 1: <Action>
<Detailed instructions>

### Step 2: <Action>
<Detailed instructions>

### Validation
Run: `<command> && echo "✅ Installed"`
```

**Agent Execution Protocol**:
1. Agent reads blueprint sequentially
2. Agent executes each step using appropriate tools:
   - Create directories: `Bash(mkdir)` or `Write`
   - Copy files: `Read` + `Write`
   - Update files: `Edit`
   - Run commands: `Bash`
3. Agent validates installation using validation commands
4. Agent reports success/failure

**Guarantees**:
- Blueprints MUST be idempotent (safe to run multiple times)
- Blueprints MUST include validation steps
- Blueprints MUST handle common errors

### 3.2 Ledger Interface

Ledgers track adopter status.

**Ledger Format**:
```markdown
## Adopter Registry

| Adopter | Version | Status | Install Date | Notes |
|---------|---------|--------|--------------|-------|
| chora-compose | 1.2.0 | Active | 2025-10-15 | Production |
| example-project | 1.0.0 | Pilot | 2025-10-01 | Testing |
```

**Update Protocol**:
1. Adopter installs/upgrades SAP
2. Adopter (or agent) updates ledger entry
3. PR created with ledger update
4. Capability owner merges PR

**Guarantees**:
- Ledger MUST list all known adopters
- Ledger MUST track versions
- Ledger MUST indicate status (Pilot, Active, Deprecated)

### 3.3 Versioning Interface

SAPs follow semantic versioning: `MAJOR.MINOR.PATCH`

**Version Format**:
- `MAJOR`: Breaking changes (protocol changes, removed features)
- `MINOR`: New features, backward-compatible
- `PATCH`: Bug fixes, documentation updates

**Compatibility Rules**:
- Same MAJOR version = compatible
- Different MAJOR version = breaking changes
- Upgrade MUST follow sequential MAJOR versions (v1 → v2 → v3, not v1 → v3)

**Upgrade Blueprint Naming**:
```
docs/reference/skilled-awareness/<capability>/upgrades/
├── v1.0-to-v1.1.md   # Minor upgrade
├── v1.1-to-v2.0.md   # Major upgrade
└── v2.0-to-v2.1.md   # Minor upgrade
```

**Guarantees**:
- Every MAJOR version change MUST have upgrade blueprint
- MINOR/PATCH changes MAY have upgrade blueprint
- Upgrade blueprints MUST be sequential

---

## 4. Data Models

### 4.1 SAP Metadata Model

```yaml
sap_metadata:
  sap_id: string              # SAP-NNN format
  capability_name: string     # kebab-case
  version: string             # semver
  status: enum                # Draft | Pilot | Active | Deprecated | Archived
  owner: string               # Capability owner name
  created: date               # YYYY-MM-DD
  last_updated: date          # YYYY-MM-DD
  phase: enum                 # Phase 1 | Phase 2 | Phase 3 | Phase 4
  scope: enum                 # Vision | Planning | Implementation | All
  dependencies:
    - sap_id: string          # Required SAP
      version: string         # Min version
  location: path              # docs/reference/skilled-awareness/<name>/
```

**JSON Schema**: See `docs/reference/skilled-awareness/schemas/sap-metadata.json` (future)

### 4.2 Adopter Record Model

```yaml
adopter_record:
  adopter_name: string        # Project name
  sap_id: string              # SAP-NNN
  version: string             # Installed version
  status: enum                # Pilot | Active | Deprecated | Archived
  install_date: date          # YYYY-MM-DD
  upgrade_date: date          # YYYY-MM-DD (last upgrade)
  notes: string               # Optional notes
```

**JSON Schema**: See `docs/reference/skilled-awareness/schemas/adopter-record.json` (future)

### 4.3 Blueprint Step Model

```yaml
blueprint_step:
  step_number: integer        # Sequential step number
  action: string              # Brief description
  instructions: string        # Detailed markdown
  tool_hint: enum             # Bash | Write | Edit | Read (for agents)
  validation: string          # Optional validation command
  error_handling: string      # Optional error guidance
```

**Format**: Encoded in markdown section headers and content

---

## 5. Behavior

### 5.1 SAP Lifecycle State Machine

```
┌─────────┐
│  Draft  │ ← Initial state
└────┬────┘
     ↓ (pilot validation)
┌────┴────┐
│  Pilot  │ ← Limited adoption
└────┬────┘
     ↓ (pilot success)
┌────┴────┐
│ Active  │ ← Production-ready
└────┬────┘
     ↓ (breaking change or replacement)
┌────┴────────┐
│ Deprecated  │ ← Migration recommended
└────┬────────┘
     ↓ (all adopters migrated)
┌────┴─────┐
│ Archived │ ← No longer maintained
└──────────┘
```

**State Transitions**:
- `Draft → Pilot`: Artifacts complete, pilot adopters identified
- `Pilot → Active`: Pilot feedback positive, ready for all adopters
- `Active → Deprecated`: Breaking change, replacement SAP exists
- `Deprecated → Archived`: All adopters migrated

**Guarantees**:
- SAPs MUST NOT skip states
- `Deprecated` SAPs MUST have migration blueprint
- `Archived` SAPs MUST preserve documentation

### 5.2 Installation Workflow

```
┌───────────────────────────────────────────────────────┐
│ 1. Agent reads adoption-blueprint.md                  │
└───────────────┬───────────────────────────────────────┘
                ↓
┌───────────────────────────────────────────────────────┐
│ 2. Agent checks prerequisites                         │
│    - Versions, dependencies, environment              │
└───────────────┬───────────────────────────────────────┘
                ↓
┌───────────────────────────────────────────────────────┐
│ 3. Agent executes installation steps sequentially     │
│    - Create directories                               │
│    - Copy/create files                                │
│    - Update existing files                            │
│    - Run configuration scripts                        │
└───────────────┬───────────────────────────────────────┘
                ↓
┌───────────────────────────────────────────────────────┐
│ 4. Agent runs validation commands                     │
│    - Verify directory structure                       │
│    - Validate configuration                           │
│    - Test basic functionality                         │
└───────────────┬───────────────────────────────────────┘
                ↓
┌───────────────────────────────────────────────────────┐
│ 5. Agent updates ledger                               │
│    - Add adopter record                               │
│    - Record version, date                             │
└───────────────┬───────────────────────────────────────┘
                ↓
┌───────────────────────────────────────────────────────┐
│ 6. Agent reports success                              │
│    ✅ SAP installed successfully                      │
└───────────────────────────────────────────────────────┘
```

**Guarantees**:
- Blueprints MUST be executable by agents
- Validation MUST catch common installation errors
- Ledger MUST be updated (via PR if needed)

### 5.3 Upgrade Workflow

```
┌───────────────────────────────────────────────────────┐
│ 1. Adopter identifies need to upgrade                 │
│    - New features, bug fixes, security patches        │
└───────────────┬───────────────────────────────────────┘
                ↓
┌───────────────────────────────────────────────────────┐
│ 2. Agent checks current version (from ledger)         │
│    - Current: v1.0.0                                  │
│    - Target: v2.0.0                                   │
└───────────────┬───────────────────────────────────────┘
                ↓
┌───────────────────────────────────────────────────────┐
│ 3. Agent locates upgrade blueprint(s)                 │
│    - v1.0-to-v1.5.md (intermediate)                   │
│    - v1.5-to-v2.0.md (final)                          │
└───────────────┬───────────────────────────────────────┘
                ↓
┌───────────────────────────────────────────────────────┐
│ 4. Agent executes upgrade blueprints sequentially     │
│    - v1.0 → v1.5 → v2.0                               │
└───────────────┬───────────────────────────────────────┘
                ↓
┌───────────────────────────────────────────────────────┐
│ 5. Agent validates upgrade                            │
│    - Run validation commands                          │
│    - Test functionality                               │
└───────────────┬───────────────────────────────────────┘
                ↓
┌───────────────────────────────────────────────────────┐
│ 6. Agent updates ledger                               │
│    - Update version to v2.0.0                         │
│    - Record upgrade date                              │
└───────────────┬───────────────────────────────────────┘
                ↓
┌───────────────────────────────────────────────────────┐
│ 7. Agent reports success                              │
│    ✅ Upgraded to v2.0.0                              │
└───────────────────────────────────────────────────────┘
```

**Guarantees**:
- Upgrades MUST be sequential (no skipping MAJOR versions)
- Upgrade blueprints MUST include rollback instructions
- Breaking changes MUST be documented in upgrade blueprint

### 5.4 Error Handling

**Installation Errors**:
- Missing prerequisites → Agent reports error, suggests resolution
- File conflicts → Agent asks user to resolve
- Validation failure → Agent reports failure, shows troubleshooting steps

**Upgrade Errors**:
- Missing intermediate version → Agent reports required upgrade path
- Rollback needed → Agent follows rollback instructions in blueprint
- Validation failure → Agent reports failure, suggests rollback

**Guarantees**:
- Blueprints MUST include error handling guidance
- Validation MUST detect common errors
- Troubleshooting MUST be actionable

---

## 6. Quality Gates

### 6.1 SAP Completeness

**Required for `Pilot` status**:
- ✅ All 5 artifacts present
- ✅ All required sections complete
- ✅ YAML frontmatter valid
- ✅ Blueprint tested by at least one agent
- ✅ At least one adopter committed to pilot

**Required for `Active` status**:
- ✅ Pilot feedback addressed
- ✅ At least 2 successful pilot adoptions
- ✅ Ledger has pilot adopter records
- ✅ No blocking issues

### 6.2 Blueprint Quality

**Required**:
- ✅ Idempotent (safe to run multiple times)
- ✅ Includes validation commands
- ✅ Error handling guidance provided
- ✅ Tested with primary agent (Claude Code)

**Recommended**:
- ⚠️ Tested with secondary agent (Cursor, etc.)
- ⚠️ Includes troubleshooting section
- ⚠️ Includes common pitfalls

### 6.3 Documentation Quality

**Required**:
- ✅ All sections present (per artifact schema)
- ✅ Examples provided
- ✅ Clear, actionable language
- ✅ Machine-readable (YAML frontmatter valid)

**Recommended**:
- ⚠️ Diagrams (state machines, workflows)
- ⚠️ Cross-references to related docs
- ⚠️ Evidence/research citations

---

## 7. Dependencies

### 7.1 Internal Dependencies

**Framework Dependencies** (every SAP depends on):
- SAP framework (this SAP)
- Root protocol (`SKILLED_AWARENESS_PACKAGE_PROTOCOL.md`)
- Document templates (`document-templates.md`)
- SAP Index (`INDEX.md`)

**Capability Dependencies** (SAP-specific):
- Listed in Charter (Section 6: Dependencies)
- Tracked in Protocol (Section 7: Dependencies)
- Enforced by blueprint prerequisites

### 7.2 External Dependencies

**Tooling**:
- Git (versioning, collaboration)
- Markdown renderer (documentation)
- YAML parser (frontmatter)
- AI agents (Claude Code, Cursor, etc.)

**Standards**:
- Semantic versioning (semver.org)
- Diataxis documentation framework
- JSON Schema (for infrastructure)

---

## 8. Versioning

### 8.1 SAP Framework Versioning

SAP framework itself follows semantic versioning:

**Version**: 1.0.0 (this document)

**Compatibility**:
- SAPs created for framework v1.x MUST work with framework v1.y (y > x)
- SAPs created for framework v1.x MAY need updates for framework v2.0

**Upgrade Path**:
- Framework upgrades documented in `sap-framework/upgrades/`
- All existing SAPs updated when framework changes (MAJOR only)

### 8.2 SAP Versioning

Individual SAPs follow semantic versioning:

**Version Format**: `MAJOR.MINOR.PATCH`

**Examples**:
- `1.0.0` → Initial release
- `1.1.0` → New feature added (backward-compatible)
- `1.0.1` → Bug fix (backward-compatible)
- `2.0.0` → Breaking change (upgrade blueprint required)

**Guarantees**:
- MAJOR: Breaking changes, upgrade blueprint required
- MINOR: New features, backward-compatible
- PATCH: Bug fixes, backward-compatible

---

## 9. Security

### 9.1 Blueprint Execution Security

**Threats**:
- Malicious blueprints executing harmful commands
- Blueprints accessing sensitive data
- Blueprints modifying critical system files

**Mitigations**:
- Blueprints are markdown (not executable scripts)
- Agents show commands before execution (transparency)
- User can intervene at any step
- Blueprints MUST NOT include hardcoded credentials

**Guarantees**:
- Blueprints MUST be human-readable
- Blueprints MUST NOT access sensitive data
- Agents MUST show commands before execution

### 9.2 Infrastructure Security

**Schemas**:
- JSON Schemas MUST NOT include sensitive defaults
- Pydantic models MUST NOT log sensitive data

**Configurations**:
- Config templates MUST use `.env.example` for secrets
- Config templates MUST NOT include real credentials

---

## 10. Examples

### 10.1 Complete SAP: inbox-coordination

**Location**: [docs/reference/skilled-awareness/inbox/](../inbox/)

**Artifacts**:
- ✅ [capability-charter.md](../inbox/capability-charter.md)
- ✅ [protocol-spec.md](../inbox/protocol-spec.md)
- ✅ [awareness-guide.md](../inbox/awareness-guide.md)
- ✅ [adoption-blueprint.md](../inbox/adoption-blueprint.md)
- ✅ [ledger.md](../inbox/ledger.md)

**Infrastructure**:
- ✅ `inbox/schemas/` (JSON Schema)
- ✅ `inbox/coordination/` (directory structure)
- ✅ `inbox/examples/health-monitoring-w3/` (complete example)

**Status**: Pilot (Phase 1)

### 10.2 Blueprint Example

From [inbox adoption-blueprint.md](../inbox/adoption-blueprint.md):

```markdown
### Step 3: Create Capability Registry

Create the capability registry directory:

mkdir -p inbox/coordination/CAPABILITIES

This directory will hold capability declarations for your project.

### Validation

Run:
ls inbox/coordination/CAPABILITIES && echo "✅ Registry created"
```

**Agent Execution**:
1. Agent reads step
2. Agent runs `mkdir -p inbox/coordination/CAPABILITIES` via Bash
3. Agent runs validation command
4. Agent sees `✅ Registry created` output
5. Agent proceeds to next step

---

## 11. Related Documents

**Root Protocol**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../../../../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)

**Framework SAP**:
- [capability-charter.md](capability-charter.md) - This SAP's charter
- [awareness-guide.md](awareness-guide.md) - Agent guidance (coming next)
- [adoption-blueprint.md](adoption-blueprint.md) - Installation (coming next)
- [ledger.md](ledger.md) - Adopter tracking (coming next)

**Templates & Index**:
- [document-templates.md](../document-templates.md) - SAP artifact templates
- [INDEX.md](../INDEX.md) - SAP registry (coming next)

**Reference Implementation**:
- [inbox SAP](../inbox/) - Complete pilot SAP

---

**Version History**:
- **1.0.0** (2025-10-27): Initial protocol specification
