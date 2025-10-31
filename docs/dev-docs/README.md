# Developer Documentation

**Purpose**: Documentation for developers working ON this project (chora-base itself)

**Audience**: Engineers building features, contributors to the codebase, AI agents implementing functionality

---

## What's Here

This directory contains process documentation using **Diátaxis for development**:

- **[workflows/](workflows/)** - Complete development lifecycle processes
  - [DOCUMENTATION_MIGRATION_WORKFLOW.md](workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md) - How to migrate docs to 4-domain structure
  - See also: static-template references TDD, BDD, DDD workflows

- **examples/** - Code walkthroughs and demonstrations
  - (To be populated in future waves)

- **vision/** - Long-term capability roadmap
  - (To be populated in future waves)

- **research/** - Technical investigations and learnings
  - [CLAUDE_Complete.md](research/CLAUDE_Complete.md) - Claude-specific learnings
  - [adopter-learnings-executable-docs.md](research/adopter-learnings-executable-docs.md) - Executable documentation insights

- **explanation/** - Conceptual deep-dives, design philosophy
  - (To be populated in future waves)

---

## Diátaxis Structure

This domain uses **Diátaxis for development processes**:

| Type | Purpose | Example |
|------|---------|---------|
| **how-to/** | Process guides | "How to implement TDD" |
| **explanation/** | Conceptual understanding | "Why test-first" |
| **reference/** | Process specifications | "Workflow definitions" |
| **tutorials/** | Learning-oriented lessons | "Your first feature using DDD→BDD→TDD" |

---

## Not Here

- **End-user guides**: See [../user-docs/](../user-docs/)
- **Sprint plans**: See [../project-docs/sprints/](../project-docs/sprints/)
- **API documentation**: See [../user-docs/reference/](../user-docs/reference/)
- **SAP documentation**: See [../skilled-awareness/](../skilled-awareness/)

---

## Related Documentation

**Other Domains**:
- [User Documentation](../user-docs/) - For product users
- [Project Documentation](../project-docs/) - Project lifecycle artifacts
- [Skilled Awareness](../skilled-awareness/) - SAP Framework (capability packages)

**Root Documentation**:
- [Architecture](../ARCHITECTURE.md) - 4-domain model explained
- [AGENTS.md](../../AGENTS.md) - Complete project guide for AI agents
- [README.md](../../README.md) - Project overview

**Examples from static-template**:
- [static-template/dev-docs/workflows/](../../static-template/dev-docs/workflows/) - TDD, BDD, DDD workflows
- [static-template/dev-docs/examples/](../../static-template/dev-docs/examples/) - Feature walkthrough

---

## How to Use This Domain

### For AI Agents

1. **Before starting feature**: Read workflows/ for processes to follow
2. **During development**: Reference research/ for learnings and patterns
3. **After feature**: Document insights in research/ or examples/

### For Human Developers

1. **Learning**: Start with workflows/ for development processes
2. **Reference**: Use explanation/ for design philosophy
3. **Improvement**: Contribute learnings to research/

### For Contributors

1. **Process docs**: Add to workflows/ if creating new development patterns
2. **Examples**: Add to examples/ for complex feature demonstrations
3. **Research**: Add to research/ for technical investigations
4. **Vision**: Add to vision/ for long-term capability planning

---

**Domain Version**: 1.0 (Wave 1)
**Last Updated**: 2025-10-28
**Status**: Active
