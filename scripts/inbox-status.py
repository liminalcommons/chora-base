#!/usr/bin/env python3
"""inbox-status.py - Comprehensive inbox status dashboard for SAP-001

Purpose: Display current status of inbox protocol workflow
Usage:
    # Quick overview
    python scripts/inbox-status.py

    # Detailed view with filters
    python scripts/inbox-status.py --detailed --priority P0 --last 7d

    # Export formats
    python scripts/inbox-status.py --format json
    python scripts/inbox-status.py --format markdown > STATUS.md

Exit codes:
    0 - Success
    1 - Error
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Colors for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

def find_repo_root() -> Path:
    """Find repository root by looking for sap-catalog.json"""
    current = Path.cwd()
    while current != current.parent:
        if (current / 'sap-catalog.json').exists():
            return current
        current = current.parent
    # If not found, assume current directory
    return Path.cwd()

REPO_ROOT = find_repo_root()
INBOX_DIR = REPO_ROOT / 'inbox'

#############################################################################
# Data Loading Functions
#############################################################################

def load_json_file(filepath: Path) -> Optional[Dict]:
    """Load and parse JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return None

def load_events(last_n: Optional[int] = None, last_days: Optional[int] = None) -> List[Dict]:
    """Load events from events.jsonl"""
    events_file = INBOX_DIR / 'coordination' / 'events.jsonl'
    if not events_file.exists():
        return []

    events = []
    try:
        with open(events_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        event = json.loads(line)
                        events.append(event)
                    except json.JSONDecodeError:
                        continue
    except FileNotFoundError:
        return []

    # Filter by date if requested
    if last_days:
        cutoff = datetime.now() - timedelta(days=last_days)
        events = [e for e in events if parse_timestamp(e.get('timestamp', '')) > cutoff]

    # Sort by timestamp (newest first)
    events.sort(key=lambda e: e.get('timestamp', ''), reverse=True)

    # Limit to last_n if requested
    if last_n:
        events = events[:last_n]

    return events

def parse_timestamp(ts: str) -> datetime:
    """Parse ISO 8601 timestamp"""
    try:
        # Handle various ISO formats
        if 'T' in ts:
            return datetime.fromisoformat(ts.replace('Z', '+00:00'))
        return datetime.fromisoformat(ts)
    except (ValueError, AttributeError):
        return datetime.min

def scan_directory(path: Path, pattern: str = '*.json') -> List[Path]:
    """Scan directory for files matching pattern"""
    if not path.exists():
        return []
    return list(path.glob(pattern))

#############################################################################
# Status Calculation Functions
#############################################################################

def count_incoming() -> Dict[str, int]:
    """Count items in incoming queue"""
    incoming = INBOX_DIR / 'incoming'

    return {
        'coordination': len(scan_directory(incoming / 'coordination', '*.json')),
        'tasks': len(scan_directory(incoming / 'tasks', '*.json')) if (incoming / 'tasks').exists() else 0,
        'context': len(scan_directory(incoming / 'context', '*')) if (incoming / 'context').exists() else 0,
    }

def count_active() -> Tuple[int, List[str]]:
    """Count and list active items"""
    active = INBOX_DIR / 'active'
    if not active.exists():
        return 0, []

    active_items = [d.name for d in active.iterdir() if d.is_dir()]
    return len(active_items), active_items

def count_completed(days: int = 30) -> Tuple[int, List[Dict]]:
    """Count recent completions"""
    completed = INBOX_DIR / 'completed'
    if not completed.exists():
        return 0, []

    cutoff = datetime.now() - timedelta(days=days)
    recent = []

    for item_dir in completed.iterdir():
        if item_dir.is_dir():
            # Try to get completion date from directory mtime
            mtime = datetime.fromtimestamp(item_dir.stat().st_mtime)
            if mtime > cutoff:
                recent.append({
                    'id': item_dir.name,
                    'completed_date': mtime.strftime('%Y-%m-%d')
                })

    recent.sort(key=lambda x: x['completed_date'], reverse=True)
    return len(recent), recent

def get_incoming_details(priority_filter: Optional[str] = None) -> List[Dict]:
    """Get detailed information about incoming items"""
    incoming = INBOX_DIR / 'incoming' / 'coordination'
    if not incoming.exists():
        return []

    items = []
    for file in scan_directory(incoming, '*.json'):
        data = load_json_file(file)
        if data and data.get('type') == 'coordination':
            # Filter by priority if specified
            if priority_filter and data.get('priority') != priority_filter:
                continue

            items.append({
                'request_id': data.get('request_id', file.stem),
                'title': data.get('title', 'Untitled'),
                'priority': data.get('priority', 'P2'),
                'urgency': data.get('urgency', 'backlog'),
                'from_repo': data.get('from_repo', 'unknown'),
                'created': data.get('created', 'unknown'),
                'deliverables_count': len(data.get('deliverables', []))
            })

    # Sort by priority
    priority_order = {'P0': 0, 'P1': 1, 'P2': 2}
    items.sort(key=lambda x: priority_order.get(x['priority'], 3))

    return items

def get_active_details() -> List[Dict]:
    """Get detailed information about active items"""
    active = INBOX_DIR / 'active'
    if not active.exists():
        return []

    items = []
    for item_dir in active.iterdir():
        if item_dir.is_dir():
            # Try to load coordination request file
            request_file = None
            for file in item_dir.glob('*.json'):
                if 'coord' in file.stem.lower() or 'request' in file.stem.lower():
                    request_file = file
                    break

            if request_file:
                data = load_json_file(request_file)
                if data:
                    items.append({
                        'id': item_dir.name,
                        'title': data.get('title', 'Untitled'),
                        'type': data.get('type', 'unknown'),
                        'priority': data.get('priority', 'P2'),
                    })
                else:
                    items.append({
                        'id': item_dir.name,
                        'title': 'Unknown',
                        'type': 'unknown',
                        'priority': 'P2',
                    })
            else:
                items.append({
                    'id': item_dir.name,
                    'title': 'Unknown',
                    'type': 'unknown',
                    'priority': 'P2',
                })

    return items

#############################################################################
# Output Formatting Functions
#############################################################################

def format_terminal(data: Dict, detailed: bool = False) -> str:
    """Format status as terminal output with colors"""
    output = []

    # Header
    output.append(f"{Colors.BLUE}{Colors.BOLD}{'=' * 70}{Colors.NC}")
    output.append(f"{Colors.BLUE}{Colors.BOLD}{'INBOX STATUS DASHBOARD':^70}{Colors.NC}")
    generated_time = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    output.append(f"{Colors.BLUE}{Colors.BOLD}{generated_time:^70}{Colors.NC}")
    output.append(f"{Colors.BLUE}{Colors.BOLD}{'=' * 70}{Colors.NC}")
    output.append("")

    # Incoming Queue
    incoming = data['incoming']
    output.append(f"{Colors.CYAN}📥 INCOMING QUEUE{Colors.NC}")
    output.append(f"  Coordination Requests: {Colors.BOLD}{incoming['summary']['coordination']}{Colors.NC}")
    if detailed and incoming['details']:
        for item in incoming['details'][:5]:  # Show first 5
            priority_color = Colors.RED if item['priority'] == 'P0' else Colors.YELLOW if item['priority'] == 'P1' else Colors.NC
            output.append(f"    • {priority_color}{item['priority']}{Colors.NC} {item['request_id']}: {item['title'][:50]}")
    output.append(f"  Implementation Tasks: {Colors.BOLD}{incoming['summary']['tasks']}{Colors.NC}")
    output.append(f"  Context Items: {Colors.BOLD}{incoming['summary']['context']}{Colors.NC}")
    output.append("")

    # Active Work
    active = data['active']
    output.append(f"{Colors.CYAN}🔄 ACTIVE WORK{Colors.NC}")
    output.append(f"  Current Items: {Colors.BOLD}{active['count']}{Colors.NC}")
    if detailed and active['details']:
        for item in active['details']:
            output.append(f"    • {item['id']}")
            output.append(f"      Type: {item['type']} | Priority: {item['priority']}")
    output.append("")

    # Recent Activity
    if data['recent_events']:
        output.append(f"{Colors.CYAN}⏱️  RECENT ACTIVITY{Colors.NC}")
        for event in data['recent_events'][:5]:  # Show last 5
            ts = event.get('timestamp', '')
            if ts:
                try:
                    dt = parse_timestamp(ts)
                    time_str = dt.strftime('%m-%d %H:%M')
                except:
                    time_str = ts[:16]
            else:
                time_str = 'unknown'

            event_type = event.get('event_type', 'unknown')
            request_id = event.get('request_id', event.get('task_id', ''))
            output.append(f"  [{time_str}] {event_type:30} • {request_id}")
        output.append("")

    # Recent Completions
    completed = data['completed']
    if completed['recent']:
        output.append(f"{Colors.CYAN}✅ RECENT COMPLETIONS (Last {completed['days']}d){Colors.NC}")
        for item in completed['recent'][:5]:  # Show last 5
            output.append(f"  {item['completed_date']}: {item['id']}")
        output.append("")

    # Summary Footer
    output.append(f"{Colors.BLUE}{'─' * 70}{Colors.NC}")
    output.append(f"{Colors.BOLD}💡 Summary:{Colors.NC}")
    output.append(f"  • {incoming['summary']['coordination']} coordination request(s) awaiting review")
    if active['count'] > 0:
        output.append(f"  • {active['count']} item(s) in active development")
    if completed['count_30d'] > 0:
        output.append(f"  • {completed['count_30d']} item(s) completed in last 30 days")
    output.append(f"{Colors.BLUE}{'─' * 70}{Colors.NC}")
    output.append("")
    output.append(f"{Colors.BLUE}For detailed view:{Colors.NC} python scripts/inbox-status.py --detailed")
    output.append(f"{Colors.BLUE}For JSON export:{Colors.NC}   python scripts/inbox-status.py --format json")
    output.append("")

    return '\n'.join(output)

def format_json(data: Dict) -> str:
    """Format status as JSON"""
    return json.dumps(data, indent=2)

def format_markdown(data: Dict) -> str:
    """Format status as Markdown"""
    output = []

    output.append("# Inbox Status Report")
    output.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append(f"**Repository**: {REPO_ROOT.name}")
    output.append("")

    # Summary
    output.append("## Summary")
    incoming = data['incoming']['summary']
    output.append(f"- **Incoming**: {incoming['coordination']} coordination, {incoming['tasks']} tasks, {incoming['context']} context")
    output.append(f"- **Active**: {data['active']['count']} item(s) in progress")
    output.append(f"- **Completed (30d)**: {data['completed']['count_30d']} item(s)")
    output.append("")

    # Incoming Queue
    output.append("## Incoming Queue")
    output.append("")
    if data['incoming']['details']:
        output.append("### Coordination Requests")
        output.append("| ID | Title | Priority | From | Created |")
        output.append("|----|-------|----------|------|---------|")
        for item in data['incoming']['details']:
            output.append(f"| {item['request_id']} | {item['title'][:40]} | {item['priority']} | {item['from_repo']} | {item['created']} |")
        output.append("")

    # Active Work
    if data['active']['details']:
        output.append("## Active Work")
        output.append("")
        for item in data['active']['details']:
            output.append(f"### {item['id']}")
            output.append(f"- **Type**: {item['type']}")
            output.append(f"- **Priority**: {item['priority']}")
            output.append("")

    # Recent Activity
    if data['recent_events']:
        output.append("## Recent Activity")
        output.append("")
        for event in data['recent_events'][:10]:
            ts = event.get('timestamp', 'unknown')[:16]
            event_type = event.get('event_type', 'unknown')
            request_id = event.get('request_id', event.get('task_id', ''))
            output.append(f"- `[{ts}]` {event_type} • {request_id}")
        output.append("")

    # Recent Completions
    if data['completed']['recent']:
        output.append("## Recent Completions")
        output.append("")
        for idx, item in enumerate(data['completed']['recent'][:5], 1):
            output.append(f"{idx}. **{item['id']}** ({item['completed_date']})")
        output.append("")

    return '\n'.join(output)

#############################################################################
# Main Function
#############################################################################

def main():
    parser = argparse.ArgumentParser(description='Inbox status dashboard for SAP-001')
    parser.add_argument('--detailed', action='store_true', help='Show detailed information')
    parser.add_argument('--format', choices=['terminal', 'json', 'markdown'], default='terminal',
                       help='Output format (default: terminal)')
    parser.add_argument('--priority', choices=['P0', 'P1', 'P2'], help='Filter by priority')
    parser.add_argument('--last', help='Show events from last N days (e.g., 7d)')
    parser.add_argument('--trace-id', help='Filter by trace ID')

    args = parser.parse_args()

    # Parse --last argument
    last_days = None
    if args.last:
        try:
            last_days = int(args.last.rstrip('d'))
        except ValueError:
            print(f"Error: Invalid --last format. Use format like '7d'", file=sys.stderr)
            sys.exit(1)

    # Collect status data
    incoming_summary = count_incoming()
    incoming_details = get_incoming_details(priority_filter=args.priority)
    active_count, active_list = count_active()
    active_details = get_active_details()
    completed_30d, completed_recent = count_completed(days=30)
    events = load_events(last_n=20, last_days=last_days)

    # Filter events by trace_id if specified
    if args.trace_id:
        events = [e for e in events if e.get('trace_id') == args.trace_id]

    # Build data structure
    data = {
        'generated': datetime.now().isoformat(),
        'repo': REPO_ROOT.name,
        'inbox_version': '1.0.0',
        'incoming': {
            'summary': incoming_summary,
            'details': incoming_details
        },
        'active': {
            'count': active_count,
            'list': active_list,
            'details': active_details
        },
        'recent_events': events,
        'completed': {
            'count_30d': completed_30d,
            'days': 30,
            'recent': completed_recent
        }
    }

    # Format and output
    if args.format == 'json':
        print(format_json(data))
    elif args.format == 'markdown':
        print(format_markdown(data))
    else:  # terminal
        print(format_terminal(data, detailed=args.detailed))

if __name__ == '__main__':
    main()
