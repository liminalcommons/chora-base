# Contributing to chora-base

Thank you for considering contributing to chora-base! This document provides guidelines for contributing to the project.

---

## 🔴 Cross-Platform Development (REQUIRED)

**CRITICAL**: All code MUST work on Windows, Mac, and Linux without modification.

### Quick Checklist

Before writing ANY code, ensure:

- [ ] Using `pathlib.Path` for file paths (not string concatenation)
- [ ] File I/O uses `encoding='utf-8'`
- [ ] Scripts with emojis have UTF-8 console reconfiguration
- [ ] No new bash scripts (use Python)
- [ ] Read [scripts/AGENTS.md](scripts/AGENTS.md) for patterns
- [ ] Copied [templates/cross-platform/python-script-template.py](templates/cross-platform/python-script-template.py) for new scripts

### Validation

```bash
# Validate your changes
python scripts/validate-windows-compat.py --file path/to/your-script.py

# Install pre-commit hook (REQUIRED)
git config core.hooksPath .githooks
```

### Resources

- **Quick Reference**: [scripts/AGENTS.md](scripts/AGENTS.md)
- **Template**: [templates/cross-platform/python-script-template.py](templates/cross-platform/python-script-template.py)
- **Complete Guide**: [SAP-030: Cross-Platform Fundamentals](docs/skilled-awareness/cross-platform-fundamentals/)
- **Testing**: [Windows Testing Checklist](docs/dev-docs/testing/windows-testing-checklist.md)

### Common Mistakes

❌ **DON'T**:
```python
# Missing encoding
with open("file.txt") as f:
    content = f.read()

# String path concatenation (Unix-only)
path = f"{base_dir}/subdir/file.txt"

# Hardcoded home directory
home = Path("~/projects")
```

✅ **DO**:
```python
# Always specify encoding
with open("file.txt", encoding='utf-8') as f:
    content = f.read()

# Use pathlib (cross-platform)
from pathlib import Path
path = Path(base_dir) / "subdir" / "file.txt"

# Platform-independent home
home = Path.home() / "projects"
```

---

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork:
git clone https://github.com/YOUR_USERNAME/chora-base.git
cd chora-base
```

### 2. Install Pre-Commit Hook (REQUIRED)

```bash
git config core.hooksPath .githooks
```

This hook prevents Windows compatibility regressions by:
- Blocking new bash scripts
- Detecting missing UTF-8 encoding
- Validating path handling
- Warning about unsafe patterns

**To bypass** (not recommended):
```bash
git commit --no-verify
```

### 3. Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt

# Optional: Install development tools
pip install pytest black flake8
```

---

## Development Workflow

### Creating New Scripts

**ALWAYS start with the template**:

```bash
# Copy template
cp templates/cross-platform/python-script-template.py scripts/your-new-script.py

# Modify for your use case
# Template includes:
# - UTF-8 console reconfiguration
# - File I/O with encoding='utf-8'
# - Pathlib usage throughout
# - Proper error handling
```

### Before Committing

```bash
# 1. Validate cross-platform compatibility
python scripts/validate-windows-compat.py --file scripts/your-script.py

# 2. Run tests (if applicable)
pytest tests/

# 3. Format code (optional)
black scripts/your-script.py

# 4. Commit (pre-commit hook runs automatically)
git add scripts/your-script.py
git commit -m "feat: add new script"
```

---

## Code Standards

### Python Style

- **Python Version**: 3.8+ (for broad compatibility)
- **Formatting**: Follow PEP 8 (black recommended)
- **Imports**: Standard library first, then third-party, then local
- **Docstrings**: Use for all public functions
- **Type Hints**: Encouraged but not required

### Cross-Platform Patterns (REQUIRED)

#### Pattern 1: UTF-8 Console Output

```python
import sys

# Required for scripts using emojis or Unicode
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
```

#### Pattern 2: File I/O

```python
# Always specify encoding for text files
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
```

#### Pattern 3: Path Handling

```python
from pathlib import Path

# Build paths with /operator
output_dir = Path(args.output)
file_path = output_dir / "subdir" / "file.txt"

# Home directory
home = Path.home()

# Current directory
current = Path.cwd()
```

---

## Pull Request Process

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow cross-platform patterns
- Add tests if applicable
- Update documentation
- Validate before committing

### 3. Create Pull Request

Use the PR template (automatically loaded):
- [ ] Cross-platform checklist completed
- [ ] Validation passed
- [ ] Tests added/updated
- [ ] Documentation updated

### 4. Code Review

- Address reviewer feedback
- Ensure CI passes on all platforms
- Maintain cross-platform compatibility

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_your_feature.py

# Run with coverage
pytest --cov=scripts --cov-report=html
```

### Cross-Platform Testing

#### Local Testing

```bash
# Validate Windows compatibility
python scripts/validate-windows-compat.py

# Test on different platforms (if available)
# - Windows: PowerShell or CMD
# - Mac: Terminal
# - Linux: Bash
```

#### CI/CD Testing

All pull requests are automatically tested on:
- Windows (latest)
- macOS (latest)
- Linux (Ubuntu latest)

With Python versions:
- 3.8
- 3.11

---

## Documentation

### What to Document

- **New Features**: Add to README.md
- **New Scripts**: Document in scripts/AGENTS.md
- **New SAPs**: Follow SAP framework (5 artifacts)
- **Breaking Changes**: Update CHANGELOG.md

### Documentation Style

- Use markdown
- Include code examples
- Provide both Unix and Windows examples for paths
- Keep it concise but complete

---

## Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(scripts): add metrics export to CSV

fix(windows): add stderr UTF-8 reconfiguration
Fixes emoji encoding errors on Windows

docs(sap-030): add path handling examples

chore(deps): update jinja2 to 3.1.0
```

---

## Release Process

Releases are managed by maintainers:

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create git tag
4. Push to GitHub
5. GitHub Actions creates release

---

## SAP Development

### Creating New SAPs

Follow SAP-029 (sap-generation):

```bash
# Generate SAP artifacts from catalog
python scripts/generate-sap.py SAP-XXX

# Or use sap-evaluator for validation
python scripts/sap-evaluator.py SAP-XXX
```

### SAP Structure

All SAPs must include 5 artifacts:
1. `capability-charter.md` - Problem/solution design
2. `protocol-spec.md` - Technical specification
3. `awareness-guide.md` or `AGENTS.md` - Agent patterns
4. `adoption-blueprint.md` - Installation guide
5. `ledger.md` - Adoption tracking

---

## Getting Help

### Resources

- **Documentation**: [docs/](docs/)
- **SAP Catalog**: [docs/skilled-awareness/INDEX.md](docs/skilled-awareness/INDEX.md)
- **Agent Awareness**: [AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md)

### Support Channels

- **Issues**: GitHub Issues for bugs and feature requests
- **Discussions**: GitHub Discussions for questions
- **Pull Requests**: For code contributions

### Common Issues

#### Issue: Pre-commit hook failing

**Solution**:
```bash
# Check what's wrong
python scripts/validate-windows-compat.py --file your-file.py

# Auto-fix common issues
python scripts/fix-encoding-issues.py --apply --file your-file.py
```

#### Issue: Emoji encoding error on Windows

**Solution**: Add UTF-8 reconfiguration to your script:
```python
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
```

#### Issue: Path issues on Windows

**Solution**: Use pathlib instead of string concatenation:
```python
from pathlib import Path
path = Path(base) / "subdir" / "file.txt"
```

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

**Positive behavior**:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Unacceptable behavior**:
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the project maintainers.

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

## Questions?

- Read [AGENTS.md](AGENTS.md) for agent-specific guidance
- Check [docs/dev-docs/](docs/dev-docs/) for developer documentation
- Review [docs/skilled-awareness/](docs/skilled-awareness/) for SAP documentation
- Open an issue if you're stuck

---

**Thank you for contributing to chora-base!** 🚀

**Remember**: Cross-platform compatibility (Windows/Mac/Linux) is non-negotiable. When in doubt, check [scripts/AGENTS.md](scripts/AGENTS.md) or copy the [template](templates/cross-platform/python-script-template.py).
