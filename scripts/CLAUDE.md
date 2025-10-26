# Claude Script Automation - mcp-orchestration

**Purpose:** Claude-specific patterns for script automation and build tooling in mcp-orchestration.

**Parent:** See [../CLAUDE.md](../CLAUDE.md) for project-level Claude guidance and [AGENTS.md](AGENTS.md) for generic script guide.

---

## Claude's Script Automation Strengths

Claude excels at script automation for mcp-orchestration because:

- **Cross-platform awareness** - Handles macOS, Linux, Windows differences
- **Error handling** - Comprehensive error checking and recovery
- **Documentation** - Clear usage instructions and examples
- **Integration** - Connects build, test, deploy workflows
- **Maintenance** - Updates scripts when dependencies change

---

## Common Script Tasks for mcp-orchestration

### Release Automation

```markdown
"Create release script for mcp-orchestration:

Steps:
1. Verify tests pass (pytest coverage ≥85%)
2. Verify type checking (mypy)
3. Update version in pyproject.toml
4. Update CHANGELOG.md with release notes
5. Sign release artifacts with Ed25519
6. Create git tag
7. Build Python package
8. Publish to PyPI

Error handling:
- Exit if tests fail
- Exit if working directory dirty
- Verify signature before publish

Generate: scripts/release.sh with --dry-run option"
```

### Key Management Scripts

```markdown
"Create Ed25519 key management script:

Operations:
1. generate - Create new Ed25519 keypair
2. rotate - Generate new key, re-sign artifacts
3. backup - Secure backup of private key
4. verify - Verify all artifact signatures

Safety:
- Never print private keys
- Secure file permissions (600)
- Verify before destructive operations
- Backup before rotation

Generate: scripts/manage-keys.sh"
```

### Storage Maintenance

```markdown
"Create content-addressable storage maintenance script:

Operations:
1. verify - Check SHA-256 integrity of all artifacts
2. compact - Remove unreferenced artifacts
3. backup - Export artifacts to archive
4. restore - Import from backup archive
5. stats - Show storage usage and artifact count

Safety:
- Dry-run mode for destructive operations
- Verify signatures before operations
- Log all maintenance actions to telemetry

Generate: scripts/storage-maintenance.sh"
```

---

## Development Workflow Scripts

### Setup Script

```markdown
"Create development environment setup script:

Steps:
1. Check Python ≥3.12
2. Create virtual environment
3. Install dependencies from pyproject.toml
4. Install pre-commit hooks
5. Initialize storage directories (var/storage, var/keys, var/telemetry)
6. Generate development Ed25519 keypair
7. Run smoke tests

Platforms: macOS, Linux
Generate: scripts/setup-dev.sh"
```

### Testing Scripts

```markdown
"Create comprehensive testing script:

Test suites:
1. Unit tests (pytest tests/)
2. Type checking (mypy src/)
3. Linting (ruff check src/)
4. Coverage report (pytest --cov, fail if <85%)
5. Integration tests (test via MCP Inspector)

Options:
- --quick: Skip slow integration tests
- --coverage: Generate HTML coverage report
- --watch: Re-run on file changes

Generate: scripts/test.sh"
```

---

## CI/CD Integration Scripts

### Pre-commit Hook Script

```markdown
"Create pre-commit validation script:

Checks:
1. ruff format --check (formatting)
2. ruff check (linting)
3. mypy (type checking)
4. pytest quick tests only (<10s)
5. Verify no secrets in commit (check for private keys)

Exit codes:
- 0: All checks pass
- 1: Formatting issues (auto-fixable)
- 2: Lint errors
- 3: Type errors
- 4: Test failures
- 5: Secrets detected (BLOCK COMMIT)

Generate: scripts/pre-commit-check.sh"
```

### Deployment Script

```markdown
"Create deployment script for mcp-orchestration:

Deployment targets:
1. Local (install to Claude Desktop)
2. Docker (build and run container)
3. PyPI (publish package)

Steps:
1. Verify version is not already deployed
2. Run full test suite
3. Build artifacts
4. Sign with Ed25519
5. Deploy to target
6. Verify deployment (smoke test)
7. Emit telemetry event

Generate: scripts/deploy.sh with --target option"
```

---

## Monitoring and Maintenance Scripts

### Telemetry Analysis

```markdown
"Create telemetry analysis script:

Analysis:
1. Parse var/telemetry/events.jsonl
2. Count events by type
3. Show error rate trends
4. Identify failing MCP tools
5. Generate usage report

Options:
- --since: Time range (24h, 7d, 30d)
- --type: Filter by event type
- --export: Export to JSON/CSV

Generate: scripts/analyze-telemetry.py"
```

### Health Check Script

```markdown
"Create health check script for mcp-orchestration:

Checks:
1. Storage accessible and writable
2. Ed25519 keys present and valid
3. MCP server responds to stdio
4. Recent telemetry events present
5. No recent error events

Usage:
- Run in cron for monitoring
- Exit code 0 = healthy, 1 = unhealthy
- JSON output for monitoring systems

Generate: scripts/health-check.sh"
```

---

## Troubleshooting Scripts

### Diagnostic Script

```markdown
"Create diagnostic script for troubleshooting:

Information gathered:
1. Python version and environment
2. Installed package versions
3. Storage directory status (size, artifact count)
4. Key status (present, permissions)
5. Recent telemetry errors (last 24h)
6. MCP server configuration
7. System info (OS, architecture)

Output:
- JSON format for support tickets
- Redact private keys and secrets

Generate: scripts/diagnostic.sh"
```

---

## Script Patterns for Claude

### Error Handling Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

error() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Example usage
[ -d "var/storage" ] || error "Storage directory not found"
success "Storage directory exists"
```

### Dry-run Pattern

```bash
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Conditional execution
if [ "$DRY_RUN" = true ]; then
    echo "Would execute: command"
else
    command
fi
```

### Signature Verification Pattern

```bash
# Verify artifact signature before operations
verify_artifact() {
    local artifact_hash=$1
    local signature=$2
    local public_key=$3

    python3 -c "
from mcp_orchestrator.crypto.signing import Signer
signer = Signer('$public_key')
is_valid = signer.verify(b'$artifact_hash', b'$signature', signer.public_key)
exit(0 if is_valid else 1)
" || error "Signature verification failed for $artifact_hash"

    success "Signature valid for $artifact_hash"
}
```

---

## Best Practices

### ✅ Do's

1. **Use strict error handling** - `set -euo pipefail` in bash
2. **Provide --dry-run** - For destructive operations
3. **Verify signatures** - Before storage/crypto operations
4. **Log to telemetry** - Emit events for important operations
5. **Document usage** - Clear help text and examples
6. **Cross-platform** - Test on macOS and Linux

### ❌ Don'ts

1. **Don't echo secrets** - Never print private keys
2. **Don't skip verification** - Always check signatures
3. **Don't ignore errors** - Exit on failures
4. **Don't assume paths** - Check existence before operations
5. **Don't skip tests** - Run tests before deployments

---

## Resources

- **Project Scripts:** [scripts/](./README.md)
- **Parent Claude Guide:** [../CLAUDE.md](../CLAUDE.md)
- **Generic Script Guide:** [AGENTS.md](AGENTS.md)
- **Telemetry Format:** var/telemetry/events.jsonl

---

**Version:** 3.3.0 (chora-base)
**Project:** mcp-orchestration v0.1.5
**Last Updated:** 2025-10-25
