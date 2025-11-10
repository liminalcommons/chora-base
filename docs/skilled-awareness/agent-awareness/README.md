# SAP-009: Agent Awareness System

**Version:** 1.1.0 | **Status:** Active | **Maturity:** Production

> Nested AGENTS.md/CLAUDE.md pattern with 5-level hierarchy—progressive context loading saves 60-70% tokens through "nearest file wins" navigation.

---

## 🚀 Quick Start (2 minutes)

```bash
# Read root awareness (project overview)
cat CLAUDE.md

# Navigate to domain-specific awareness
cat docs/skilled-awareness/CLAUDE.md

# Read SAP-specific awareness
cat docs/skilled-awareness/inbox/CLAUDE.md

# Validate awareness structure
bash scripts/validate-awareness-links.sh
```

**First time?** → Read root [CLAUDE.md](../../../CLAUDE.md) for navigation guide

---

## 📖 What Is SAP-009?

SAP-009 provides the **nested AGENTS.md/CLAUDE.md pattern** with 5-level hierarchy (root → domain → SAP → feature → component) for progressive context loading. The "nearest file wins" principle enables agents to navigate efficiently, loading only necessary context and achieving 60-70% token savings vs reading all documentation upfront.

**Key Innovation**: Meta-SAP documenting the awareness system itself—proves SAP framework can capture recursive, self-referential systems.

---

## 🎯 When to Use

Use SAP-009 when you need to:

1. **Progressive context loading** - Load docs incrementally (0-10k → 10-50k → 50-200k tokens)
2. **Nested navigation** - Navigate from root → domain → capability → feature
3. **Token optimization** - 60-70% savings through domain-specific awareness files
4. **Self-documenting systems** - Capture meta-patterns and recursive structures
5. **Agent onboarding** - Guide agents through project structure efficiently

**Not needed for**: Simple projects (<5 files), or if project has single README only

---

## ✨ Key Features

- ✅ **5-Level Hierarchy** - root → domain → SAP → feature → component
- ✅ **"Nearest File Wins"** - Read closest AGENTS.md/CLAUDE.md for context
- ✅ **60-70% Token Savings** - Domain-specific files vs reading all docs
- ✅ **Progressive Loading** - 3 phases (Essential 0-10k, Extended 10-50k, Comprehensive 50-200k)
- ✅ **Dual Files** - AGENTS.md (generic) + CLAUDE.md (Claude-specific)
- ✅ **Validation** - Scripts check structure, links, token tracking
- ✅ **Integration** - ALL 32+ SAPs use this pattern

---

## 📚 Quick Reference

### 5-Level Hierarchy

```
/CLAUDE.md                          ← Level 1: Root (project overview)
/AGENTS.md

docs/skilled-awareness/             ← Level 2: Domain (SAP capabilities)
├── CLAUDE.md
├── AGENTS.md
│
├── inbox/                          ← Level 3: SAP (specific capability)
│   ├── CLAUDE.md
│   ├── AGENTS.md
│   │
│   └── features/                   ← Level 4: Feature (optional)
│       ├── CLAUDE.md
│       └── coordination.md
│
└── scripts/                        ← Level 5: Component (optional)
    ├── CLAUDE.md
    └── specific-script-patterns.md
```

---

### 3 Progressive Loading Phases

#### Phase 1: Essential (0-10k tokens)
**Goal**: Understand project structure and navigation

**Read**:
- `/CLAUDE.md` - Root navigation guide
- Domain-level `CLAUDE.md` for target area

**Output**: Know where to find detailed information

---

#### Phase 2: Extended (10-50k tokens)
**Goal**: Load technical specifications for task

**Read**:
- SAP-level `protocol-spec.md` for complete technical details
- SAP-level `AGENTS.md`/`CLAUDE.md` for operating patterns

**Output**: Complete technical understanding

---

#### Phase 3: Comprehensive (50-200k tokens)
**Goal**: Deep understanding for complex implementations

**Read**:
- `capability-charter.md` for design rationale
- `ledger.md` for adoption metrics
- `adoption-blueprint.md` for installation from scratch
- Source code files as needed

**Output**: Comprehensive understanding

---

## 🔗 Integration with Other SAPs

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-000** (SAP Framework) | Foundation | All SAPs use nested awareness pattern |
| **SAP-002** (Chora-Base) | Meta-Container | Chora-base itself uses SAP-009 for navigation |
| **ALL 32+ SAPs** | Universal Pattern | Every SAP has AGENTS.md + awareness-guide.md (or CLAUDE.md) |
| **SAP-016** (Link Validation) | Quality | Validates awareness file links |
| **SAP-031** (Enforcement) | Layer 3 | Awareness structure validation (5-10% prevention) |

---

## 🏆 Success Metrics

- **Token Savings**: 60-70% via domain-specific awareness files
- **Coverage**: 100% of SAPs have AGENTS.md/awareness-guide.md
- **Navigation Efficiency**: 3-level lookup finds any capability in <30s
- **Integration**: ALL 32+ SAPs use this pattern (universal adoption)

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete nested awareness specification
- **[AGENTS.md](AGENTS.md)** - Generic agent navigation patterns (17KB)
- **[CLAUDE.md](CLAUDE.md)** - Claude-specific progressive loading (15KB)
- **[Root CLAUDE.md](../../../CLAUDE.md)** - Project-level navigation guide
- **[adoption-blueprint.md](adoption-blueprint.md)** - How to create awareness files

---

**Version History**:
- **1.1.0** (2025-10-28) - Added 5-level hierarchy, progressive loading phases, 60-70% token savings
- **1.0.0** (2025-06-15) - Initial nested AGENTS.md pattern

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
