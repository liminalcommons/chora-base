"""
Pytest configuration and fixtures for {{ project_name }} tests

This file provides reusable fixtures and test utilities for the test suite.
"""

import sys
import json
import pytest
from pathlib import Path
from typing import Dict, Any
from unittest.mock import Mock, MagicMock

# Add project root to Python path for imports
repo_root = Path(__file__).parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))


# ============================================================================
# Filesystem Fixtures
# ============================================================================

@pytest.fixture
def temp_workspace(tmp_path) -> Path:
    """
    Create a temporary workspace directory for tests.

    This fixture provides a clean temporary directory for each test that needs
    a filesystem workspace. Useful for testing file operations, config files, etc.

    Example:
        def test_config_creation(temp_workspace):
            config_file = temp_workspace / "config.json"
            config_file.write_text('{"key": "value"}')
            assert config_file.exists()
    """
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace


@pytest.fixture
def temp_project_structure(temp_workspace) -> Path:
    """
    Create a typical project directory structure for testing.

    Structure:
        workspace/
        ├── src/
        ├── tests/
        ├── docs/
        └── config/

    Example:
        def test_project_layout(temp_project_structure):
            assert (temp_project_structure / "src").exists()
            assert (temp_project_structure / "tests").exists()
    """
    directories = ["src", "tests", "docs", "config"]
    for dir_name in directories:
        (temp_workspace / dir_name).mkdir()
    return temp_workspace


# ============================================================================
# Module Loading Fixtures (for testing hyphenated scripts)
# ============================================================================

@pytest.fixture
def load_hyphenated_script():
    """
    Factory fixture for loading Python scripts with hyphens in filename.

    Many CLI scripts use hyphens (e.g., my-script.py) which can't be imported
    normally. This fixture provides a helper to load them using importlib.

    Example:
        def test_script_function(load_hyphenated_script):
            script = load_hyphenated_script("scripts/my-script.py", "my_script")
            result = script.some_function()
            assert result == expected

    Credit: Pattern from chora-workspace SAP-004 reference tests
    """
    import importlib.util

    def _load_script(script_path: str, module_name: str):
        """Load a Python script with hyphens in the filename.

        Args:
            script_path: Path to the script (str or Path)
            module_name: Name to give the loaded module (use underscores)

        Returns:
            The loaded module
        """
        path = Path(script_path)
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    return _load_script


# ============================================================================
# Mock Data Fixtures
# ============================================================================

@pytest.fixture
def sample_json_data() -> Dict[str, Any]:
    """
    Sample JSON data for testing parsers, serializers, etc.

    Example:
        def test_json_parser(sample_json_data):
            result = parse_json(sample_json_data)
            assert result["name"] == "Test Item"
    """
    return {
        "name": "Test Item",
        "version": "1.0.0",
        "description": "Test data for unit tests",
        "items": [
            {"id": 1, "value": "item1"},
            {"id": 2, "value": "item2"},
        ],
        "metadata": {
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z"
        }
    }


# ============================================================================
# Mocking Utilities
# ============================================================================

@pytest.fixture
def mock_file_operations(monkeypatch):
    """
    Mock file I/O operations to avoid actual filesystem access.

    Returns a Mock object with read, write, exists methods.
    Use this for unit tests that should not touch the filesystem.

    Example:
        def test_config_read(mock_file_operations):
            mock_file_operations.read.return_value = '{"key": "value"}'
            result = load_config("config.json")
            assert result["key"] == "value"
    """
    mock = Mock()
    mock.read = MagicMock(return_value="")
    mock.write = MagicMock(return_value=None)
    mock.exists = MagicMock(return_value=True)

    return mock


@pytest.fixture
def captured_output(monkeypatch):
    """
    Capture print() output for testing console messages.

    Returns a list that accumulates all print() calls.

    Example:
        def test_console_output(captured_output):
            print_message("Hello, World!")
            assert "Hello, World!" in captured_output[0]
    """
    output_lines = []

    def mock_print(*args, **kwargs):
        output_lines.append(' '.join(str(arg) for arg in args))

    monkeypatch.setattr('builtins.print', mock_print)

    return output_lines


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual functions"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests with real file operations"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take longer to run"
    )
    config.addinivalue_line(
        "markers", "async: Asynchronous tests (requires pytest-asyncio)"
    )
