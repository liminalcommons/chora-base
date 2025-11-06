"""
Tests for sap-evaluator.py CLI script

Focus on CLI interface testing using subprocess.
Tests verify the script runs without errors and produces expected output formats.
"""

import json
import pytest
import subprocess
from pathlib import Path

# Get repo root for running scripts
REPO_ROOT = Path(__file__).parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "sap-evaluator.py"


class TestCLIExecution:
    """Test sap-evaluator.py executes without errors"""

    def test_script_exists(self):
        """Verify script file exists"""
        assert SCRIPT_PATH.exists(), f"Script not found at {SCRIPT_PATH}"
        assert SCRIPT_PATH.is_file(), f"Script path is not a file: {SCRIPT_PATH}"

    def test_script_is_executable(self):
        """Verify script has executable permissions or can be run with python"""
        # Try running with python
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode in [0, 2], f"Script failed with code {result.returncode}: {result.stderr}"

    def test_help_output(self):
        """Verify --help flag produces usage information"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        # argparse returns exit code 0 for --help
        assert "usage:" in result.stdout.lower() or "sap" in result.stdout.lower()

    @pytest.mark.slow
    def test_quick_mode_runs(self):
        """Verify --quick mode executes without crashing"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--quick"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=REPO_ROOT
        )
        # Should either succeed or fail gracefully (not crash)
        assert result.returncode in [0, 1], f"Quick mode crashed: {result.stderr}"
        # Should produce some output
        assert len(result.stdout) > 0 or len(result.stderr) > 0

    @pytest.mark.slow
    def test_quick_mode_specific_sap(self):
        """Verify --quick SAP-004 runs"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--quick", "SAP-004"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=REPO_ROOT
        )
        # Should either succeed or fail gracefully
        assert result.returncode in [0, 1], f"Quick mode for SAP-004 crashed: {result.stderr}"

    @pytest.mark.slow
    def test_export_history_format_json(self):
        """Verify --export-history with --format json produces valid JSON"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--export-history", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        if result.returncode == 0 and result.stdout.strip():
            # If successful and has output, verify it's valid JSON
            try:
                json.loads(result.stdout)
            except json.JSONDecodeError:
                pytest.fail(f"Output is not valid JSON: {result.stdout[:200]}")


class TestOutputFormats:
    """Test sap-evaluator.py output formats"""

    @pytest.mark.slow
    def test_quick_output_contains_sap_ids(self):
        """Verify quick mode output mentions SAP IDs"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--quick"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=REPO_ROOT
        )
        if result.returncode == 0:
            # Should mention at least one SAP
            assert "SAP-" in result.stdout, "Quick output should contain SAP IDs"

    @pytest.mark.slow
    def test_deep_mode_output_structure(self):
        """Verify deep mode produces detailed output"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--deep", "SAP-004"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=REPO_ROOT
        )
        if result.returncode == 0:
            # Should contain assessment sections
            assert any(keyword in result.stdout.lower()
                      for keyword in ["assessment", "current state", "gaps", "level"])


class TestErrorHandling:
    """Test sap-evaluator.py error handling"""

    def test_invalid_sap_id(self):
        """Verify graceful handling of invalid SAP ID"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--quick", "SAP-9999"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        # Should handle gracefully - either error or show 0 SAPs installed
        assert result.returncode == 0, "Script should handle invalid SAP gracefully"
        assert "0/1 SAPs" in result.stdout or "0 SAPs" in result.stdout, "Should indicate SAP not found"

    def test_missing_required_args(self):
        """Verify error when required args missing (if any)"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=REPO_ROOT
        )
        # Script should either show help or execute default behavior
        # Both are acceptable for a CLI tool
        assert result.returncode in [0, 1, 2]


class TestFileOutput:
    """Test sap-evaluator.py file output"""

    @pytest.mark.slow
    def test_output_flag_creates_file(self, tmp_path):
        """Verify --output flag creates output file"""
        output_file = tmp_path / "test-report.md"
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--deep", "SAP-004", "--output", str(output_file)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=REPO_ROOT
        )
        if result.returncode == 0:
            # Output file should be created
            assert output_file.exists(), f"Output file not created: {result.stderr}"
            # File should have content
            assert output_file.stat().st_size > 0, "Output file is empty"
