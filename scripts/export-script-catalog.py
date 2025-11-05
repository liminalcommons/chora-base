#!/usr/bin/env python3
"""
Export Script Catalog

Generates a machine-readable catalog of all automation scripts in scripts/
with metadata extracted from justfile and script headers.

Part of Phase 1.5: Curatorial Enhancements
SAP Integration: SAP-008 (automation-scripts)

Usage:
    python scripts/export-script-catalog.py                    # Export to scripts/script-catalog.json
    python scripts/export-script-catalog.py --output custom.json  # Custom output path
    python scripts/export-script-catalog.py --format yaml      # Export as YAML
"""

import json
import yaml
import os
import re
import glob
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone


def parse_justfile(justfile_path: str = "justfile") -> Dict[str, Dict[str, str]]:
    """
    Parse justfile to extract recipe metadata.

    Returns:
        Dict mapping recipe names to metadata:
        {
            "generate-sap": {
                "command": "python scripts/generate-sap.py {{SAP_ID}}",
                "description": "Generate SAP artifacts from catalog metadata",
                "params": ["SAP_ID"]
            }
        }
    """
    recipes = {}

    if not os.path.exists(justfile_path):
        print(f"Warning: {justfile_path} not found")
        return recipes

    with open(justfile_path, 'r') as f:
        content = f.read()

    # Regex to match recipe definitions
    # Pattern: # comment\nrecipe-name PARAMS:\n    command
    recipe_pattern = r'#\s*([^\n]+)\n(\w[\w-]*)\s*([^:]*?):\s*\n\s+(.+?)(?=\n\S|\n#|\Z)'

    for match in re.finditer(recipe_pattern, content, re.MULTILINE | re.DOTALL):
        description = match.group(1).strip()
        recipe_name = match.group(2).strip()
        params = match.group(3).strip()
        command = match.group(4).strip()

        # Parse parameters
        param_list = []
        if params:
            # Extract parameters like SAP_ID, PATH=".", etc.
            param_tokens = re.findall(r'(\w+)(?:="[^"]*")?', params)
            param_list = param_tokens

        recipes[recipe_name] = {
            "description": description,
            "command": command,
            "params": param_list
        }

    return recipes


def parse_script_header(script_path: str) -> Dict[str, Any]:
    """
    Parse script header docstring/comments to extract metadata.

    Looks for:
    - Purpose/description
    - SAP integration
    - Usage examples
    """
    metadata = {
        "description": "",
        "sap": None,
        "purpose": "",
        "usage": []
    }

    try:
        with open(script_path, 'r') as f:
            lines = f.readlines()

        # Look for docstring or comments in first 30 lines
        in_docstring = False
        docstring_lines = []

        for i, line in enumerate(lines[:30]):
            # Python docstring
            if '"""' in line or "'''" in line:
                in_docstring = not in_docstring
                if not in_docstring:
                    break
                continue

            if in_docstring:
                docstring_lines.append(line.strip())

            # Shell comment
            elif line.strip().startswith('#') and not line.strip().startswith('#!'):
                docstring_lines.append(line.strip().lstrip('#').strip())

        # Parse collected lines for metadata
        full_text = '\n'.join(docstring_lines)

        # Extract SAP reference
        sap_match = re.search(r'SAP[- ]?(\d{3})', full_text, re.IGNORECASE)
        if sap_match:
            metadata['sap'] = f"SAP-{sap_match.group(1)}"

        # Extract description (first line or "Purpose:" section)
        purpose_match = re.search(r'Purpose:?\s*([^\n]+)', full_text, re.IGNORECASE)
        if purpose_match:
            metadata['purpose'] = purpose_match.group(1).strip()
        elif docstring_lines:
            # Use first non-empty line as purpose
            for line in docstring_lines:
                if line and not line.startswith('=') and not line.startswith('-'):
                    metadata['purpose'] = line
                    break

        # Description is full docstring
        metadata['description'] = full_text.strip() if full_text.strip() else metadata['purpose']

    except Exception as e:
        print(f"Warning: Could not parse {script_path}: {e}")

    return metadata


def classify_script_safety(script_path: str, command: str = "") -> str:
    """
    Classify script safety level based on operations.

    Returns:
        "read_only" | "modifying" | "destructive"
    """
    script_name = os.path.basename(script_path).lower()
    combined_text = script_name + " " + command.lower()

    # Destructive patterns
    destructive_keywords = ['delete', 'remove', 'rm ', 'drop', 'destroy', 'purge', 'rollback', 'force']
    if any(kw in combined_text for kw in destructive_keywords):
        return "destructive"

    # Read-only patterns
    readonly_keywords = ['validate', 'check', 'analyze', 'query', 'status', 'list', 'show', 'export', 'inventory']
    if any(kw in combined_text for kw in readonly_keywords):
        return "read_only"

    # Default to modifying if creates/modifies files
    modifying_keywords = ['generate', 'create', 'install', 'update', 'merge', 'bump', 'propagate']
    if any(kw in combined_text for kw in modifying_keywords):
        return "modifying"

    return "read_only"  # Conservative default


def infer_affects_files(script_name: str, purpose: str, command: str) -> Dict[str, List[str]]:
    """
    Infer which files a script affects based on name and purpose.

    Returns:
        {
            "reads": [...],
            "modifies": [...],
            "creates": [...]
        }
    """
    affects = {
        "reads": [],
        "modifies": [],
        "creates": []
    }

    name_lower = script_name.lower()

    # SAP scripts
    if 'sap' in name_lower:
        affects['reads'].append('sap-catalog.json')
        if 'generate' in name_lower or 'create' in name_lower:
            affects['creates'].append('docs/skilled-awareness/**/*.md')
        if 'validate' in name_lower or 'evaluate' in name_lower:
            affects['reads'].append('docs/skilled-awareness/**/*.md')

    # Inbox scripts
    if 'inbox' in name_lower or 'coordination' in name_lower:
        affects['reads'].append('inbox/coordination/*.jsonl')
        if 'generate' in name_lower or 'respond' in name_lower:
            affects['modifies'].append('inbox/coordination/*.jsonl')

    # Version/release scripts
    if 'version' in name_lower or 'release' in name_lower:
        affects['modifies'].append('pyproject.toml')
        affects['modifies'].append('package.json')

    # Link validation
    if 'link' in name_lower or 'validate-links' in name_lower:
        affects['reads'].append('**/*.md')

    # Documentation scripts
    if 'doc' in name_lower or 'readme' in name_lower or 'index' in name_lower:
        affects['reads'].append('docs/**/*.md')
        if 'generate' in name_lower or 'merge' in name_lower:
            affects['modifies'].append('docs/**/*.md')

    return affects


def categorize_script(script_name: str, purpose: str) -> List[str]:
    """
    Categorize script by function.

    Categories:
    - setup: Initialization and configuration
    - development: Development workflow tools
    - validation: Validation and quality checks
    - generation: Code/content generation
    - release: Version management and releases
    - documentation: Documentation tools
    - sap: SAP-specific tools
    - inbox: Inbox coordination tools
    - mcp: MCP-related tools
    - migration: Migration and rollback tools
    """
    categories = []
    name_lower = script_name.lower()
    purpose_lower = purpose.lower()
    combined = name_lower + " " + purpose_lower

    if any(kw in combined for kw in ['validate', 'check', 'evaluate', 'analyze', 'quality']):
        categories.append('validation')

    if any(kw in combined for kw in ['generate', 'create']):
        categories.append('generation')

    if any(kw in combined for kw in ['sap-', 'sap_', 'sap ', 'skilled awareness']):
        categories.append('sap')

    if any(kw in combined for kw in ['inbox', 'coordination', 'coord']):
        categories.append('inbox')

    if any(kw in combined for kw in ['version', 'release', 'bump', 'publish']):
        categories.append('release')

    if any(kw in combined for kw in ['doc', 'readme', 'index', 'markdown']):
        categories.append('documentation')

    if any(kw in combined for kw in ['mcp', 'model context protocol']):
        categories.append('mcp')

    if any(kw in combined for kw in ['install', 'init', 'setup', 'config']):
        categories.append('setup')

    if any(kw in combined for kw in ['migrate', 'rollback', 'merge-upstream']):
        categories.append('migration')

    if any(kw in combined for kw in ['develop', 'workflow', 'automation']):
        categories.append('development')

    return categories if categories else ['other']


def export_script_catalog(output_path: str = "scripts/script-catalog.json", format: str = "json"):
    """
    Generate comprehensive script catalog.
    """
    scripts_dir = "scripts"
    justfile_recipes = parse_justfile()

    catalog = {
        "version": "1.0.0",
        "generated": datetime.now(timezone.utc).isoformat(),
        "total_scripts": 0,
        "scripts": []
    }

    # Find all scripts
    script_files = []
    for ext in ['*.py', '*.sh']:
        script_files.extend(glob.glob(f"{scripts_dir}/{ext}"))

    script_files = sorted(script_files)
    catalog["total_scripts"] = len(script_files)

    for script_path in script_files:
        script_name = os.path.basename(script_path)
        base_name = os.path.splitext(script_name)[0]

        # Parse script header
        header_metadata = parse_script_header(script_path)

        # Find matching justfile recipe
        # Try exact match, then fuzzy match (script-name.py -> script-name)
        justfile_recipe = None
        recipe_name = None

        # Try direct matches
        for recipe in justfile_recipes:
            if base_name.replace('_', '-') == recipe or base_name == recipe:
                justfile_recipe = justfile_recipes[recipe]
                recipe_name = recipe
                break

            # Check if recipe command references this script
            command = justfile_recipes[recipe].get('command', '')
            if script_name in command:
                justfile_recipe = justfile_recipes[recipe]
                recipe_name = recipe
                break

        # Build script metadata
        purpose = header_metadata.get('purpose', '')
        if not purpose and justfile_recipe:
            purpose = justfile_recipe.get('description', '')

        command = justfile_recipe.get('command', f"python {script_path}") if justfile_recipe else f"python {script_path}"
        if script_path.endswith('.sh'):
            command = justfile_recipe.get('command', f"bash {script_path}") if justfile_recipe else f"bash {script_path}"

        safety = classify_script_safety(script_path, command)
        affects_files = infer_affects_files(script_name, purpose, command)
        categories = categorize_script(script_name, purpose)

        script_entry = {
            "path": script_path,
            "name": script_name,
            "base_name": base_name,
            "purpose": purpose,
            "description": header_metadata.get('description', purpose),
            "sap": header_metadata.get('sap'),
            "justfile_recipe": recipe_name,
            "command": command,
            "params": justfile_recipe.get('params', []) if justfile_recipe else [],
            "safety": safety,
            "categories": categories,
            "affects_files": affects_files,
            "related_scripts": []  # TODO: Infer from common patterns
        }

        catalog["scripts"].append(script_entry)

    # Write catalog
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    if format == "json":
        with open(output_path, 'w') as f:
            json.dump(catalog, f, indent=2)
        print(f"✅ Script catalog exported to {output_path}")
        print(f"   Total scripts: {catalog['total_scripts']}")
    elif format == "yaml":
        output_path = output_path.replace('.json', '.yaml')
        with open(output_path, 'w') as f:
            yaml.dump(catalog, f, default_flow_style=False, sort_keys=False)
        print(f"✅ Script catalog exported to {output_path}")
        print(f"   Total scripts: {catalog['total_scripts']}")

    # Summary by category
    category_counts = {}
    for script in catalog["scripts"]:
        for cat in script["categories"]:
            category_counts[cat] = category_counts.get(cat, 0) + 1

    print(f"\n   Categories:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"     - {cat}: {count}")

    return catalog


def main():
    parser = argparse.ArgumentParser(description="Export script catalog with metadata")
    parser.add_argument(
        "--output",
        default="scripts/script-catalog.json",
        help="Output file path (default: scripts/script-catalog.json)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "yaml"],
        default="json",
        help="Output format (default: json)"
    )

    args = parser.parse_args()

    export_script_catalog(args.output, args.format)


if __name__ == "__main__":
    main()
