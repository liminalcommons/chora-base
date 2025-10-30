#!/usr/bin/env python3
"""merge-readme-md.py - Intelligent merge for README.md

Merge Strategy: template-variables

Updates structural README sections while preserving project-specific variables.

Usage:
  python scripts/merge-readme-md.py [--dry-run] [--output PATH]

Algorithm:
  1. Parse template variables from current README.md
  2. Get upstream README.md template
  3. Replace template placeholders with project values
  4. Preserve specified sections from current
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Install with: pip install PyYAML")
    sys.exit(1)

def load_config(chorabase_path: str = '.chorabase') -> dict:
    """Load .chorabase configuration for README.md"""
    if not Path(chorabase_path).exists():
        print(f"Error: {chorabase_path} not found")
        sys.exit(1)

    with open(chorabase_path, 'r') as f:
        config = yaml.safe_load(f)

    return config.get('hybrid', {}).get('README.md', {})

def extract_project_variables(readme_path: str, config: dict) -> Dict[str, str]:
    """Extract project-specific variables from current README.md

    Uses heuristics to find:
    - PROJECT_NAME: First # heading
    - PROJECT_DESCRIPTION: Text in first paragraph
    - REPOSITORY_URL: GitHub repo URL in badges or links
    """
    if not Path(readme_path).exists():
        return {}

    with open(readme_path, 'r') as f:
        content = f.read()

    variables = {}

    # Extract project name (first # heading)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        variables['PROJECT_NAME'] = title_match.group(1).strip()

    # Extract description (first paragraph after title)
    desc_match = re.search(
        r'^#\s+.+\n\n(.+?)(?:\n\n|\n#)',
        content,
        re.MULTILINE | re.DOTALL
    )
    if desc_match:
        # Clean up description (remove extra whitespace, badges)
        desc = desc_match.group(1).strip()
        # Remove badge lines
        desc = re.sub(r'\[!\[.*?\]\(.*?\)\]\(.*?\)', '', desc)
        desc = re.sub(r'\s+', ' ', desc).strip()
        variables['PROJECT_DESCRIPTION'] = desc

    # Extract repository URL
    repo_match = re.search(
        r'github\.com/([^/\s]+/[^/\s\)]+)',
        content
    )
    if repo_match:
        repo_path = repo_match.group(1)
        # Remove .git suffix if present
        repo_path = repo_path.replace('.git', '')
        variables['REPOSITORY_URL'] = f'https://github.com/{repo_path}'

    return variables

def get_upstream_readme() -> Optional[str]:
    """Get README.md content from upstream using git"""
    import subprocess

    try:
        # Try to read from upstream
        result = subprocess.run(
            ['git', 'show', 'chora-base/main:README.md'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        # Fallback: try static-template/README.md if it exists
        try:
            result = subprocess.run(
                ['git', 'show', 'chora-base/main:static-template/README.md'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return None

def apply_template_variables(template: str, variables: Dict[str, str]) -> str:
    """Replace {{ VARIABLE }} placeholders with values"""
    result = template

    for var_name, var_value in variables.items():
        # Replace {{ VAR_NAME }}
        placeholder = f'{{{{ {var_name} }}}}'
        result = result.replace(placeholder, var_value)

        # Also try without spaces
        placeholder_no_space = f'{{{{{var_name}}}}}'
        result = result.replace(placeholder_no_space, var_value)

    return result

def extract_sections(content: str) -> Dict[str, str]:
    """Extract sections from markdown content

    Returns: {section_title: section_content}
    """
    sections = {}
    current_section = None
    current_content = []

    # Pattern for section headers (##)
    header_pattern = re.compile(r'^##\s+(.+)$')

    for line in content.split('\n'):
        match = header_pattern.match(line)

        if match:
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content)

            # Start new section
            current_section = match.group(1).strip()
            current_content = [line]
        elif current_section:
            current_content.append(line)

    # Save last section
    if current_section:
        sections[current_section] = '\n'.join(current_content)

    return sections

def merge_with_preserved_sections(
    upstream_content: str,
    current_readme_path: str,
    preserve_sections: list
) -> str:
    """Merge upstream with preserved sections from current"""

    if not Path(current_readme_path).exists():
        return upstream_content

    with open(current_readme_path, 'r') as f:
        current_content = f.read()

    # Extract sections
    upstream_sections = extract_sections(upstream_content)
    current_sections = extract_sections(current_content)

    # Replace preserved sections with current versions
    for section_title in preserve_sections:
        if section_title in current_sections:
            upstream_sections[section_title] = current_sections[section_title]

    # Reconstruct content maintaining upstream section order
    result_lines = []

    # Add preamble (content before first ##)
    preamble = upstream_content.split('\n## ')[0]
    result_lines.append(preamble)

    # Add sections
    for section_title, section_content in upstream_sections.items():
        if not section_content.startswith('##'):
            result_lines.append(f'\n## {section_title}')
            result_lines.append(section_content.split('\n', 1)[1] if '\n' in section_content else '')
        else:
            result_lines.append('\n' + section_content)

    return '\n'.join(result_lines)

def write_merged_file(content: str, output_path: str, dry_run: bool) -> None:
    """Write merged content to file"""
    if dry_run:
        print("=" * 70)
        print("DRY RUN - Would write merged content:")
        print("=" * 70)
        print(content[:1500])  # Show first 1500 chars
        if len(content) > 1500:
            print(f"\n... ({len(content) - 1500} more characters)")
        print("=" * 70)
    else:
        with open(output_path, 'w') as f:
            f.write(content)
        print(f"✓ Merged README.md written to: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Intelligent merge for README.md using template-variables strategy",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show merge preview without writing file'
    )
    parser.add_argument(
        '--output',
        default='README.md',
        help='Output file path (default: README.md)'
    )
    parser.add_argument(
        '--current',
        default='README.md',
        help='Current README.md file (default: README.md)'
    )
    parser.add_argument(
        '--chorabase',
        default='.chorabase',
        help='Path to .chorabase config (default: .chorabase)'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("README.md Template-Variables Merge")
    print("=" * 70)
    print()

    # Load config
    config = load_config(args.chorabase)
    if not config:
        print("Error: No README.md configuration found in .chorabase")
        sys.exit(1)

    template_vars = config.get('template_variables', {})
    preserve_sections = config.get('preserve_sections', [])

    print(f"✓ Loaded merge configuration from {args.chorabase}")
    print(f"  - Template variables: {', '.join(template_vars.keys())}")
    print(f"  - Preserve sections: {', '.join(preserve_sections)}")
    print()

    # Extract project variables from current README
    print(f"Extracting variables from {args.current}...")
    project_vars = extract_project_variables(args.current, config)
    print(f"✓ Extracted {len(project_vars)} variables:")
    for var_name, var_value in project_vars.items():
        display_value = var_value[:50] + '...' if len(var_value) > 50 else var_value
        print(f"  - {var_name}: {display_value}")
    print()

    # Get upstream README template
    print("Fetching upstream README.md template...")
    upstream_template = get_upstream_readme()

    if not upstream_template:
        print("⚠ Warning: Could not fetch upstream README.md")
        print("  Cannot perform merge without upstream template")
        sys.exit(1)

    print("✓ Fetched upstream README.md template")
    print()

    # Apply template variables
    print("Applying template variables...")
    merged_content = apply_template_variables(upstream_template, project_vars)
    print("✓ Template variables applied")
    print()

    # Merge with preserved sections
    if preserve_sections:
        print("Preserving sections from current README...")
        merged_content = merge_with_preserved_sections(
            merged_content,
            args.current,
            preserve_sections
        )
        print(f"✓ Preserved {len(preserve_sections)} sections from current")
        print()

    # Write output
    write_merged_file(merged_content, args.output, args.dry_run)

    if not args.dry_run:
        print()
        print("Next steps:")
        print("  1. Review merged README.md")
        print("  2. Make any manual adjustments needed")
        print("  3. Commit: git add README.md && git commit -m 'docs: Merge README.md from upstream'")

if __name__ == '__main__':
    main()
