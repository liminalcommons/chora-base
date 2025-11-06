"""
Tests for scripts/track-recipe-usage.py - Recipe usage tracking.

Test coverage for:
- RecipeUsageTracker initialization
- Logging recipe executions
- Reading logs with date filtering
- Calculating statistics
- Printing formatted output
- CLI argument parsing
"""

import json
import pytest
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO
import importlib.util

# Import the module under test (has dash in filename, so use importlib)
repo_root = Path(__file__).parent.parent
track_recipe_usage_path = repo_root / "scripts" / "track-recipe-usage.py"

# Load module using importlib
spec = importlib.util.spec_from_file_location("track_recipe_usage", track_recipe_usage_path)
track_recipe_usage = importlib.util.module_from_spec(spec)
sys.modules['track_recipe_usage'] = track_recipe_usage
spec.loader.exec_module(track_recipe_usage)

# Import symbols for convenience
RecipeUsageTracker = track_recipe_usage.RecipeUsageTracker
main = track_recipe_usage.main
VERSION = track_recipe_usage.VERSION


# Fixtures

@pytest.fixture
def temp_log_file(tmp_path):
    """Create a temporary log file path."""
    log_file = tmp_path / "recipe-usage.jsonl"
    return log_file


@pytest.fixture
def tracker(temp_log_file):
    """Create a tracker instance with temporary log file."""
    return RecipeUsageTracker(log_path=temp_log_file)


@pytest.fixture
def sample_log_entries():
    """Sample log entries for testing."""
    now = datetime.now(timezone.utc)
    entries = [
        {
            "timestamp": now.isoformat().replace('+00:00', 'Z'),
            "recipe": "test",
            "status": "success",
            "duration_ms": 1000
        },
        {
            "timestamp": (now - timedelta(days=1)).isoformat().replace('+00:00', 'Z'),
            "recipe": "build",
            "status": "success",
            "duration_ms": 2000
        },
        {
            "timestamp": (now - timedelta(days=8)).isoformat().replace('+00:00', 'Z'),
            "recipe": "test",
            "status": "failure"
        },
    ]
    return entries


@pytest.fixture
def tracker_with_logs(temp_log_file, sample_log_entries):
    """Create a tracker with pre-populated logs."""
    # Write sample entries to log file
    with temp_log_file.open('w', encoding='utf-8') as f:
        for entry in sample_log_entries:
            f.write(json.dumps(entry) + '\n')

    return RecipeUsageTracker(log_path=temp_log_file)


# Test RecipeUsageTracker Initialization

class TestRecipeUsageTrackerInit:
    """Test RecipeUsageTracker initialization."""

    def test_init_default_path(self):
        """Test initialization with default log path."""
        from track_recipe_usage import USAGE_LOG
        tracker = RecipeUsageTracker()
        assert tracker.log_path == USAGE_LOG

    def test_init_custom_path(self, temp_log_file):
        """Test initialization with custom log path."""
        tracker = RecipeUsageTracker(log_path=temp_log_file)
        assert tracker.log_path == temp_log_file

    def test_init_creates_parent_directory(self, tmp_path):
        """Test that initialization creates parent directories."""
        nested_path = tmp_path / "nested" / "dir" / "log.jsonl"
        tracker = RecipeUsageTracker(log_path=nested_path)
        assert nested_path.parent.exists()


# Test log_usage Method

class TestLogUsage:
    """Test log_usage functionality."""

    def test_log_usage_basic(self, tracker, temp_log_file, capsys):
        """Test logging a basic recipe execution."""
        tracker.log_usage("test-recipe")

        # Verify file was written
        assert temp_log_file.exists()

        # Verify content
        with temp_log_file.open('r') as f:
            entry = json.loads(f.read().strip())

        assert entry["recipe"] == "test-recipe"
        assert entry["status"] == "success"
        assert "timestamp" in entry
        assert "duration_ms" not in entry

        # Verify output
        captured = capsys.readouterr()
        assert "Logged: test-recipe (success)" in captured.out

    def test_log_usage_with_status(self, tracker, temp_log_file):
        """Test logging with custom status."""
        tracker.log_usage("build", status="failure")

        with temp_log_file.open('r') as f:
            entry = json.loads(f.read().strip())

        assert entry["recipe"] == "build"
        assert entry["status"] == "failure"

    def test_log_usage_with_duration(self, tracker, temp_log_file):
        """Test logging with duration."""
        tracker.log_usage("test", status="success", duration_ms=1500)

        with temp_log_file.open('r') as f:
            entry = json.loads(f.read().strip())

        assert entry["duration_ms"] == 1500

    def test_log_usage_multiple_entries(self, tracker, temp_log_file):
        """Test logging multiple entries."""
        tracker.log_usage("test")
        tracker.log_usage("build")
        tracker.log_usage("deploy")

        with temp_log_file.open('r') as f:
            lines = f.readlines()

        assert len(lines) == 3
        entries = [json.loads(line) for line in lines]
        assert entries[0]["recipe"] == "test"
        assert entries[1]["recipe"] == "build"
        assert entries[2]["recipe"] == "deploy"

    def test_log_usage_timestamp_format(self, tracker, temp_log_file):
        """Test that timestamp is in correct ISO format with Z suffix."""
        tracker.log_usage("test")

        with temp_log_file.open('r') as f:
            entry = json.loads(f.read().strip())

        timestamp = entry["timestamp"]
        assert timestamp.endswith('Z')

        # Verify it's parseable
        parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        assert parsed.tzinfo == timezone.utc

    def test_log_usage_write_error(self, tracker, capsys):
        """Test error handling when write fails."""
        # Make log path a directory to cause write error
        tracker.log_path.parent.mkdir(parents=True, exist_ok=True)
        tracker.log_path.mkdir()

        with pytest.raises(SystemExit) as exc_info:
            tracker.log_usage("test")

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error logging usage" in captured.err


# Test read_logs Method

class TestReadLogs:
    """Test read_logs functionality."""

    def test_read_logs_empty(self, tracker):
        """Test reading logs when file doesn't exist."""
        entries = tracker.read_logs()
        assert entries == []

    def test_read_logs_all(self, tracker_with_logs, sample_log_entries):
        """Test reading all logs."""
        entries = tracker_with_logs.read_logs()
        assert len(entries) == len(sample_log_entries)

    def test_read_logs_with_days_filter(self, tracker_with_logs):
        """Test reading logs with date filter."""
        # Only logs from last 7 days
        entries = tracker_with_logs.read_logs(days=7)

        # Should exclude the entry from 8 days ago
        assert len(entries) == 2
        assert all(e["recipe"] in ["test", "build"] for e in entries)

    def test_read_logs_with_days_filter_strict(self, temp_log_file):
        """Test reading logs with strict date filter."""
        # Create entries with specific old dates
        now = datetime.now(timezone.utc)
        old_entry = {
            "timestamp": (now - timedelta(days=100)).isoformat().replace('+00:00', 'Z'),
            "recipe": "old",
            "status": "success"
        }

        with temp_log_file.open('w') as f:
            f.write(json.dumps(old_entry) + '\n')

        tracker = RecipeUsageTracker(log_path=temp_log_file)

        # Request logs from last 7 days (should exclude 100-day-old entry)
        entries = tracker.read_logs(days=7)
        assert len(entries) == 0

    def test_read_logs_skip_empty_lines(self, temp_log_file):
        """Test that empty lines are skipped."""
        with temp_log_file.open('w') as f:
            f.write('{"recipe": "test", "status": "success", "timestamp": "2025-11-05T10:00:00Z"}\n')
            f.write('\n')  # Empty line
            f.write('{"recipe": "build", "status": "success", "timestamp": "2025-11-05T11:00:00Z"}\n')

        tracker = RecipeUsageTracker(log_path=temp_log_file)
        entries = tracker.read_logs()
        assert len(entries) == 2

    def test_read_logs_malformed_json(self, temp_log_file, capsys):
        """Test error handling for malformed JSON."""
        with temp_log_file.open('w') as f:
            f.write('{"recipe": "test", invalid json\n')

        tracker = RecipeUsageTracker(log_path=temp_log_file)
        entries = tracker.read_logs()

        assert entries == []
        captured = capsys.readouterr()
        assert "Error reading logs" in captured.err


# Test get_statistics Method

class TestGetStatistics:
    """Test get_statistics functionality."""

    def test_get_statistics_empty(self, tracker):
        """Test statistics with no logs."""
        stats = tracker.get_statistics()

        assert stats["total_executions"] == 0
        assert stats["unique_recipes"] == 0
        assert stats["success_rate"] == 0.0
        assert stats["recipes"] == {}

    def test_get_statistics_single_recipe(self, tracker, temp_log_file):
        """Test statistics with single recipe."""
        tracker.log_usage("test", status="success", duration_ms=1000)

        stats = tracker.get_statistics()

        assert stats["total_executions"] == 1
        assert stats["unique_recipes"] == 1
        assert stats["success_rate"] == 100.0
        assert "test" in stats["recipes"]
        assert stats["recipes"]["test"]["executions"] == 1
        assert stats["recipes"]["test"]["successes"] == 1
        assert stats["recipes"]["test"]["failures"] == 0
        assert stats["recipes"]["test"]["success_rate"] == 100.0
        assert stats["recipes"]["test"]["avg_duration_ms"] == 1000

    def test_get_statistics_multiple_recipes(self, tracker_with_logs):
        """Test statistics with multiple recipes."""
        stats = tracker_with_logs.get_statistics()

        assert stats["total_executions"] == 3
        assert stats["unique_recipes"] == 2
        assert "test" in stats["recipes"]
        assert "build" in stats["recipes"]

    def test_get_statistics_success_rate(self, tracker, temp_log_file):
        """Test success rate calculation."""
        tracker.log_usage("test", status="success")
        tracker.log_usage("test", status="success")
        tracker.log_usage("test", status="failure")
        tracker.log_usage("build", status="success")

        stats = tracker.get_statistics()

        # Overall: 3 successes out of 4 = 75%
        assert stats["success_rate"] == 75.0

        # Test recipe: 2 successes out of 3 = 66.67%
        assert abs(stats["recipes"]["test"]["success_rate"] - 66.67) < 0.1

        # Build recipe: 1 success out of 1 = 100%
        assert stats["recipes"]["build"]["success_rate"] == 100.0

    def test_get_statistics_status_breakdown(self, tracker, temp_log_file):
        """Test status breakdown."""
        tracker.log_usage("test", status="success")
        tracker.log_usage("test", status="failure")
        tracker.log_usage("test", status="skipped")

        stats = tracker.get_statistics()

        assert stats["status_breakdown"]["success"] == 1
        assert stats["status_breakdown"]["failure"] == 1
        assert stats["status_breakdown"]["skipped"] == 1

    def test_get_statistics_avg_duration(self, tracker, temp_log_file):
        """Test average duration calculation."""
        tracker.log_usage("test", duration_ms=1000)
        tracker.log_usage("test", duration_ms=2000)
        tracker.log_usage("test", duration_ms=3000)

        stats = tracker.get_statistics()

        assert stats["recipes"]["test"]["avg_duration_ms"] == 2000

    def test_get_statistics_no_duration(self, tracker, temp_log_file):
        """Test statistics when no duration is logged."""
        tracker.log_usage("test")  # No duration

        stats = tracker.get_statistics()

        assert stats["recipes"]["test"]["avg_duration_ms"] is None

    def test_get_statistics_mixed_duration(self, tracker, temp_log_file):
        """Test statistics with some entries having duration."""
        tracker.log_usage("test", duration_ms=1000)
        tracker.log_usage("test")  # No duration
        tracker.log_usage("test", duration_ms=3000)

        stats = tracker.get_statistics()

        # Average of 1000 and 3000 = 2000
        assert stats["recipes"]["test"]["avg_duration_ms"] == 2000

    def test_get_statistics_with_days_filter(self, tracker_with_logs):
        """Test statistics with date filter."""
        stats = tracker_with_logs.get_statistics(days=7)

        # Should only include recent entries (2 out of 3)
        assert stats["total_executions"] == 2
        assert stats["time_period_days"] == 7


# Test print_statistics Method

class TestPrintStatistics:
    """Test print_statistics functionality."""

    def test_print_statistics_empty(self, tracker, capsys):
        """Test printing statistics with no logs."""
        tracker.print_statistics()

        captured = capsys.readouterr()
        assert "No recipe usage recorded yet" in captured.out
        assert "track-recipe-usage.py log <recipe-name>" in captured.out

    def test_print_statistics_basic(self, tracker, temp_log_file, capsys):
        """Test printing basic statistics."""
        tracker.log_usage("test", status="success", duration_ms=1500)
        tracker.log_usage("build", status="success")

        tracker.print_statistics()

        captured = capsys.readouterr()
        assert "Recipe Usage Statistics (all time)" in captured.out
        assert "Total executions: 2" in captured.out
        assert "Unique recipes: 2" in captured.out
        assert "Overall success rate: 100.0%" in captured.out
        assert "test:" in captured.out
        assert "build:" in captured.out
        assert "1.50s" in captured.out  # Duration for test

    def test_print_statistics_with_days(self, tracker_with_logs, capsys):
        """Test printing statistics with date filter."""
        tracker_with_logs.print_statistics(days=7)

        captured = capsys.readouterr()
        assert "Recipe Usage Statistics (last 7 days)" in captured.out

    def test_print_statistics_sorted_by_executions(self, tracker, temp_log_file, capsys):
        """Test that recipes are sorted by execution count."""
        tracker.log_usage("test")
        tracker.log_usage("test")
        tracker.log_usage("test")
        tracker.log_usage("build")

        tracker.print_statistics()

        captured = capsys.readouterr()
        # Test should appear before build (3 vs 1 execution)
        test_pos = captured.out.find("test:")
        build_pos = captured.out.find("build:")
        assert test_pos < build_pos


# Test print_top_recipes Method

class TestPrintTopRecipes:
    """Test print_top_recipes functionality."""

    def test_print_top_recipes_empty(self, tracker, capsys):
        """Test printing top recipes with no logs."""
        tracker.print_top_recipes()

        captured = capsys.readouterr()
        assert "No recipe usage recorded yet" in captured.out

    def test_print_top_recipes_basic(self, tracker, temp_log_file, capsys):
        """Test printing top recipes."""
        tracker.log_usage("test")
        tracker.log_usage("test")
        tracker.log_usage("build")

        tracker.print_top_recipes(limit=2)

        captured = capsys.readouterr()
        assert "Top 2 Recipes (all time)" in captured.out
        assert "1. test" in captured.out
        assert "2 executions (66.7% of total)" in captured.out
        assert "2. build" in captured.out
        assert "1 executions (33.3% of total)" in captured.out

    def test_print_top_recipes_with_days(self, tracker_with_logs, capsys):
        """Test printing top recipes with date filter."""
        tracker_with_logs.print_top_recipes(days=7)

        captured = capsys.readouterr()
        assert "Top 10 Recipes (last 7 days)" in captured.out

    def test_print_top_recipes_respects_limit(self, tracker, temp_log_file, capsys):
        """Test that limit is respected."""
        for i in range(5):
            tracker.log_usage(f"recipe-{i}")

        tracker.print_top_recipes(limit=3)

        captured = capsys.readouterr()
        assert "Top 3 Recipes" in captured.out
        # Should only show 3 recipes
        assert captured.out.count("executions") == 3


# Test main CLI Function

class TestMainCLI:
    """Test main CLI function."""

    def test_main_no_command(self, capsys):
        """Test main with no command shows help."""
        with patch('sys.argv', ['track-recipe-usage.py']):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1

    def test_main_version(self, capsys):
        """Test --version flag."""
        with patch('sys.argv', ['track-recipe-usage.py', '--version']):
            with pytest.raises(SystemExit) as exc_info:
                main()

            captured = capsys.readouterr()
            assert VERSION in captured.out

    def test_main_log_command(self, capsys):
        """Test log command."""
        # Mock the log_usage method to avoid file I/O
        with patch('sys.argv', ['track-recipe-usage.py', 'log', 'test-recipe']):
            with patch.object(RecipeUsageTracker, 'log_usage') as mock_log:
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 0
                # Verify log_usage was called with correct arguments
                mock_log.assert_called_once_with('test-recipe', 'success', None)

    def test_main_log_command_with_status(self):
        """Test log command with status."""
        with patch('sys.argv', ['track-recipe-usage.py', 'log', 'test', '--status', 'failure']):
            with patch.object(RecipeUsageTracker, 'log_usage') as mock_log:
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 0
                # Verify log_usage was called with correct status
                mock_log.assert_called_once_with('test', 'failure', None)

    def test_main_log_command_with_duration(self):
        """Test log command with duration."""
        with patch('sys.argv', ['track-recipe-usage.py', 'log', 'test', '--duration', '1500']):
            with patch.object(RecipeUsageTracker, 'log_usage') as mock_log:
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 0
                # Verify log_usage was called with correct duration
                mock_log.assert_called_once_with('test', 'success', 1500)

    def test_main_stats_command(self, tmp_path, capsys):
        """Test stats command."""
        log_file = tmp_path / "test-log.jsonl"

        # Create some log entries
        tracker = RecipeUsageTracker(log_path=log_file)
        tracker.log_usage("test")

        with patch('sys.argv', ['track-recipe-usage.py', 'stats']):
            with patch('track_recipe_usage.USAGE_LOG', log_file):
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "Recipe Usage Statistics" in captured.out

    def test_main_stats_command_with_days(self, tmp_path, capsys):
        """Test stats command with days filter."""
        log_file = tmp_path / "test-log.jsonl"

        tracker = RecipeUsageTracker(log_path=log_file)
        tracker.log_usage("test")

        with patch('sys.argv', ['track-recipe-usage.py', 'stats', '--days', '7']):
            with patch('track_recipe_usage.USAGE_LOG', log_file):
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "last 7 days" in captured.out

    def test_main_top_command(self, tmp_path, capsys):
        """Test top command."""
        log_file = tmp_path / "test-log.jsonl"

        tracker = RecipeUsageTracker(log_path=log_file)
        tracker.log_usage("test")

        with patch('sys.argv', ['track-recipe-usage.py', 'top']):
            with patch('track_recipe_usage.USAGE_LOG', log_file):
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "Top 10 Recipes" in captured.out

    def test_main_top_command_with_limit(self, tmp_path, capsys):
        """Test top command with limit."""
        log_file = tmp_path / "test-log.jsonl"

        tracker = RecipeUsageTracker(log_path=log_file)
        tracker.log_usage("test")

        with patch('sys.argv', ['track-recipe-usage.py', 'top', '--limit', '5']):
            with patch('track_recipe_usage.USAGE_LOG', log_file):
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "Top 5 Recipes" in captured.out

    def test_main_top_command_with_days(self, tmp_path, capsys):
        """Test top command with days filter."""
        log_file = tmp_path / "test-log.jsonl"

        tracker = RecipeUsageTracker(log_path=log_file)
        tracker.log_usage("test")

        with patch('sys.argv', ['track-recipe-usage.py', 'top', '--days', '30']):
            with patch('track_recipe_usage.USAGE_LOG', log_file):
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "last 30 days" in captured.out


# Integration Tests

class TestIntegration:
    """Integration tests for complete workflows."""

    def test_log_and_retrieve_workflow(self, tracker, temp_log_file):
        """Test complete workflow: log entries and retrieve statistics."""
        # Log several entries
        tracker.log_usage("test", status="success", duration_ms=1000)
        tracker.log_usage("test", status="success", duration_ms=1500)
        tracker.log_usage("build", status="success", duration_ms=2000)
        tracker.log_usage("deploy", status="failure")

        # Get statistics
        stats = tracker.get_statistics()

        assert stats["total_executions"] == 4
        assert stats["unique_recipes"] == 3
        assert stats["success_rate"] == 75.0
        assert stats["recipes"]["test"]["executions"] == 2
        assert stats["recipes"]["test"]["avg_duration_ms"] == 1250
        assert stats["recipes"]["deploy"]["success_rate"] == 0.0

    def test_date_filtering_workflow(self, tracker, temp_log_file):
        """Test workflow with date filtering."""
        # Log entries at different times
        now = datetime.now(timezone.utc)

        # Recent entry
        entry1 = {
            "timestamp": now.isoformat().replace('+00:00', 'Z'),
            "recipe": "recent",
            "status": "success"
        }

        # Old entry (10 days ago)
        entry2 = {
            "timestamp": (now - timedelta(days=10)).isoformat().replace('+00:00', 'Z'),
            "recipe": "old",
            "status": "success"
        }

        with temp_log_file.open('w') as f:
            f.write(json.dumps(entry1) + '\n')
            f.write(json.dumps(entry2) + '\n')

        # Get all statistics
        all_stats = tracker.get_statistics()
        assert all_stats["total_executions"] == 2

        # Get last 7 days statistics
        recent_stats = tracker.get_statistics(days=7)
        assert recent_stats["total_executions"] == 1
        assert "recent" in recent_stats["recipes"]
        assert "old" not in recent_stats["recipes"]
