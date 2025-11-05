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
docs/skilled-awareness/<capability-name>/
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
docs/skilled-awareness/<capability>/upgrades/
├── v1.0-to-v1.1.md   # Minor upgrade
├── v1.1-to-v2.0.md   # Major upgrade
└── v2.0-to-v2.1.md   # Minor upgrade
```

**Guarantees**:
- Every MAJOR version change MUST have upgrade blueprint
- MINOR/PATCH changes MAY have upgrade blueprint
- Upgrade blueprints MUST be sequential

### 3.4 Installation Tooling Interface

As of v4.1.0, chora-base provides automated installation tooling for SAPs and SAP sets.

#### 3.4.1 Installation Script

**Script**: `scripts/install-sap.py`

**Purpose**: Automated SAP installation from chora-base to target repositories.

**Usage**:
```bash
# Install single SAP
python scripts/install-sap.py SAP-XXX --source /path/to/chora-base

# Install SAP set (curated bundle)
python scripts/install-sap.py --set <set-name> --source /path/to/chora-base

# Dry run (preview without installing)
python scripts/install-sap.py SAP-XXX --source /path/to/chora-base --dry-run

# List available SAP sets
python scripts/install-sap.py --list-sets
```

**What the script does**:
1. Loads `sap-catalog.json` (machine-readable SAP registry)
2. Resolves dependencies automatically
3. Copies 5 artifacts to `docs/skilled-awareness/{sap-name}/`
4. Copies system files (if applicable) to project root
5. Validates installation (checks for all 5 artifacts)
6. Reports success/failure

**Guarantees**:
- Installation MUST be idempotent (safe to run multiple times)
- Already-installed SAPs MUST be skipped automatically
- Dependencies MUST be resolved and installed first
- Installation MUST validate all artifacts exist
- Script MUST work from any target directory

#### 3.4.2 SAP Catalog

**File**: `sap-catalog.json`

**Purpose**: Machine-readable registry of all SAPs, sets, and metadata.

**Schema**:
```json
{
  "version": "4.1.0",
  "total_saps": 18,
  "saps": [
    {
      "id": "SAP-000",
      "name": "sap-framework",
      "status": "active",
      "version": "1.0.0",
      "size_kb": 125,
      "description": "Core SAP framework",
      "capabilities": ["..."],
      "dependencies": [],
      "tags": ["meta", "required"],
      "location": "docs/skilled-awareness/sap-framework",
      "artifacts": { "capability_charter": true, ... },
      "system_files": []
    }
  ],
  "sap_sets": {
    "minimal-entry": {
      "saps": ["SAP-000", "SAP-001", "SAP-009", "SAP-016", "SAP-002"],
      "estimated_tokens": 29000,
      "estimated_hours": "3-5",
      "use_cases": ["..."]
    }
  }
}
```

**Guarantees**:
- Catalog MUST list all SAPs
- Catalog MUST specify dependencies
- Catalog MUST define all standard SAP sets
- Catalog MUST be valid JSON
- Catalog version MUST match chora-base version

#### 3.4.3 SAP Sets

**SAP Sets** are curated bundles of SAPs for specific use cases.

**Standard Sets** (as of v4.1.0):
| Set | SAPs | Tokens | Time | Use Case |
|-----|------|--------|------|----------|
| minimal-entry | 5 | ~29k | 3-5 hours | Ecosystem coordination |
| recommended | 10 | ~60k | 1-2 days | Core development workflow |
| testing-focused | 6 | ~35k | 4-6 hours | Testing and quality |
| mcp-server | 10 | ~55k | 1 day | MCP server development |
| full | 18 | ~100k | 2-4 weeks | Comprehensive coverage |

**Custom Sets**: Organizations can define custom sets via `.chorabase` file in repository root.

**Custom Set Format**:
```yaml
# .chorabase
version: "4.1.0"
project_type: "custom"

sap_sets:
  my-org-minimal:
    name: "MyOrg Minimal Entry"
    description: "Our organization's standard minimal set"
    saps:
      - SAP-000  # Framework (required)
      - SAP-001  # Inbox coordination
      - SAP-004  # Testing (required by our org)
    estimated_tokens: 34000
    estimated_hours: "4-6"
    use_cases:
      - "New repos in our organization"
```

**Installation**:
```bash
python scripts/install-sap.py --set my-org-minimal --source /path/to/chora-base
```

**Guarantees**:
- Standard sets MUST be defined in sap-catalog.json
- Custom sets MUST be defined in .chorabase file
- Set installation MUST skip already-installed SAPs
- Set installation MUST install dependencies first
- Set installation MUST validate all SAPs

**Related Documentation**:
- [How to Install SAP Sets](../../user-docs/how-to/install-sap-set.md)
- [How to Create Custom SAP Sets](../../user-docs/how-to/create-custom-sap-sets.md)
- [Standard SAP Sets Reference](../../user-docs/reference/standard-sap-sets.md)

### 3.5 Supplemental Documentation (Optional)

While the 5 core artifacts (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger) are mandatory for every SAP, some SAPs may benefit from **supplemental documentation** for architecture deep dives, integration patterns, design philosophy, or other specialized content that doesn't fit cleanly into the core structure.

#### 3.5.1 When to Add Supplemental Documentation

Create supplemental documentation when:

**Size**: protocol-spec.md exceeds 3,000-4,000 lines
- Complex architectures require detailed technical specifications beyond the core protocol
- Splitting content improves readability and maintainability
- Example: SAP-018 protocol-spec.md (4,006 lines) could have split MCP tool specifications into separate file

**Architecture Deep Dives**: System architecture requires detailed diagrams and explanations
- 3-tier architectures, data flow diagrams, component interactions
- Visual explanations complement textual protocol specifications
- Example: SAP-018 architecture-overview.md (830 lines) documents Collections 3-tier model, caching system, context resolution flow

**Design Philosophy**: Design rationale and principles need dedicated space
- Trade-off discussions, alternative approaches considered
- Architectural decision records (ADRs)
- Example: SAP-018 design-philosophy.md (840 lines) explains generator plugin architecture, caching strategy rationale

**Integration Patterns**: Common integration scenarios span multiple systems
- Cross-system workflows, API integration examples
- Multi-tool orchestration patterns
- Example: SAP-018 integration-patterns.md (884 lines) documents MCP client integration, observability system integration

**Reference Materials**: Large catalogs, lookup tables, or reference data
- Tool catalogs, error code references, configuration option tables
- Content that users reference frequently but read selectively

#### 3.5.2 Naming Convention

Supplemental documentation files MUST follow these conventions:

**File Naming**: Use kebab-case matching content focus
- `architecture-overview.md` - System architecture deep dive
- `design-philosophy.md` - Design principles and rationale
- `integration-patterns.md` - Common integration scenarios
- `error-catalog.md` - Comprehensive error reference
- `performance-tuning.md` - Optimization guidance
- `migration-guides.md` - Version migration details

**Location**: Place in SAP directory alongside 5 core artifacts
```
docs/skilled-awareness/<capability-name>/
├── capability-charter.md         # Core artifact 1
├── protocol-spec.md              # Core artifact 2
├── awareness-guide.md            # Core artifact 3
├── adoption-blueprint.md         # Core artifact 4
├── ledger.md                     # Core artifact 5
├── architecture-overview.md      # Supplemental (optional)
├── design-philosophy.md          # Supplemental (optional)
└── integration-patterns.md       # Supplemental (optional)
```

**YAML Frontmatter**: Include metadata linking to parent SAP
```yaml
---
sap_id: SAP-018
artifact_type: supplemental
artifact_name: architecture-overview
version: 2.0.0
status: active
last_updated: 2025-11-04
---
```

#### 3.5.3 Integration with Core Artifacts

Supplemental documentation MUST be referenced from core artifacts:

**From protocol-spec.md**: Link to architecture deep dives
```markdown
## 2. System Architecture

For comprehensive architecture documentation including diagrams and data flow, see:
- [Architecture Overview](architecture-overview.md) - 3-tier model, components, interactions
- [Design Philosophy](design-philosophy.md) - Architectural decisions and trade-offs
```

**From awareness-guide.md**: Link to integration patterns
```markdown
## 5. Integration

For detailed integration scenarios and examples, see:
- [Integration Patterns](integration-patterns.md) - MCP clients, observability systems, CI/CD
```

**From adoption-blueprint.md**: Link to migration guides
```markdown
## 6. Upgrading

For version-specific migration guidance, see:
- [Migration Guides](migration-guides.md) - Detailed upgrade procedures for breaking changes
```

#### 3.5.4 Quality Standards

Supplemental documentation MUST maintain same quality as core artifacts:

**Required**:
- ✅ YAML frontmatter with SAP ID, version, status
- ✅ Referenced from at least one core artifact
- ✅ Clear purpose statement at top of document
- ✅ Maintained in sync with core artifact versions

**Recommended**:
- ⚠️ Table of contents for documents > 500 lines
- ⚠️ Cross-references to related supplemental docs
- ⚠️ Examples and diagrams where applicable

#### 3.5.5 Examples

**SAP-018 (chora-compose Meta)**: 3 supplemental documents beyond 5 core artifacts
- `architecture-overview.md` (830 lines) - System architecture with diagrams
- `design-philosophy.md` (840 lines) - Design principles, trade-offs
- `integration-patterns.md` (884 lines) - Integration scenarios

**SAP-019 (SAP Self-Evaluation)**: Schemas directory for JSON schemas
- `schemas/evaluation-result.json` - EvaluationResult schema
- `schemas/gap.json` - Gap model schema
- `schemas/adoption-roadmap.json` - AdoptionRoadmap schema

**Future Example**: SAP with error catalog
- `error-catalog.md` - Comprehensive error code reference (500+ lines)
- Referenced from protocol-spec.md troubleshooting section

#### 3.5.6 Guarantees

**Core Artifacts Take Precedence**: Supplemental docs are optional enhancements
- Core 5 artifacts MUST be complete and self-contained
- Readers MUST be able to understand SAP from core artifacts alone
- Supplemental docs provide depth, not essential information

**Versioning Alignment**: Supplemental docs MUST match core artifact versions
- Same version number in YAML frontmatter
- Updated in sync with core artifact changes
- Archived when parent SAP reaches Archived status

**No Duplication**: Supplemental docs MUST NOT duplicate core content
- Provide additional detail, not repetition
- Cross-reference core artifacts, don't restate
- Extend core concepts, don't replace

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
  location: path              # docs/skilled-awareness/<name>/
```

**JSON Schema**: See `docs/skilled-awareness/schemas/sap-metadata.json` (future)

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

**JSON Schema**: See `docs/skilled-awareness/schemas/adopter-record.json` (future)

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

## 6. Common SAP Patterns

This section documents recurring patterns across multiple SAPs that SAP authors can reuse to maintain consistency and quality.

### 6.1 Pattern: Multiple Adoption Paths (Modality Selection)

**When to use**: SAP supports multiple integration paths or deployment modalities (e.g., library vs. MCP server vs. CLI vs. Docker, or different workflow approaches).

**Problem**: Users need guidance on which adoption path best fits their use case, team structure, or technical environment.

**Solution**: Provide decision trees in awareness-guide.md and organize protocol-spec.md by modality.

**How to implement**:

1. **awareness-guide.md §2: Decision Trees**
   - Add "Decision Trees" section early in awareness guide
   - Create flowchart guiding users to appropriate modality
   - Use questions based on user role, environment, or requirements

**Example Decision Tree Format**:
```markdown
## 2. Decision Trees

### Modality Selection

**START** → What is your primary use case?

├─ **Individual developer** → Do you have Python 3.12+?
│   ├─ Yes → **Recommendation: pip (library) modality**
│   └─ No → **Recommendation: CLI modality**
│
├─ **AI agent (Claude, etc.)** → **Recommendation: MCP server modality**
│
└─ **Team deployment** → Do you need workflow automation (n8n, etc.)?
    ├─ Yes → **Recommendation: Docker modality**
    └─ No → **Recommendation: MCP server modality**
```

2. **protocol-spec.md: Organize by Modality**
   - Create separate sections for each modality (§3.1 pip, §3.2 MCP, §3.3 CLI, §3.4 Docker)
   - Document interfaces, configuration, and examples per modality
   - Include modality-specific trade-offs (performance, complexity, features)

3. **adoption-blueprint.md: Separate Adoption Paths**
   - Provide installation steps per modality
   - Link to decision tree from Getting Started section
   - Include validation commands specific to each path

**Real-world example**: [SAP-017 (chora-compose Integration)](../chora-compose-integration/) - 4 modalities with decision trees guiding selection based on role (developer/AI agent/team lead/DevOps)

**Benefits**:
- Reduces time-to-decision (5-10 min → 1-2 min with interactive selector)
- Prevents adoption of suboptimal modality for use case
- Improves user confidence in choice

### 6.2 Pattern: Performance Metrics Documentation

**When to use**: SAP provides tooling with measurable performance characteristics (latency, throughput, cache hit rates, resource usage).

**Problem**: Users lack objective performance data for capacity planning, optimization decisions, or modality selection.

**Solution**: Document performance metrics in ledger.md with test environment details and interpretation guidance.

**How to implement**:

1. **ledger.md §4: Performance Metrics**
   - Add "Performance Metrics" section to ledger
   - Include metric table with values, measurement date, and notes
   - Document test environment (hardware, software versions, configuration)
   - Provide interpretation guidance (what metrics mean for users)

**Example Metrics Table Format**:
```markdown
## 4. Performance Metrics

### Measurement Environment

- **Hardware**: M1 Mac, 16GB RAM, 8-core CPU
- **Software**: Python 3.12, chora-compose v1.5.0
- **Date**: 2025-11-04
- **Methodology**: 100 iterations per operation, median + p95 reported

### Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| **MCP Tool Invocation Latency** | < 50ms (p50), < 120ms (p95) | Async I/O, includes JSON parsing |
| **Content Generation (simple)** | 100-500ms | Jinja2 template, 1KB context |
| **Artifact Assembly (5 content)** | 500ms-2s | Sequential assembly, no caching |
| **Collection Generation (10 members)** | 5-20s | Parallel execution (4 workers) |
| **Cache Hit Rate** | 94%+ | SHA-256 deterministic caching |
| **Throughput (batch generation)** | 50-80 content/min | Parallel execution, cached context |

### Interpretation

- **For single operations**: Use MCP tools directly, expect < 100ms latency
- **For bulk generation**: Use Collections with parallel execution (4-8× speedup vs sequential)
- **For repeated generation**: Caching provides 5-10× speedup (context resolution skipped)
```

2. **protocol-spec.md: Reference Metrics in Technical Specification**
   - Link to ledger.md performance section from protocol-spec
   - Use metrics to justify architectural decisions (e.g., "SHA-256 caching chosen for 94%+ hit rates")
   - Include performance considerations in API/interface documentation

3. **Optional: Benchmarking Script**
   - Create `benchmarks/` directory with reproducible benchmark scripts
   - Document how to run benchmarks in different environments
   - Provide baseline comparisons (e.g., pip vs MCP vs CLI modality performance)

**Real-world example**: [SAP-018 (chora-compose Meta)](../chora-compose-meta/ledger.md) §4 - Performance metrics for MCP tools, Collections, caching with test environment and interpretation

**Benefits**:
- Enables capacity planning and resource estimation
- Provides objective basis for optimization decisions
- Helps users select appropriate patterns for performance requirements

### 6.3 Pattern: Tool/API Specification

**When to use**: SAP documents MCP tools, REST APIs, CLI commands, or other programmatic interfaces.

**Problem**: Users and AI agents need complete, unambiguous specifications for programmatic usage - parameter types, return values, error conditions.

**Solution**: Organize tools by category in protocol-spec.md, provide comprehensive specifications for each tool including error examples.

**How to implement**:

1. **protocol-spec.md §2: Tools/API Specification**
   - Organize tools by functional category (Core, Config, Storage, Discovery, etc.)
   - For each tool, provide complete specification

**Example Tool Specification Format**:
```markdown
### 2.3.1 generate_content

**Purpose**: Generate content from template and context using specified generator.

**Category**: Core Generation

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content_id` | string | Yes | - | Unique content identifier (matches config filename) |
| `generator` | string | No | "jinja2" | Generator to use (jinja2, demonstration, etc.) |
| `context` | object | No | {} | Additional context to merge with config context |
| `force` | boolean | No | false | Force regeneration (skip cache) |
| `output_path` | string | No | null | Custom output path (overrides config) |

**Returns**:

```json
{
  "success": true,
  "content_id": "readme-intro",
  "generator": "jinja2",
  "output_path": "output/readme-intro.md",
  "cached": false,
  "generation_time_ms": 245
}
```

**Error Codes**:

| Code | Message | Resolution |
|------|---------|------------|
| `config_not_found` | Content config '{content_id}' not found | Check config ID spelling or create config first |
| `invalid_context` | Context JSON parsing failed | Verify context is valid JSON object |
| `generation_failed` | Template rendering failed | Check template syntax and context variables |
| `write_failed` | Cannot write to output path | Check permissions and disk space |

**Error Response Examples**:

*Example 1: Config not found*
```json
{
  "success": false,
  "error": {
    "code": "config_not_found",
    "message": "Content config 'api-docs' not found in configs/content/",
    "details": {
      "searched_path": "/path/to/configs/content/api-docs.json",
      "available_configs": ["readme-intro", "changelog"]
    },
    "resolution": "Check config ID spelling or create config with 'draft_config' first"
  }
}
```

*Example 2: Invalid context*
```json
{
  "success": false,
  "error": {
    "code": "invalid_context",
    "message": "Context JSON parsing failed",
    "details": {
      "parse_error": "Unexpected token } at position 42",
      "provided_context": "{\"key\": \"value\"}"
    },
    "resolution": "Verify context is valid JSON object (use JSON validator)"
  }
}
```

**Example MCP Invocation**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "generate_content",
    "arguments": {
      "content_id": "readme-intro",
      "generator": "jinja2",
      "context": {"project_name": "chora-base", "version": "4.1.0"},
      "force": false
    }
  },
  "id": 1
}
```

**Response**:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "content_id": "readme-intro",
    "generator": "jinja2",
    "output_path": "output/readme-intro.md",
    "cached": false,
    "generation_time_ms": 245
  },
  "id": 1
}
```
```

2. **awareness-guide.md: Tool Selection Flowchart**
   - Create tool selection guide for common workflows
   - Map use cases to appropriate tools
   - Provide quick reference table (Tool → Purpose → Common Use Cases)

3. **Error Response Examples (Critical for AI Agents)**
   - For each tool, provide 2-3 error response examples
   - Show complete error structure with resolution guidance
   - Include edge cases (missing dependencies, permissions, etc.)

**Real-world example**: [SAP-018 (chora-compose Meta)](../chora-compose-meta/protocol-spec.md) §2 - 24 MCP tools organized by 7 categories, each with parameters, returns, errors, and JSON-RPC examples

**Benefits**:
- Enables AI agents to use tools correctly without trial-and-error
- Reduces support burden (errors are self-explanatory with resolution steps)
- Provides contract-level specification for integration testing

### 6.4 Pattern: Decision Tree Templates

**Reusable decision tree format** for awareness-guide.md:

```markdown
## Decision Tree: [Choice Name]

**Use Case**: [When to use this decision tree]

**Decision Factors**:
- Factor 1: [Question to ask]
- Factor 2: [Question to ask]
- Factor 3: [Question to ask]

**Decision Flow**:

```
START
  ├─ [Question 1]
  │   ├─ [Answer A] → **Recommendation A**: [Brief description]
  │   └─ [Answer B] → **Recommendation B**: [Brief description]
  └─ [Question 2]
      ├─ [Answer C] → **Recommendation C**: [Brief description]
      └─ [Answer D] → **Recommendation D**: [Brief description]
```

**Recommendation Details**:

**Recommendation A**: [Name]
- **When to use**: [Specific use case]
- **Pros**: [Benefits]
- **Cons**: [Trade-offs]
- **Getting started**: [Link to adoption-blueprint section]

**Recommendation B**: [Name]
- **When to use**: [Specific use case]
- **Pros**: [Benefits]
- **Cons**: [Trade-offs]
- **Getting started**: [Link to adoption-blueprint section]
```

**Optional enhancement**: Create interactive Python script (e.g., `scripts/select-modality.py`) that asks questions and recommends path.

### 6.5 Pattern: Identity and Scope Clarity

**When to use**: Every SAP, especially when creating new SAPs or major version rewrites.

**Problem**: SAPs may accidentally document wrong capabilities (identity crisis), leading to user confusion and mismatched expectations.

**Solution**: Explicitly document both what the SAP **is** and what it **is not** in capability-charter.md scope section.

**How to implement**:

1. **capability-charter.md §3: Scope**
   - In "In Scope" section: Be explicit and concrete about what SAP covers
   - In "Out of Scope" section: Explicitly state what SAP does NOT cover
   - Use contrasting examples to prevent confusion

**Example Scope Format**:
```markdown
### In Scope

SAP-017 (chora-compose Integration Guide) provides step-by-step integration for chora-compose content generation framework:

- **4 Integration Modalities**: pip (Python library), MCP (Model Context Protocol server), CLI (command-line tool), Docker (containerized deployment)
- **Installation Procedures**: Prerequisites, setup steps, validation commands per modality
- **Project Integration Workflows**: Git workflows, team collaboration, CI/CD integration

### Out of Scope

SAP-017 focuses exclusively on chora-compose integration. The following topics are covered by related SAPs:

**NOT Docker Compose orchestration** (covered by SAP-011: docker-operations):
- SAP-017 documents **chora-compose** (content generation framework)
- SAP-017 does NOT document **Docker Compose** (container orchestration)
- Docker modality in SAP-017 uses Docker to deploy chora-compose, not general Docker Compose patterns

**NOT chora-compose Architecture** (covered by SAP-018: chora-compose Meta):
- MCP tool specifications, generator internals, caching architecture
- Use SAP-018 for architecture understanding, SAP-017 for integration steps

**NOT Usage Patterns** (covered by future SAP-031):
- Template design best practices, context organization, performance optimization
```

2. **ledger.md: Version History with Identity Notes**
   - Document identity crises in version history
   - Explain what was wrong and how it was resolved
   - Archive incorrect versions with clear explanation

**Example Identity Crisis Documentation**:
```markdown
## Version History

### v2.0.0 (2025-11-04): Complete Rewrite - CORRECT SCOPE
**Changes**: Resolved identity crisis from v1.0.0
- NOW DOCUMENTS: chora-compose integration (pip/MCP/CLI/Docker modalities)
- NO LONGER DOCUMENTS: Docker Compose orchestration (moved to SAP-011 or future SAP-030)
- Identity clarity: Added explicit "Out of Scope" contrasts in capability-charter

### v1.0.0 (2025-10-29): ARCHIVED - Identity Crisis
**Problem**: Documented Docker Compose orchestration instead of chora-compose integration
- Mixed content: Docker Compose services, networking, volumes vs. chora-compose content generation
- 3,500 lines of wrong tool documentation
- Archived to `archives/sap-017-v1.0.0-docker-compose/`
```

**Real-world example**: Both [SAP-017](../chora-compose-integration/) and [SAP-018](../chora-compose-meta/) had v1.0.0 identity crises (documented Docker Compose instead of chora-compose), resolved in v2.0.0 rewrites with explicit scope clarity.

**Benefits**:
- Prevents 100% of identity crises (most common SAP quality issue)
- Reduces user confusion about SAP purpose
- Provides clear boundaries between related SAPs

### 6.6 Using These Patterns

**When creating a new SAP**:
1. Review relevant patterns from this section
2. Apply patterns matching SAP characteristics (e.g., if SAP has multiple modalities, use Pattern 6.1)
3. Reference this section in SAP documentation (e.g., "This SAP follows Pattern 6.3: Tool/API Specification")

**When reviewing existing SAPs**:
1. Check if SAP could benefit from documented patterns
2. Recommend pattern adoption in review feedback
3. Update SAP to follow patterns as quality improvement

**Pattern evolution**:
- As new patterns emerge across SAPs, document them in this section
- Submit proposals for new patterns via PR to SAP-000
- Patterns become standard practice for all new SAPs

---

## 7. Quality Gates

### 7.1 SAP Completeness

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

### 7.2 Blueprint Quality

**Required**:
- ✅ Idempotent (safe to run multiple times)
- ✅ Includes validation commands
- ✅ Error handling guidance provided
- ✅ Tested with primary agent (Claude Code)

**Recommended**:
- ⚠️ Tested with secondary agent (Cursor, etc.)
- ⚠️ Includes troubleshooting section
- ⚠️ Includes common pitfalls

### 7.3 Documentation Quality

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

## 8. Dependencies

### 8.1 Internal Dependencies

**Framework Dependencies** (every SAP depends on):
- SAP framework (this SAP)
- Root protocol (`SKILLED_AWARENESS_PACKAGE_PROTOCOL.md`)
- Document templates (`document-templates.md`)
- SAP Index (`INDEX.md`)

**Capability Dependencies** (SAP-specific):
- Listed in Charter (Section 6: Dependencies)
- Tracked in Protocol (Section 7: Dependencies)
- Enforced by blueprint prerequisites

### 8.2 External Dependencies

**Tooling**:
- Git (versioning, collaboration)
- Markdown renderer (documentation)
- YAML parser (frontmatter)
- AI agents (Claude Code, Cursor, etc.)

**Standards**:
- Semantic versioning (semver.org)
- Diataxis documentation framework
- JSON Schema (for infrastructure)

### 8.3 External Dependency Review Cadence

**Purpose**: Prevent dependency drift, security vulnerabilities, and incompatibility issues

**Review Frequency**: Quarterly (every 3 months)

**Review Checklist**:

1. **Version Currency Check**:
   - [ ] Are external tools/frameworks still actively maintained?
   - [ ] Are we using deprecated versions?
   - [ ] Are major versions behind latest stable?

2. **Security Assessment**:
   - [ ] Any known security vulnerabilities in dependencies?
   - [ ] Security advisories published since last review?
   - [ ] Recommended security updates available?

3. **Compatibility Verification**:
   - [ ] Still compatible with chora-base supported environments?
   - [ ] Breaking changes in newer versions that affect us?
   - [ ] Migration path clear if upgrade needed?

4. **Alternative Evaluation**:
   - [ ] New tools/standards emerged that might be better fit?
   - [ ] Community consensus shifted to different approaches?
   - [ ] Cost/benefit of switching vs. maintaining status quo?

**Actions Based on Review**:

| Finding | Priority | Action |
|---------|----------|--------|
| Security vulnerability in dependency | **Critical** | Update SAP immediately, notify adopters |
| Dependency deprecated, replacement exists | **High** | Create migration blueprint, schedule update |
| Major version behind, breaking changes | **Medium** | Evaluate upgrade, document decision |
| Minor version drift | **Low** | Note for next scheduled update |
| Alternative better suited | **Low** | Research, propose in next major version |

**Documentation**:

After each quarterly review, update SAP ledger with:

```markdown
## Dependency Review History

### 2025-11-04 Q4 Review

**Reviewer**: [Name/Team]
**Date**: 2025-11-04

**Findings**:
- Git 2.42 → 2.45 available (MINOR: recommend update)
- Markdown renderers: No changes
- AI agents: Claude Sonnet 3.5 → 4.5 (performance improvements, recommend update)

**Actions Taken**:
- Updated protocol-spec.md §8.2 to reference Claude 4.5+
- No breaking changes required
- Notified adopters via ledger update

**Next Review**: 2026-02-04 (Q1 2026)
```

**Anti-Patterns to Avoid**:
- ❌ Never reviewing external dependencies (leads to security vulnerabilities)
- ❌ Upgrading dependencies without testing (breaks adopter environments)
- ❌ Not documenting dependency decisions (loses institutional knowledge)
- ❌ Ignoring deprecation warnings (forces emergency migrations later)

**Example from SAP-018**:

SAP-018 (chora-compose Meta) has quarterly reviews for:
- Python version requirements (currently 3.12+)
- MCP protocol version (currently 1.0)
- chora-compose framework version (currently 1.5.0+)

**Trigger for Ad-Hoc Review** (outside quarterly schedule):
- Critical security advisory published
- External dependency announces deprecation
- Adopter reports compatibility issue
- Major ecosystem shift (e.g., new protocol version)

---

## 9. Versioning

### 9.1 SAP Framework Versioning

SAP framework itself follows semantic versioning:

**Version**: 1.0.0 (this document)

**Compatibility**:
- SAPs created for framework v1.x MUST work with framework v1.y (y > x)
- SAPs created for framework v1.x MAY need updates for framework v2.0

**Upgrade Path**:
- Framework upgrades documented in `sap-framework/upgrades/`
- All existing SAPs updated when framework changes (MAJOR only)

### 9.2 SAP Versioning

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

## 10. Security

### 10.1 Blueprint Execution Security

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

### 10.2 Infrastructure Security

**Schemas**:
- JSON Schemas MUST NOT include sensitive defaults
- Pydantic models MUST NOT log sensitive data

**Configurations**:
- Config templates MUST use `.env.example` for secrets
- Config templates MUST NOT include real credentials

---

## 11. Examples

### 11.1 Complete SAP: inbox-coordination

**Location**: [docs/skilled-awareness/inbox/](../inbox/)

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

### 11.2 Blueprint Example

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

## 12. Related Documents

**Root Protocol**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)

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
