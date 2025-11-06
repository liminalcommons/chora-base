"""
Tests for scripts/inbox-query.py

Tests the InboxQuery class and related functions for querying
inbox coordination items.
"""

import json
import pytest
from pathlib import Path
from datetime import datetime, timedelta
import sys
import os
import importlib.util

# Import the module under test (has dash in filename, so use importlib)
repo_root = Path(__file__).parent.parent
inbox_query_path = repo_root / "scripts" / "inbox-query.py"

# Load module using importlib
spec = importlib.util.spec_from_file_location("inbox_query", inbox_query_path)
inbox_query = importlib.util.module_from_spec(spec)
sys.modules['inbox_query'] = inbox_query
spec.loader.exec_module(inbox_query)

# Import symbols for convenience
InboxQuery = inbox_query.InboxQuery
format_output = inbox_query.format_output
main = inbox_query.main
VERSION = inbox_query.VERSION


class TestInboxQuery:
    """Test InboxQuery class."""

    def test_init(self, mock_inbox):
        """Test InboxQuery initialization."""
        query = InboxQuery(inbox_path=mock_inbox, verbose=False)
        assert query.inbox_path == mock_inbox
        assert query.verbose == False

    def test_get_incoming_empty(self, mock_inbox):
        """Test getting incoming items from empty inbox."""
        query = InboxQuery(inbox_path=mock_inbox)
        items = query.get_incoming()
        assert items == []

    def test_get_incoming_with_items(self, mock_inbox, sample_coordination_request):
        """Test getting incoming items with coordination requests."""
        # Create a coordination request file
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-2025-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        query = InboxQuery(inbox_path=mock_inbox)
        items = query.get_incoming()

        assert len(items) == 1
        assert items[0]['id'] == 'COORD-2025-001'
        assert items[0]['title'] == 'Test Coordination Request'
        assert items[0]['priority'] == 'P1'
        assert items[0]['type'] == 'coordination'

    def test_get_incoming_unacknowledged(self, mock_inbox, sample_coordination_request):
        """Test filtering unacknowledged items."""
        # Create a coordination request
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-2025-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        query = InboxQuery(inbox_path=mock_inbox)

        # Without filter, should return item
        items = query.get_incoming(unacknowledged=False)
        assert len(items) == 1

        # With unacknowledged filter (and no active file), should return item
        items = query.get_incoming(unacknowledged=True)
        assert len(items) == 1

        # Create active file (marks as acknowledged)
        active_file = mock_inbox / "active" / "COORD-2025-001.json"
        with open(active_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        # Now unacknowledged filter should exclude it
        items = query.get_incoming(unacknowledged=True)
        assert len(items) == 0

    def test_get_active(self, mock_inbox, sample_coordination_request):
        """Test getting active items."""
        # Create an active item
        active_file = mock_inbox / "active" / "COORD-2025-001.json"
        with open(active_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        query = InboxQuery(inbox_path=mock_inbox)
        items = query.get_active()

        assert len(items) == 1
        assert items[0]['id'] == 'COORD-2025-001'
        assert items[0]['title'] == 'Test Coordination Request'

    def test_get_item(self, mock_inbox, sample_coordination_request):
        """Test getting specific item by ID."""
        # Create a coordination request
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-2025-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        query = InboxQuery(inbox_path=mock_inbox)
        item = query.get_item("COORD-2025-001")

        assert item is not None
        assert item['id'] == 'COORD-2025-001'
        assert item['location'] == 'incoming'
        assert item['title'] == 'Test Coordination Request'

    def test_get_item_not_found(self, mock_inbox):
        """Test getting non-existent item."""
        query = InboxQuery(inbox_path=mock_inbox)
        item = query.get_item("COORD-NONEXISTENT")
        assert item is None

    def test_count_by_status(self, mock_inbox, sample_coordination_request):
        """Test counting items by status."""
        # Create items in different locations
        incoming_file = mock_inbox / "incoming" / "coordination" / "COORD-2025-001.json"
        with open(incoming_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        active_request = sample_coordination_request.copy()
        active_request['request_id'] = 'COORD-2025-002'
        active_file = mock_inbox / "active" / "COORD-2025-002.json"
        with open(active_file, 'w') as f:
            json.dump(active_request, f)

        query = InboxQuery(inbox_path=mock_inbox)
        counts = query.count_by_status()

        assert counts['incoming_coordination'] == 1
        assert counts['active'] == 1
        assert counts['unacknowledged'] == 1  # COORD-2025-001 not acknowledged

    def test_is_acknowledged(self, mock_inbox, sample_coordination_request):
        """Test checking if item is acknowledged."""
        query = InboxQuery(inbox_path=mock_inbox)

        # Initially not acknowledged
        assert not query._is_acknowledged("COORD-2025-001")

        # Create active file (acknowledges it)
        active_file = mock_inbox / "active" / "COORD-2025-001.json"
        with open(active_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        # Now acknowledged
        assert query._is_acknowledged("COORD-2025-001")

    def test_get_status_from_events(self, mock_inbox, mock_events_file):
        """Test getting status from events log."""
        query = InboxQuery(inbox_path=mock_inbox)
        status = query._get_status_from_events("COORD-2025-001")

        # Should be 'acknowledged' from last event
        assert status == "acknowledged"

    def test_matches_age_filter(self, mock_inbox):
        """Test age filter matching."""
        query = InboxQuery(inbox_path=mock_inbox)

        # Test various filters
        assert query._matches_age_filter(72, ">24h")  # 72h > 24h
        assert query._matches_age_filter(48, ">1d")   # 48h > 24h
        assert not query._matches_age_filter(12, ">24h")  # 12h not > 24h
        assert query._matches_age_filter(12, "<24h")  # 12h < 24h
        assert not query._matches_age_filter(168, ">1w")  # 168h = 1w, not > 1w
        assert query._matches_age_filter(169, ">1w")  # 169h > 168h

        # Test >= and <= operators
        assert query._matches_age_filter(24, ">=24h")  # 24h >= 24h
        assert query._matches_age_filter(24, "<=24h")  # 24h <= 24h
        assert query._matches_age_filter(25, ">=24h")  # 25h >= 24h
        assert query._matches_age_filter(23, "<=24h")  # 23h <= 24h

        # Test = operator (within 1 hour)
        assert query._matches_age_filter(24, "=24h")  # 24h = 24h (exact)
        assert query._matches_age_filter(24.5, "=24h")  # 24.5h ≈ 24h (within 1h)
        assert not query._matches_age_filter(26, "=24h")  # 26h not ≈ 24h

        # Test invalid filter (returns True, no filtering)
        assert query._matches_age_filter(100, "invalid")  # Invalid format

        # Test unknown operator (else branch - line 343)
        assert query._matches_age_filter(100, "!24h")  # Unknown operator

    def test_verbose_logging(self, mock_inbox, capsys):
        """Test verbose logging output."""
        query = InboxQuery(inbox_path=mock_inbox, verbose=True)

        # Test log method
        query.log("Test message")
        captured = capsys.readouterr()
        assert "[DEBUG] Test message" in captured.err

    def test_get_incoming_missing_directory_verbose(self, mock_inbox, capsys):
        """Test get_incoming when directory doesn't exist with verbose logging."""
        # Remove incoming directory
        import shutil
        incoming_dir = mock_inbox / "incoming" / "coordination"
        if incoming_dir.exists():
            shutil.rmtree(incoming_dir)

        query = InboxQuery(inbox_path=mock_inbox, verbose=True)
        items = query.get_incoming()

        # Should return empty and log message
        assert items == []
        captured = capsys.readouterr()
        assert "does not exist" in captured.err


class TestFormatOutput:
    """Test output formatting functions."""

    def test_format_json(self):
        """Test JSON formatting."""
        items = [
            {"id": "COORD-001", "title": "Test", "priority": "P1"}
        ]
        output = format_output(items, "json")
        parsed = json.loads(output)
        assert len(parsed) == 1
        assert parsed[0]['id'] == 'COORD-001'

    def test_format_table_empty(self):
        """Test table formatting with empty list."""
        output = format_output([], "table")
        assert output == "No items found."

    def test_format_table_with_items(self):
        """Test table formatting with items."""
        items = [
            {
                "id": "COORD-001",
                "title": "Test Coordination",
                "priority": "P1",
                "status": "acknowledged"
            }
        ]
        output = format_output(items, "table")
        assert "COORD-001" in output
        assert "Test Coordination" in output
        assert "P1" in output

    def test_format_summary(self):
        """Test summary formatting."""
        items = [
            {
                "id": "COORD-001",
                "title": "Test Coordination",
                "priority": "P1",
                "urgency": "next_sprint"
            }
        ]
        output = format_output(items, "summary")
        assert "[COORD-001]" in output
        assert "Test Coordination" in output
        assert "P1" in output
        assert "next_sprint" in output

    def test_format_summary_empty(self):
        """Test summary format with empty list."""
        output = format_output([], "summary")
        assert output == "No items found."

    def test_format_summary_with_status(self):
        """Test summary format with status field."""
        items = [
            {
                "id": "COORD-001",
                "title": "Test Coordination",
                "priority": "P1",
                "urgency": "next_sprint",
                "status": "in_progress"
            }
        ]
        output = format_output(items, "summary")
        assert "[COORD-001]" in output
        assert "Status: in_progress" in output


class TestInboxQueryExtended:
    """Extended tests for edge cases and error handling."""

    def test_get_incoming_with_age_filter(self, mock_inbox, sample_coordination_request):
        """Test get_incoming with age filter."""
        # Create a coordination request
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-2025-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        query = InboxQuery(inbox_path=mock_inbox)

        # Get items older than 0 hours (should include all)
        items = query.get_incoming(age_filter=">0h")
        assert len(items) == 1

        # Get items less than 1 hour old (should include recent ones)
        items = query.get_incoming(age_filter="<1000h")
        assert len(items) == 1

        # Get items older than 1000 hours (should exclude all)
        items = query.get_incoming(age_filter=">1000h")
        assert len(items) == 0

    def test_get_incoming_with_error_handling(self, mock_inbox, capsys):
        """Test get_incoming with malformed JSON."""
        # Create invalid JSON file
        invalid_file = mock_inbox / "incoming" / "coordination" / "INVALID.json"
        with open(invalid_file, 'w') as f:
            f.write("{ invalid json")

        query = InboxQuery(inbox_path=mock_inbox, verbose=True)
        items = query.get_incoming()

        # Should skip invalid file
        assert len(items) == 0

        # Check error was logged
        captured = capsys.readouterr()
        assert "Error reading" in captured.err

    def test_get_active_no_directory(self, mock_inbox):
        """Test get_active when directory doesn't exist."""
        # Remove active directory
        active_dir = mock_inbox / "active"
        if active_dir.exists():
            import shutil
            shutil.rmtree(active_dir)

        query = InboxQuery(inbox_path=mock_inbox)
        items = query.get_active()
        assert items == []

    def test_get_active_with_error_handling(self, mock_inbox, capsys):
        """Test get_active with malformed JSON."""
        # Create invalid JSON file in active
        invalid_file = mock_inbox / "active" / "INVALID.json"
        with open(invalid_file, 'w') as f:
            f.write("{ invalid json")

        query = InboxQuery(inbox_path=mock_inbox, verbose=True)
        items = query.get_active()

        # Should skip invalid file
        assert len(items) == 0

        # Check error was logged
        captured = capsys.readouterr()
        assert "Error reading" in captured.err

    def test_get_item_with_error_handling(self, mock_inbox, capsys):
        """Test get_item with malformed JSON."""
        # Create invalid JSON file
        invalid_file = mock_inbox / "incoming" / "coordination" / "COORD-ERROR.json"
        with open(invalid_file, 'w') as f:
            f.write("{ invalid json")

        query = InboxQuery(inbox_path=mock_inbox, verbose=True)
        item = query.get_item("COORD-ERROR")

        # Should return None
        assert item is None

        # Check error was logged
        captured = capsys.readouterr()
        assert "Error reading" in captured.err

    def test_is_acknowledged_via_events(self, mock_inbox):
        """Test _is_acknowledged checking events file."""
        # Create events file with acknowledgment
        events_file = mock_inbox / "coordination" / "events.jsonl"
        events = [
            {"request_id": "COORD-2025-001", "event_type": "acknowledged"},
            {"request_id": "COORD-2025-002", "event_type": "accepted"},
            {"request_id": "COORD-2025-003", "event_type": "declined"},
        ]
        with open(events_file, 'w') as f:
            for event in events:
                f.write(json.dumps(event) + '\n')

        query = InboxQuery(inbox_path=mock_inbox)

        # Check acknowledged items
        assert query._is_acknowledged("COORD-2025-001")
        assert query._is_acknowledged("COORD-2025-002")
        assert query._is_acknowledged("COORD-2025-003")
        assert not query._is_acknowledged("COORD-NOTFOUND")

    def test_is_acknowledged_error_handling(self, mock_inbox, capsys):
        """Test _is_acknowledged with malformed events file."""
        # Create malformed events file
        events_file = mock_inbox / "coordination" / "events.jsonl"
        with open(events_file, 'w') as f:
            f.write("{ invalid json\n")

        query = InboxQuery(inbox_path=mock_inbox, verbose=True)
        result = query._is_acknowledged("COORD-2025-001")

        # Should return False and log error
        assert result == False
        captured = capsys.readouterr()
        assert "Error reading events" in captured.err

    def test_get_status_from_events_all_types(self, mock_inbox):
        """Test _get_status_from_events with all event types."""
        # Create events file with various event types
        events_file = mock_inbox / "coordination" / "events.jsonl"
        events = [
            {"request_id": "COORD-001", "event_type": "coordination_request_created"},
            {"request_id": "COORD-002", "event_type": "acknowledged"},
            {"request_id": "COORD-003", "event_type": "accepted"},
            {"request_id": "COORD-004", "event_type": "declined"},
            {"request_id": "COORD-005", "event_type": "in_progress"},
            {"request_id": "COORD-006", "event_type": "completed"},
            {"request_id": "COORD-007", "event_type": "blocked"},
        ]
        with open(events_file, 'w') as f:
            for event in events:
                f.write(json.dumps(event) + '\n')

        query = InboxQuery(inbox_path=mock_inbox)

        # Test all event type mappings
        assert query._get_status_from_events("COORD-001") == "created"
        assert query._get_status_from_events("COORD-002") == "acknowledged"
        assert query._get_status_from_events("COORD-003") == "accepted"
        assert query._get_status_from_events("COORD-004") == "declined"
        assert query._get_status_from_events("COORD-005") == "in_progress"
        assert query._get_status_from_events("COORD-006") == "completed"
        assert query._get_status_from_events("COORD-007") == "blocked"

    def test_get_status_from_events_no_file(self, mock_inbox):
        """Test _get_status_from_events when events file doesn't exist."""
        query = InboxQuery(inbox_path=mock_inbox)
        status = query._get_status_from_events("COORD-2025-001")
        assert status == "unknown"

    def test_get_status_from_events_error_handling(self, mock_inbox, capsys):
        """Test _get_status_from_events with malformed events file."""
        # Create malformed events file
        events_file = mock_inbox / "coordination" / "events.jsonl"
        with open(events_file, 'w') as f:
            f.write("{ invalid json\n")

        query = InboxQuery(inbox_path=mock_inbox, verbose=True)
        status = query._get_status_from_events("COORD-2025-001")

        # Should return unknown and log error
        assert status == "unknown"
        captured = capsys.readouterr()
        assert "Error reading events" in captured.err


class TestMainCLI:
    """Test main CLI function."""

    def test_main_count_by_status(self, mock_inbox, sample_coordination_request, capsys):
        """Test main with --count-by-status."""
        # Create some items
        incoming_file = mock_inbox / "incoming" / "coordination" / "COORD-2025-001.json"
        with open(incoming_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-query.py', '--count-by-status', '--inbox-path', str(mock_inbox)]):
            main()

        captured = capsys.readouterr()
        assert "Inbox Status Counts:" in captured.out
        assert "Incoming Coordination: 1" in captured.out

    def test_main_count_by_status_json(self, mock_inbox, capsys):
        """Test main with --count-by-status --format json."""
        from unittest.mock import patch
        with patch('sys.argv', ['inbox-query.py', '--count-by-status', '--format', 'json', '--inbox-path', str(mock_inbox)]):
            main()

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert 'incoming_coordination' in data

    def test_main_request_by_id(self, mock_inbox, sample_coordination_request, capsys):
        """Test main with --request."""
        # Create item
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-2025-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-query.py', '--request', 'COORD-2025-001', '--inbox-path', str(mock_inbox)]):
            main()

        captured = capsys.readouterr()
        assert "Request: COORD-2025-001" in captured.out
        assert "Test Coordination Request" in captured.out

    def test_main_request_by_id_json(self, mock_inbox, sample_coordination_request, capsys):
        """Test main with --request --format json."""
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-2025-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-query.py', '--request', 'COORD-2025-001', '--format', 'json', '--inbox-path', str(mock_inbox)]):
            main()

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data['id'] == 'COORD-2025-001'

    def test_main_request_not_found(self, mock_inbox, capsys):
        """Test main with --request for non-existent item."""
        from unittest.mock import patch
        with patch('sys.argv', ['inbox-query.py', '--request', 'COORD-NOTFOUND', '--inbox-path', str(mock_inbox)]):
            with pytest.raises(SystemExit) as exc_info:
                main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Item not found" in captured.err

    def test_main_active(self, mock_inbox, sample_coordination_request, capsys):
        """Test main with --active."""
        active_file = mock_inbox / "active" / "COORD-2025-001.json"
        with open(active_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-query.py', '--active', '--inbox-path', str(mock_inbox)]):
            main()

        captured = capsys.readouterr()
        assert "COORD-2025-001" in captured.out

    def test_main_active_with_status_filter(self, mock_inbox, sample_coordination_request, mock_events_file, capsys):
        """Test main with --active --status."""
        active_file = mock_inbox / "active" / "COORD-2025-001.json"
        with open(active_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-query.py', '--active', '--status', 'acknowledged', '--inbox-path', str(mock_inbox)]):
            main()

        captured = capsys.readouterr()
        assert "COORD-2025-001" in captured.out

    def test_main_incoming_default(self, mock_inbox, sample_coordination_request, capsys):
        """Test main with --incoming (default mode)."""
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-2025-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-query.py', '--incoming', '--inbox-path', str(mock_inbox)]):
            main()

        captured = capsys.readouterr()
        assert "COORD-2025-001" in captured.out

    def test_main_incoming_with_type(self, mock_inbox, capsys):
        """Test main with --incoming --type tasks."""
        # Create a task item
        task_request = {"type": "task", "title": "Test Task", "priority": "P2"}
        task_file = mock_inbox / "incoming" / "tasks" / "TASK-001.json"
        with open(task_file, 'w') as f:
            json.dump(task_request, f)

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-query.py', '--incoming', '--type', 'tasks', '--inbox-path', str(mock_inbox)]):
            main()

        captured = capsys.readouterr()
        assert "TASK-001" in captured.out

    def test_main_incoming_unacknowledged(self, mock_inbox, sample_coordination_request, capsys):
        """Test main with --incoming --unacknowledged."""
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-2025-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-query.py', '--incoming', '--unacknowledged', '--inbox-path', str(mock_inbox)]):
            main()

        captured = capsys.readouterr()
        assert "COORD-2025-001" in captured.out

    def test_main_incoming_with_age_filter(self, mock_inbox, sample_coordination_request, capsys):
        """Test main with --incoming --age filter."""
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-2025-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-query.py', '--incoming', '--age', '<1000h', '--inbox-path', str(mock_inbox)]):
            main()

        captured = capsys.readouterr()
        assert "COORD-2025-001" in captured.out

    def test_main_incoming_with_status_filter(self, mock_inbox, sample_coordination_request, mock_events_file, capsys):
        """Test main with --incoming --status."""
        coord_file = mock_inbox / "incoming" / "coordination" / "COORD-2025-001.json"
        with open(coord_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        from unittest.mock import patch
        with patch('sys.argv', ['inbox-query.py', '--incoming', '--status', 'acknowledged', '--inbox-path', str(mock_inbox)]):
            main()

        captured = capsys.readouterr()
        assert "COORD-2025-001" in captured.out

    def test_main_exception_handling(self, mock_inbox, capsys):
        """Test main with exception."""
        from unittest.mock import patch, Mock
        with patch('sys.argv', ['inbox-query.py', '--count-by-status', '--inbox-path', str(mock_inbox)]):
            with patch.object(InboxQuery, 'count_by_status', side_effect=Exception("Test error")):
                with pytest.raises(SystemExit) as exc_info:
                    main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error: Test error" in captured.err

    def test_main_verbose_exception(self, mock_inbox, capsys):
        """Test main with --verbose and exception."""
        from unittest.mock import patch, Mock
        with patch('sys.argv', ['inbox-query.py', '--count-by-status', '--inbox-path', str(mock_inbox), '--verbose']):
            with patch.object(InboxQuery, 'count_by_status', side_effect=Exception("Test error")):
                with pytest.raises(SystemExit) as exc_info:
                    main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        # With verbose, should include traceback
        assert "Error: Test error" in captured.err


class TestInboxQueryIntegration:
    """Integration tests with full inbox structure."""

    def test_full_workflow(self, mock_inbox, sample_coordination_request):
        """Test complete workflow: incoming -> active -> completed."""
        query = InboxQuery(inbox_path=mock_inbox)

        # Start: Create incoming request
        incoming_file = mock_inbox / "incoming" / "coordination" / "COORD-2025-001.json"
        with open(incoming_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        # Check incoming
        items = query.get_incoming()
        assert len(items) == 1
        assert items[0]['id'] == 'COORD-2025-001'

        # Move to active
        active_file = mock_inbox / "active" / "COORD-2025-001.json"
        with open(active_file, 'w') as f:
            json.dump(sample_coordination_request, f)

        # Check active
        items = query.get_active()
        assert len(items) == 1

        # Check counts
        counts = query.count_by_status()
        assert counts['incoming_coordination'] == 1  # Still in incoming dir
        assert counts['active'] == 1
