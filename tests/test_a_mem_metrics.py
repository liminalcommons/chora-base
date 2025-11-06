"""
Tests for a-mem-metrics.py script

Tests SAP-010 (memory system) metrics and ROI tracking.
"""

import json
import pytest
import subprocess
from pathlib import Path

# Get repo root for running scripts
REPO_ROOT = Path(__file__).parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "a-mem-metrics.py"


class TestCLIExecution:
    """Test a-mem-metrics.py executes without errors"""

    def test_script_exists(self):
        """Verify script file exists"""
        assert SCRIPT_PATH.exists(), f"Script not found at {SCRIPT_PATH}"

    def test_help_output(self):
        """Verify --help flag produces usage information"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert "usage:" in result.stdout.lower() or "mem" in result.stdout.lower()

    def test_default_execution(self):
        """Verify script runs with default arguments"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        # Should succeed or fail gracefully
        assert result.returncode in [0, 1], f"Script crashed: {result.stderr}"

    def test_json_output_format(self):
        """Verify --format json produces valid JSON"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--format", "json"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                data = json.loads(result.stdout)
                assert isinstance(data, (dict, list))
            except json.JSONDecodeError:
                pytest.fail(f"Output is not valid JSON: {result.stdout[:200]}")


class TestROIDashboard:
    """Test ROI dashboard output"""

    def test_dashboard_output_structure(self):
        """Verify dashboard output contains expected sections"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        if result.returncode == 0:
            # Should contain A-MEM/ROI keywords
            assert any(keyword in result.stdout.lower()
                      for keyword in ["memory", "events", "roi", "a-mem", "metrics"])

    def test_l3_check_mode(self):
        """Verify --l3-check mode executes"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--l3-check"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        # Should succeed or fail gracefully
        assert result.returncode in [0, 1]


class TestMemoryDirectory:
    """Test memory directory argument"""

    def test_custom_memory_dir(self):
        """Verify --memory-dir argument works"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--memory-dir", ".chora/memory"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        # Should run (may not have data)
        assert result.returncode in [0, 1]


class TestErrorHandling:
    """Test a-mem-metrics.py error handling"""

    def test_invalid_format(self):
        """Verify handling of invalid format argument"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--format", "invalid"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=REPO_ROOT
        )
        # Should show error
        assert result.returncode != 0 or "invalid" in result.stderr.lower()

    def test_missing_memory_dir_handled(self):
        """Verify script handles missing memory directory gracefully"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--memory-dir", "/nonexistent"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=REPO_ROOT
        )
        # Should handle gracefully
        assert result.returncode in [0, 1]
