# SAP-007: Documentation Framework

**Version:** 1.1.0 | **Status:** Pilot | **Maturity:** Production

> Diátaxis-based documentation with 4 document types (Tutorial, How-To, Reference, Explanation)—organize docs by user intent with frontmatter validation and executable How-Tos.

---

## 🚀 Quick Start (2 minutes)

```bash
# Show documentation structure
just doc-structure

# Extract tests from How-To guides
just extract-doc-tests

# Check documentation completeness
just doc-completeness

# Convert How-To to BDD scenario (L3 pattern)
just doc-to-bdd docs/user-docs/how-to/feature.md
```

**First time?** → Read [adoption-blueprint.md](adoption-blueprint.md) for Diátaxis setup (10-min read)

---

## 📖 What Is SAP-007?

SAP-007 provides **Diátaxis-based documentation** organized by user intent into 4 document types: Tutorial (learning), How-To (problem-solving), Reference (information), Explanation (understanding). It includes frontmatter validation, executable How-Tos with test extraction, and documentation-driven development workflows.

**Key Innovation**: Documentation-First approach with executable How-Tos—write docs before code, extract tests from docs, ensuring docs stay accurate and testable.

---

## 🎯 When to Use

Use SAP-007 when you need to:

1. **Organize documentation** - Structure docs by user intent (learning vs problem-solving vs reference)
2. **Documentation-Driven Development** - Write docs before code (DDD workflow)
3. **Executable documentation** - Extract tests from How-To guides to keep docs accurate
4. **Dual audience** - Serve humans (learning) and AI agents (task execution)
5. **Quality standards** - Validate frontmatter, enforce structure, measure completeness

**Not needed for**: Simple README-only projects, or if you prefer alternative doc frameworks (Sphinx, MkDocs)

---

## ✨ Key Features

- ✅ **Diátaxis-Based** - 4 document types organized by user intent
- ✅ **Frontmatter-Validated** - YAML metadata with schema enforcement
- ✅ **Executable How-Tos** - Code examples extractable to pytest tests
- ✅ **Documentation-First** - Write docs before code (DDD workflow)
- ✅ **Dual Audience** - Serves humans (learning) and AI agents (task execution)
- ✅ **4 CLI Commands** - doc-structure, extract-doc-tests, doc-completeness, doc-to-bdd
- ✅ **Template System** - Standardized templates for each document type
- ✅ **Integration** - Links to SAP-012 (Lifecycle) for L3 Documentation-First pattern

---

## 📚 Quick Reference

### 4 Diátaxis Document Types

#### 1. **Tutorial** (Learning-Oriented)
- **Purpose**: Teach through step-by-step lessons
- **User Intent**: "Teach me how to use this"
- **Structure**: Sequential steps with expected output
- **Example**: "Build your first MCP server"
- **Location**: `docs/user-docs/tutorials/`

#### 2. **How-To Guide** (Task-Oriented)
- **Purpose**: Solve specific problems
- **User Intent**: "Show me how to solve X"
- **Structure**: Problem → Solution with variations
- **Example**: "How to add custom error handling"
- **Location**: `docs/user-docs/how-to/`
- **Special**: Executable (extract tests via `just extract-doc-tests`)

#### 3. **Reference** (Information-Oriented)
- **Purpose**: Provide technical specifications
- **User Intent**: "What parameters does this take?"
- **Structure**: API docs, schemas, configurations
- **Example**: "MCP Protocol Schema Reference"
- **Location**: `docs/user-docs/reference/`

#### 4. **Explanation** (Understanding-Oriented)
- **Purpose**: Explain concepts and design decisions
- **User Intent**: "Why does this work this way?"
- **Structure**: Context, rationale, trade-offs
- **Example**: "Why we use Diátaxis for documentation"
- **Location**: `docs/user-docs/explanation/`

---

### 4 CLI Commands

#### **doc-structure** - Show Diátaxis Structure
```bash
just doc-structure
# Shows: 4-domain hierarchy with file counts
# Use: Understand current documentation organization
```

#### **extract-doc-tests** - Extract Tests from How-Tos
```bash
just extract-doc-tests
# Runs: python scripts/extract-doc-tests.py docs/user-docs/how-to/ tests/extracted/
# Output: pytest tests extracted from code blocks in How-To guides
# Use: Keep documentation testable and accurate
```

#### **doc-completeness** - Check Documentation Coverage
```bash
just doc-completeness
# Shows: Missing document types, coverage percentage
# Use: Ensure all 4 Diátaxis types are represented
```

#### **doc-to-bdd** - Convert How-To to BDD (L3 Pattern)
```bash
just doc-to-bdd docs/user-docs/how-to/feature.md
# Output: BDD scenario in features/feature.feature
# Use: Documentation-First workflow (write docs → generate BDD → implement)
```

---

## 🔗 Integration with Other SAPs

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-012** (Lifecycle) | L3 Pattern | Documentation-First: write How-To → extract BDD → implement with TDD |
| **SAP-004** (Testing) | Test Extraction | Extract pytest tests from How-To code blocks |
| **SAP-031** (Enforcement) | Layer 3 Validation | Frontmatter validation, structure checks (5-10% prevention) |
| **SAP-016** (Link Validation) | Doc Quality | Validate links in all markdown files |
| **SAP-003** (Bootstrap) | Templates | Generated projects include docs/ with Diátaxis structure |

**Documentation-First Workflow (L3 Pattern)**:
```bash
# Phase 3 (Requirements): Write How-To BEFORE implementation
# 1. Write executable How-To guide
cat > docs/user-docs/how-to/user-authentication.md <<EOF
# How to Add User Authentication

## Quick Start
\`\`\`bash
# Step 1: Install auth library
pip install fastapi-auth
\`\`\`

## Implementation
\`\`\`python
from fastapi import FastAPI
from auth import authenticate

app = FastAPI()

@app.post("/login")
def login(username: str, password: str):
    return authenticate(username, password)
\`\`\`
EOF

# 2. Extract BDD scenario from How-To
just doc-to-bdd docs/user-docs/how-to/user-authentication.md
# Output: features/user-authentication.feature

# 3. Run BDD (RED - not implemented yet)
pytest features/ --gherkin

# 4. Implement with TDD until BDD turns GREEN
just tdd-cycle tests/test_authentication.py

# 5. Confirm BDD scenarios pass
pytest features/ --gherkin  # ✅ GREEN
```

---

## 📂 Directory Structure

```
docs/
├── user-docs/              # User-facing documentation
│   ├── tutorials/          # Learning-oriented
│   ├── how-to/             # Task-oriented (executable)
│   ├── reference/          # Information-oriented
│   └── explanation/        # Understanding-oriented
├── dev-docs/               # Developer documentation
│   ├── architecture/
│   └── contributing/
├── project-docs/           # Project management
│   ├── plans/
│   └── decisions/
└── skilled-awareness/      # SAP capabilities
    ├── sap-framework/
    └── ... (32+ SAPs)
```

---

## 🏆 Success Metrics

- **Documentation Coverage**: 100% (all 4 Diátaxis types represented)
- **Executable How-Tos**: 80%+ have extractable tests
- **Frontmatter Compliance**: 95%+ docs have valid YAML frontmatter
- **Documentation-First Adoption**: 60%+ features start with How-To guides
- **Time Savings**: 40-60% improvement in doc quality (vs ad-hoc documentation)

---

## 🎓 Diátaxis Decision Matrix

| User Says | Document Type | Location |
|-----------|---------------|----------|
| "I'm new, how do I get started?" | **Tutorial** | docs/user-docs/tutorials/ |
| "How do I solve problem X?" | **How-To** | docs/user-docs/how-to/ |
| "What parameters does function Y take?" | **Reference** | docs/user-docs/reference/ |
| "Why was this designed this way?" | **Explanation** | docs/user-docs/explanation/ |

---

## 🔧 Troubleshooting

**Problem**: `extract-doc-tests` fails with "no code blocks found"

**Solution**: Ensure How-To guides have code blocks in proper format:
```markdown
## Implementation
\`\`\`python
# This will be extracted to tests
def example():
    return "Hello"
\`\`\`
```

---

**Problem**: Documentation feels disorganized

**Solution**: Apply Diátaxis decision matrix:
- Is it teaching? → Tutorial
- Is it problem-solving? → How-To
- Is it specification? → Reference
- Is it explanation? → Explanation

---

**Problem**: Frontmatter validation fails

**Solution**: Add required YAML frontmatter:
```yaml
---
title: "How to Add Authentication"
audience: [developers, agents]
time: 15 minutes
prerequisites: [Python 3.11+, FastAPI]
difficulty: intermediate
---
```

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete Diátaxis specification (18KB)
- **[AGENTS.md](AGENTS.md)** - AI agent documentation workflows (17KB, 9-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude-specific doc patterns (15KB, 8-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Diátaxis setup guide (10-min read)
- **[capability-charter.md](capability-charter.md)** - Design rationale
- **[ledger.md](ledger.md)** - Production adoption metrics

---

## 📞 Support

- **Documentation**: Read [protocol-spec.md](protocol-spec.md) for complete reference
- **Issues**: Report bugs via GitHub issues with `[SAP-007]` prefix
- **Feedback**: Log adoption feedback in [ledger.md](ledger.md)
- **Diátaxis**: See diataxis.fr for framework reference

---

**Version History**:
- **1.1.0** (2025-10-28) - Added executable How-Tos, test extraction, L3 Documentation-First pattern
- **1.0.0** (2025-06-15) - Initial Diátaxis-based documentation with 4 document types

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
