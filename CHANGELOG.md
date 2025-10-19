# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-10-18

### Fixed

#### CRITICAL Generalization Issues (12 issues fixed)

**Python Import Errors:**
- Fixed hardcoded `mcp_n8n` package imports in memory module
- Converted `template/src/{{package_name}}/memory/__init__.py` → `__init__.py.jinja`
- Converted `template/src/{{package_name}}/memory/trace.py` → `trace.py.jinja`
- Changed `from mcp_n8n.memory.*` → `from {{ package_name }}.memory.*`
- Changed `source: str = "mcp-n8n"` → `source: str = "{{ project_slug }}"`
- **Impact:** Generated projects would have ImportError without this fix

**Hardcoded Absolute Paths:**
- Removed hardcoded `/Users/victorpiper/code/*` paths from 3 scripts
- `check-env.sh.jinja`: Removed mcp-n8n-specific backend checks
- `mcp-tool.sh.jinja`: Use script directory detection instead of hardcoded path
- `handoff.sh.jinja`: Generic `/path/to/` instead of absolute paths
- **Impact:** Scripts would fail for all users except original developer

**Placeholder GitHub Usernames:**
- Fixed `yourusername` placeholder in 3 files → `{{ github_username }}`
- `CONTRIBUTING.md.jinja` (line 59)
- `publish-prod.sh.jinja` (line 161)
- `diagnose.sh.jinja` (line 196)
- **Impact:** Generated docs would have placeholder URLs

**Security Email Placeholder:**
- Added `security_email` copier variable (defaults to `{{ author_email }}`)
- Fixed `security@example.com` → `{{ security_email }}` in CONTRIBUTING.md (2 instances)
- **Impact:** Projects would have non-functional contact email

#### HIGH Priority Generalization Issues (6 issues fixed)

**.chora/memory/README.md.jinja Project References:**
- Line 3: `working with mcp-n8n` → `working with {{ project_slug }}`
- Line 62: `"source": "mcp-n8n"` → `"source": "{{ project_slug }}"`
- Lines 64-65: `chora:*`/`chora-composer` → `example:*`/`example-backend`
- Line 243: `"to": "chora-composer"` → `"to": "other-project"`
- Lines 323-326: Handoff example made generic
- Line 477: `between mcp-n8n and chora-composer` → `between {{ project_slug }} and other projects`
- Line 495: Removed Phase reference, made compatibility note generic
- **Impact:** Memory system docs would confuse adopters

### Added

- **Generalization Audit Documentation:** `docs/GENERALIZATION_AUDIT_2025-10-18.md`
  - Comprehensive audit of all 35 template files
  - 47 total issues identified
  - 18 issues fixed in v1.2.0 (12 CRITICAL + 6 HIGH)
  - 29 remaining issues documented for future releases

### Changed

- **copier.yml**: Added `security_email` variable for security contact configuration
- **Python source files**: Now use .jinja extension to enable template variable substitution

### Technical Details

**Audit Scope:** All template files (.jinja, .py, .sh, .yml, .md)
**Issues Fixed:** 18 of 47 identified issues
**Remaining Issues:** 29 (17 HIGH, 10 MEDIUM, 2 LOW)
**Breaking Changes:** None (all fixes improve generalization)

**Testing:**
- ✅ No hardcoded `mcp-n8n`, `chora-composer`, `mcp-server-coda`
- ✅ No hardcoded `/Users/victorpiper/code/*` paths
- ✅ Python imports use template variables
- ✅ Security email configurable

**Migration:** No action required - template improvements only affect new project generation

## [1.1.1] - 2025-10-18

### Added

#### Knowledge Note Metadata Documentation
- **Frontmatter Schema**: Complete YAML frontmatter specification in `.chora/memory/README.md`
  - Required fields: `id`, `created`, `updated`, `tags`
  - Optional fields: `confidence`, `source`, `linked_to`, `status`, `author`, `related_traces`
  - Standards compliance notes (Obsidian, Zettlr, LogSeq, Foam compatibility)
  - Complete example with all fields
- **AGENTS.md Metadata Reference**: New "Knowledge Note Metadata Standards" section
  - Field definitions with enums and examples
  - Rationale for YAML frontmatter (semantic search, tool compatibility, knowledge graph)
  - Cross-reference to memory/README.md for complete schema
  - Updated Project Structure showing knowledge/ subdirectories

### Technical Details
- Documentation-only changes (98 lines added)
- Zero code modifications (conservative approach)
- Codifies existing Zettelkasten best practices
- Maintains AGENTS.md standard compliance (no frontmatter in AGENTS.md itself)
- Full tool interoperability preserved

## [1.1.0] - 2025-10-18

### Added

#### Documentation Suite (Diátaxis Framework)
- Complete documentation strategy in DOCUMENTATION_PLAN.md (390 lines)
- How-To Guide: Generate New MCP Server - Quick start for new projects
- How-To Guide: Rip-and-Replace Existing Server - 8-phase migration workflow
- Reference: Template Configuration - Complete lookup table for 30+ variables
- Reference: Rip-and-Replace Decision Matrix - Decision support for migration strategies
- Updated README with Documentation section separating human vs agent audiences

#### AGENTS.md Enhancements (+645 lines)
- **A-MEM Integration**: Complete 8-step learning loop with visual diagram
- **Memory Troubleshooting**: 260 lines of agent self-service debugging
  - CLI errors (commands not found, empty queries, JSON parsing)
  - Event log troubleshooting (emission verification, trace correlation)
  - Knowledge graph issues (broken links, tag corruption, search problems)
  - Trace context debugging (CHORA_TRACE_ID propagation)
- **Agent Self-Service Workflows**: Complete bash examples
  - Learning from past errors workflow
  - Creating knowledge from debugging
  - Rate limit fix example with 96% improvement metrics
- **Diátaxis Framework**: Documentation philosophy for dual audiences
  - Recommended reading order for AI agents
  - Human learning path
  - DDD/BDD/TDD workflow explanation
- **Common Tasks**: MCP tool implementation with memory integration examples

### Changed
- README.md: Added comprehensive Documentation section with Diátaxis structure
- README.md: Separated "For Human Developers" vs "For AI Agents" quick links

### Technical Details
- Total additions: 1,897 lines
- AGENTS.md grows from ~900 to ~1,294 lines when generated
- All enhancements validated with copier template generation
- Maintains 100% compliance with AGENTS.md official standard (OpenAI/Sourcegraph/Google)
- Implements cutting-edge A-MEM research (Jan 2025) for agent memory

## [1.0.0] - 2025-10-17

### Added
- Initial chora-base template extracted from mcp-n8n Phase 4.5/4.6
- Core infrastructure: project structure, dependency management, testing
- AI Agent Features: AGENTS.md, memory system (event log, knowledge graph, trace context)
- CLI Tools: chora-memory command for querying events and managing knowledge
- Quality Gates: pre-commit hooks, 85%+ test coverage, type checking, linting
- CI/CD: GitHub Actions workflows (test, lint, smoke, release, security)
- Developer Experience: setup scripts, justfile tasks, automated tooling
- Documentation: README, CONTRIBUTING, DEVELOPMENT, TROUBLESHOOTING templates
- Project Types: MCP server, library, CLI tool, web service support
- Memory Architecture: Event schema v1.0, CHORA_TRACE_ID propagation
- Copier template with 30+ configuration variables

[1.2.0]: https://github.com/liminalcommons/chora-base/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/liminalcommons/chora-base/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/liminalcommons/chora-base/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/liminalcommons/chora-base/releases/tag/v1.0.0
