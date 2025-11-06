"""
Tests for scripts/sap-evaluator.py - SAP Self-Evaluation CLI Tool

This test suite covers:
- Terminal output formatters
- File output savers (markdown, JSON, YAML)
- CLI main() function and argument parsing
- Different evaluation modes (quick, deep, strategic)
"""

import json
import pytest
import sys
from pathlib import Path
from datetime import datetime, date, timezone
from unittest.mock import Mock, patch, MagicMock, call
from io import StringIO

# Import the CLI script (has dash in filename, so use importlib)
import importlib.util

repo_root = Path(__file__).parent.parent
sap_evaluator_path = repo_root / "scripts" / "sap-evaluator.py"

# Load module using importlib
spec = importlib.util.spec_from_file_location("sap_evaluator", sap_evaluator_path)
sap_evaluator = importlib.util.module_from_spec(spec)
sys.modules['sap_evaluator'] = sap_evaluator
spec.loader.exec_module(sap_evaluator)

# Import functions
print_quick_results_terminal = sap_evaluator.print_quick_results_terminal
print_deep_results_terminal = sap_evaluator.print_deep_results_terminal
print_strategic_results_terminal = sap_evaluator.print_strategic_results_terminal
save_markdown_report = sap_evaluator.save_markdown_report
save_json_output = sap_evaluator.save_json_output
save_yaml_roadmap = sap_evaluator.save_yaml_roadmap
main = sap_evaluator.main

from utils.sap_evaluation import (
    EvaluationResult,
    Gap,
    AdoptionRoadmap,
    PrioritizedGap
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_quick_result():
    """Create a mock quick check result."""
    return EvaluationResult(
        sap_id="SAP-004",
        sap_name="testing-framework",
        evaluation_type="quick",
        timestamp=datetime(2025, 11, 5, 12, 0, 0, tzinfo=timezone.utc),
        is_installed=True,
        current_level=1,
        completion_percent=33.3,
        next_milestone="Level 2",
        blockers=[]
    )


@pytest.fixture
def mock_deep_result():
    """Create a mock deep dive result."""
    gap1 = Gap(
        gap_id="GAP-001",
        gap_type="quality",
        title="Low test coverage",
        description="Coverage is below 85%",
        impact="high",
        effort="medium",
        priority="P0",
        urgency="blocks_sprint",
        current_state="50% coverage",
        desired_state="85% coverage",
        estimated_hours=8.0
    )

    gap2 = Gap(
        gap_id="GAP-002",
        gap_type="integration",
        title="Missing integration",
        description="Not integrated with CI/CD",
        impact="medium",
        effort="low",
        priority="P1",
        urgency="next_sprint",
        estimated_hours=2.0
    )

    return EvaluationResult(
        sap_id="SAP-004",
        sap_name="testing-framework",
        evaluation_type="deep",
        timestamp=datetime(2025, 11, 5, 12, 0, 0, tzinfo=timezone.utc),
        is_installed=True,
        current_level=1,
        completion_percent=50.0,
        next_milestone="Level 2",
        validation_results={"coverage": False, "ci_integration": True},
        gaps=[gap1, gap2],
        blockers=["Low test coverage"],
        warnings=["Coverage below threshold"],
        duration_seconds=5.2
    )


@pytest.fixture
def mock_roadmap():
    """Create a mock strategic roadmap."""
    gap = Gap(
        gap_id="GAP-001",
        gap_type="quality",
        title="Test gap",
        description="Test description",
        impact="high",
        effort="low",
        priority="P0",
        urgency="blocks_sprint"
    )

    prioritized_gap = PrioritizedGap(
        rank=1,
        sap_id="SAP-004",
        gap=gap,
        priority_score=0.9,
        sprint="current"
    )

    return AdoptionRoadmap(
        generated_at=datetime(2025, 11, 5, 12, 0, 0, tzinfo=timezone.utc),
        target_quarter="Q1-2026",
        total_saps_installed=5,
        average_adoption_level=1.5,
        adoption_distribution={"level_0": 2, "level_1": 3, "level_2": 0, "level_3": 0},
        priority_gaps=[prioritized_gap]
    )


# ============================================================================
# Terminal Output Formatter Tests
# ============================================================================

class TestTerminalFormatters:
    """Test terminal output formatting functions."""

    def test_print_quick_results_single(self, capsys, mock_quick_result):
        """Test printing single quick result to terminal."""
        print_quick_results_terminal(mock_quick_result)

        captured = capsys.readouterr()
        output = captured.out

        assert "SAP-004" in output
        assert "testing-framework" in output
        assert "Level: 1" in output
        assert "Next: Level 2" in output

    def test_print_quick_results_list(self, capsys, mock_quick_result):
        """Test printing list of quick results to terminal."""
        results = [mock_quick_result, mock_quick_result]
        print_quick_results_terminal(results)

        captured = capsys.readouterr()
        output = captured.out

        assert "Installed: 2/2 SAPs" in output

    def test_print_deep_results(self, capsys, mock_deep_result):
        """Test printing deep dive results to terminal."""
        print_deep_results_terminal(mock_deep_result)

        captured = capsys.readouterr()
        output = captured.out

        assert "SAP-004" in output
        assert "Deep Dive Assessment" in output
        assert "Adoption Level: 1" in output
        assert "Completion: 50% toward next level" in output
        assert "Gaps Identified (2)" in output
        assert "Gap 1: Low test coverage" in output
        assert "P0" in output
        assert "Blockers" in output
        assert "Low test coverage" in output
        assert "Warnings" in output
        assert "Coverage below threshold" in output

    def test_print_deep_results_validation(self, capsys, mock_deep_result):
        """Test printing deep dive validation results."""
        print_deep_results_terminal(mock_deep_result)

        captured = capsys.readouterr()
        output = captured.out

        assert "Validation Results" in output
        assert "coverage" in output
        assert "ci_integration" in output

    def test_print_strategic_results(self, capsys, mock_roadmap):
        """Test printing strategic analysis results to terminal."""
        print_strategic_results_terminal(mock_roadmap)

        captured = capsys.readouterr()
        output = captured.out

        assert "SAP Adoption Roadmap" in output
        assert "Target Quarter: Q1-2026" in output
        assert "Total SAPs Installed: 5" in output
        assert "Average Level: 1.50" in output
        assert "Distribution by Level" in output
        assert "level_0: 2" in output
        assert "Priority Gaps (1)" in output


# ============================================================================
# File Saver Tests
# ============================================================================

class TestFileSavers:
    """Test file output saving functions."""

    def test_save_markdown_report(self, temp_workspace, mock_deep_result):
        """Test saving deep dive result as markdown."""
        output_path = temp_workspace / "reports" / "sap-004-report.md"

        with patch('builtins.print') as mock_print:
            save_markdown_report(mock_deep_result, output_path)

        # Check file was created
        assert output_path.exists()

        # Check content
        content = output_path.read_text()
        assert "# SAP-004 (testing-framework) - Deep Dive Assessment" in content
        assert "## Current State" in content
        assert "Adoption Level**: 1" in content
        assert "## Gap Analysis (2 gaps identified)" in content
        assert "### Gap 1: Low test coverage (P0)" in content
        assert "## Blockers" in content
        assert "## Warnings" in content
        assert "Generated by SAP-019 Self-Evaluation" in content

        # Check print was called with success message
        mock_print.assert_called_once()
        assert "Report saved to" in str(mock_print.call_args)

    def test_save_json_output(self, temp_workspace):
        """Test saving evaluation result as JSON."""
        output_path = temp_workspace / "output.json"
        data = {
            "sap_id": "SAP-004",
            "current_level": 1,
            "is_installed": True
        }

        with patch('builtins.print') as mock_print:
            save_json_output(data, output_path)

        # Check file was created
        assert output_path.exists()

        # Check content
        with open(output_path) as f:
            loaded = json.load(f)

        assert loaded["sap_id"] == "SAP-004"
        assert loaded["current_level"] == 1

        # Check print was called
        mock_print.assert_called_once()
        assert "JSON saved to" in str(mock_print.call_args)

    def test_save_json_creates_parent_dirs(self, temp_workspace):
        """Test that save_json_output creates parent directories."""
        output_path = temp_workspace / "deep" / "nested" / "path" / "output.json"
        data = {"test": "data"}

        save_json_output(data, output_path)

        assert output_path.exists()
        assert output_path.parent.exists()

    def test_save_yaml_roadmap(self, temp_workspace, mock_roadmap):
        """Test saving strategic roadmap as YAML."""
        output_path = temp_workspace / "roadmap.yaml"

        with patch('builtins.print') as mock_print:
            save_yaml_roadmap(mock_roadmap, output_path)

        # Check file was created
        assert output_path.exists()

        # Check content
        content = output_path.read_text()
        assert "# SAP Adoption Roadmap" in content
        assert "metadata:" in content
        assert "target_quarter: Q1-2026" in content
        assert "current_state:" in content
        assert "total_saps_installed: 5" in content
        assert "average_adoption_level: 1.50" in content
        assert "distribution:" in content
        assert "level_0: 2" in content
        assert "priority_gaps:" in content
        assert "rank: 1" in content
        assert "sap_id: SAP-004" in content

        # Check print was called
        mock_print.assert_called_once()
        assert "Roadmap saved to" in str(mock_print.call_args)


# ============================================================================
# CLI Main Function Tests
# ============================================================================

class TestMainCLI:
    """Test main() CLI function."""

    @patch('sap_evaluator.SAPEvaluator')
    def test_main_quick_check_single(self, mock_evaluator_class, mock_quick_result, capsys):
        """Test main with --quick for single SAP."""
        mock_evaluator = Mock()
        mock_evaluator.quick_check.return_value = mock_quick_result
        mock_evaluator_class.return_value = mock_evaluator

        with patch('sys.argv', ['sap-evaluator.py', '--quick', 'SAP-004']):
            exit_code = main()

        assert exit_code == 0
        mock_evaluator.quick_check.assert_called_once_with('SAP-004')

        # Check output
        captured = capsys.readouterr()
        assert "SAP-004" in captured.out

    @patch('sap_evaluator.SAPEvaluator')
    def test_main_quick_check_all(self, mock_evaluator_class, mock_quick_result, capsys):
        """Test main with --quick for all SAPs."""
        mock_evaluator = Mock()
        mock_evaluator.quick_check_all.return_value = [mock_quick_result, mock_quick_result]
        mock_evaluator_class.return_value = mock_evaluator

        with patch('sys.argv', ['sap-evaluator.py', '--quick']):
            exit_code = main()

        assert exit_code == 0
        mock_evaluator.quick_check_all.assert_called_once()

    @patch('sap_evaluator.SAPEvaluator')
    def test_main_deep_dive(self, mock_evaluator_class, mock_deep_result, capsys):
        """Test main with --deep."""
        mock_evaluator = Mock()
        mock_evaluator.deep_dive.return_value = mock_deep_result
        mock_evaluator_class.return_value = mock_evaluator

        with patch('sys.argv', ['sap-evaluator.py', '--deep', 'SAP-004']):
            exit_code = main()

        assert exit_code == 0
        mock_evaluator.deep_dive.assert_called_once_with('SAP-004')

        # Check output
        captured = capsys.readouterr()
        assert "Deep Dive Assessment" in captured.out

    @patch('sap_evaluator.SAPEvaluator')
    def test_main_strategic_analysis(self, mock_evaluator_class, mock_roadmap, capsys):
        """Test main with --strategic."""
        mock_evaluator = Mock()
        mock_evaluator.strategic_analysis.return_value = mock_roadmap
        mock_evaluator_class.return_value = mock_evaluator

        with patch('sys.argv', ['sap-evaluator.py', '--strategic']):
            exit_code = main()

        assert exit_code == 0
        mock_evaluator.strategic_analysis.assert_called_once()

        # Check output
        captured = capsys.readouterr()
        assert "SAP Adoption Roadmap" in captured.out

    @patch('sap_evaluator.SAPEvaluator')
    def test_main_quick_json_output(self, mock_evaluator_class, mock_quick_result, capsys):
        """Test main with --quick --format json."""
        mock_evaluator = Mock()
        mock_evaluator.quick_check.return_value = mock_quick_result
        mock_evaluator_class.return_value = mock_evaluator

        with patch('sys.argv', ['sap-evaluator.py', '--quick', 'SAP-004', '--format', 'json']):
            exit_code = main()

        assert exit_code == 0

        # Check JSON output
        captured = capsys.readouterr()
        output_data = json.loads(captured.out)
        assert output_data['sap_id'] == 'SAP-004'

    @patch('sap_evaluator.SAPEvaluator')
    def test_main_deep_with_output_file(self, mock_evaluator_class, mock_deep_result, temp_workspace):
        """Test main with --deep --output file.md."""
        mock_evaluator = Mock()
        mock_evaluator.deep_dive.return_value = mock_deep_result
        mock_evaluator_class.return_value = mock_evaluator

        output_file = temp_workspace / "report.md"

        with patch('sys.argv', ['sap-evaluator.py', '--deep', 'SAP-004', '--output', str(output_file)]):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

        content = output_file.read_text()
        assert "SAP-004" in content
        assert "Deep Dive Assessment" in content

    @patch('sap_evaluator.SAPEvaluator')
    def test_main_strategic_with_yaml_output(self, mock_evaluator_class, mock_roadmap, temp_workspace):
        """Test main with --strategic --output file.yaml."""
        mock_evaluator = Mock()
        mock_evaluator.strategic_analysis.return_value = mock_roadmap
        mock_evaluator_class.return_value = mock_evaluator

        output_file = temp_workspace / "roadmap.yaml"

        with patch('sys.argv', ['sap-evaluator.py', '--strategic', '--output', str(output_file)]):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

        content = output_file.read_text()
        assert "SAP Adoption Roadmap" in content
        assert "Q1-2026" in content

    @patch('sap_evaluator.SAPEvaluator')
    def test_main_deep_json_with_output(self, mock_evaluator_class, mock_deep_result, temp_workspace):
        """Test main with --deep --format json --output file.json."""
        mock_evaluator = Mock()
        mock_evaluator.deep_dive.return_value = mock_deep_result
        mock_evaluator_class.return_value = mock_evaluator

        output_file = temp_workspace / "result.json"

        with patch('sys.argv', ['sap-evaluator.py', '--deep', 'SAP-004', '--format', 'json', '--output', str(output_file)]):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()

        with open(output_file) as f:
            data = json.load(f)

        assert data['sap_id'] == 'SAP-004'
        assert data['evaluation_type'] == 'deep'

    @patch('sap_evaluator.SAPEvaluator')
    def test_main_keyboard_interrupt(self, mock_evaluator_class, capsys):
        """Test main handles KeyboardInterrupt."""
        mock_evaluator = Mock()
        mock_evaluator.quick_check_all.side_effect = KeyboardInterrupt()
        mock_evaluator_class.return_value = mock_evaluator

        with patch('sys.argv', ['sap-evaluator.py', '--quick']):
            exit_code = main()

        assert exit_code == 130

        # Check error message
        captured = capsys.readouterr()
        assert "cancelled by user" in captured.err

    @patch('sap_evaluator.SAPEvaluator')
    def test_main_exception(self, mock_evaluator_class, capsys):
        """Test main handles general exceptions."""
        mock_evaluator = Mock()
        mock_evaluator.quick_check_all.side_effect = Exception("Test error")
        mock_evaluator_class.return_value = mock_evaluator

        with patch('sys.argv', ['sap-evaluator.py', '--quick']):
            exit_code = main()

        assert exit_code == 1

        # Check error message
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "Test error" in captured.err


# ============================================================================
# Integration Tests
# ============================================================================

class TestCLIIntegration:
    """Integration tests with real evaluator (mocked filesystem)."""

    def test_quick_check_integration(self, temp_workspace, mock_sap_catalog):
        """Test --quick with real evaluator on temp workspace."""
        # Create minimal SAP structure
        sap_dir = temp_workspace / "saps" / "SAP-000-framework"
        sap_dir.mkdir(parents=True)

        artifacts = ["capability-charter.md", "protocol-spec.md",
                     "awareness-guide.md", "adoption-blueprint.md", "ledger.md"]
        for artifact in artifacts:
            (sap_dir / artifact).write_text(f"# {artifact}")

        # Update catalog to include location
        catalog_data = json.loads(mock_sap_catalog.read_text())
        catalog_data["saps"][0]["location"] = "saps/SAP-000-framework"
        mock_sap_catalog.write_text(json.dumps(catalog_data))

        with patch('sys.argv', ['sap-evaluator.py', '--quick', 'SAP-000']):
            with patch('sap_evaluator.repo_root', temp_workspace):
                exit_code = main()

        # Should succeed
        assert exit_code == 0

    def test_deep_dive_integration(self, temp_workspace, mock_sap_catalog):
        """Test --deep with real evaluator."""
        # Create SAP structure
        sap_dir = temp_workspace / "saps" / "SAP-001-inbox"
        sap_dir.mkdir(parents=True)

        artifacts = ["capability-charter.md", "protocol-spec.md",
                     "awareness-guide.md", "adoption-blueprint.md", "ledger.md"]
        for artifact in artifacts:
            (sap_dir / artifact).write_text(f"# {artifact}")

        # Update catalog
        catalog_data = json.loads(mock_sap_catalog.read_text())
        catalog_data["saps"][1]["location"] = "saps/SAP-001-inbox"
        mock_sap_catalog.write_text(json.dumps(catalog_data))

        output_file = temp_workspace / "deep-report.md"

        with patch('sys.argv', ['sap-evaluator.py', '--deep', 'SAP-001', '--output', str(output_file)]):
            with patch('sap_evaluator.repo_root', temp_workspace):
                exit_code = main()

        assert exit_code == 0
        assert output_file.exists()
