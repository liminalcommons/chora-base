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
      "tags": ["meta", "required", "foundational"],
      "location": "docs/skilled-awareness/sap-framework",
      "artifacts": { "capability_charter": true, ... },
      "system_files": [],

      // NEW: Curatorial Metadata (Phase 2.1)
      "category": "Meta & Ecosystem",
      "subcategory": "Framework",
      "audience": ["developers", "agents", "maintainers"],
      "complexity": "intermediate",
      "setup_effort_hours": "0.5-1",
      "learning_curve": "medium",
      "related_saps": {
        "depends_on": [],
        "integrates_with": ["SAP-029", "SAP-019"],
        "complements": ["SAP-009"],
        "alternative_to": [],
        "supersedes": [],
        "superseded_by": null
      },
      "last_verified": "2025-11-04",
      "maturity_indicators": {
        "adopters": 5,
        "pilot_duration_weeks": 8,
        "breaking_changes_count": 0,
        "documentation_completeness": 0.95
      },
      "affects_files": {
        "creates": [],
        "modifies": ["sap-catalog.json"],
        "reads": ["sap-catalog.json", "docs/skilled-awareness/**/*.md"]
      },
      "affects_domains": ["docs/skilled-awareness"]
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

**Standardized Relationship Fields**:

All SAPs SHOULD use these standardized relationship fields in sap-catalog.json for consistent curation and dependency analysis:

```json
{
  "id": "SAP-015",
  "name": "task-tracking",
  // ... other fields ...
  "dependencies": ["SAP-000"],           // Hard dependencies (REQUIRED for installation)
  "related_saps": {                      // Soft relationships (NOT required, but beneficial)
    "integrates_with": ["SAP-001", "SAP-010"],  // Bi-directional integrations
    "complements": ["SAP-009"],                  // Enhances but not required
    "alternative_to": [],                        // Mutually exclusive options
    "supersedes": [],                            // Replaces older SAP
    "superseded_by": null                        // Deprecated, use this instead
  },
  "tags": ["task-tracking", "beads", "agent-memory"]  // Use vocabulary from .chora/conventions/tag-vocabulary.yaml
}
```

**Relationship Field Definitions**:
- `dependencies`: Hard dependencies. Installation MUST install these first. Installation MUST fail if dependencies cannot be satisfied.
- `integrates_with`: Bi-directional soft integration. Both SAPs benefit when used together. Example: SAP-001 + SAP-015 (inbox decomposes into beads tasks).
- `complements`: One-directional enhancement. This SAP enhances the referenced SAP. Example: SAP-009 complements all SAPs (provides awareness).
- `alternative_to`: Mutually exclusive. Use one OR the other, not both. Example: SAP-X (zustand) alternative_to SAP-Y (redux).
- `supersedes`: This SAP replaces an older SAP. Old SAP should be deprecated. Example: SAP-015 supersedes SAP-014 (if SAP-014 existed).
- `superseded_by`: This SAP is deprecated. Use the referenced SAP instead. Status SHOULD be "deprecated".

**Tag Vocabulary**:

All SAPs MUST use tags from the standardized vocabulary defined in `.chora/conventions/tag-vocabulary.yaml`. This ensures consistent filtering, search, and curation.

**Tag Usage Guidelines**:
- Use 2-5 tags per SAP (optimize for discoverability)
- Include at least one taxonomy parent tag (e.g., `meta`, `frontend`, `ci-cd`)
- Use canonical tags, not aliases (e.g., `coordination` not `coord`)
- Consult `.chora/conventions/tag-vocabulary.yaml` for complete vocabulary

**File Touch Metadata**:

All SAPs SHOULD document which files they create, modify, or read using the `affects_files` field. This enables impact analysis, conflict detection, and rollback planning.

```json
{
  "id": "SAP-003",
  "name": "project-bootstrap",
  // ... other fields ...
  "affects_files": {
    "creates": [
      "static-template/**",
      "pyproject.toml",
      "README.md"
    ],
    "modifies": [
      ".gitignore",
      "pyproject.toml"
    ],
    "reads": [
      ".chora/config.yaml",
      "sap-catalog.json"
    ]
  },
  "affects_domains": [
    "implementation",
    "docs/user-docs"
  ]
}
```

**Field Definitions**:
- `affects_files.creates`: File patterns created by this SAP during adoption. Use glob patterns (e.g., `**/*.py` for all Python files).
- `affects_files.modifies`: File patterns modified by this SAP. May overlap with `creates` if SAP creates then modifies.
- `affects_files.reads`: File patterns read by this SAP (dependencies, configs). Useful for understanding SAP's environmental requirements.
- `affects_domains`: Documentation domains affected (e.g., `docs/skilled-awareness`, `docs/dev-docs`, `implementation` for source code).

**Use Cases**:
- **Impact Analysis**: "Which SAPs will be affected if I change `pyproject.toml`?"
- **Conflict Detection**: "Do SAP-003 and SAP-011 both modify `.gitignore`?"
- **Rollback Planning**: "Which files should I remove to uninstall SAP-003?"
- **Curation**: "Show me all SAPs that create configuration files"

**Glob Pattern Guidelines**:
- Use `**` for recursive directory matching (e.g., `src/**/*.py`)
- Use `*` for single-level wildcard (e.g., `*.md`)
- Be specific where possible (e.g., `pyproject.toml` not `*.toml`)
- Group related files (e.g., `static-template/**` instead of listing 50 individual files)

**Curatorial Metadata Fields (Phase 2.1)**:

All SAPs SHOULD include the following curatorial metadata to enable filtering, recommendation, and progress tracking:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `category` | string | ✅ Yes | Top-level taxonomy category | `"Meta & Ecosystem"`, `"Frontend Development"`, `"CI/CD & Deployment"` |
| `subcategory` | string | ❌ No | Finer-grained grouping within category | `"Framework"`, `"State Management"`, `"Testing"` |
| `audience` | array | ✅ Yes | Primary users of this SAP | `["developers", "agents", "maintainers"]` |
| `complexity` | enum | ✅ Yes | Skill level required | `"beginner"`, `"intermediate"`, `"advanced"` |
| `setup_effort_hours` | string | ✅ Yes | Time to adopt (range) | `"0.5-1"`, `"2-4"`, `"8-16"` |
| `learning_curve` | enum | ✅ Yes | Learning difficulty | `"low"`, `"medium"`, `"high"` |
| `last_verified` | date | ✅ Yes | Last adoption validation | `"2025-11-04"` |
| `maturity_indicators` | object | ✅ Yes | Production-readiness signals | See below |

**Maturity Indicators Sub-Fields**:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `adopters` | integer | Number of successful adoptions | `5` |
| `pilot_duration_weeks` | integer | How long SAP was in pilot phase | `8` |
| `breaking_changes_count` | integer | Number of breaking changes since 1.0 | `0` |
| `documentation_completeness` | float | Completeness score (0.0-1.0) | `0.95` |

**Standard Categories**:

Use these standardized category names for consistency:

1. **Meta & Ecosystem** - SAPs about SAPs (SAP-000, SAP-029, SAP-019, etc.)
2. **Development Lifecycle** - Process and workflow (SAP-012, SAP-003, etc.)
3. **Quality & Testing** - Testing frameworks and validation (SAP-004, SAP-013, etc.)
4. **CI/CD & Deployment** - Automation and deployment (SAP-005, SAP-011, etc.)
5. **Documentation** - Documentation frameworks (SAP-007, SAP-016, etc.)
6. **Agent & Memory** - Agent capabilities and memory (SAP-009, SAP-010, SAP-015, etc.)
7. **Architecture & Design** - Design patterns and methodologies (SAP-012, etc.)
8. **Frontend Development** - React/frontend SAPs (SAP-017, SAP-018, SAP-026, etc.)
9. **Backend Development** - Backend/API SAPs (future)
10. **Infrastructure** - Docker, configs, tooling (SAP-011, SAP-008, etc.)

**Audience Values**:

- `developers` - Software engineers adopting SAP
- `agents` - AI agents (Claude Code, etc.) using SAP
- `maintainers` - SAP maintainers and contributors
- `users` - End users (rare, usually for user-facing SAPs)

**Complexity Values**:

- `beginner` - Minimal prerequisites, simple concepts, quick setup
- `intermediate` - Some experience required, moderate complexity
- `advanced` - Expert knowledge needed, complex integration

**Learning Curve Values**:

- `low` - Understand in <30 minutes
- `medium` - Understand in 1-2 hours
- `high` - Understand in 4+ hours

**Curation Use Cases**:

```javascript
// Filter SAPs by audience and complexity
const agentSAPs = saps.filter(s =>
  s.audience.includes("agents") &&
  s.complexity === "beginner"
);

// Find SAPs for quick adoption (low effort + low learning curve)
const quickWins = saps.filter(s =>
  parseFloat(s.setup_effort_hours.split('-')[1]) <= 2 &&
  s.learning_curve === "low"
);

// Find production-ready SAPs (high maturity)
const productionReady = saps.filter(s =>
  s.maturity_indicators.adopters >= 3 &&
  s.maturity_indicators.breaking_changes_count === 0 &&
  s.maturity_indicators.documentation_completeness >= 0.85
);

// Find SAPs in specific category
const frontendSAPs = saps.filter(s =>
  s.category === "Frontend Development"
);

// Recommend SAPs based on current adoption
function recommendNextSAP(currentSAPs) {
  const integratesWith = currentSAPs.flatMap(sap =>
    sap.related_saps.integrates_with || []
  );
  return saps.filter(s => integratesWith.includes(s.id));
}
```

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

## 6. Quality Gates

### 6.1 SAP Completeness

**Required for `Pilot` status**:
- ✅ All 5 artifacts present
- ✅ All required sections complete
- ✅ YAML frontmatter valid
- ✅ **Diataxis compliance: 4/5 artifacts pass category alignment check**
- ✅ Blueprint tested by at least one agent
- ✅ At least one adopter committed to pilot

**Required for `Active` status**:
- ✅ Pilot feedback addressed
- ✅ At least 2 successful pilot adoptions
- ✅ Ledger has pilot adopter records
- ✅ **Diataxis compliance: 5/5 artifacts fully aligned with their categories**
- ✅ **No critical Diataxis category misalignments** (e.g., tutorials in reference docs)
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

### 6.4 Diataxis Framework Compliance

**Background**: SAP structure is explicitly designed around the [Diataxis framework](https://diataxis.fr/), which defines four distinct documentation types based on user intent. Each SAP artifact maps to a specific Diataxis category.

**Artifact-to-Diataxis Mapping**:

| SAP Artifact | Diataxis Category | Primary Purpose | Key Characteristics |
|--------------|-------------------|-----------------|---------------------|
| **capability-charter.md** | **Explanation** | Understanding-oriented | WHY it exists, context, rationale, trade-offs |
| **protocol-spec.md** | **Reference** | Information-oriented | Technical specs, APIs, data models, contracts |
| **awareness-guide.md** | **How-To Guide** | Task-oriented | Solve specific problems, workflows, patterns |
| **adoption-blueprint.md** | **Tutorial** | Learning-oriented | Step-by-step installation, getting started |
| **ledger.md** | **Reference** | Information-oriented | Factual records, version history, adoptions |

**Required for Diataxis Compliance**:

**Capability-Charter (Explanation)**:
- ✅ Explains WHY capability exists (not just WHAT it does)
- ✅ Provides context, background, motivation
- ✅ Discusses trade-offs and design decisions
- ❌ Avoids step-by-step instructions (belongs in blueprint)
- ❌ Avoids API specifications (belongs in protocol-spec)

**Protocol-Spec (Reference)**:
- ✅ Factual, comprehensive, structured technical information
- ✅ API/schema/data model specifications
- ✅ Constraints, guarantees, error cases
- ❌ Avoids learning journeys or progressive teaching (belongs in tutorial)
- ❌ Avoids task-solving patterns (belongs in how-to)

**Awareness-Guide (How-To)**:
- ✅ Solves specific problems (task-oriented)
- ✅ Assumes knowledge (not teaching fundamentals)
- ✅ Concrete examples for each task
- ✅ Cross-references to related content (2+ domains recommended)
- ❌ Avoids teaching fundamentals step-by-step (belongs in blueprint)
- ❌ Avoids pure specifications without context (belongs in protocol-spec)

**Adoption-Blueprint (Tutorial)**:
- ✅ Learning-oriented (teaches while doing)
- ✅ Sequential steps with expected outcomes
- ✅ Safe to experiment (clear validation points)
- ✅ Beginner-friendly (no assumed knowledge beyond prerequisites)
- ❌ Avoids problem-solving focus (belongs in how-to)
- ❌ Avoids detailed specifications (belongs in protocol-spec)

**Ledger (Reference)**:
- ✅ Factual adoption records
- ✅ Version history with dates
- ❌ No explanatory or tutorial content

**Validation Process**:
- Follow [SAP Audit Workflow](../../dev-docs/workflows/SAP_AUDIT_WORKFLOW.md) Step 4.6
- Use Diataxis compliance scorecard (pass/partial/fail per artifact)
- Address critical category misalignments before Pilot status
- Achieve full compliance before Active status

**Common Anti-Patterns to Avoid**:
- ❌ Tutorial content in reference docs (e.g., "First, do X, then Y" in protocol-spec)
- ❌ API specifications in tutorials (e.g., schema definitions in adoption-blueprint)
- ❌ Design rationale in how-to guides (e.g., "we chose this approach because..." in awareness-guide)
- ❌ Problem-solving patterns in tutorials (e.g., "if you encounter error X, do Y" belongs in awareness-guide troubleshooting)
- ❌ Generic problem statements without context in charters

**Reference**:
- [SAP Diataxis Decision Matrix](../../user-docs/reference/sap-diataxis-mapping.md) (to be created)
- [Diataxis Framework Documentation](https://diataxis.fr/)
- [SAP-007: Documentation Framework](../documentation-framework/) - Comprehensive Diataxis guidance

---

## 6.5 Template vs Project-Level Adoption Pattern

**Background**: Some projects serve dual roles as both **template providers** (distributing infrastructure to downstream projects) and **development projects** (the repository itself). This pattern applies to meta-projects like chora-base.

**Adoption Levels by Role**:

**Template-Level Adoption**:
- Infrastructure location: `static-template/` or similar distribution directory
- Infrastructure is ready for downstream consumption
- Level reflects capability of distributed template
- Example: `static-template/.github/workflows/` with 8 workflows → Template-Level L3

**Project-Level Adoption**:
- Infrastructure location: Project root (`.github/workflows/`, `pytest.ini`, etc.)
- Infrastructure actively used by the meta-project itself
- Level reflects actual usage within the repository
- Example: No `.github/workflows/` in root → Project-Level L0

**When to Use This Pattern**:

Use this pattern when:
- ✅ Project distributes templates or blueprints to other projects
- ✅ Project's own needs differ from template capabilities
- ✅ Infrastructure exists in `static-template/` or similar
- ✅ Meta-project (primarily documentation + templates, minimal code)

Do NOT use this pattern when:
- ❌ Project is a regular application/library (not a template provider)
- ❌ Infrastructure only exists in project root
- ❌ Project uses all capabilities it distributes

**Ledger Documentation**:

When using this pattern, ledgers MUST document both levels:

**Header Format**:
```markdown
**Status**: Active (Level X - Template, Level Y - Project)
```

**Example** (from SAP-005 CI/CD Workflows):
```markdown
**Status**: Active (Level 3 - Template, Level 0 - Project)
```

**Required Section** (add to ledger immediately after header):
```markdown
## ⚠️ IMPORTANT: Template vs Project-Level Adoption

**SAP-XXX Adoption Levels:**
- **Template-Level Adoption: LX** ✅ (This ledger tracks template adoption)
  - Location: `static-template/[infrastructure-path]`
  - [Description of distributed infrastructure]
  - [Projects inheriting template get capability]

- **Project-Level Adoption: LY** ⚠️ ([project-name] repository itself)
  - Location: `[infrastructure-path]` (project root)
  - [Description of project-level usage or intentional non-usage]
  - [Explanation if L0: why meta-project doesn't need this capability]

**Why This Matters**:
- Template-level LX = Infrastructure ready for distribution ✅
- Project-level LY = [project-name] itself [does/doesn't] use [capability] ⚠️
- This pattern applies to [other SAPs using this pattern]
```

**Deployment Tracking Table**:

Ledgers using this pattern MUST track both adoption types:

```markdown
| Project | Adoption Type | Infrastructure Installed | Status | Notes |
|---------|---------------|--------------------------|--------|-------|
| [project] (template) | Template-Level LX | ✅ [details] | ✅ Active | Distributed to downstream projects |
| [project] (project) | Project-Level LY | [✅/❌] [details] | [✅/⚠️] [status] | [Explanation] |
```

**Validation**:

Infrastructure validation scripts MUST:
- Check both template-level and project-level infrastructure
- Accept L0 project-level for template providers (intentional gap acceptable)
- Validate template infrastructure matches claimed template-level
- Flag over-reports (claimed L3 template but no infrastructure in `static-template/`)

**Examples**:

**SAP-003 (project-bootstrap)**:
- Template-Level L3: Complete `static-template/` with all project files ✅
- Project-Level L0: chora-base already bootstrapped, doesn't re-bootstrap itself ⚠️

**SAP-004 (testing-framework)**:
- Template-Level L3: `static-template/pytest.ini` with 85% threshold ✅
- Project-Level L1: Tests exist (60 tests, 100% pass), but only 4% coverage ⚠️

**SAP-005 (ci-cd-workflows)**:
- Template-Level L3: `static-template/.github/workflows/` with 8 workflows ✅
- Project-Level L0: No `.github/workflows/` in root (meta-project, no CI needed) ⚠️

**SAP-006 (quality-gates)**:
- Template-Level L3: `static-template/.pre-commit-config.yaml` with 7 hooks ✅
- Project-Level L0: No `.pre-commit-config.yaml` in root (meta-project, manual QA) ⚠️

**Guarantees**:
- Ledgers using this pattern MUST document both levels in header
- Ledgers MUST include explanatory section immediately after header
- Deployment tables MUST track both template and project adoption
- L0 project-level is ACCEPTABLE for template providers (not a failure)
- Infrastructure validators MUST accept intentional L0 gaps for meta-projects

**References**:
- SAP-004 ledger: [docs/skilled-awareness/testing-framework/ledger.md](../testing-framework/ledger.md)
- SAP-005 ledger: [docs/skilled-awareness/ci-cd-workflows/ledger.md](../ci-cd-workflows/ledger.md)
- SAP-006 ledger: [docs/skilled-awareness/quality-gates/ledger.md](../quality-gates/ledger.md)
- Infrastructure validation script: [scripts/validate-sap-infrastructure.py](../../../scripts/validate-sap-infrastructure.py)

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

## 10. Self-Evaluation Criteria (SAP-009 Phase 4)

This section documents the validation criteria for SAP-000 awareness files (AGENTS.md and CLAUDE.md), required by SAP-009 Phase 4.

### Validation Commands

```bash
# Check awareness files exist
ls docs/skilled-awareness/sap-framework/{AGENTS,CLAUDE}.md

# Validate structure
python scripts/sap-evaluator.py --deep SAP-000

# Check YAML frontmatter
head -20 docs/skilled-awareness/sap-framework/AGENTS.md | grep -A 15 "^---$"
head -20 docs/skilled-awareness/sap-framework/CLAUDE.md | grep -A 15 "^---$"
```

### Expected Workflow Coverage

**AGENTS.md**: 5 workflows
1. Create New SAP (15-30 min) - Generate 5 artifacts with templates
2. Install SAP (5-15 min) - Follow adoption blueprint
3. Validate SAP Structure (1-2 min) - Check artifacts and YAML
4. Upgrade SAP Version (10-30 min) - Follow migration path
5. Query SAP Catalog (30s) - Filter by status/domain

**CLAUDE.md**: 5 workflows
1. Creating New SAP with Write and Bash - Tool-specific artifact creation
2. Installing SAP with Read and Bash - Blueprint execution patterns
3. Validating SAP Structure with Bash - Evaluator usage
4. Upgrading SAP Version with Read and Edit - Version updates
5. Querying SAP Catalog with Read and Grep - jq filtering

**Rationale for Equivalent Coverage**: Both files have 5 workflows. AGENTS.md focuses on generic agent patterns (templates, validation, migration), while CLAUDE.md shows specific Claude Code tool usage (Write for artifacts, Read for blueprints, Edit for updates, Bash for validation, jq for queries). Different organization but equivalent guidance.

### User Signal Pattern Tables

**AGENTS.md**: 4 tables
- SAP Creation (4 signals: "create new SAP", "package this capability", etc.)
- SAP Installation (3 signals: "install SAP-NNN", "adopt SAP-NNN", etc.)
- SAP Validation (4 signals: "validate SAP-NNN", "check SAP structure", etc.)
- SAP Upgrade (3 signals: "upgrade SAP-NNN", "migrate to v2.0.0", etc.)

**CLAUDE.md**: Workflows incorporate user signals inline (not separate tables)

**Rationale**: AGENTS.md uses pattern tables for quick lookup (generic agent pattern), CLAUDE.md embeds signals in workflows (Claude Code pattern). Different formats, equivalent coverage.

### Progressive Loading

Both files use YAML frontmatter with phase-based loading:
- phase_1: Quick reference + core workflows (0-50k tokens)
- phase_2: Advanced operations (50-100k tokens)
- phase_3: Full including troubleshooting (100k+ tokens)

### Known Acceptable Gaps

**P2 Gap - Coverage Variance**: AGENTS.md and CLAUDE.md have different workflow organizations (pattern tables vs inline signals). This is acceptable because:
1. Both provide equivalent guidance for SAP framework operations
2. AGENTS.md optimized for generic agent quick lookup
3. CLAUDE.md optimized for Claude Code tool demonstrations
4. Tolerance: ±30% workflow count difference acceptable per SAP-009 protocol

---

**Version History**:
- **1.0.0** (2025-10-27): Initial protocol specification
