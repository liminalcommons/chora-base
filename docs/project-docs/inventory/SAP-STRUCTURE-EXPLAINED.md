# SAP Structure Explained

**Purpose**: Clarify the structure of SAPs and the different uses of "blueprint"

---

## Where Are All The SAP Files Stored?

### SAP Documentation Location

All **14 SAPs** are stored in:
```
docs/reference/skilled-awareness/
```

Each SAP has its own directory with **5 standard artifacts**:

### SAP Directory Structure

```
docs/reference/skilled-awareness/
├── sap-framework/              (SAP-000)
│   ├── capability-charter.md
│   ├── protocol-spec.md
│   ├── awareness-guide.md
│   ├── adoption-blueprint.md   ← Documentation for adopting this SAP
│   └── ledger.md
├── inbox/                      (SAP-001)
│   ├── capability-charter.md
│   ├── protocol-spec.md
│   ├── awareness-guide.md
│   ├── adoption-blueprint.md
│   └── ledger.md
├── chora-base/                 (SAP-002)
│   ├── capability-charter.md
│   ├── protocol-spec.md
│   ├── awareness-guide.md
│   ├── adoption-blueprint.md
│   └── ledger.md
├── project-bootstrap/          (SAP-003)
│   ├── capability-charter.md
│   ├── protocol-spec.md
│   ├── awareness-guide.md
│   ├── adoption-blueprint.md
│   └── ledger.md
├── testing-framework/          (SAP-004)
├── ci-cd-workflows/            (SAP-005)
├── quality-gates/              (SAP-006)
├── documentation-framework/    (SAP-007)
├── automation-scripts/         (SAP-008)
├── agent-awareness/            (SAP-009)
├── memory-system/              (SAP-010)
├── docker-operations/          (SAP-011)
├── development-lifecycle/      (SAP-012)
└── metrics-tracking/           (SAP-013)
```

**Total**: 14 SAPs × 5 artifacts each = **70 SAP documentation files**

---

## The Two Different "Blueprint" Concepts

### 1. SAP Adoption Blueprints (Documentation)

**What**: Documentation files that guide you through adopting a SAP
**Where**: `docs/reference/skilled-awareness/{sap-name}/adoption-blueprint.md`
**Count**: 14 files (one per SAP)
**Purpose**: Step-by-step adoption guide

**Example** - `docs/reference/skilled-awareness/project-bootstrap/adoption-blueprint.md`:
```markdown
# Adoption Blueprint: Project Bootstrap

## Level 1: First Project Generation (30 minutes)
- [ ] Clone chora-base
- [ ] Run setup.py to generate first project
- [ ] Verify generated project structure
...
```

These are **guides for humans/agents** on how to install and use the capability.

---

### 2. Project Template Blueprints (Template Files)

**What**: Template files with `{{ variable }}` placeholders for project generation
**Where**: `blueprints/` (root directory of chora-base)
**Count**: 11 files
**Purpose**: Templates used by SAP-003 (project-bootstrap) to generate new MCP server projects

**Example** - `blueprints/README.md.blueprint`:
```markdown
# {{ project_name }}

{{ project_description }}

## Installation

pip install {{ package_name }}
...
```

These are **actual template files** that get processed by `setup.py` when generating a new project.

#### Complete List of Project Template Blueprints

```
blueprints/
├── .env.example.blueprint      → .env.example
├── .gitignore.blueprint        → .gitignore
├── AGENTS.md.blueprint         → AGENTS.md
├── CHANGELOG.md.blueprint      → CHANGELOG.md
├── CLAUDE.md.blueprint         → CLAUDE.md
├── README.md.blueprint         → README.md
├── ROADMAP.md.blueprint        → ROADMAP.md
├── mcp__init__.py.blueprint    → src/{package}/mcp/__init__.py
├── package__init__.py.blueprint → src/{package}/__init__.py
├── pyproject.toml.blueprint    → pyproject.toml
└── server.py.blueprint         → src/{package}/mcp/server.py
```

When you run `python setup.py my-new-project`, these 11 blueprint files get processed:
- `{{ project_name }}` → "my-new-project"
- `{{ package_name }}` → "my_new_project"
- etc.

---

## How They Work Together

### SAP-003 (Project Bootstrap) Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ SAP-003: Project Bootstrap                                  │
│                                                             │
│ Documentation (in docs/reference/skilled-awareness/):      │
│   ├── capability-charter.md    (what & why)                │
│   ├── protocol-spec.md          (technical contracts)       │
│   ├── awareness-guide.md        (agent workflows)           │
│   ├── adoption-blueprint.md     (how to adopt) ◄── Doc!    │
│   └── ledger.md                 (adoption tracking)         │
│                                                             │
│ Implementation (root of chora-base):                       │
│   ├── setup.py                  (orchestrator script)       │
│   ├── blueprints/               (template files) ◄── Templates!
│   │   ├── README.md.blueprint                               │
│   │   ├── AGENTS.md.blueprint                               │
│   │   └── ... (11 total)                                    │
│   └── static-template/          (100+ static files)         │
│       ├── tests/                                            │
│       ├── scripts/                                          │
│       └── ...                                               │
└─────────────────────────────────────────────────────────────┘
```

**Flow**:
1. Read **adoption-blueprint.md** (documentation) to learn how to use SAP-003
2. Run `python setup.py my-project` (implementation)
3. `setup.py` copies `static-template/` files
4. `setup.py` processes `blueprints/*.blueprint` files
5. New project is generated!

---

## Why The Naming Overlap?

Both use "blueprint" but mean different things:

| Concept | Type | Purpose |
|---------|------|---------|
| **SAP adoption-blueprint.md** | Documentation | Guide for adopting a SAP capability |
| **Project template .blueprint files** | Template code/docs | Templates for generating new projects |

The naming is coincidental - they serve completely different purposes:
- **adoption-blueprint.md**: "Here's the blueprint (plan) for adopting this capability"
- **README.md.blueprint**: "This is a blueprint (template) file that will become README.md"

---

## Summary

### All 14 SAPs are in:
```
docs/reference/skilled-awareness/{sap-name}/
```

Each has 5 artifacts including an **adoption-blueprint.md** (documentation).

### The template blueprints are in:
```
blueprints/
```

These are the 11 template files used by SAP-003 to generate new projects.

### Are blueprints/ actively a part of SAPs?

**Yes!** The `blueprints/` directory and its 11 template files are **covered by SAP-003 (project-bootstrap)** because they're the templates that SAP-003 uses to generate new MCP server projects.

However, they're **implementation files** (templates), not SAP documentation. The **documentation** for SAP-003 is in:
```
docs/reference/skilled-awareness/project-bootstrap/
├── capability-charter.md
├── protocol-spec.md
├── awareness-guide.md
├── adoption-blueprint.md    ← Doc explaining how to use SAP-003
└── ledger.md
```

The **implementation** of SAP-003 includes:
```
setup.py                     ← Orchestrator
blueprints/                  ← Templates (11 files)
static-template/             ← Static files (100+ files)
```

All three are covered by SAP-003 in the inventory.
