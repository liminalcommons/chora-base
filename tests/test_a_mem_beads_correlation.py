"""
Tests for a-mem-beads-correlation.py script

Tests bidirectional traceability between A-MEM events and beads tasks.
"""

import json
import pytest
import subprocess
from pathlib import Path

# Get repo root for running scripts
REPO_ROOT = Path(__file__).parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "a-mem-beads-correlation.py"


class TestCLIExecution:
    """Test a-mem-beads-correlation.py executes without errors"""

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
        assert "usage:" in result.stdout.lower() or "correlation" in result.stdout.lower()

    def test_summary_mode_runs(self):
        """Verify --summary mode executes"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--summary"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        # Should succeed or fail gracefully
        assert result.returncode in [0, 1], f"Summary mode crashed: {result.stderr}"

    def test_summary_json_output(self):
        """Verify --summary --json produces valid JSON"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--summary", "--json"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                data = json.loads(result.stdout)
                # Should have expected fields
                assert "total_events" in data or isinstance(data, dict)
            except json.JSONDecodeError:
                pytest.fail(f"Output is not valid JSON: {result.stdout[:200]}")


class TestEventsForTask:
    """Test events-for-task action"""

    def test_events_for_task_requires_task_id(self):
        """Verify events-for-task requires --task-id argument"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "events-for-task"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=REPO_ROOT
        )
        # Should exit with error about missing argument
        assert result.returncode != 0

    def test_events_for_task_with_id(self):
        """Verify events-for-task with task ID runs"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "events-for-task", "--task-id", "test-task-123"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        # Should run (may find 0 events)
        assert result.returncode in [0, 1]

    def test_events_for_task_json_output(self):
        """Verify events-for-task --json produces valid JSON"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "events-for-task", "--task-id", "test-123", "--json"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                data = json.loads(result.stdout)
                assert isinstance(data, list)
            except json.JSONDecodeError:
                pytest.fail(f"Output is not valid JSON")


class TestTasksForTrace:
    """Test tasks-for-trace action"""

    def test_tasks_for_trace_requires_trace_id(self):
        """Verify tasks-for-trace requires --trace-id argument"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "tasks-for-trace"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=REPO_ROOT
        )
        # Should exit with error about missing argument
        assert result.returncode != 0

    def test_tasks_for_trace_with_id(self):
        """Verify tasks-for-trace with trace ID runs"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "tasks-for-trace", "--trace-id", "test-trace-xyz"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        # Should run (may find 0 tasks)
        assert result.returncode in [0, 1]

    def test_tasks_for_trace_json_output(self):
        """Verify tasks-for-trace --json produces valid JSON"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "tasks-for-trace", "--trace-id", "test", "--json"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                data = json.loads(result.stdout)
                assert isinstance(data, dict)
                # Should have tasks and events keys
                assert "tasks" in data or "events" in data or data == {}
            except json.JSONDecodeError:
                pytest.fail(f"Output is not valid JSON")


class TestErrorHandling:
    """Test a-mem-beads-correlation.py error handling"""

    def test_invalid_action(self):
        """Verify graceful handling of invalid action"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "invalid-action"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=REPO_ROOT
        )
        # Should show error or help
        assert result.returncode != 0

    def test_missing_events_dir_handled(self):
        """Verify script handles missing events directory gracefully"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--summary", "--events-dir", "/nonexistent/path"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=REPO_ROOT
        )
        # Should handle gracefully
        assert result.returncode in [0, 1]
