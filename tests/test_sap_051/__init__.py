"""
SAP-051 Git Workflow Patterns - Test Suite

Comprehensive validation tests for SAP-051 implementation including:
- Git hook validation (commit-msg, pre-push, pre-commit)
- Justfile recipe automation tests
- End-to-end workflow integration tests

Test Coverage:
- Hook Tests: ~340 lines (40%)
- Recipe Tests: ~220 lines (26%)
- Integration Tests: ~280 lines (33%)
- Total: ~840 lines across 80+ test cases

Usage:
    pytest tests/test_sap_051/ -v

See README.md for detailed documentation.
"""

__version__ = "1.0.0"
__all__ = [
    "test_commit_msg_hook",
    "test_pre_push_hook",
    "test_justfile_recipes",
    "test_integration",
    "conftest",
]
