#!/usr/bin/env python3
"""Test script for rendering MCP script templates with test data.

Tests the GAP-003 Track 2 script templates:
- bump-version.py.template
- create-release.py.template
- justfile.template
"""

import json
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def main():
    # Configure UTF-8 output for Windows
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    # Load test data
    test_data_file = Path("test-data/mcp-test-project.json")
    if not test_data_file.exists():
        print(f"Error: Test data file not found: {test_data_file}")
        sys.exit(1)

    with open(test_data_file, encoding='utf-8') as f:
        data = json.load(f)

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('static-template/mcp-templates'))

    # Test templates
    templates_to_test = [
        'bump-version.py.template',
        'create-release.py.template',
        'justfile.template'
    ]

    print("=" * 80)
    print("Testing GAP-003 Track 2 Script Template Rendering")
    print("=" * 80)
    print()

    output_dir = Path(".test_target")
    output_dir.mkdir(exist_ok=True)

    for template_name in templates_to_test:
        print(f"Testing: {template_name}")
        try:
            template = env.get_template(template_name)
            output = template.render(**data)

            # Write to output file
            output_file = output_dir / template_name.replace('.template', '')
            output_file.write_text(output, encoding='utf-8')

            # Check for template variables that weren't substituted
            if '{{' in output or '}}' in output:
                print(f"  ⚠️  Warning: Unsubstituted template variables found")
                # Count occurrences
                count = output.count('{{')
                print(f"     Found {count} unsubstituted variables")
            else:
                print(f"  ✅ Successfully rendered ({len(output)} characters)")

            print(f"     Output: {output_file}")

        except Exception as e:
            print(f"  ❌ Error: {e}")
            sys.exit(1)

        print()

    print("=" * 80)
    print("Integration Test Summary")
    print("=" * 80)
    print()
    print("✅ All templates rendered successfully")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print()
    print("Next steps:")
    print("  1. Review rendered files in .test_target/")
    print("  2. Check for syntax errors: python -m py_compile .test_target/*.py")
    print("  3. Validate justfile syntax: cd .test_target && just --list")
    print()

if __name__ == '__main__':
    main()
