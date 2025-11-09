#!/usr/bin/env python3
"""Link Validation Script v2.0 (Python rewrite).

Part of SAP-016: Link Validation & Reference Management

Simplified MVP focusing on internal markdown link validation.
Validates that internal links in markdown files point to existing files/directories.

Usage:
    python scripts/validate-links.py [PATH]
    python scripts/validate-links.py docs/
    python scripts/validate-links.py --json  # JSON output

Exit codes:
    0 - All links valid
    1 - Broken links found
"""

import json
import re
import sys
from pathlib import Path


# Link extraction pattern
MARKDOWN_LINK_PATTERN = r'\[([^\]]+)\]\(([^)]+)\)'


def extract_links(content):
    """Extract all markdown links from content.

    Args:
        content: Markdown file content

    Returns:
        List of tuples (link_text, link_url)
    """
    return re.findall(MARKDOWN_LINK_PATTERN, content)


def is_external_link(url):
    """Check if a URL is external (http, mailto, tel, javascript, etc.).

    Args:
        url: Link URL

    Returns:
        bool: True if external, False if internal
    """
    external_prefixes = ('http://', 'https://', 'mailto:', 'tel:', 'javascript:', 'ftp://')
    return url.startswith(external_prefixes)


def is_anchor_only(url):
    """Check if a URL is anchor-only (#section).

    Args:
        url: Link URL

    Returns:
        bool: True if anchor-only
    """
    return url == '#' or url.startswith('#')


def resolve_link_path(link_url, base_file_path, repo_root=None):
    """Resolve a link URL to an absolute path.

    Args:
        link_url: The link URL (may be relative or absolute from repo root)
        base_file_path: Path of the file containing the link
        repo_root: Repository root directory (default: current directory)

    Returns:
        Path object for the resolved link target
    """
    if repo_root is None:
        repo_root = Path.cwd()

    # Strip anchor from link
    link_file = link_url.split('#')[0]

    if not link_file:
        # Anchor-only link (valid within same file)
        return base_file_path

    # Get base directory of the file containing the link
    base_dir = base_file_path.parent

    if link_file.startswith('/'):
        # Absolute from repo root (remove leading /)
        resolved = repo_root / link_file[1:]
    else:
        # Relative path
        resolved = (base_dir / link_file).resolve()

    return resolved


def validate_file(file_path, repo_root=None):
    """Validate all links in a single markdown file.

    Args:
        file_path: Path to markdown file
        repo_root: Repository root directory

    Returns:
        dict with keys: file, total_links, broken_links (list of dicts)
    """
    if repo_root is None:
        repo_root = Path.cwd()

    try:
        content = file_path.read_text(encoding='utf-8')
    except (IOError, UnicodeDecodeError) as e:
        return {
            "file": str(file_path),
            "error": f"Could not read file: {e}",
            "total_links": 0,
            "broken_links": []
        }

    # Extract all links
    all_links = extract_links(content)

    # Filter to internal links only
    internal_links = [
        (text, url) for text, url in all_links
        if not is_external_link(url) and not is_anchor_only(url)
    ]

    # Validate each internal link
    broken_links = []

    for link_text, link_url in internal_links:
        resolved_path = resolve_link_path(link_url, file_path, repo_root)

        # Check if target exists (file or directory)
        if not resolved_path.exists():
            broken_links.append({
                "link_text": link_text,
                "link_url": link_url,
                "resolved_path": str(resolved_path),
                "reason": "Target does not exist"
            })

    return {
        "file": str(file_path),
        "total_links": len(internal_links),
        "broken_links": broken_links
    }


def find_markdown_files(search_path):
    """Find all markdown files in the given path.

    Args:
        search_path: File or directory path

    Returns:
        List of Path objects
    """
    path = Path(search_path)

    if path.is_file():
        return [path] if path.suffix == '.md' else []
    elif path.is_dir():
        return sorted(path.glob('**/*.md'))
    else:
        return []


def validate_links(search_path='.'):
    """Validate all links in markdown files.

    Args:
        search_path: Path to file or directory

    Returns:
        dict with keys: files_scanned, links_checked, broken_count, results (list)
    """
    repo_root = Path.cwd()
    markdown_files = find_markdown_files(search_path)

    results = []
    total_links = 0
    total_broken = 0

    for md_file in markdown_files:
        result = validate_file(md_file, repo_root)
        results.append(result)

        total_links += result.get("total_links", 0)
        total_broken += len(result.get("broken_links", []))

    return {
        "files_scanned": len(markdown_files),
        "links_checked": total_links,
        "broken_count": total_broken,
        "results": results
    }


def format_human_readable(data):
    """Format validation results as human-readable text.

    Args:
        data: Results from validate_links()

    Returns:
        str: Formatted output
    """
    output = []

    output.append("=" * 60)
    output.append("Link Validation Report")
    output.append("=" * 60)
    output.append(f"Files scanned: {data['files_scanned']}")
    output.append(f"Links checked: {data['links_checked']}")
    output.append("")

    # Show broken links
    if data['broken_count'] > 0:
        output.append(f"[FAIL] Broken links: {data['broken_count']}")
        output.append("")

        for result in data['results']:
            if result.get('broken_links'):
                output.append(f"[FAIL] {result['file']}")

                for broken in result['broken_links']:
                    output.append(f"   -> {broken['link_url']}")
                    output.append(f"      (resolved to: {broken['resolved_path']})")
                    output.append("")
    else:
        output.append("[PASS] Broken links: 0")

    output.append("")
    output.append("=" * 60)

    if data['broken_count'] == 0:
        output.append("[PASS] Status: PASS")
    else:
        output.append("[FAIL] Status: FAIL")

    output.append("")
    return "\n".join(output)


def main():
    """Main entry point."""
    # Parse arguments
    args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    output_json = '--json' in sys.argv

    # Get search path (default to current directory)
    search_path = args[0] if args else '.'

    # Validate links
    results = validate_links(search_path)

    # Output
    if output_json:
        print(json.dumps(results, indent=2))
    else:
        print(format_human_readable(results))

    # Exit with appropriate code
    sys.exit(0 if results['broken_count'] == 0 else 1)


if __name__ == "__main__":
    main()
