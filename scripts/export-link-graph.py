#!/usr/bin/env python3
"""
Export Link Graph

Generates a machine-readable graph of all markdown links in the repository
for link validation, broken link detection, and document relationship mapping.

Part of Phase 3: Machine-Readable Exports (Curatorial Enhancements)
SAP Integration: SAP-016 (link-validation)

Usage:
    python scripts/export-link-graph.py                    # Export to scripts/link-graph.json
    python scripts/export-link-graph.py --output custom.json  # Custom output path
    python scripts/export-link-graph.py --format yaml      # Export as YAML
    python scripts/export-link-graph.py --validate         # Include broken link detection
"""

import json
import yaml
import os
import re
import glob
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Tuple
from datetime import datetime, timezone
from urllib.parse import urlparse

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def is_external_link(link: str) -> bool:
    """Check if a link is external (http/https)."""
    return link.startswith('http://') or link.startswith('https://')


def is_anchor_link(link: str) -> bool:
    """Check if a link is an anchor (starts with #)."""
    return link.startswith('#')


def normalize_path(link: str, source_file: str) -> str:
    """
    Normalize a relative link path to absolute path from repo root.

    Args:
        link: The markdown link (e.g., "../sap-framework/protocol-spec.md")
        source_file: The file containing the link (e.g., "docs/skilled-awareness/inbox/AGENTS.md")

    Returns:
        Normalized absolute path from repo root
    """
    if is_external_link(link) or is_anchor_link(link):
        return link

    # Remove anchor fragments
    if '#' in link:
        link = link.split('#')[0]

    # Get directory of source file
    source_dir = os.path.dirname(source_file)

    # Join with source directory and normalize
    absolute_path = os.path.normpath(os.path.join(source_dir, link))

    return absolute_path


def extract_links_from_markdown(file_path: str) -> List[Dict[str, str]]:
    """
    Extract all markdown links from a file.

    Returns:
        List of dicts with keys: text, url, line_number
    """
    links = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Regex for markdown links: [text](url)
        # Also captures reference-style links: [text][ref] and [ref]: url
        inline_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        reference_link_pattern = r'^\[([^\]]+)\]:\s*(.+)$'

        for line_num, line in enumerate(lines, 1):
            # Find inline links
            for match in re.finditer(inline_link_pattern, line):
                text = match.group(1)
                url = match.group(2)

                links.append({
                    'text': text,
                    'url': url,
                    'line_number': line_num,
                    'link_type': 'inline'
                })

            # Find reference-style link definitions
            match = re.match(reference_link_pattern, line)
            if match:
                text = match.group(1)
                url = match.group(2)

                links.append({
                    'text': text,
                    'url': url,
                    'line_number': line_num,
                    'link_type': 'reference'
                })

    except Exception as e:
        print(f"Warning: Could not parse {file_path}: {e}")

    return links


def categorize_link(link: str) -> str:
    """
    Categorize a link by type.

    Returns:
        "external" | "internal" | "anchor" | "email" | "unknown"
    """
    if is_anchor_link(link):
        return "anchor"

    if is_external_link(link):
        return "external"

    if link.startswith('mailto:'):
        return "email"

    # Internal file link
    if link.endswith('.md') or '/' in link or link.endswith('.yaml') or link.endswith('.json'):
        return "internal"

    return "unknown"


def validate_internal_link(link: str, source_file: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that an internal link points to an existing file.

    Returns:
        (is_valid, error_message)
    """
    normalized = normalize_path(link, source_file)

    # Check if file exists
    if os.path.exists(normalized):
        return (True, None)

    # Check if it's a directory link (should have index.md or similar)
    if os.path.isdir(normalized):
        if os.path.exists(os.path.join(normalized, 'README.md')):
            return (True, None)
        if os.path.exists(os.path.join(normalized, 'INDEX.md')):
            return (True, None)
        return (False, f"Directory exists but no INDEX.md or README.md: {normalized}")

    return (False, f"File not found: {normalized}")


def build_link_graph(
    paths: List[str] = None,
    validate: bool = False,
    exclude_patterns: List[str] = None
) -> Dict[str, Any]:
    """
    Build a complete link graph from markdown files.

    Args:
        paths: List of paths to search (defaults to common doc directories)
        validate: Whether to validate internal links
        exclude_patterns: Patterns to exclude (e.g., ['node_modules', '.git'])

    Returns:
        Dict with nodes (files) and edges (links)
    """
    if paths is None:
        paths = [
            'docs/',
            'README.md',
            'CLAUDE.md',
            'AGENTS.md',
            'inbox/',
            '.chora/'
        ]

    if exclude_patterns is None:
        exclude_patterns = ['node_modules', '.git', 'venv', '__pycache__', '.beads']

    # Find all markdown files
    markdown_files = []
    for path in paths:
        if os.path.isfile(path) and path.endswith('.md'):
            markdown_files.append(path)
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                # Exclude directories
                dirs[:] = [d for d in dirs if d not in exclude_patterns]

                for file in files:
                    if file.endswith('.md'):
                        file_path = os.path.join(root, file)
                        markdown_files.append(file_path)

    # Build graph
    nodes = {}
    edges = []
    broken_links = []

    for md_file in sorted(markdown_files):
        links = extract_links_from_markdown(md_file)

        # Add node for this file
        nodes[md_file] = {
            'path': md_file,
            'outbound_links': len(links),
            'inbound_links': 0,  # Will be calculated later
            'external_links': 0,
            'internal_links': 0,
            'anchor_links': 0,
            'broken_links': 0
        }

        # Process each link
        for link_info in links:
            url = link_info['url']
            category = categorize_link(url)

            # Update counts
            if category == 'external':
                nodes[md_file]['external_links'] += 1
            elif category == 'internal':
                nodes[md_file]['internal_links'] += 1
            elif category == 'anchor':
                nodes[md_file]['anchor_links'] += 1

            # Normalize internal links
            if category == 'internal':
                normalized_target = normalize_path(url, md_file)

                # Validate if requested
                is_valid = True
                error_msg = None
                if validate:
                    is_valid, error_msg = validate_internal_link(url, md_file)
                    if not is_valid:
                        nodes[md_file]['broken_links'] += 1
                        broken_links.append({
                            'source': md_file,
                            'target': url,
                            'normalized_target': normalized_target,
                            'line_number': link_info['line_number'],
                            'error': error_msg
                        })

                # Add edge
                edges.append({
                    'source': md_file,
                    'target': normalized_target,
                    'link_text': link_info['text'],
                    'line_number': link_info['line_number'],
                    'valid': is_valid,
                    'error': error_msg
                })
            elif category == 'external':
                # Add external link edge
                edges.append({
                    'source': md_file,
                    'target': url,
                    'link_text': link_info['text'],
                    'line_number': link_info['line_number'],
                    'external': True
                })

    # Calculate inbound link counts
    for edge in edges:
        target = edge['target']
        if target in nodes:
            nodes[target]['inbound_links'] += 1

    # Graph statistics
    total_nodes = len(nodes)
    total_edges = len(edges)
    total_broken = len(broken_links)

    internal_edges = [e for e in edges if not e.get('external', False)]
    external_edges = [e for e in edges if e.get('external', False)]

    # Find orphaned files (no inbound links)
    orphaned = [path for path, node in nodes.items() if node['inbound_links'] == 0]

    # Find hub files (high inbound links)
    hubs = sorted(
        [(path, node['inbound_links']) for path, node in nodes.items()],
        key=lambda x: -x[1]
    )[:10]

    return {
        'metadata': {
            'generated': datetime.now(timezone.utc).isoformat(),
            'validation_enabled': validate,
            'paths_scanned': paths,
            'exclude_patterns': exclude_patterns
        },
        'statistics': {
            'total_files': total_nodes,
            'total_links': total_edges,
            'internal_links': len(internal_edges),
            'external_links': len(external_edges),
            'broken_links': total_broken,
            'orphaned_files': len(orphaned)
        },
        'nodes': nodes,
        'edges': edges,
        'broken_links': broken_links if validate else None,
        'orphaned_files': orphaned,
        'top_hubs': [{'path': path, 'inbound_links': count} for path, count in hubs]
    }


def export_link_graph(
    output_path: str = "scripts/link-graph.json",
    format: str = "json",
    validate: bool = False,
    paths: List[str] = None
):
    """
    Generate and export link graph.
    """
    print(f"🔍 Scanning markdown files...")
    graph = build_link_graph(paths=paths, validate=validate)

    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    # Export
    if format == "json":
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph, f, indent=2)
        print(f"✅ Link graph exported to {output_path}")
    elif format == "yaml":
        output_path = output_path.replace('.json', '.yaml')
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(graph, f, default_flow_style=False, sort_keys=False)
        print(f"✅ Link graph exported to {output_path}")

    # Print summary
    stats = graph['statistics']
    print(f"\n📊 Link Graph Statistics:")
    print(f"   Files: {stats['total_files']}")
    print(f"   Total Links: {stats['total_links']}")
    print(f"     - Internal: {stats['internal_links']}")
    print(f"     - External: {stats['external_links']}")

    if validate:
        print(f"   Broken Links: {stats['broken_links']}")
        if stats['broken_links'] > 0:
            print(f"\n❌ Found {stats['broken_links']} broken links:")
            for broken in graph['broken_links'][:5]:  # Show first 5
                print(f"      {broken['source']}:{broken['line_number']} -> {broken['target']}")
                print(f"         Error: {broken['error']}")
            if stats['broken_links'] > 5:
                print(f"      ... and {stats['broken_links'] - 5} more (see {output_path})")

    print(f"\n📈 Top 5 Hub Files (most inbound links):")
    for hub in graph['top_hubs'][:5]:
        print(f"   {hub['path']}: {hub['inbound_links']} links")

    print(f"\n🔗 Orphaned Files (no inbound links): {stats['orphaned_files']}")
    if stats['orphaned_files'] > 0:
        for orphan in graph['orphaned_files'][:5]:
            print(f"   {orphan}")
        if stats['orphaned_files'] > 5:
            print(f"   ... and {stats['orphaned_files'] - 5} more")

    return graph


def main():
    parser = argparse.ArgumentParser(description="Export link graph from markdown files")
    parser.add_argument(
        "--output",
        default="scripts/link-graph.json",
        help="Output file path (default: scripts/link-graph.json)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "yaml"],
        default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate internal links and detect broken links"
    )
    parser.add_argument(
        "--paths",
        nargs="+",
        help="Custom paths to scan (default: docs/, README.md, CLAUDE.md, inbox/)"
    )

    args = parser.parse_args()

    export_link_graph(
        output_path=args.output,
        format=args.format,
        validate=args.validate,
        paths=args.paths
    )


if __name__ == "__main__":
    main()
