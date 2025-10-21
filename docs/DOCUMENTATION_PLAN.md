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

## Phase 4: Advanced Documentation Features (v1.7.0)

### Overview

Building on the v1.6.0 documentation standard, Phase 4 adds advanced features for power users who want even more sophisticated documentation tooling.

These features are **opt-in** via `documentation_advanced_features: true` (default: `false`) to avoid overwhelming new adopters.

### What's Included

When `documentation_advanced_features: true`, generated projects get:

#### 1. Advanced Test Extraction

Enhanced `extract_tests.py` with support for:

**Fixture Support:**
- Extract pytest fixtures from docs using `# FIXTURE: name` marker
- Auto-generated `@pytest.fixture` decorators
- Fixtures available to all tests in same file

**Async/Await Support:**
- Auto-detect async functions and `await` keywords
- Generate `@pytest.mark.asyncio` decorators
- Auto-import `pytest_asyncio` with installation warning

**Parameterized Tests:**
- Extract data-driven tests using `# PARAMETERIZE:` marker
- Generate `@pytest.mark.parametrize` decorators
- Supports multiple parameter sets

**Bash Test Support:**
- Extract bash/shell tests from documentation
- Generate executable `test_from_docs.sh` with colored output
- Support `# EXPECT_EXIT:` and `# EXPECT_OUTPUT:` markers

#### 2. Documentation Metrics (`scripts/docs_metrics.py`)

Generate comprehensive `DOCUMENTATION_METRICS.md` report with:

**Coverage Metrics:**
- % of code modules with corresponding docs
- API documentation count

**Health Score (0-100):**
- Broken Links (40 points): No broken internal links
- Staleness (30 points): <10% of docs >90 days old
- Frontmatter Completeness (30 points): >90% have all required fields

**Score Interpretation:**
- 🟢 80-100: Excellent health
- 🟡 60-79: Good, needs attention
- 🔴 <60: Poor, requires immediate action

**Activity Metrics:**
- Docs updated in last 30/60/90 days
- New (draft) documents count
- Deprecated documents count

**Quality Metrics:**
- Cross-reference density (% with `related:` links)
- Test extraction usage (% with `test_extraction: true`)
- Document type distribution

**Recommendations:**
- Actionable items based on metrics
- Prioritized by impact

#### 3. Documentation Query Tool (`scripts/query_docs.py`)

CLI for programmatic documentation search (AI agent friendly):

**Search Methods:**
- **Full-text search** with relevance scoring
- **Tag-based filtering** (multiple tags supported)
- **Graph traversal** (find related docs via `related:` links)
- **Type filtering** (tutorial, how-to, reference, explanation)
- **Combined queries** (topic + type, etc.)

**Relevance Scoring:**
- Title match: 1.0
- Tag match: 0.8
- Content match: 0.1 per occurrence (capped at 0.5)

**Output:**
- JSON format for machine consumption
- Sorted by relevance
- Includes all frontmatter fields

**AI Agent Integration:**
```python
import subprocess, json
result = subprocess.run(
    ["python", "scripts/query_docs.py", "--topic", "authentication"],
    capture_output=True, text=True
)
docs = json.loads(result.stdout)["results"]
```

#### 4. Enhanced CI Workflow

When `documentation_advanced_features: true`, `.github/workflows/docs-quality.yml` includes:

**New Job: `generate-metrics`**
- Runs on push to main/develop (not PRs)
- Generates `DOCUMENTATION_METRICS.md`
- Uploads as artifact (30-day retention)
- Displays summary in CI logs
- Non-blocking (doesn't fail build)

### Benefits for Adopters

**Living Documentation:**
- All test types supported (sync, async, fixtures, parameterized, bash)
- Examples stay executable across refactoring
- Bash integration tests extractable from docs

**Visibility:**
- Metrics show doc health at a glance
- Health score provides actionable targets
- Coverage tracking ensures completeness

**Discoverability:**
- Query tool helps find relevant docs fast
- Tag-based navigation for AI agents
- Graph traversal for exploring related content

**AI-Friendly:**
- JSON output for machine consumption
- Relevance scoring for ranking results
- Structured frontmatter for metadata extraction

### When to Enable

**Enable (`documentation_advanced_features: true`):**
- Large projects (50+ docs)
- Complex codebases with async patterns
- Projects needing documentation metrics tracking
- AI agent integrations requiring programmatic doc access
- Teams tracking documentation health over time

**Disable (`documentation_advanced_features: false`, default):**
- Small projects (<20 docs)
- Teams new to documentation standards
- Projects not using async/fixtures/parameterized tests
- Simple documentation needs

### Implementation Details

**Total Additions:** ~1,020 lines of Python code

**Scripts Enhanced:**
- `extract_tests.py` - Enhanced from ~200 to ~470 lines

**Scripts Created:**
- `docs_metrics.py` - ~300 lines
- `query_docs.py` - ~250 lines

**Files Modified:**
- `copier.yml` - Added `documentation_advanced_features` option
- `DOCUMENTATION_STANDARD.md` - Added ~310 line Advanced Features section
- `.github/workflows/docs-quality.yml` - Added `generate-metrics` job

**Advanced Features:**
1. Fixture extraction with `# FIXTURE:` marker
2. Async test detection and `@pytest.mark.asyncio` decoration
3. Parameterized tests with `# PARAMETERIZE:` marker
4. Bash test extraction with expectations
5. Documentation health scoring (0-100)
6. Metrics generation with recommendations
7. Programmatic doc query with JSON output

### Inspiration

Advanced features were developed based on:
- mcp-n8n's documentation-as-product practices
- Real-world usage patterns in chora-compose
- AI agent requirements for programmatic doc access
- Pytest best practices (fixtures, async, parameterized)

---

## Related Resources

- [README.md](../../README.md) - Template overview
- [Agentic Coding Best Practices Research](../research/Agentic%20Coding%20Best%20Practices%20Research.pdf) - Foundational research
- [Diátaxis Framework](https://diataxis.fr/) - Documentation system
- [A-MEM Paper](https://arxiv.org/abs/2502.12110) - Agentic Memory for LLM Agents
- [mcp-n8n Documentation Standard](https://github.com/liminalcommons/mcp-n8n/blob/main/docs/process/DOCUMENTATION_STANDARD.md) - Inspiration

---

**Documentation Plan Version:** 1.3.0
**Template Version:** chora-base v1.7.0
**Created:** 2025-10-17
**Last Updated:** 2025-10-21
**Status:** Phase 1-2 in progress (5/19 docs created) + Documentation Standard (v1.6.0) + Advanced Features (v1.7.0)

🤖 This plan ensures LLM agents are first-class users alongside human developers.
