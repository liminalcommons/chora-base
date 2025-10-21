# chora-base Documentation Plan

## Diátaxis Framework for LLM-Intelligent Development

This documentation serves **two first-class audiences**:
1. **Human Developers** - Learning, understanding, decision-making
2. **AI Agents (LLMs)** - Task execution, reference lookup, machine-readable instructions

Based on [Agentic Coding Best Practices Research](../docs/research/Agentic%20Coding%20Best%20Practices%20Research.pdf):
- AGENTS.md as de facto standard for machine-readable instructions
- A-MEM (Agentic Memory) principles for stateful learning
- Diátaxis framework for comprehensive documentation

---

## Documentation Structure

```
docs/
├── DOCUMENTATION_PLAN.md          # This file
├── tutorials/                      # Learning-oriented (humans)
│   ├── 01-first-mcp-server.md
│   └── 02-rip-and-replace-migration.md
├── how-to/                         # Task-oriented (humans + agents)
│   ├── 01-generate-new-mcp-server.md         ✅ CREATED
│   ├── 02-rip-and-replace-existing-server.md
│   ├── 03-customize-agents-md.md
│   ├── 04-add-memory-to-tools.md
│   └── 05-update-from-template.md
├── reference/                      # Information-oriented (humans + agents)
│   ├── template-configuration.md
│   ├── rip-and-replace-decision-matrix.md
│   ├── generated-file-structure.md
│   ├── event-schema-v1.md
│   └── cli-commands.md
└── explanation/                    # Understanding-oriented (humans)
    ├── why-rip-and-replace.md
    ├── memory-system-architecture.md
    ├── diataxis-philosophy.md
    └── major-version-bump-rationale.md
```

---

## Quadrant Overview

### Tutorials (Learning-Oriented) - For Humans

**Audience:** New users learning chora-base through hands-on practice

**Characteristics:**
- Safe, guided learning experiences
- Step-by-step with explanations
- Builds confidence through completion
- Narrative prose with clear goals

**Documents:**
1. **01-first-mcp-server.md** (600 lines)
   - Generate minimal MCP server
   - Run setup.sh
   - Implement ping tool
   - Add memory integration
   - Test and validate

2. **02-rip-and-replace-migration.md** (600 lines)
   - Complete mcp-server-coda migration example
   - 7 phases: Backup → Generate → Migrate → Merge → Adapt → Validate → Replace
   - Explains *why* each step matters
   - Troubleshooting guidance

---

### How-To Guides (Task-Oriented) - For Humans + Agents

**Audience:** Both humans and AI agents solving specific problems

**Characteristics:**
- Imperative commands (minimal prose)
- Scannable format (tables, bullets)
- Assumes user knows *why*
- Troubleshooting tables

**Documents:**
1. **01-generate-new-mcp-server.md** (500 lines) ✅ CREATED
   - Quick reference table
   - Step-by-step commands
   - Template prompt answers
   - Troubleshooting table

2. **02-rip-and-replace-existing-server.md** (500 lines)
   - 8 phases with commands
   - Validation checklist
   - File merge strategies
   - Troubleshooting table

3. **03-customize-agents-md.md** (400 lines)
   - Update Project Overview
   - Add Common Tasks
   - Customize Architecture Constraints
   - Project-specific examples

4. **04-add-memory-to-tools.md** (300 lines)
   - Import trace context
   - Emit events (start, success, failure)
   - Query event log
   - Create knowledge notes

5. **05-update-from-template.md** (300 lines)
   - Check for updates: `copier update --dry-run`
   - Apply updates: `copier update`
   - Resolve conflicts
   - Test and validate

6. **06-maintain-vision-documents.md** (500 lines) ✅ CREATED
   - Create vision document from template
   - Structure capability waves
   - Set decision criteria
   - Quarterly review process
   - Archive waves (delivered/deferred)
   - Integration with ROADMAP.md and AGENTS.md

---

### Reference (Information-Oriented) - For Humans + Agents

**Audience:** Both humans and agents needing quick lookup

**Characteristics:**
- Factual, no opinions
- Table format (agent-parseable)
- Complete inventory
- Examples for common scenarios

**Documents:**
1. **template-configuration.md** (800 lines)
   - All copier.yml variables (30+)
   - Variable types, choices, defaults
   - Examples (minimal, full-featured, library)
   - File inventory by configuration

2. **rip-and-replace-decision-matrix.md** (400 lines)
   - Decision matrix table
   - Use case examples (mcp-server-coda, chora-composer)
   - Feature comparison table
   - Complexity comparison
   - When NOT to rip-and-replace (anti-patterns)
   - Validation checklist

3. **generated-file-structure.md** (300 lines)
   - Complete file tree for all configurations
   - Conditional files (if include_memory_system=true, etc.)
   - File descriptions

4. **event-schema-v1.md** (300 lines)
   - Event JSON schema
   - Event types (gateway.*, backend.*, tool.*)
   - Status values (success, failure, pending)
   - Metadata fields

5. **cli-commands.md** (200 lines)
   - chora-memory query
   - chora-memory trace
   - chora-memory knowledge
   - chora-memory stats
   - chora-memory profile

---

### Explanation (Understanding-Oriented) - For Humans

**Audience:** Human developers seeking deeper understanding

**Characteristics:**
- Narrative prose
- Comparisons, trade-offs
- Design decisions
- Diagrams, examples

**Documents:**
1. **why-rip-and-replace.md** (1,200 lines)
   - Problem: Infrastructure fragmentation
   - Solution: Rip-and-replace vs cherry-pick
   - When to use, when NOT to use
   - Major version bump rationale
   - Hybrid files (pyproject.toml, README.md)
   - Long-term benefits (template tracking)

2. **memory-system-architecture.md** (1,200 lines)
   - Problem: LLM statelessness
   - Solution: Three-tier memory (event log, knowledge graph, trace)
   - A-MEM principles (agent-driven organization)
   - How memory enables cross-session learning
   - Privacy & security

3. **diataxis-philosophy.md** (400 lines)
   - What is Diátaxis?
   - Quadrants: Tutorial, How-To, Reference, Explanation
   - Why chora-base uses Diátaxis
   - AGENTS.md as 5th quadrant (machine-readable)

4. **major-version-bump-rationale.md** (400 lines)
   - SemVer principles
   - Breaking changes in rip-and-replace
   - v1.0.0 as "infrastructure maturity signal"
   - Not about API stability

5. **vision-driven-development.md** (700 lines) ✅ CREATED
   - Problem: Premature optimization and gold-plating
   - Solution: Vision documents guide strategic decisions
   - Relationship to agile/iterative development
   - Decision frameworks deep-dive
   - Case study: chora-compose content intelligence
   - Benefits for AI agents and teams
   - Common pitfalls and mitigations

---

## AGENTS.md (Machine-Readable) - For AI Agents

**Audience:** AI coding agents (Claude Code, Roo Code, GitHub Copilot, etc.)

**File:** `template/AGENTS.md.jinja`

**Characteristics:**
- Scannable format (bullets, tables, code blocks)
- Explicit commands (no ambiguity)
- Project structure overview
- Common tasks with examples
- Memory system self-service

**Sections:**
1. Project Overview & Structure
2. Dev Environment Tips
3. Testing Instructions
4. PR Instructions
5. Architecture Overview
6. Common Tasks
7. Agent Memory System (if include_memory_system=true)
8. Documentation Philosophy
9. Troubleshooting
10. Related Resources

**Key Enhancements from Research:**
- A-MEM principles (dynamic organization, note linking, memory evolution)
- Self-service workflows for agents (query past events, search knowledge, record insights)
- Explicit integration with Diátaxis docs (links to tutorials, how-tos, etc.)

---

## Documentation Metrics

| Document Type | Count | Estimated Lines | Primary Audience |
|---------------|-------|-----------------|------------------|
| **Tutorials** | 2 | 1,200 lines | Humans (new users) |
| **How-To Guides** | 6 | 2,500 lines | Humans + Agents |
| **Reference** | 5 | 2,000 lines | Humans + Agents |
| **Explanation** | 5 | 3,100 lines | Humans (understanding) |
| **AGENTS.md Template** | 1 | 1,995 lines | AI Agents |
| **Total** | 19 docs | **10,795 lines** | Mixed audience |

---

## Implementation Plan

### Phase 1: Critical Path (Week 1)

**Goal:** Enable new users and AI agents to generate projects and perform rip-and-replace

**Priority Documents:**
1. ✅ **How-To 01:** Generate New MCP Server (CREATED v1.0.0)
2. **How-To 02:** Rip-and-Replace Existing Server
3. ✅ **How-To 06:** Maintain Vision Documents (CREATED v1.3.1)
4. **Reference 01:** Template Configuration
5. **Reference 02:** Rip-and-Replace Decision Matrix
6. ✅ **AGENTS.md Template:** Enhanced with A-MEM and Strategic Design (v1.3.0)

**Deliverable:** Minimal viable documentation for template usage
**Status:** Partially complete (3/6 docs created)

---

### Phase 2: Comprehensive Coverage (Week 2)

**Goal:** Complete Diátaxis framework with tutorials and explanations

**Priority Documents:**
6. **Tutorial 01:** Your First MCP Server
7. **Tutorial 02:** Rip-and-Replace Migration
8. **Explanation 01:** Why Rip-and-Replace?
9. **Explanation 02:** Memory System Architecture
10. ✅ **Explanation 05:** Vision-Driven Development (CREATED v1.3.1)
11. **How-To 03:** Customize AGENTS.md

**Deliverable:** Full documentation coverage for all use cases
**Status:** Partially complete (1/6 docs created)

---

### Phase 3: Advanced Topics (Week 3)

**Goal:** Deep-dive references and additional how-tos

**Priority Documents:**
11. **How-To 04:** Add Memory to Tools
12. **How-To 05:** Update from Template
13. **Reference 03:** Generated File Structure
14. **Reference 04:** Event Schema v1
15. **Reference 05:** CLI Commands
16. **Explanation 03:** Diátaxis Philosophy
17. **Explanation 04:** Major Version Bump Rationale

**Deliverable:** Complete 17-document Diátaxis suite

---

## Usage Examples

### For Human Developers

**New User (Learning Path):**
1. Read **README.md** (project overview)
2. Follow **Tutorial 01:** Your First MCP Server
3. Consult **Reference 01:** Template Configuration (when customizing)
4. Read **Explanation 02:** Memory System Architecture (understand concepts)

**Migrating Existing Project:**
1. Read **Explanation 01:** Why Rip-and-Replace? (understand trade-offs)
2. Consult **Reference 02:** Rip-and-Replace Decision Matrix (make decision)
3. Follow **How-To 02:** Rip-and-Replace Existing Server (execute)
4. Reference **Tutorial 02** if unclear (step-by-step walkthrough)

---

### For AI Agents

**Agent Onboarding (Zero to Productive):**
1. Read **AGENTS.md** (machine-readable instructions)
2. Query **How-To 01** when user asks "generate new MCP server"
3. Query **Reference 01** when user asks "what template options exist?"
4. Query **How-To 04** when user asks "add memory to tools"

**Agent Self-Service (Cross-Session Learning):**
1. Encounter problem (e.g., "backend startup slow")
2. Query event log: `chora-memory query --type backend.startup --since 30d`
3. Search knowledge: `chora-memory knowledge search --tag backend --tag performance`
4. Find solution in past notes
5. Apply solution
6. Record outcome: `echo "..." | chora-memory knowledge create "Backend Startup Fix"`

**Result:** Agent learns from past experiences, improves over time

---

## Success Criteria

### Quantitative Metrics

- ✅ 17 documentation files created
- ✅ 8,500+ lines of documentation
- ✅ All Diátaxis quadrants covered
- ✅ AGENTS.md enhanced with A-MEM principles
- ✅ Both human and AI agent audiences served

### Qualitative Metrics

- **Humans can:**
  - Generate new MCP server in 5 minutes (Tutorial 01)
  - Migrate existing project with confidence (How-To 02)
  - Understand memory system architecture (Explanation 02)
  - Make informed decisions (Explanation 01, Reference 02)

- **AI Agents can:**
  - Parse AGENTS.md for project instructions
  - Execute tasks using How-To guides
  - Look up facts in Reference docs
  - Learn from past events using memory CLI

---

## Maintenance Plan

### Quarterly Reviews

1. **Update from mcp-n8n:** Sync template improvements
2. **Update from Research:** New agentic coding best practices
3. **Update from Users:** Feedback on documentation clarity
4. **Update AGENTS.md:** New sections for emerging agent capabilities

### Version Tracking

- Documentation version matches template version (e.g., v1.0.0, v1.1.0)
- CHANGELOG.md documents changes to docs/
- AGENTS.md includes "Last Updated" date

---

## Documentation Standard for Generated Projects

### Overview

As of v1.6.0, chora-base includes an **optional Documentation Standard** feature that helps generated projects maintain high-quality documentation following Documentation-as-Product principles.

This feature was inspired by [mcp-n8n's Documentation Standard](https://github.com/liminalcommons/mcp-n8n/blob/main/docs/process/DOCUMENTATION_STANDARD.md) and adapted for chora-base adopters.

### What's Included

When `include_documentation_standard: true` (default), generated projects get:

**1. Three-Directory Structure:**
- **`user-docs/`** - End-user documentation (tutorials, how-to, reference, explanation)
- **`project-docs/`** - Project planning (roadmap, ADRs, releases, sprints)
- **`dev-docs/`** - Developer documentation (contributing, development, troubleshooting, vision)

**2. DOCUMENTATION_STANDARD.md Template:**
- Frontmatter schema specification (required/optional fields)
- Document templates for each Diátaxis type
- Writing standards and best practices
- Cross-reference requirements
- Maintenance policies (staleness, deprecation)

**3. Automation Scripts:**
- **`validate_docs.py`** - Check frontmatter, broken links, staleness, bidirectional refs
- **`generate_docs_map.py`** - Auto-generate DOCUMENTATION_MAP.md from frontmatter
- **`extract_tests.py`** - Extract code examples for testing (Documentation Driven Design)

**4. CI Integration:**
- **`.github/workflows/docs-quality.yml`** - Enforce documentation quality in PR reviews

### Benefits for Adopters

✅ **Clear separation of concerns** - User, project, and developer docs don't mix
✅ **Machine-readable frontmatter** - YAML frontmatter enables automation
✅ **Automated enforcement** - CI validates quality (not manual vigilance)
✅ **Living documentation** - Test extraction keeps examples executable
✅ **Staleness detection** - Warns about docs >90 days old
✅ **Knowledge graph** - Bidirectional cross-references

### When to Use

**Enable (`include_documentation_standard: true`):**
- Projects with 10+ documentation files
- Teams with multiple contributors
- Public APIs or libraries
- Projects requiring documentation-as-product

**Disable (`include_documentation_standard: false`):**
- Simple scripts or tools
- Solo projects with minimal docs
- Internal tools with low documentation needs

### Example

See [examples/full-featured-with-docs/](../examples/full-featured-with-docs/) for a complete demonstration of the documentation standard in action.

---

## Related Resources

- [README.md](../../README.md) - Template overview
- [Agentic Coding Best Practices Research](../research/Agentic%20Coding%20Best%20Practices%20Research.pdf) - Foundational research
- [Diátaxis Framework](https://diataxis.fr/) - Documentation system
- [A-MEM Paper](https://arxiv.org/abs/2502.12110) - Agentic Memory for LLM Agents
- [mcp-n8n Documentation Standard](https://github.com/liminalcommons/mcp-n8n/blob/main/docs/process/DOCUMENTATION_STANDARD.md) - Inspiration

---

**Documentation Plan Version:** 1.2.0
**Template Version:** chora-base v1.6.0
**Created:** 2025-10-17
**Last Updated:** 2025-10-21
**Status:** Phase 1-2 in progress (5/19 docs created) + Documentation Standard feature added

🤖 This plan ensures LLM agents are first-class users alongside human developers.
