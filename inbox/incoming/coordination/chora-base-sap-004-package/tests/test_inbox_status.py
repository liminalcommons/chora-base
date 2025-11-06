"""
Tests for scripts/inbox-status.py

Tests the inbox status dashboard functions for displaying
current inbox protocol workflow status.
"""

import json
import pytest
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

# Import the module by reading and executing it
import importlib.util
spec = importlib.util.spec_from_file_location("inbox_status", scripts_dir / "inbox-status.py")
inbox_status = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inbox_status)


class TestFindRepoRoot:
    """Test find_repo_root function."""

    def test_find_repo_root_with_catalog(self, mock_sap_catalog, tmp_path, monkeypatch):
        """Test finding repo root with sap-catalog.json present."""
        # Change to the temp workspace directory
        monkeypatch.chdir(mock_sap_catalog.parent)

        # The function should find the root
        root = inbox_status.find_repo_root()
        # Resolve both paths to handle symlinks (e.g., /var -> /private/var on macOS)
        assert root.resolve() == mock_sap_catalog.parent.resolve()

    def test_find_repo_root_without_catalog(self, tmp_path, monkeypatch):
        """Test finding repo root without sap-catalog.json."""
        # Change to temp directory without catalog
        monkeypatch.chdir(tmp_path)

        # Should return current directory
        root = inbox_status.find_repo_root()
        assert root == tmp_path


class TestDataLoading:
    """Test data loading functions."""

    def test_load_json_file_success(self, tmp_path):
        """Test loading valid JSON file."""
        test_file = tmp_path / "test.json"
        test_data = {"key": "value"}
        with open(test_file, 'w') as f:
            json.dump(test_data, f)

        result = inbox_status.load_json_file(test_file)
        assert result == test_data

    def test_load_json_file_not_found(self, tmp_path):
        """Test loading non-existent file."""
        result = inbox_status.load_json_file(tmp_path / "nonexistent.json")
        assert result is None

    def test_load_json_file_invalid(self, tmp_path):
        """Test loading invalid JSON file."""
        test_file = tmp_path / "invalid.json"
        with open(test_file, 'w') as f:
            f.write("invalid json {")

        result = inbox_status.load_json_file(test_file)
        assert result is None

    def test_load_events_empty(self, mock_inbox):
        """Test loading events from non-existent file."""
        # Temporarily override INBOX_DIR
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        events = inbox_status.load_events()
        assert events == []

        # Restore
        inbox_status.INBOX_DIR = original_inbox

    def test_load_events_with_data(self, mock_inbox, mock_events_file):
        """Test loading events from file."""
        # Override INBOX_DIR
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        events = inbox_status.load_events()
        assert len(events) == 2
        assert events[0]['event_type'] == 'acknowledged'  # Newest first
        assert events[1]['event_type'] == 'coordination_request_created'

        # Restore
        inbox_status.INBOX_DIR = original_inbox

    def test_parse_timestamp(self):
        """Test timestamp parsing."""
        # Valid ISO timestamp
        ts = "2025-11-03T10:00:00Z"
        dt = inbox_status.parse_timestamp(ts)
        assert isinstance(dt, datetime)

        # Invalid timestamp
        dt = inbox_status.parse_timestamp("invalid")
        assert dt == datetime.min

    def test_scan_directory(self, tmp_path):
        """Test directory scanning."""
        # Create test files
        (tmp_path / "test1.json").touch()
        (tmp_path / "test2.json").touch()
        (tmp_path / "test.txt").touch()

        # Scan for JSON files
        files = inbox_status.scan_directory(tmp_path, "*.json")
        assert len(files) == 2

        # Scan non-existent directory
        files = inbox_status.scan_directory(tmp_path / "nonexistent")
        assert files == []


class TestStatusCalculation:
    """Test status calculation functions."""

    def test_count_incoming_empty(self, mock_inbox):
        """Test counting incoming items in empty inbox."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        counts = inbox_status.count_incoming()
        assert counts['coordination'] == 0
        assert counts['tasks'] == 0
        assert counts['context'] == 0

        inbox_status.INBOX_DIR = original_inbox

    def test_count_incoming_with_items(self, mock_inbox, sample_coordination_request):
        """Test counting incoming items."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Create coordination request
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        counts = inbox_status.count_incoming()
        assert counts['coordination'] == 1
        assert counts['tasks'] == 0

        inbox_status.INBOX_DIR = original_inbox

    def test_count_active_empty(self, mock_inbox):
        """Test counting active items when none exist."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        count, items = inbox_status.count_active()
        assert count == 0
        assert items == []

        inbox_status.INBOX_DIR = original_inbox

    def test_count_active_with_items(self, mock_inbox):
        """Test counting active items."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Create active directories (inbox status looks for directories, not files)
        (mock_inbox / "active" / "COORD-001").mkdir()
        (mock_inbox / "active" / "COORD-002").mkdir()

        count, items = inbox_status.count_active()
        assert count == 2
        assert "COORD-001" in items
        assert "COORD-002" in items

        inbox_status.INBOX_DIR = original_inbox

    def test_get_incoming_details(self, mock_inbox, sample_coordination_request):
        """Test getting detailed incoming item information."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Create coordination request
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        details = inbox_status.get_incoming_details()
        assert len(details) == 1
        assert details[0]['request_id'] == 'COORD-2025-001'
        assert details[0]['priority'] == 'P1'
        assert details[0]['deliverables_count'] == 1

        inbox_status.INBOX_DIR = original_inbox

    def test_get_incoming_details_priority_filter(self, mock_inbox, sample_coordination_request):
        """Test filtering incoming details by priority."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Create P1 request
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        # Create P2 request
        p2_request = sample_coordination_request.copy()
        p2_request['priority'] = 'P2'
        p2_request['request_id'] = 'COORD-002'
        coord_file2 = mock_inbox / "incoming" / "coordination" / "COORD-002.json"
        with open(coord_file2, 'w') as f:
            json.dump(p2_request, f)

        # Filter for P1 only
        details = inbox_status.get_incoming_details(priority_filter='P1')
        assert len(details) == 1
        assert details[0]['priority'] == 'P1'

        inbox_status.INBOX_DIR = original_inbox


class TestOutputFormatting:
    """Test output formatting functions."""

    def test_format_json(self):
        """Test JSON formatting."""
        data = {
            "incoming": {"summary": {"coordination": 1, "tasks": 0, "context": 0}, "details": []},
            "active": {"count": 0, "list": [], "details": []},
            "recent_events": [],
            "completed": {"count_30d": 0, "days": 30, "recent": []}
        }

        output = inbox_status.format_json(data)
        parsed = json.loads(output)
        assert parsed['incoming']['summary']['coordination'] == 1

    def test_format_markdown(self):
        """Test Markdown formatting."""
        data = {
            "incoming": {"summary": {"coordination": 1, "tasks": 0, "context": 0}, "details": []},
            "active": {"count": 0, "list": [], "details": []},
            "recent_events": [],
            "completed": {"count_30d": 0, "days": 30, "recent": []}
        }

        output = inbox_status.format_markdown(data)
        assert "# Inbox Status Report" in output
        assert "## Summary" in output
        assert "**Incoming**" in output  # Markdown bold format

    def test_format_terminal(self):
        """Test terminal formatting."""
        data = {
            "incoming": {"summary": {"coordination": 1, "tasks": 0, "context": 0}, "details": []},
            "active": {"count": 0, "list": [], "details": []},
            "recent_events": [],
            "completed": {"count_30d": 0, "days": 30, "recent": []}
        }

        output = inbox_status.format_terminal(data, detailed=False)
        assert "INBOX STATUS DASHBOARD" in output
        assert "INCOMING QUEUE" in output
        assert "Coordination Requests:" in output


class TestExtendedDataLoading:
    """Extended tests for data loading with filters."""

    def test_load_events_with_date_filter(self, mock_inbox):
        """Test loading events with date filtering."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Create events file with various dates
        events_file = mock_inbox / "coordination" / "events.jsonl"
        now = datetime.now()
        old_event = {
            "event_type": "old_event",
            "timestamp": (now - timedelta(days=10)).isoformat(),
            "request_id": "COORD-OLD"
        }
        recent_event = {
            "event_type": "recent_event",
            "timestamp": (now - timedelta(days=2)).isoformat(),
            "request_id": "COORD-RECENT"
        }

        with open(events_file, 'w') as f:
            f.write(json.dumps(old_event) + '\n')
            f.write(json.dumps(recent_event) + '\n')

        # Load events from last 7 days
        events = inbox_status.load_events(last_days=7)
        assert len(events) == 1
        assert events[0]['event_type'] == 'recent_event'

        inbox_status.INBOX_DIR = original_inbox

    def test_load_events_with_last_n_limit(self, mock_inbox):
        """Test loading events with limit."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Create events file with multiple events
        events_file = mock_inbox / "coordination" / "events.jsonl"
        events_data = []
        for i in range(10):
            events_data.append({
                "event_type": f"event_{i}",
                "timestamp": datetime.now().isoformat(),
                "request_id": f"COORD-{i}"
            })

        with open(events_file, 'w') as f:
            for event in events_data:
                f.write(json.dumps(event) + '\n')

        # Load only last 3
        events = inbox_status.load_events(last_n=3)
        assert len(events) == 3

        inbox_status.INBOX_DIR = original_inbox

    def test_load_events_with_malformed_lines(self, mock_inbox):
        """Test load_events skips malformed JSON lines."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Create events file with malformed JSON
        events_file = mock_inbox / "coordination" / "events.jsonl"
        good_event = {
            "event_type": "good",
            "timestamp": datetime.now().isoformat(),
            "request_id": "COORD-GOOD"
        }

        with open(events_file, 'w') as f:
            f.write("{ malformed json\n")
            f.write(json.dumps(good_event) + '\n')
            f.write("another bad line\n")

        events = inbox_status.load_events()
        assert len(events) == 1
        assert events[0]['event_type'] == 'good'

        inbox_status.INBOX_DIR = original_inbox


class TestCountCompleted:
    """Test count_completed function."""

    def test_count_completed_empty(self, mock_inbox):
        """Test count_completed with no completed items."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        count, recent = inbox_status.count_completed(days=30)
        assert count == 0
        assert recent == []

        inbox_status.INBOX_DIR = original_inbox

    def test_count_completed_no_directory(self, mock_inbox):
        """Test count_completed when directory doesn't exist."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Remove completed directory
        completed_dir = mock_inbox / "completed"
        if completed_dir.exists():
            import shutil
            shutil.rmtree(completed_dir)

        count, recent = inbox_status.count_completed(days=30)
        assert count == 0
        assert recent == []

        inbox_status.INBOX_DIR = original_inbox

    def test_count_completed_with_recent_items(self, mock_inbox):
        """Test count_completed with recent completions."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Create completed directories
        completed_dir = mock_inbox / "completed"
        item1 = completed_dir / "COORD-RECENT"
        item2 = completed_dir / "COORD-OLD"
        item1.mkdir()
        item2.mkdir()

        # Make item1 recent (within 30 days), item2 old
        import os
        now = datetime.now().timestamp()
        recent_time = (datetime.now() - timedelta(days=5)).timestamp()
        old_time = (datetime.now() - timedelta(days=60)).timestamp()

        os.utime(item1, (recent_time, recent_time))
        os.utime(item2, (old_time, old_time))

        count, recent = inbox_status.count_completed(days=30)
        assert count == 1
        assert len(recent) == 1
        assert recent[0]['id'] == 'COORD-RECENT'
        assert 'completed_date' in recent[0]

        inbox_status.INBOX_DIR = original_inbox


class TestGetActiveDetails:
    """Test get_active_details function."""

    def test_get_active_details_empty(self, mock_inbox):
        """Test get_active_details with no active items."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        details = inbox_status.get_active_details()
        assert details == []

        inbox_status.INBOX_DIR = original_inbox

    def test_get_active_details_no_directory(self, mock_inbox):
        """Test get_active_details when directory doesn't exist."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Remove active directory
        active_dir = mock_inbox / "active"
        if active_dir.exists():
            import shutil
            shutil.rmtree(active_dir)

        details = inbox_status.get_active_details()
        assert details == []

        inbox_status.INBOX_DIR = original_inbox

    def test_get_active_details_with_coordination_file(self, mock_inbox, sample_coordination_request):
        """Test get_active_details with coordination request file."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Create active item with coordination file
        active_dir = mock_inbox / "active" / "COORD-001"
        active_dir.mkdir()
        coord_file = active_dir / "coordination-request.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        details = inbox_status.get_active_details()
        assert len(details) == 1
        assert details[0]['id'] == 'COORD-001'
        assert details[0]['title'] == 'Test Coordination Request'
        assert details[0]['priority'] == 'P1'

        inbox_status.INBOX_DIR = original_inbox

    def test_get_active_details_with_request_file(self, mock_inbox, sample_coordination_request):
        """Test get_active_details with request file."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Create active item with 'request' in filename
        active_dir = mock_inbox / "active" / "COORD-002"
        active_dir.mkdir()
        request_file = active_dir / "request.json"
        with open(request_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        details = inbox_status.get_active_details()
        assert len(details) == 1
        assert details[0]['id'] == 'COORD-002'

        inbox_status.INBOX_DIR = original_inbox

    def test_get_active_details_with_malformed_json(self, mock_inbox):
        """Test get_active_details with malformed JSON file."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Create active item with malformed JSON
        active_dir = mock_inbox / "active" / "COORD-003"
        active_dir.mkdir()
        coord_file = active_dir / "coord.json"
        with open(coord_file, 'w') as f:
            f.write("{ malformed json")

        details = inbox_status.get_active_details()
        assert len(details) == 1
        assert details[0]['id'] == 'COORD-003'
        assert details[0]['title'] == 'Unknown'
        assert details[0]['type'] == 'unknown'

        inbox_status.INBOX_DIR = original_inbox

    def test_get_active_details_without_json_file(self, mock_inbox):
        """Test get_active_details with directory but no JSON files."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Create active item directory without JSON
        active_dir = mock_inbox / "active" / "COORD-004"
        active_dir.mkdir()

        details = inbox_status.get_active_details()
        assert len(details) == 1
        assert details[0]['id'] == 'COORD-004'
        assert details[0]['title'] == 'Unknown'

        inbox_status.INBOX_DIR = original_inbox


class TestGetIncomingDetailsExtended:
    """Extended tests for get_incoming_details."""

    def test_get_incoming_details_no_directory(self, mock_inbox):
        """Test get_incoming_details when directory doesn't exist."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Remove incoming coordination directory
        incoming_dir = mock_inbox / "incoming" / "coordination"
        if incoming_dir.exists():
            import shutil
            shutil.rmtree(incoming_dir)

        details = inbox_status.get_incoming_details()
        assert details == []

        inbox_status.INBOX_DIR = original_inbox


class TestFormatTerminalExtended:
    """Extended tests for format_terminal with detailed mode."""

    def test_format_terminal_detailed_with_incoming(self, sample_coordination_request):
        """Test format_terminal in detailed mode with incoming items."""
        data = {
            "incoming": {
                "summary": {"coordination": 1, "tasks": 0, "context": 0},
                "details": [{
                    "request_id": "COORD-001",
                    "title": "Test Request",
                    "priority": "P0",
                    "urgency": "immediate",
                    "from_repo": "test-repo",
                    "created": "2025-11-01"
                }]
            },
            "active": {"count": 0, "list": [], "details": []},
            "recent_events": [],
            "completed": {"count_30d": 0, "days": 30, "recent": []}
        }

        output = inbox_status.format_terminal(data, detailed=True)
        assert "COORD-001" in output
        assert "Test Request" in output

    def test_format_terminal_detailed_with_active(self):
        """Test format_terminal in detailed mode with active items."""
        data = {
            "incoming": {"summary": {"coordination": 0, "tasks": 0, "context": 0}, "details": []},
            "active": {
                "count": 2,
                "list": ["COORD-001", "COORD-002"],
                "details": [
                    {"id": "COORD-001", "type": "coordination", "priority": "P1"},
                    {"id": "COORD-002", "type": "task", "priority": "P2"}
                ]
            },
            "recent_events": [],
            "completed": {"count_30d": 0, "days": 30, "recent": []}
        }

        output = inbox_status.format_terminal(data, detailed=True)
        assert "COORD-001" in output
        assert "coordination" in output
        assert "P1" in output

    def test_format_terminal_with_recent_events(self):
        """Test format_terminal with recent events."""
        data = {
            "incoming": {"summary": {"coordination": 0, "tasks": 0, "context": 0}, "details": []},
            "active": {"count": 0, "list": [], "details": []},
            "recent_events": [
                {
                    "event_type": "coordination_request_created",
                    "request_id": "COORD-001",
                    "timestamp": "2025-11-03T10:00:00Z"
                }
            ],
            "completed": {"count_30d": 0, "days": 30, "recent": []}
        }

        output = inbox_status.format_terminal(data, detailed=False)
        assert "RECENT ACTIVITY" in output
        assert "coordination_request_created" in output
        assert "COORD-001" in output

    def test_format_terminal_with_completions(self):
        """Test format_terminal with recent completions."""
        data = {
            "incoming": {"summary": {"coordination": 0, "tasks": 0, "context": 0}, "details": []},
            "active": {"count": 0, "list": [], "details": []},
            "recent_events": [],
            "completed": {
                "count_30d": 2,
                "days": 30,
                "recent": [
                    {"id": "COORD-001", "completed_date": "2025-11-01"},
                    {"id": "COORD-002", "completed_date": "2025-11-02"}
                ]
            }
        }

        output = inbox_status.format_terminal(data, detailed=False)
        assert "RECENT COMPLETIONS" in output
        assert "COORD-001" in output
        assert "2 item(s) completed in last 30 days" in output

    def test_format_terminal_with_active_summary(self):
        """Test format_terminal shows active items in summary."""
        data = {
            "incoming": {"summary": {"coordination": 0, "tasks": 0, "context": 0}, "details": []},
            "active": {"count": 3, "list": [], "details": []},
            "recent_events": [],
            "completed": {"count_30d": 0, "days": 30, "recent": []}
        }

        output = inbox_status.format_terminal(data, detailed=False)
        assert "3 item(s) in active development" in output


class TestFormatMarkdownExtended:
    """Extended tests for format_markdown with full data."""

    def test_format_markdown_with_incoming_details(self):
        """Test format_markdown with incoming coordination details."""
        data = {
            "incoming": {
                "summary": {"coordination": 1, "tasks": 0, "context": 0},
                "details": [{
                    "request_id": "COORD-001",
                    "title": "Test Request",
                    "priority": "P1",
                    "from_repo": "test-repo",
                    "created": "2025-11-01"
                }]
            },
            "active": {"count": 0, "list": [], "details": []},
            "recent_events": [],
            "completed": {"count_30d": 0, "days": 30, "recent": []}
        }

        output = inbox_status.format_markdown(data)
        assert "### Coordination Requests" in output
        assert "| ID | Title | Priority | From | Created |" in output
        assert "| COORD-001 |" in output

    def test_format_markdown_with_active_details(self):
        """Test format_markdown with active work details."""
        data = {
            "incoming": {"summary": {"coordination": 0, "tasks": 0, "context": 0}, "details": []},
            "active": {
                "count": 1,
                "list": [],
                "details": [
                    {"id": "COORD-001", "type": "coordination", "priority": "P1"}
                ]
            },
            "recent_events": [],
            "completed": {"count_30d": 0, "days": 30, "recent": []}
        }

        output = inbox_status.format_markdown(data)
        assert "## Active Work" in output
        assert "### COORD-001" in output
        assert "**Type**: coordination" in output
        assert "**Priority**: P1" in output

    def test_format_markdown_with_recent_events(self):
        """Test format_markdown with recent activity."""
        data = {
            "incoming": {"summary": {"coordination": 0, "tasks": 0, "context": 0}, "details": []},
            "active": {"count": 0, "list": [], "details": []},
            "recent_events": [
                {
                    "event_type": "acknowledged",
                    "request_id": "COORD-001",
                    "timestamp": "2025-11-03T10:00:00Z"
                }
            ],
            "completed": {"count_30d": 0, "days": 30, "recent": []}
        }

        output = inbox_status.format_markdown(data)
        assert "## Recent Activity" in output
        assert "acknowledged • COORD-001" in output

    def test_format_markdown_with_completions(self):
        """Test format_markdown with recent completions."""
        data = {
            "incoming": {"summary": {"coordination": 0, "tasks": 0, "context": 0}, "details": []},
            "active": {"count": 0, "list": [], "details": []},
            "recent_events": [],
            "completed": {
                "count_30d": 2,
                "days": 30,
                "recent": [
                    {"id": "COORD-001", "completed_date": "2025-11-01"},
                    {"id": "COORD-002", "completed_date": "2025-11-02"}
                ]
            }
        }

        output = inbox_status.format_markdown(data)
        assert "## Recent Completions" in output
        assert "**COORD-001**" in output
        assert "(2025-11-01)" in output


class TestMainCLI:
    """Test main CLI function."""

    def test_main_default_terminal_output(self, mock_inbox, capsys, monkeypatch):
        """Test main with default terminal output."""
        original_inbox = inbox_status.INBOX_DIR
        original_repo = inbox_status.REPO_ROOT
        inbox_status.INBOX_DIR = mock_inbox
        inbox_status.REPO_ROOT = mock_inbox.parent

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-status.py']):
            inbox_status.main()

        captured = capsys.readouterr()
        assert "INBOX STATUS DASHBOARD" in captured.out

        inbox_status.INBOX_DIR = original_inbox
        inbox_status.REPO_ROOT = original_repo

    def test_main_json_format(self, mock_inbox, capsys):
        """Test main with JSON format."""
        original_inbox = inbox_status.INBOX_DIR
        original_repo = inbox_status.REPO_ROOT
        inbox_status.INBOX_DIR = mock_inbox
        inbox_status.REPO_ROOT = mock_inbox.parent

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-status.py', '--format', 'json']):
            inbox_status.main()

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert 'incoming' in data
        assert 'active' in data

        inbox_status.INBOX_DIR = original_inbox
        inbox_status.REPO_ROOT = original_repo

    def test_main_markdown_format(self, mock_inbox, capsys):
        """Test main with markdown format."""
        original_inbox = inbox_status.INBOX_DIR
        original_repo = inbox_status.REPO_ROOT
        inbox_status.INBOX_DIR = mock_inbox
        inbox_status.REPO_ROOT = mock_inbox.parent

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-status.py', '--format', 'markdown']):
            inbox_status.main()

        captured = capsys.readouterr()
        assert "# Inbox Status Report" in captured.out

        inbox_status.INBOX_DIR = original_inbox
        inbox_status.REPO_ROOT = original_repo

    def test_main_with_detailed_flag(self, mock_inbox, capsys):
        """Test main with --detailed flag."""
        original_inbox = inbox_status.INBOX_DIR
        original_repo = inbox_status.REPO_ROOT
        inbox_status.INBOX_DIR = mock_inbox
        inbox_status.REPO_ROOT = mock_inbox.parent

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-status.py', '--detailed']):
            inbox_status.main()

        captured = capsys.readouterr()
        assert "INBOX STATUS DASHBOARD" in captured.out

        inbox_status.INBOX_DIR = original_inbox
        inbox_status.REPO_ROOT = original_repo

    def test_main_with_priority_filter(self, mock_inbox, sample_coordination_request, capsys):
        """Test main with --priority filter."""
        original_inbox = inbox_status.INBOX_DIR
        original_repo = inbox_status.REPO_ROOT
        inbox_status.INBOX_DIR = mock_inbox
        inbox_status.REPO_ROOT = mock_inbox.parent

        # Create P1 request
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-status.py', '--priority', 'P1', '--format', 'json']):
            inbox_status.main()

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        # P1 filter should include our P1 request
        assert data['incoming']['summary']['coordination'] == 1

        inbox_status.INBOX_DIR = original_inbox
        inbox_status.REPO_ROOT = original_repo

    def test_main_with_last_days(self, mock_inbox, capsys):
        """Test main with --last filter."""
        original_inbox = inbox_status.INBOX_DIR
        original_repo = inbox_status.REPO_ROOT
        inbox_status.INBOX_DIR = mock_inbox
        inbox_status.REPO_ROOT = mock_inbox.parent

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-status.py', '--last', '7d', '--format', 'json']):
            inbox_status.main()

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert 'recent_events' in data

        inbox_status.INBOX_DIR = original_inbox
        inbox_status.REPO_ROOT = original_repo

    def test_main_with_trace_id_filter(self, mock_inbox, capsys):
        """Test main with --trace-id filter."""
        original_inbox = inbox_status.INBOX_DIR
        original_repo = inbox_status.REPO_ROOT
        inbox_status.INBOX_DIR = mock_inbox
        inbox_status.REPO_ROOT = mock_inbox.parent

        # Create event with trace_id
        events_file = mock_inbox / "coordination" / "events.jsonl"
        event_with_trace = {
            "event_type": "test",
            "request_id": "COORD-001",
            "timestamp": datetime.now().isoformat(),
            "trace_id": "trace-123"
        }
        with open(events_file, 'w') as f:
            f.write(json.dumps(event_with_trace) + '\n')

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-status.py', '--trace-id', 'trace-123', '--format', 'json']):
            inbox_status.main()

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert len(data['recent_events']) == 1
        assert data['recent_events'][0]['trace_id'] == 'trace-123'

        inbox_status.INBOX_DIR = original_inbox
        inbox_status.REPO_ROOT = original_repo

    def test_main_with_invalid_last_format(self, mock_inbox, capsys):
        """Test main with invalid --last format."""
        original_inbox = inbox_status.INBOX_DIR
        original_repo = inbox_status.REPO_ROOT
        inbox_status.INBOX_DIR = mock_inbox
        inbox_status.REPO_ROOT = mock_inbox.parent

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-status.py', '--last', 'invalid']):
            with pytest.raises(SystemExit) as exc_info:
                inbox_status.main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Invalid --last format" in captured.err

        inbox_status.INBOX_DIR = original_inbox
        inbox_status.REPO_ROOT = original_repo


class TestIntegration:
    """Integration tests."""

    def test_full_status_generation(self, mock_inbox, sample_coordination_request, mock_events_file):
        """Test generating complete status report."""
        original_inbox = inbox_status.INBOX_DIR
        inbox_status.INBOX_DIR = mock_inbox

        # Set up test data
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-2025-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        # Collect status data (simulating main function logic)
        incoming_summary = inbox_status.count_incoming()
        incoming_details = inbox_status.get_incoming_details()
        active_count, active_list = inbox_status.count_active()
        events = inbox_status.load_events()

        # Verify data structure
        assert incoming_summary['coordination'] == 1
        assert len(incoming_details) == 1
        assert active_count == 0
        assert len(events) == 2

        inbox_status.INBOX_DIR = original_inbox
