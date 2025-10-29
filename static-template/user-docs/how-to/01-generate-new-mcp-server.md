# How-To: Generate New MCP Server from chora-base

## Quick Reference

**Time:** 5 minutes
**Prerequisites:** Python 3.11+
**Result:** Working MCP server with memory system, scripts, workflows

---

## Steps

### 1. Run the Blueprint Generator

```bash
python setup.py /path/to/new-project
```

### 2. Provide Project Details

| Prompt | Answer | Notes |
|--------|--------|-------|
| `project_name` | `my-mcp-server` | Kebab-case |
| `project_slug` | `my-mcp-server` | Auto-derived |
| `package_name` | `my_mcp_server` | Snake_case |
| `project_description` | "MCP server for..." | Short description |
| `python_version` | `3.11` | Choose 3.11, 3.12, or 3.13 |
| `project_type` | `mcp_server` | **Important for MCP** |
| `include_memory_system` | `true` | Agent learning capability |
| `include_agents_md` | `true` | AI agent instructions |
| `include_cli` | `true` | CLI tools for memory |
| `cli_framework` | `click` | Click or Typer |
| `include_tests` | `true` | Testing infrastructure |
| `test_coverage_threshold` | `85` | 85% coverage required |
| `include_pre_commit` | `true` | Quality gates |
| `include_github_actions` | `true` | CI/CD workflows |
| `include_justfile` | `true` | Task automation |
| `license` | `MIT` | Choose license |

### 3. Run Setup

```bash
cd /path/to/new-project
./scripts/setup.sh
```

**What setup.sh does:**
- Creates virtual environment
- Installs dependencies
- Installs pre-commit hooks
- Runs smoke tests

### 4. Verify Installation

```bash
# Check entry point
my-mcp-server --help

# Check memory CLI
my-mcp-server-memory --help

# Run smoke tests
./scripts/smoke-test.sh
```

**Expected output:**
```
===== test session starts =====
collected 5 items

tests/test_server.py::test_ping PASSED
tests/test_memory.py::test_event_emission PASSED
...

===== 5 passed in 2.34s =====
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Setup script exits early | Ensure Python 3.11+ is active (`python --version`) |
| `setup.sh: Permission denied` | Run `chmod +x scripts/setup.sh` |
| Tests failing | Check Python version with `python --version` |

---

## Next Steps

- [How-To: Add Custom MCP Tools](03-add-custom-mcp-tools.md)
- [How-To: Integrate Memory System](04-add-memory-to-tools.md)
- [Reference: chora-base Blueprint Configuration](../reference/template-configuration.md)
