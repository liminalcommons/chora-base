# Git Hooks for SAP-051

Client-side git hooks for enforcing Git Workflow Patterns (SAP-051).

## Hooks

### commit-msg
Validates commit messages against [Conventional Commits v1.0.0](https://www.conventionalcommits.org/):
- Format: `<type>(<scope>): <description>`
- Valid types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
- Configurable via git config

### pre-push
Validates branch names before push:
- Format: `<type>/<identifier>-<description>`
- Valid types: feature, bugfix, hotfix, chore, docs, refactor, test
- Skips main/master branches

### pre-commit
Optional pre-commit checks (disabled by default):
- Trailing whitespace detection
- Large file warnings (>1MB)
- Secret pattern detection

## Installation

```bash
# Install hooks
git config core.hooksPath .githooks
git config hooks.commit-msg-enabled true
git config hooks.pre-push-enabled true
git config hooks.pre-commit-enabled false  # optional
```

Or use the justfile recipe:
```bash
just git-setup
```

## Configuration

### Commit Message Validation

```bash
# Custom commit types
git config conventional-commits.types "feat,fix,docs,custom"

# Max subject length (default: 72)
git config conventional-commits.max-subject-length 100

# Strict mode (fail on warnings)
git config conventional-commits.strict true
```

### Branch Name Validation

```bash
# Custom branch types
git config branch-naming.types "feature,bugfix,custom"

# Max branch length (default: 100)
git config branch-naming.max-length 80

# Enable conflict checking
git config branch-naming.check-conflicts true
```

### Disable Hooks

```bash
# Disable specific hooks
git config hooks.commit-msg-enabled false
git config hooks.pre-push-enabled false

# Bypass hooks for single commit
git commit --no-verify
```

## Testing

See [tests/test_sap_051/README.md](../tests/test_sap_051/README.md) for test suite documentation.

## Troubleshooting

### Hook not running

```bash
# Check configuration
git config --get core.hooksPath
git config --get hooks.commit-msg-enabled

# Verify hooks are executable
ls -la .githooks/
chmod +x .githooks/*  # Unix/Mac
```

### Permission denied (Unix/Mac)

```bash
chmod +x .githooks/*
```

### Hook fails on Windows

Ensure Git Bash is installed and used for hook execution.

## References

- [SAP-051 Documentation](../docs/skilled-awareness/git-workflow-patterns/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
