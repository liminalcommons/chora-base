## Description

<!-- Provide a brief description of your changes -->

## Type of Change

<!-- Check all that apply -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test addition/update

---

## 🔴 Cross-Platform Checklist (REQUIRED)

**ALL code must work on Windows, Mac, and Linux**

### Code Quality

- [ ] No new bash scripts added (use Python instead)
- [ ] All file I/O uses `encoding='utf-8'`
- [ ] All paths use `pathlib.Path` (not string concatenation)
- [ ] Scripts with emojis have UTF-8 console reconfiguration
- [ ] Copied [python-script-template.py](../templates/cross-platform/python-script-template.py) for new scripts
- [ ] Read [scripts/AGENTS.md](../scripts/AGENTS.md) for patterns

### Validation

- [ ] Ran `python scripts/validate-windows-compat.py`
- [ ] No critical issues found (or fixed before committing)
- [ ] Pre-commit hook passed (or explained bypass reason below)
- [ ] Tested on at least one platform (specify below)

### Testing Platform

<!-- Check all that you tested on -->

- [ ] Windows (specify version: _____________)
- [ ] macOS (specify version: _____________)
- [ ] Linux (specify distro: _____________)
- [ ] CI/CD (GitHub Actions)

**Note**: If you can't test on all platforms, that's OK - CI will validate.

---

## Testing

### Manual Testing

<!-- Describe what manual testing you performed -->

```bash
# Example:
python scripts/your-script.py --help
# Expected output: Help text with emojis (or graceful degradation)
```

### Automated Tests

- [ ] Added tests for new functionality
- [ ] Updated existing tests
- [ ] All tests pass locally (`pytest`)
- [ ] No tests needed (explain why below)

---

## Documentation

- [ ] Updated README.md (if user-facing changes)
- [ ] Updated scripts/AGENTS.md (if new script patterns)
- [ ] Updated relevant SAP documentation
- [ ] Added docstrings to new functions
- [ ] Updated CHANGELOG.md (for releases)

---

## Related Issues

<!-- Link related issues -->

Closes #<!-- issue number -->
Relates to #<!-- issue number -->

---

## Pre-Commit Hook Status

<!-- If you bypassed the hook, explain why -->

- [ ] Pre-commit hook passed automatically
- [ ] Bypassed hook (explain reason):
  - **Reason**: _______________________________
  - **Validated manually**: [ ]

---

## Screenshots (if applicable)

<!-- Add screenshots for UI changes or terminal output -->

---

## Additional Context

<!-- Add any other context about the PR here -->

### Why This Change?

<!-- Explain the motivation behind this change -->

### Alternatives Considered

<!-- What other approaches did you consider? -->

### Risks/Breaking Changes

<!-- Are there any risks or breaking changes? -->

---

## Cross-Platform Validation Results

<!-- Paste output of validation script -->

```bash
$ python scripts/validate-windows-compat.py
# Paste output here
```

---

## Checklist Before Requesting Review

- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Commented code in hard-to-understand areas
- [ ] Updated documentation
- [ ] No new warnings generated
- [ ] Added tests that prove fix/feature works
- [ ] New and existing tests pass locally
- [ ] Cross-platform checklist completed
- [ ] Ready for review

---

**For Reviewers**:

### Review Focus Areas

- [ ] Cross-platform compatibility verified
- [ ] No hardcoded platform-specific paths
- [ ] Proper encoding for file I/O
- [ ] Error handling appropriate
- [ ] Documentation clear and complete
- [ ] Tests adequate

---

<!--
Thank you for contributing to chora-base! 🚀

Remember:
- Cross-platform compatibility (Windows/Mac/Linux) is non-negotiable
- When in doubt, check scripts/AGENTS.md or copy the template
- Pre-commit hook is your friend - let it guide you
-->
