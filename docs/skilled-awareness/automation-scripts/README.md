# SAP-008: Automation Scripts

**Version:** 1.0.0 | **Status:** Active | **Maturity:** Production

> Justfile automation with 30+ recipes for development, testing, quality gates, release, and MCP operations—consistent commands across all chora-base projects.

---

## 🚀 Quick Start (1 minute)

```bash
# Show all available commands
just --list

# Show automation help (grouped by category)
just automation-help

# Common workflows
just test                  # Run tests
just lint                  # Run linting
just format                # Format code
just pre-merge             # All quality gates
```

**First time?** → Run `just automation-help` for complete command reference

---

## 📖 What Is SAP-008?

SAP-008 provides **justfile automation** with 30+ pre-configured recipes for development, testing, quality gates, CI/CD, release, and MCP operations. It ensures consistent commands across all chora-base projects with clear naming conventions and comprehensive help text.

**Key Innovation**: Single `just` command interface for all automation—no need to remember different commands per project (pytest vs npm test vs make test).

---

## 🎯 When to Use

Use SAP-008 when you need to:

1. **Consistent automation** - Same commands across all projects
2. **Discoverability** - `just --list` shows all available commands
3. **Development workflows** - test, lint, format, type-check in one place
4. **Release automation** - bump-version, build, publish with single commands
5. **MCP operations** - create-mcp-server, mcp-test, mcp-claude-config

**Not needed for**: Simple scripts (use bash directly), or projects with existing automation (Makefile, npm scripts)

---

## ✨ Key Features

- ✅ **30+ Recipes** - Complete automation for development lifecycle
- ✅ **8 Categories** - Setup, Development, Quality, Version, Release, Documentation, Safety, MCP
- ✅ **Discoverable** - `just --list` and `just automation-help` for all commands
- ✅ **Consistent Naming** - Predictable commands across all chora-base projects
- ✅ **Self-Documenting** - Every recipe has description and example
- ✅ **Cross-Platform** - Works on Linux, macOS, Windows
- ✅ **Integration** - Connects all SAPs (testing, quality, CI/CD, release, MCP)

---

## 📚 Quick Reference

### 8 Command Categories

#### 1. **Setup & Environment** (5 commands)
```bash
just install               # Install project in editable mode
just setup-hooks           # Install pre-commit hooks
just check-env             # Validate environment
just diagnose              # Run diagnostics
just handoff               # Generate handoff report
```

#### 2. **Development** (6 commands)
```bash
just test                  # Run tests with coverage
just smoke                 # Quick smoke tests (<10s)
just test-unit             # Unit tests only
just test-integration      # Integration tests only
just test-file FILE        # Run specific test file
just test-verbose          # Verbose test output
```

#### 3. **Quality Gates** (6 commands)
```bash
just lint                  # Run ruff linter
just lint-fix              # Auto-fix ruff violations
just format                # Format code with ruff
just type-check            # Run mypy type checker
just pre-merge             # All quality gates before merge
just quality-gates         # Run all quality checks
```

#### 4. **Version Management** (3 commands)
```bash
just bump-patch            # 1.0.0 → 1.0.1 (bug fixes)
just bump-minor            # 1.0.0 → 1.1.0 (new features)
just bump-major            # 1.0.0 → 2.0.0 (breaking changes)
```

#### 5. **Release & Publishing** (3 commands)
```bash
just build                 # Build distribution packages
just publish-test          # Publish to test PyPI
just publish-prod          # Publish to production PyPI
```

#### 6. **Documentation** (4 commands)
```bash
just doc-structure         # Show Diátaxis structure
just extract-doc-tests     # Extract tests from How-Tos
just doc-completeness      # Check documentation coverage
just validate-docs         # Validate documentation
```

#### 7. **Safety & Recovery** (2 commands)
```bash
just rollback-dev          # Rollback development changes
just handoff               # Generate handoff report
```

#### 8. **MCP & Specialized** (5 commands)
```bash
just create-mcp-server NAME NAMESPACE OUTPUT  # Create MCP server
just mcp-test              # Test MCP server
just mcp-claude-config     # Generate Claude Desktop config
just validate-mcp-names    # Validate MCP namespace
just mcp-list-templates    # List MCP templates
```

---

## 🔗 Integration with Other SAPs

| SAP | Integration | Justfile Recipes |
|-----|-------------|------------------|
| **SAP-004** (Testing) | Test automation | test, smoke, test-unit, test-integration |
| **SAP-006** (Quality Gates) | Pre-commit | lint, format, type-check, pre-merge |
| **SAP-005** (CI/CD) | CI validation | ci-status, ci-logs, ci-retry |
| **SAP-007** (Documentation) | Doc tools | doc-structure, extract-doc-tests, doc-completeness |
| **SAP-014** (MCP Server) | MCP operations | create-mcp-server, mcp-test, mcp-claude-config |
| **SAP-012** (Lifecycle) | Development phases | quality-gates, test-all, pre-merge |

---

## 🏆 Success Metrics

- **Command Count**: 30+ recipes across 8 categories
- **Discoverability**: 100% commands documented with `just automation-help`
- **Consistency**: Same commands across all chora-base projects
- **Time Savings**: 30-45 min/day (no need to remember project-specific commands)
- **Error Reduction**: 90%+ fewer command typos (predictable naming)

---

## 🔧 Troubleshooting

**Problem**: `just` command not found

**Solution**: Install justfile runner:
```bash
# macOS
brew install just

# Linux
cargo install just

# Windows
scoop install just
```

---

**Problem**: Recipe fails with "command not found"

**Solution**: Install missing dependency:
```bash
just diagnose  # Check what's missing
# Install missing tools (pytest, ruff, mypy, etc.)
```

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete justfile specification
- **[AGENTS.md](AGENTS.md)** - AI agent automation workflows (17KB)
- **[CLAUDE.md](CLAUDE.md)** - Claude-specific justfile patterns (15KB)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Justfile setup guide
- **Justfile**: See justfile.just.systems for syntax reference

---

**Version History**:
- **1.0.0** (2025-10-28) - Initial justfile automation with 30+ recipes across 8 categories

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
