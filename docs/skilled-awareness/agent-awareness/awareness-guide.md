# Awareness Guide: Agent Awareness

**SAP ID**: SAP-009
**Version**: 1.0.0
**Target Audience**: AI agents
**Last Updated**: 2025-10-28

---

## 1. Quick Reference

**Read awareness files**:
- Working on project root? → Read root AGENTS.md
- Working on tests? → Read tests/AGENTS.md
- Working on scripts? → Read scripts/AGENTS.md
- Using Claude? → Also read corresponding CLAUDE.md

**Principle**: "Nearest File Wins" - Read awareness file closest to code you're editing

---

## 2. Agent Context Loading

**Essential Context (2-3k tokens)**:
- [protocol-spec.md](protocol-spec.md) Sections 2, 3 - File structure, context optimization

**For writing awareness files**:
- [protocol-spec.md](protocol-spec.md) Section 4 - Content guidelines

---

## 3. Common Workflows

### 3.1 Read Appropriate Awareness File

**Steps**:
1. Identify working directory (e.g., tests/)
2. Check for AGENTS.md in that directory
3. If exists, read tests/AGENTS.md
4. If not exists, read parent directory AGENTS.md
5. If using Claude, also read CLAUDE.md (same directory)

**Example**:
- Editing tests/test_server.py → Read tests/AGENTS.md + tests/CLAUDE.md
- Editing src/server.py → Read root AGENTS.md + root CLAUDE.md
- Running scripts/build.sh → Read scripts/AGENTS.md + scripts/CLAUDE.md

### 3.2 Optimize Context Loading (Claude)

**Context**: 2k tokens (Protocol Section 3)

**Progressive Loading**:
1. **Phase 1** (0-10k): Essential - Task + relevant AGENTS.md + active files
2. **Phase 2** (10-50k): Extended - Related modules + tests + docs
3. **Phase 3** (50-200k): Full - Entire codebase (complex refactoring only)

**Token Budget by Task**:
- Small feature: 15-30k
- Large feature: 30-60k
- Bug fix: 5-10k
- Refactor: 20-40k

---

## 4. Best Practices

**DO**:
- ✅ Read nearest awareness file first
- ✅ Use progressive context loading
- ✅ Create checkpoints every 5-10 interactions (Claude)
- ✅ Follow token budgets

**DON'T**:
- ❌ Read entire project AGENTS.md for domain task
- ❌ Load full context (50-200k) for simple tasks
- ❌ Skip domain-specific awareness files

---

## 5. Related Resources

- [protocol-spec.md](protocol-spec.md) - Technical contract
- [AGENTS.md.blueprint](/blueprints/AGENTS.md.blueprint)
- [CLAUDE.md.blueprint](/blueprints/CLAUDE.md.blueprint)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial awareness guide
