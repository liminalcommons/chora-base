"""
Pytest configuration and fixtures for chora-base tests

Wave 5 (v4.1.0) - Testing install-sap.py script
"""

import json
import pytest
from pathlib import Path
from typing import Dict, Any
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_catalog() -> Dict[str, Any]:
    """
    Minimal valid catalog for testing.

    Contains 3 SAPs with various dependencies for testing dependency resolution.
    """
    return {
        "version": "4.1.0",
        "updated": "2025-10-30",
        "description": "Test catalog",
        "total_saps": 3,
        "saps": [
            {
                "id": "SAP-000",
                "name": "sap-framework",
                "full_name": "SAP Framework",
                "status": "active",
                "version": "1.0.0",
                "included_by_default": True,
                "size_kb": 125,
                "description": "Core SAP framework",
                "capabilities": ["SAP protocol"],
                "dependencies": [],
                "tags": ["meta", "required", "foundational"],
                "author": "chora-base",
                "location": "docs/skilled-awareness/sap-framework",
                "artifacts": {
                    "capability_charter": True,
                    "protocol_spec": True,
                    "awareness_guide": True,
                    "adoption_blueprint": True,
                    "ledger": True
                },
                "system_files": [],
                "phase": "Phase 1",
                "priority": "P0"
            },
            {
                "id": "SAP-001",
                "name": "inbox",
                "full_name": "Inbox Coordination Protocol",
                "status": "pilot",
                "version": "1.0.0",
                "included_by_default": False,
                "size_kb": 45,
                "description": "Cross-repo coordination protocol",
                "capabilities": ["Cross-repo coordination"],
                "dependencies": [],
                "tags": ["meta", "coordination"],
                "author": "chora-base",
                "location": "docs/skilled-awareness/inbox",
                "artifacts": {
                    "capability_charter": True,
                    "protocol_spec": True,
                    "awareness_guide": True,
                    "adoption_blueprint": True,
                    "ledger": True
                },
                "system_files": ["inbox/README.md", "inbox/INBOX_PROTOCOL.md"],
                "phase": "Phase 1",
                "priority": "P1"
            },
            {
                "id": "SAP-004",
                "name": "testing-framework",
                "full_name": "Testing Framework",
                "status": "active",
                "version": "1.0.0",
                "included_by_default": False,
                "size_kb": 85,
                "description": "Testing framework with pytest",
                "capabilities": ["Testing", "Coverage", "CI/CD"],
                "dependencies": ["SAP-000"],
                "tags": ["testing", "quality"],
                "author": "chora-base",
                "location": "docs/skilled-awareness/testing-framework",
                "artifacts": {
                    "capability_charter": True,
                    "protocol_spec": True,
                    "awareness_guide": True,
                    "adoption_blueprint": True,
                    "ledger": True
                },
                "system_files": [],
                "phase": "Wave 1",
                "priority": "P0"
            }
        ],
        "sap_sets": {
            "test-minimal": {
                "name": "Test Minimal Set",
                "description": "Minimal set for testing",
                "saps": ["SAP-000", "SAP-001"],
                "estimated_tokens": 20000,
                "estimated_hours": "2-3",
                "warnings": ["SAP-001 is in Pilot status"]
            },
            "test-with-deps": {
                "name": "Test Set With Dependencies",
                "description": "Set requiring dependency resolution",
                "saps": ["SAP-004"],
                "estimated_tokens": 10000,
                "estimated_hours": "1-2",
                "warnings": []
            }
        }
    }


@pytest.fixture
def invalid_catalog_json() -> str:
    """Invalid JSON for testing error handling."""
    return "{ invalid json: missing quotes }"


@pytest.fixture
def temp_source_dir(tmp_path, mock_catalog) -> Path:
    """
    Create temporary source directory with catalog and SAP files.

    Structure:
        source/
        ├── sap-catalog.json
        └── docs/
            └── skilled-awareness/
                ├── sap-framework/
                │   ├── capability-charter.md
                │   ├── protocol-spec.md
                │   ├── awareness-guide.md
                │   ├── adoption-blueprint.md
                │   └── ledger.md
                ├── inbox/
                │   └── [5 artifacts]
                └── testing-framework/
                    └── [5 artifacts]
    """
    source = tmp_path / "source"
    source.mkdir()

    # Create catalog
    catalog_file = source / "sap-catalog.json"
    catalog_file.write_text(json.dumps(mock_catalog, indent=2))

    # Create SAP directories with artifacts
    for sap in mock_catalog["saps"]:
        sap_dir = source / sap["location"]
        sap_dir.mkdir(parents=True, exist_ok=True)

        # Create 5 required artifacts
        artifacts = [
            "capability-charter.md",
            "protocol-spec.md",
            "awareness-guide.md",
            "adoption-blueprint.md",
            "ledger.md"
        ]
        for artifact in artifacts:
            (sap_dir / artifact).write_text(f"# {artifact}\n\nTest content for {sap['id']}")

        # Create system files if any
        for sys_file in sap.get("system_files", []):
            sys_file_path = source / sys_file
            sys_file_path.parent.mkdir(parents=True, exist_ok=True)
            sys_file_path.write_text(f"# {sys_file}\n\nSystem file content")

    return source


@pytest.fixture
def temp_target_dir(tmp_path) -> Path:
    """
    Create temporary target directory for installation.

    This directory starts empty and will be populated by tests.
    """
    target = tmp_path / "target"
    target.mkdir()
    return target


@pytest.fixture
def temp_source_with_invalid_catalog(tmp_path, invalid_catalog_json) -> Path:
    """Source directory with invalid catalog JSON."""
    source = tmp_path / "source_invalid"
    source.mkdir()

    catalog_file = source / "sap-catalog.json"
    catalog_file.write_text(invalid_catalog_json)

    return source


@pytest.fixture
def temp_source_without_catalog(tmp_path) -> Path:
    """Source directory missing catalog file."""
    source = tmp_path / "source_no_catalog"
    source.mkdir()
    return source


@pytest.fixture
def custom_chorabase_config() -> Dict[str, Any]:
    """
    Sample .chorabase configuration for testing custom sets.
    """
    return {
        "sap_sets": {
            "custom-test-set": {
                "name": "Custom Test Set",
                "description": "Custom set for testing",
                "saps": ["SAP-000", "SAP-004"],
                "estimated_tokens": 15000,
                "estimated_hours": "2-3",
                "tags": ["custom", "test"]
            },
            "custom-invalid": {
                "name": "Invalid Custom Set",
                "description": "References non-existent SAP",
                "saps": ["SAP-999"],
                "estimated_tokens": 5000,
                "estimated_hours": "1"
            }
        }
    }


@pytest.fixture
def temp_target_with_chorabase(tmp_path, custom_chorabase_config) -> Path:
    """Target directory with .chorabase file."""
    import yaml

    target = tmp_path / "target_with_chorabase"
    target.mkdir()

    chorabase_file = target / ".chorabase"
    chorabase_file.write_text(yaml.dump(custom_chorabase_config))

    return target


@pytest.fixture
def mock_shutil(monkeypatch):
    """
    Mock shutil operations to avoid actual file I/O in unit tests.

    Returns a Mock object with copytree and copy2 methods.
    Use this fixture for unit tests that should not touch the filesystem.
    """
    mock = Mock()
    mock.copytree = MagicMock(return_value=None)
    mock.copy2 = MagicMock(return_value=None)

    monkeypatch.setattr('shutil.copytree', mock.copytree)
    monkeypatch.setattr('shutil.copy2', mock.copy2)

    return mock


@pytest.fixture
def captured_output(monkeypatch):
    """
    Capture print() output for testing console messages.

    Returns a list that accumulates all print() calls.
    """
    output_lines = []

    def mock_print(*args, **kwargs):
        output_lines.append(' '.join(str(arg) for arg in args))

    monkeypatch.setattr('builtins.print', mock_print)

    return output_lines


@pytest.fixture
def installed_sap_structure(temp_target_dir, mock_catalog) -> Path:
    """
    Create a target directory with SAP-000 already installed.

    Useful for testing idempotency and dependency checking.
    """
    # Install SAP-000 structure
    sap = mock_catalog["saps"][0]  # SAP-000
    sap_dir = temp_target_dir / sap["location"]
    sap_dir.mkdir(parents=True, exist_ok=True)

    # Create 5 required artifacts
    artifacts = [
        "capability-charter.md",
        "protocol-spec.md",
        "awareness-guide.md",
        "adoption-blueprint.md",
        "ledger.md"
    ]
    for artifact in artifacts:
        (sap_dir / artifact).write_text(f"# {artifact}\n\nAlready installed")

    return temp_target_dir


@pytest.fixture
def incomplete_sap_installation(temp_target_dir, mock_catalog) -> Path:
    """
    Create a target directory with incomplete SAP installation (missing artifacts).

    Useful for testing validation failure cases.
    """
    sap = mock_catalog["saps"][0]  # SAP-000
    sap_dir = temp_target_dir / sap["location"]
    sap_dir.mkdir(parents=True, exist_ok=True)

    # Create only 3 of 5 required artifacts (missing 2)
    (sap_dir / "capability-charter.md").write_text("# Charter")
    (sap_dir / "protocol-spec.md").write_text("# Protocol")
    (sap_dir / "awareness-guide.md").write_text("# Guide")
    # Missing: adoption-blueprint.md, ledger.md

    return temp_target_dir


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual functions"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests with real file operations"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take longer to run"
    )
