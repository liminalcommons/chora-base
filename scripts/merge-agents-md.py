#!/usr/bin/env python3
"""merge-agents-md.py - Intelligent merge for AGENTS.md

Merge Strategy: section-by-section

Preserves project-specific sections while updating structural sections from upstream.

Usage:
  python scripts/merge-agents-md.py [--dry-run] [--output PATH]

Algorithm:
  1. Parse both current and upstream AGENTS.md into sections
  2. Identify section types using markers from .chorabase
  3. Keep preserve_sections from current (project-specific)
  4. Take merge_sections from upstream (structural updates)
  5. Merge while maintaining section order
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

class Section:
    """Represents a markdown section"""
    def __init__(self, title: str, level: int, content: List[str], line_start: int):
        self.title = title
        self.level = level
        self.content = content
        self.line_start = line_start

    def __repr__(self):
        return f"Section(title='{self.title}', level={self.level}, lines={len(self.content)})"

def parse_agents_md(file_path: str) -> Tuple[List[str], Dict[str, Section]]:
    """Parse AGENTS.md into sections

    Returns:
        (preamble_lines, sections_dict)
        - preamble_lines: Lines before first section
        - sections_dict: {section_title: Section}
    """
    if not Path(file_path).exists():
        return [], {}

    with open(file_path, 'r') as f:
        lines = f.readlines()

    preamble = []
    sections = {}
    current_section = None
    current_content = []
    line_num = 0

    # Pattern for section headers (## or ###)
    header_pattern = re.compile(r'^(#{2,3})\s+(.+)$')

    for i, line in enumerate(lines):
        match = header_pattern.match(line.strip())

        if match:
            # Save previous section
            if current_section:
                sections[current_section.title] = current_section

            # Start new section
            level = len(match.group(1))
            title = match.group(2).strip()
            current_section = Section(title, level, [line], i)
            current_content = [line]
        elif current_section:
            # Add to current section
            current_section.content.append(line)
        else:
            # Preamble (before first section)
            preamble.append(line)

    # Save last section
    if current_section:
        sections[current_section.title] = current_section

    return preamble, sections

def load_config(chorabase_path: str = '.chorabase') -> dict:
    """Load .chorabase configuration"""
    if not Path(chorabase_path).exists():
        print(f"Error: {chorabase_path} not found")
        sys.exit(1)

    with open(chorabase_path, 'r') as f:
        config = yaml.safe_load(f)

    return config.get('hybrid', {}).get('AGENTS.md', {})

def get_upstream_file(file_path: str = 'AGENTS.md') -> Optional[str]:
    """Get file content from upstream using git"""
    import subprocess

    try:
        # Try to read from upstream
        result = subprocess.run(
            ['git', 'show', f'chora-base/main:{file_path}'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        # Fallback: try origin/main if chora-base remote doesn't exist
        try:
            result = subprocess.run(
                ['git', 'show', f'origin/main:{file_path}'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return None

def merge_sections(
    current_preamble: List[str],
    current_sections: Dict[str, Section],
    upstream_sections: Dict[str, Section],
    config: dict
) -> List[str]:
    """Merge sections according to strategy

    Strategy:
      - preserve_sections: Keep from current (project-specific)
      - merge_sections: Take from upstream (structural updates)
      - Maintain section order from current, append new upstream sections
    """
    preserve_sections = set(config.get('preserve_sections', []))
    merge_sections = set(config.get('merge_sections', []))

    merged_lines = []

    # Add preamble from current
    merged_lines.extend(current_preamble)
    if merged_lines and not merged_lines[-1].endswith('\n'):
        merged_lines.append('\n')

    # Track which sections we've processed
    processed_sections = set()

    # First pass: Process sections in current order
    for title, section in current_sections.items():
        if title in preserve_sections:
            # Keep from current (project-specific)
            merged_lines.extend(section.content)
            if not merged_lines[-1].endswith('\n\n'):
                merged_lines.append('\n')
        elif title in merge_sections and title in upstream_sections:
            # Take from upstream (structural update)
            merged_lines.extend(upstream_sections[title].content)
            if not merged_lines[-1].endswith('\n\n'):
                merged_lines.append('\n')
        else:
            # Not specified - default to preserve current
            merged_lines.extend(section.content)
            if not merged_lines[-1].endswith('\n\n'):
                merged_lines.append('\n')

        processed_sections.add(title)

    # Second pass: Add new sections from upstream that weren't in current
    for title, section in upstream_sections.items():
        if title not in processed_sections and title in merge_sections:
            merged_lines.extend(section.content)
            if not merged_lines[-1].endswith('\n\n'):
                merged_lines.append('\n')

    return merged_lines

def write_merged_file(lines: List[str], output_path: str, dry_run: bool) -> None:
    """Write merged content to file"""
    content = ''.join(lines)

    if dry_run:
        print("=" * 70)
        print("DRY RUN - Would write merged content:")
        print("=" * 70)
        print(content[:1000])  # Show first 1000 chars
        if len(content) > 1000:
            print(f"\n... ({len(content) - 1000} more characters)")
        print("=" * 70)
    else:
        with open(output_path, 'w') as f:
            f.write(content)
        print(f"✓ Merged AGENTS.md written to: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Intelligent merge for AGENTS.md using section-by-section strategy",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show merge preview without writing file'
    )
    parser.add_argument(
        '--output',
        default='AGENTS.md',
        help='Output file path (default: AGENTS.md)'
    )
    parser.add_argument(
        '--current',
        default='AGENTS.md',
        help='Current AGENTS.md file (default: AGENTS.md)'
    )
    parser.add_argument(
        '--chorabase',
        default='.chorabase',
        help='Path to .chorabase config (default: .chorabase)'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("AGENTS.md Section-by-Section Merge")
    print("=" * 70)
    print()

    # Load config
    config = load_config(args.chorabase)
    if not config:
        print("Error: No AGENTS.md configuration found in .chorabase")
        sys.exit(1)

    print(f"✓ Loaded merge configuration from {args.chorabase}")
    print(f"  - Preserve sections: {', '.join(config.get('preserve_sections', []))}")
    print(f"  - Merge sections: {', '.join(config.get('merge_sections', []))}")
    print()

    # Parse current AGENTS.md
    current_preamble, current_sections = parse_agents_md(args.current)
    print(f"✓ Parsed current {args.current}")
    print(f"  - Sections found: {len(current_sections)}")
    if current_sections:
        print(f"  - Section titles: {', '.join(current_sections.keys())}")
    print()

    # Get upstream AGENTS.md
    print("Fetching upstream AGENTS.md...")
    upstream_content = get_upstream_file('AGENTS.md')

    if not upstream_content:
        print("⚠ Warning: Could not fetch upstream AGENTS.md")
        print("  Falling back to current file only")
        upstream_sections = {}
    else:
        # Write to temp file for parsing
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as tmp:
            tmp.write(upstream_content)
            tmp_path = tmp.name

        _, upstream_sections = parse_agents_md(tmp_path)
        Path(tmp_path).unlink()  # Clean up

        print(f"✓ Parsed upstream AGENTS.md")
        print(f"  - Sections found: {len(upstream_sections)}")
        if upstream_sections:
            print(f"  - Section titles: {', '.join(upstream_sections.keys())}")
        print()

    # Perform merge
    print("Merging sections...")
    merged_lines = merge_sections(
        current_preamble,
        current_sections,
        upstream_sections,
        config
    )
    print(f"✓ Merge complete - {len(merged_lines)} lines")
    print()

    # Write output
    write_merged_file(merged_lines, args.output, args.dry_run)

    if not args.dry_run:
        print()
        print("Next steps:")
        print("  1. Review merged AGENTS.md")
        print("  2. Make any manual adjustments needed")
        print("  3. Commit: git add AGENTS.md && git commit -m 'docs: Merge AGENTS.md from upstream'")

if __name__ == '__main__':
    main()
