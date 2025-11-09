#!/usr/bin/env python3
"""
Export Awareness Index

Generates a machine-readable index of all AGENTS.md and CLAUDE.md files
across the repository for agent navigation and progressive context loading.

Part of Phase 3: Machine-Readable Exports (Curatorial Enhancements)
SAP Integration: SAP-009 (agent-awareness)

Usage:
    python scripts/export-awareness-index.py                    # Export to scripts/awareness-index.json
    python scripts/export-awareness-index.py --output custom.json  # Custom output path
    python scripts/export-awareness-index.py --format yaml      # Export as YAML
    python scripts/export-awareness-index.py --extract-metadata # Extract frontmatter metadata
"""

import json
import yaml
import os
import re
import glob
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from datetime import datetime, timezone, date

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime and date objects."""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


def extract_yaml_frontmatter(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Extract YAML frontmatter from a markdown file.

    Returns:
        Dict of frontmatter fields, or None if no frontmatter found
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for YAML frontmatter (--- at start and end)
        if not content.startswith('---\n'):
            return None

        # Find the closing ---
        end_marker = content.find('\n---\n', 4)
        if end_marker == -1:
            return None

        # Extract frontmatter
        frontmatter_text = content[4:end_marker]

        # Parse YAML
        frontmatter = yaml.safe_load(frontmatter_text)

        return frontmatter if isinstance(frontmatter, dict) else None

    except Exception as e:
        print(f"Warning: Could not extract frontmatter from {file_path}: {e}")
        return None


def extract_first_heading(file_path: str) -> Optional[str]:
    """
    Extract the first markdown heading (# or ##) from a file.

    Returns:
        The heading text without the # symbols
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            # Skip frontmatter
            if line.strip() == '---':
                continue

            # Find first heading
            match = re.match(r'^#{1,2}\s+(.+)$', line.strip())
            if match:
                return match.group(1).strip()

        return None

    except Exception as e:
        print(f"Warning: Could not extract heading from {file_path}: {e}")
        return None


def estimate_token_count(file_path: str) -> int:
    """
    Estimate token count for a file (rough approximation: 4 chars = 1 token).

    Returns:
        Estimated token count
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Rough approximation: 4 characters = 1 token
        return len(content) // 4

    except Exception as e:
        print(f"Warning: Could not estimate tokens for {file_path}: {e}")
        return 0


def categorize_awareness_file(file_path: str) -> str:
    """
    Categorize an awareness file by its location in the repo.

    Returns:
        "root" | "domain" | "capability" | "feature" | "component"
    """
    parts = Path(file_path).parts

    # Root level (AGENTS.md, CLAUDE.md at repo root)
    if len(parts) == 1:
        return "root"

    # Domain level (docs/skilled-awareness/AGENTS.md)
    if len(parts) == 3 and parts[0] == 'docs':
        return "domain"

    # Capability level (docs/skilled-awareness/sap-framework/AGENTS.md)
    if len(parts) == 4 and parts[0] == 'docs':
        return "capability"

    # Feature level (deeper nesting)
    if len(parts) == 5:
        return "feature"

    # Component level (even deeper)
    if len(parts) >= 6:
        return "component"

    return "unknown"


def find_awareness_files(
    paths: List[str] = None,
    exclude_patterns: List[str] = None
) -> List[str]:
    """
    Find all AGENTS.md and CLAUDE.md files in the repository.

    Args:
        paths: List of paths to search (defaults to entire repo)
        exclude_patterns: Patterns to exclude (e.g., ['node_modules', '.git'])

    Returns:
        List of file paths
    """
    if paths is None:
        paths = ['.']

    if exclude_patterns is None:
        exclude_patterns = ['node_modules', '.git', 'venv', '__pycache__', '.beads']

    awareness_files = []

    for path in paths:
        if os.path.isfile(path) and (path.endswith('AGENTS.md') or path.endswith('CLAUDE.md')):
            awareness_files.append(path)
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                # Exclude directories
                dirs[:] = [d for d in dirs if d not in exclude_patterns]

                for file in files:
                    if file in ['AGENTS.md', 'CLAUDE.md']:
                        file_path = os.path.join(root, file)
                        awareness_files.append(file_path)

    return sorted(awareness_files)


def build_awareness_index(
    paths: List[str] = None,
    extract_metadata: bool = False,
    exclude_patterns: List[str] = None
) -> Dict[str, Any]:
    """
    Build a complete awareness index from AGENTS.md and CLAUDE.md files.

    Args:
        paths: List of paths to search
        extract_metadata: Whether to extract frontmatter metadata
        exclude_patterns: Patterns to exclude

    Returns:
        Dict with awareness files, hierarchy, and statistics
    """
    awareness_files = find_awareness_files(paths=paths, exclude_patterns=exclude_patterns)

    # Build index
    files = []
    hierarchy = {
        'root': [],
        'domain': [],
        'capability': [],
        'feature': [],
        'component': [],
        'unknown': []
    }

    total_tokens = 0
    agents_count = 0
    claude_count = 0

    for file_path in awareness_files:
        # Categorize
        category = categorize_awareness_file(file_path)
        file_type = 'agents' if file_path.endswith('AGENTS.md') else 'claude'

        # Extract metadata
        frontmatter = extract_yaml_frontmatter(file_path) if extract_metadata else None
        heading = extract_first_heading(file_path)
        token_estimate = estimate_token_count(file_path)

        total_tokens += token_estimate

        if file_type == 'agents':
            agents_count += 1
        else:
            claude_count += 1

        # Build file entry
        file_entry = {
            'path': file_path,
            'type': file_type,
            'category': category,
            'heading': heading,
            'token_estimate': token_estimate
        }

        # Add frontmatter if extracted
        if frontmatter:
            file_entry['metadata'] = frontmatter

            # Extract progressive loading hints if present
            if 'progressive_loading' in frontmatter:
                file_entry['progressive_loading'] = frontmatter['progressive_loading']

            # Extract SAP ID if present
            if 'sap_id' in frontmatter:
                file_entry['sap_id'] = frontmatter['sap_id']

            # Extract complexity if present
            if 'complexity' in frontmatter:
                file_entry['complexity'] = frontmatter['complexity']

        files.append(file_entry)
        hierarchy[category].append(file_path)

    # Build navigation tree (root -> domain -> capability -> feature -> component)
    navigation_tree = {}

    for file_entry in files:
        path_parts = Path(file_entry['path']).parts
        current = navigation_tree

        for i, part in enumerate(path_parts[:-1]):  # Exclude filename
            if part not in current:
                current[part] = {'_files': [], '_children': {}}
            current = current[part]['_children']

        # Add file to final directory
        filename = path_parts[-1]
        if filename not in current:
            current[filename] = file_entry

    # Statistics
    statistics = {
        'total_files': len(files),
        'agents_files': agents_count,
        'claude_files': claude_count,
        'total_token_estimate': total_tokens,
        'by_category': {
            'root': len(hierarchy['root']),
            'domain': len(hierarchy['domain']),
            'capability': len(hierarchy['capability']),
            'feature': len(hierarchy['feature']),
            'component': len(hierarchy['component']),
            'unknown': len(hierarchy['unknown'])
        }
    }

    # Find files with progressive loading metadata
    progressive_loading_files = [
        f for f in files
        if 'progressive_loading' in f
    ]

    # Find files by complexity
    complexity_breakdown = {}
    for file_entry in files:
        if 'complexity' in file_entry:
            complexity = file_entry['complexity']
            complexity_breakdown[complexity] = complexity_breakdown.get(complexity, 0) + 1

    return {
        'metadata': {
            'generated': datetime.now(timezone.utc).isoformat(),
            'extraction_enabled': extract_metadata,
            'paths_scanned': paths or ['.'],
            'exclude_patterns': exclude_patterns or []
        },
        'statistics': statistics,
        'files': files,
        'hierarchy': hierarchy,
        'navigation_tree': navigation_tree,
        'progressive_loading_files': [f['path'] for f in progressive_loading_files],
        'complexity_breakdown': complexity_breakdown
    }


def export_awareness_index(
    output_path: str = "scripts/awareness-index.json",
    format: str = "json",
    extract_metadata: bool = False,
    paths: List[str] = None
):
    """
    Generate and export awareness index.
    """
    print(f"🔍 Scanning awareness files (AGENTS.md, CLAUDE.md)...")
    index = build_awareness_index(paths=paths, extract_metadata=extract_metadata)

    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    # Export
    if format == "json":
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, cls=DateTimeEncoder)
        print(f"✅ Awareness index exported to {output_path}")
    elif format == "yaml":
        output_path = output_path.replace('.json', '.yaml')
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(index, f, default_flow_style=False, sort_keys=False)
        print(f"✅ Awareness index exported to {output_path}")

    # Print summary
    stats = index['statistics']
    print(f"\n📊 Awareness Index Statistics:")
    print(f"   Total Files: {stats['total_files']}")
    print(f"     - AGENTS.md: {stats['agents_files']}")
    print(f"     - CLAUDE.md: {stats['claude_files']}")
    print(f"   Estimated Tokens: {stats['total_token_estimate']:,}")

    print(f"\n📁 Files by Category:")
    for category, count in stats['by_category'].items():
        if count > 0:
            print(f"   {category.capitalize()}: {count}")

    if index['progressive_loading_files']:
        print(f"\n⚡ Progressive Loading Files: {len(index['progressive_loading_files'])}")
        for path in index['progressive_loading_files'][:5]:
            print(f"   {path}")
        if len(index['progressive_loading_files']) > 5:
            print(f"   ... and {len(index['progressive_loading_files']) - 5} more")

    if index['complexity_breakdown']:
        print(f"\n🎯 Complexity Breakdown:")
        for complexity, count in sorted(index['complexity_breakdown'].items()):
            print(f"   {complexity}: {count}")

    return index


def main():
    parser = argparse.ArgumentParser(description="Export awareness file index")
    parser.add_argument(
        "--output",
        default="scripts/awareness-index.json",
        help="Output file path (default: scripts/awareness-index.json)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "yaml"],
        default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--extract-metadata",
        action="store_true",
        help="Extract frontmatter metadata from awareness files"
    )
    parser.add_argument(
        "--paths",
        nargs="+",
        help="Custom paths to scan (default: entire repo)"
    )

    args = parser.parse_args()

    export_awareness_index(
        output_path=args.output,
        format=args.format,
        extract_metadata=args.extract_metadata,
        paths=args.paths
    )


if __name__ == "__main__":
    main()
