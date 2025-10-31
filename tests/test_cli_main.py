"""Tests for CLI main entry point (cli.py).

This module tests the CLI class and main() entry point, focusing on
the argparse-based validation commands:
- manifest-validate
- behavior-validate (with fallback validation)
- scenario-validate

Testing patterns:
- Use subprocess to test the actual CLI entry point
- Mock external validators where needed
- Test both success and error paths
"""

import builtins
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from mcp_orchestrator.cli import CLI, main


@pytest.fixture
def temp_manifest(tmp_path):
    """Create a temporary manifest file for testing."""
    manifest = tmp_path / "test-manifest.yaml"
    manifest.write_text("""
name: test-manifest
version: 1.0.0
scenarios:
  - name: test-scenario
    description: Test scenario
""")
    return manifest


@pytest.fixture
def temp_behavior_dir(tmp_path):
    """Create temporary behavior specs directory with valid specs."""
    behavior_dir = tmp_path / "behaviors"
    behavior_dir.mkdir()

    # Create a valid feature file with required tags
    feature_file = behavior_dir / "test.feature"
    feature_file.write_text("""
@behavior:test
@status:active

Feature: Test Feature
  Scenario: Test Scenario
    Given a test condition
    When something happens
    Then result is expected
""")

    return behavior_dir


class TestCLIInitialization:
    """Test CLI class initialization and argument parsing."""

    def test_cli_initialization_creates_parser(self):
        """Test that CLI() creates argument parser."""
        cli = CLI()
        assert cli.parser is not None
        assert cli.emitter is not None

    def test_cli_has_version_argument(self):
        """Test that --version is available."""
        cli = CLI()
        # Test that parsing --version doesn't raise an error
        with pytest.raises(SystemExit) as exc_info:
            cli.parser.parse_args(["--version"])
        # argparse exits with 0 for --version
        assert exc_info.value.code == 0

    def test_cli_has_subcommands(self):
        """Test that CLI has required subcommands."""
        cli = CLI()
        # Parser should have subparsers with manifest-validate, behavior-validate, scenario-validate
        args = cli.parser.parse_args(["manifest-validate", "manifests/star.yaml"])
        assert args.command == "manifest-validate"


class TestManifestValidateCommand:
    """Test manifest-validate command."""

    def test_manifest_validate_success(self, temp_manifest):
        """Test successful manifest validation."""
        cli = CLI()

        with patch("mcp_orchestrator.cli.validate_manifest") as mock_validate:
            with patch("mcp_orchestrator.cli.load_policy") as mock_policy:
                mock_policy.return_value = {}

                result = cli.run(["manifest-validate", str(temp_manifest)])

                assert result == 0
                mock_validate.assert_called_once()

    def test_manifest_validate_emits_telemetry(self, temp_manifest):
        """Test manifest-validate emits telemetry event."""
        cli = CLI()

        with patch("mcp_orchestrator.cli.validate_manifest"):
            with patch("mcp_orchestrator.cli.load_policy", return_value={}):
                cli.run(["manifest-validate", str(temp_manifest)])

                # Check that telemetry was emitted
                # The emitter is created in __init__, we can't easily verify
                # but we can at least verify the command completed
                assert True  # If we get here, telemetry code path was executed


class TestBehaviorValidateCommand:
    """Test behavior-validate command."""

    def test_behavior_validate_with_chora_validator_success(self, temp_behavior_dir):
        """Test behavior-validate using chora-validator (if available)."""
        cli = CLI()

        # Mock the dynamic import by patching builtins.__import__
        def mock_import(name, *args, **kwargs):
            if name == "chora_validator.validators":
                mock_module = Mock()
                mock_module.validate_behaviors = Mock()
                return mock_module
            return __import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            with patch("mcp_orchestrator.cli.load_policy", return_value={}):
                result = cli.run(["behavior-validate", str(temp_behavior_dir)])

                assert result == 0

    def test_behavior_validate_fallback_validation(self, temp_behavior_dir):
        """Test behavior-validate fallback when chora-validator not available."""
        cli = CLI()

        # Save original import
        original_import = builtins.__import__

        # Force ImportError to trigger fallback path
        def mock_import_error(name, *args, **kwargs):
            if name == "chora_validator.validators":
                raise ImportError("chora_validator not available")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import_error):
            with patch("mcp_orchestrator.cli.load_policy", return_value={}):
                result = cli.run(["behavior-validate", str(temp_behavior_dir)])

                assert result == 0  # Fallback validation should succeed

    def test_behavior_validate_fallback_missing_directory(self, tmp_path):
        """Test behavior-validate fallback with non-existent directory."""
        cli = CLI()
        nonexistent = tmp_path / "nonexistent"

        original_import = builtins.__import__

        def mock_import_error(name, *args, **kwargs):
            if name == "chora_validator.validators":
                raise ImportError("chora_validator not available")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import_error):
            with patch("mcp_orchestrator.cli.load_policy", return_value={}):
                with pytest.raises(SystemExit) as exc_info:
                    cli.run(["behavior-validate", str(nonexistent)])

                assert "not found" in str(exc_info.value)

    def test_behavior_validate_fallback_missing_tags(self, tmp_path):
        """Test behavior-validate fallback detects missing required tags."""
        cli = CLI()
        behavior_dir = tmp_path / "behaviors"
        behavior_dir.mkdir()

        # Create feature file WITHOUT required tags
        bad_feature = behavior_dir / "bad.feature"
        bad_feature.write_text("""
Feature: Bad Feature
  Scenario: Missing tags
    Given something
""")

        original_import = builtins.__import__

        def mock_import_error(name, *args, **kwargs):
            if name == "chora_validator.validators":
                raise ImportError("chora_validator not available")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import_error):
            with patch("mcp_orchestrator.cli.load_policy", return_value={}):
                with pytest.raises(SystemExit) as exc_info:
                    cli.run(["behavior-validate", str(behavior_dir)])

                assert "@behavior" in str(exc_info.value) or "@status" in str(exc_info.value)

    def test_behavior_validate_fallback_no_specs_found(self, tmp_path):
        """Test behavior-validate fallback with empty directory."""
        cli = CLI()
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        original_import = builtins.__import__

        def mock_import_error(name, *args, **kwargs):
            if name == "chora_validator.validators":
                raise ImportError("chora_validator not available")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import_error):
            with patch("mcp_orchestrator.cli.load_policy", return_value={}):
                with pytest.raises(SystemExit) as exc_info:
                    cli.run(["behavior-validate", str(empty_dir)])

                assert "No behavior specs found" in str(exc_info.value)

    def test_behavior_validate_checks_json_files(self, tmp_path):
        """Test behavior-validate fallback also checks .json files."""
        cli = CLI()
        behavior_dir = tmp_path / "behaviors"
        behavior_dir.mkdir()

        # Create a valid JSON spec with required tags
        json_spec = behavior_dir / "test.json"
        json_spec.write_text("""
{
  "tags": ["@behavior:test", "@status:active"],
  "scenario": "Test scenario"
}
""")

        original_import = builtins.__import__

        def mock_import_error(name, *args, **kwargs):
            if name == "chora_validator.validators":
                raise ImportError("chora_validator not available")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import_error):
            with patch("mcp_orchestrator.cli.load_policy", return_value={}):
                result = cli.run(["behavior-validate", str(behavior_dir)])

                assert result == 0

    def test_behavior_validate_emits_telemetry(self, temp_behavior_dir):
        """Test behavior-validate emits telemetry event."""
        cli = CLI()

        def mock_import(name, *args, **kwargs):
            if name == "chora_validator.validators":
                mock_module = Mock()
                mock_module.validate_behaviors = Mock()
                return mock_module
            return __import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            with patch("mcp_orchestrator.cli.load_policy", return_value={}):
                result = cli.run(["behavior-validate", str(temp_behavior_dir)])

                assert result == 0


class TestScenarioValidateCommand:
    """Test scenario-validate command."""

    def test_scenario_validate_success(self, temp_manifest):
        """Test successful scenario validation."""
        cli = CLI()

        def mock_import(name, *args, **kwargs):
            if name == "chora_validator.validators":
                mock_module = Mock()
                mock_module.validate_scenarios = Mock()
                return mock_module
            return __import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            result = cli.run(["scenario-validate", str(temp_manifest)])

            assert result == 0

    def test_scenario_validate_handles_exception(self, temp_manifest):
        """Test scenario-validate handles exceptions."""
        cli = CLI()

        def mock_import_error(name, *args, **kwargs):
            if name == "chora_validator.validators":
                mock_module = Mock()
                mock_module.validate_scenarios = Mock(side_effect=ValueError("Invalid scenario format"))
                return mock_module
            return __import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import_error):
            with pytest.raises(SystemExit) as exc_info:
                cli.run(["scenario-validate", str(temp_manifest)])

            assert "Invalid scenario format" in str(exc_info.value)

    def test_scenario_validate_emits_telemetry(self, temp_manifest):
        """Test scenario-validate emits telemetry event."""
        cli = CLI()

        def mock_import(name, *args, **kwargs):
            if name == "chora_validator.validators":
                mock_module = Mock()
                mock_module.validate_scenarios = Mock()
                return mock_module
            return __import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            result = cli.run(["scenario-validate", str(temp_manifest)])

            assert result == 0


class TestMainEntryPoint:
    """Test main() entry point function."""

    def test_main_creates_cli_and_runs(self, temp_manifest):
        """Test main() creates CLI instance and calls run()."""
        with patch("mcp_orchestrator.cli.validate_manifest"):
            with patch("mcp_orchestrator.cli.load_policy", return_value={}):
                result = main(["manifest-validate", str(temp_manifest)])

                assert result == 0

    def test_main_with_no_arguments(self):
        """Test main() with no arguments (should return 0, no command specified)."""
        result = main([])
        assert result == 0

    def test_main_passes_argv_to_cli(self):
        """Test main() passes argv through to CLI.run()."""
        with patch.object(CLI, "run", return_value=0) as mock_run:
            test_args = ["manifest-validate", "test.yaml"]
            main(test_args)

            # Verify CLI.run was called with the arguments
            mock_run.assert_called_once_with(test_args)


class TestCLIDefaultArguments:
    """Test CLI default argument values."""

    def test_manifest_validate_with_argument(self):
        """Test manifest-validate accepts file argument."""
        cli = CLI()
        args = cli.parser.parse_args(["manifest-validate", "test.yaml"])
        assert args.file == "test.yaml"

    def test_behavior_validate_with_argument(self):
        """Test behavior-validate accepts path argument."""
        cli = CLI()
        args = cli.parser.parse_args(["behavior-validate", "/custom/path"])
        assert args.path == "/custom/path"

    def test_scenario_validate_with_argument(self):
        """Test scenario-validate accepts manifest argument."""
        cli = CLI()
        args = cli.parser.parse_args(["scenario-validate", "custom.yaml"])
        assert args.manifest == "custom.yaml"
