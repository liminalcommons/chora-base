# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[1.1.1]: https://github.com/liminalcommons/chora-base/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/liminalcommons/chora-base/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/liminalcommons/chora-base/releases/tag/v1.0.0
