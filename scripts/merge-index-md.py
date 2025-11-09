#!/usr/bin/env python3
"""merge-index-md.py - Intelligent merge for docs/skilled-awareness/INDEX.md

Merge Strategy: table-rows

Merges SAP index tables by rows, preserving project-specific SAP entries while
updating framework SAPs from upstream.

Usage:
  python scripts/merge-index-md.py [--dry-run] [--output PATH]

Algorithm:
  1. Parse both current and upstream INDEX.md tables
  2. Identify framework SAPs (SAP-000) - merge from upstream
  3. Identify project SAPs (SAP-001+) - preserve from current
  4. Merge tables maintaining proper formatting
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Install with: pip install PyYAML")
    sys.exit(1)

class TableRow:
    """Represents a markdown table row"""
    def __init__(self, sap_id: str, cells: List[str], line: str):
        self.sap_id = sap_id
        self.cells = cells
        self.line = line

    def __repr__(self):
        return f"TableRow(sap_id='{self.sap_id}', cells={len(self.cells)})"

def load_config(chorabase_path: str = '.chorabase') -> dict:
    """Load .chorabase configuration for INDEX.md"""
    if not Path(chorabase_path).exists():
        print(f"Error: {chorabase_path} not found")
        sys.exit(1)

    with open(chorabase_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    return config.get('hybrid', {}).get('docs/skilled-awareness/INDEX.md', {})

def parse_index_table(content: str) -> Tuple[List[str], Dict[str, TableRow], List[str]]:
    """Parse INDEX.md and extract table rows

    Returns:
        (header_lines, table_rows_dict, footer_lines)
        - header_lines: Everything before the table
        - table_rows_dict: {sap_id: TableRow}
        - footer_lines: Everything after the table
    """
    lines = content.split('\n')

    header_lines = []
    table_rows = {}
    footer_lines = []

    in_table = False
    table_ended = False

    # Pattern for table rows: | SAP-XXX | ... |
    table_row_pattern = re.compile(r'^\|\s*(SAP-\d+)\s*\|(.+)\|$')
    table_separator_pattern = re.compile(r'^\|[-\s:|]+\|$')

    for line in lines:
        if not in_table and not table_ended:
            # Look for table start (header row with "SAP ID")
            if '| SAP ID' in line or '|SAP ID' in line:
                in_table = True
                header_lines.append(line)
            else:
                header_lines.append(line)
        elif in_table:
            # Check if it's a separator line
            if table_separator_pattern.match(line):
                header_lines.append(line)
                continue

            # Check if it's a table row
            match = table_row_pattern.match(line)
            if match:
                sap_id = match.group(1).strip()
                cells = [cell.strip() for cell in match.group(2).split('|')]
                table_rows[sap_id] = TableRow(sap_id, cells, line)
            elif line.strip() and not line.startswith('|'):
                # Table ended
                in_table = False
                table_ended = True
                footer_lines.append(line)
            elif line.strip():
                # Still in table but different format - keep in header
                header_lines.append(line)
        else:
            # After table
            footer_lines.append(line)

    return header_lines, table_rows, footer_lines

def get_upstream_index() -> Optional[str]:
    """Get INDEX.md content from upstream using git"""
    import subprocess


# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    try:
        # Try to read from upstream
        result = subprocess.run(
            ['git', 'show', 'chora-base/main:docs/skilled-awareness/INDEX.md'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None

def merge_table_rows(
    current_rows: Dict[str, TableRow],
    upstream_rows: Dict[str, TableRow],
    config: dict
) -> Dict[str, TableRow]:
    """Merge table rows according to strategy

    Strategy:
      - preserve_rows: Update from upstream (framework SAPs like SAP-000)
      - project_specific_rows: Keep from current (project SAPs)
      - New upstream rows: Add if in preserve_rows list
    """
    preserve_rows = set(config.get('preserve_rows', []))
    project_specific_rows = set(config.get('project_specific_rows', []))
    merge_rows = set(config.get('merge_rows', []))

    merged = {}

    # First, add all current rows
    for sap_id, row in current_rows.items():
        if sap_id in preserve_rows or sap_id in merge_rows:
            # This is a framework SAP - should be updated from upstream
            if sap_id in upstream_rows:
                merged[sap_id] = upstream_rows[sap_id]
            else:
                # Keep current if not in upstream
                merged[sap_id] = row
        else:
            # Project-specific SAP - keep from current
            merged[sap_id] = row

    # Second, add any new framework SAPs from upstream
    for sap_id, row in upstream_rows.items():
        if sap_id not in merged and (sap_id in preserve_rows or sap_id in merge_rows):
            merged[sap_id] = row

    return merged

def reconstruct_index(
    header_lines: List[str],
    table_rows: Dict[str, TableRow],
    footer_lines: List[str]
) -> str:
    """Reconstruct INDEX.md from parsed components"""
    lines = []

    # Add header
    lines.extend(header_lines)

    # Add sorted table rows (by SAP ID)
    sorted_sap_ids = sorted(table_rows.keys(), key=lambda x: int(x.split('-')[1]))
    for sap_id in sorted_sap_ids:
        lines.append(table_rows[sap_id].line)

    # Add footer
    if footer_lines:
        lines.append('')  # Blank line before footer
        lines.extend(footer_lines)

    return '\n'.join(lines)

def write_merged_file(content: str, output_path: str, dry_run: bool) -> None:
    """Write merged content to file"""
    if dry_run:
        print("=" * 70)
        print("DRY RUN - Would write merged content:")
        print("=" * 70)
        # Show table rows section
        table_start = content.find('| SAP-')
        if table_start != -1:
            table_section = content[max(0, table_start-200):table_start+1500]
            print(table_section)
        else:
            print(content[:1500])
        if len(content) > 1500:
            print(f"\n... ({len(content) - 1500} more characters)")
        print("=" * 70)
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Merged INDEX.md written to: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Intelligent merge for INDEX.md using table-rows strategy",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show merge preview without writing file'
    )
    parser.add_argument(
        '--output',
        default='docs/skilled-awareness/INDEX.md',
        help='Output file path (default: docs/skilled-awareness/INDEX.md)'
    )
    parser.add_argument(
        '--current',
        default='docs/skilled-awareness/INDEX.md',
        help='Current INDEX.md file (default: docs/skilled-awareness/INDEX.md)'
    )
    parser.add_argument(
        '--chorabase',
        default='.chorabase',
        help='Path to .chorabase config (default: .chorabase)'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("INDEX.md Table-Rows Merge")
    print("=" * 70)
    print()

    # Load config
    config = load_config(args.chorabase)
    if not config:
        print("Error: No INDEX.md configuration found in .chorabase")
        sys.exit(1)

    preserve_rows = config.get('preserve_rows', [])
    project_rows = config.get('project_specific_rows', [])

    print(f"✓ Loaded merge configuration from {args.chorabase}")
    print(f"  - Preserve rows (merge from upstream): {', '.join(preserve_rows)}")
    print(f"  - Project-specific rows (keep current): {len(project_rows)} SAPs")
    print()

    # Parse current INDEX.md
    if not Path(args.current).exists():
        print(f"Error: Current INDEX.md not found: {args.current}")
        sys.exit(1)

    with open(args.current, 'r', encoding='utf-8') as f:
        current_content = f.read()

    print(f"Parsing current {args.current}...")
    current_header, current_rows, current_footer = parse_index_table(current_content)
    print(f"✓ Parsed current INDEX.md")
    print(f"  - Table rows found: {len(current_rows)}")
    if current_rows:
        sap_ids = sorted(current_rows.keys(), key=lambda x: int(x.split('-')[1]))
        print(f"  - SAP IDs: {', '.join(sap_ids[:5])}" + (f", ... and {len(sap_ids)-5} more" if len(sap_ids) > 5 else ""))
    print()

    # Get upstream INDEX.md
    print("Fetching upstream INDEX.md...")
    upstream_content = get_upstream_index()

    if not upstream_content:
        print("⚠ Warning: Could not fetch upstream INDEX.md")
        print("  Using current rows only")
        upstream_rows = {}
    else:
        _, upstream_rows, _ = parse_index_table(upstream_content)
        print(f"✓ Parsed upstream INDEX.md")
        print(f"  - Table rows found: {len(upstream_rows)}")
        if upstream_rows:
            sap_ids = sorted(upstream_rows.keys(), key=lambda x: int(x.split('-')[1]))
            print(f"  - SAP IDs: {', '.join(sap_ids)}")
        print()

    # Merge table rows
    print("Merging table rows...")
    merged_rows = merge_table_rows(current_rows, upstream_rows, config)
    print(f"✓ Merge complete - {len(merged_rows)} rows in merged table")
    print()

    # Reconstruct INDEX.md
    merged_content = reconstruct_index(current_header, merged_rows, current_footer)

    # Write output
    write_merged_file(merged_content, args.output, args.dry_run)

    if not args.dry_run:
        print()
        print("Next steps:")
        print("  1. Review merged INDEX.md")
        print("  2. Verify SAP entries are correct")
        print("  3. Commit: git add docs/skilled-awareness/INDEX.md && git commit -m 'docs: Merge INDEX.md from upstream'")

if __name__ == '__main__':
    main()
