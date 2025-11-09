#!/usr/bin/env python3
"""Test script for rendering SAP templates with test data."""

import json
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/render-template-test.py <template_name> <test_data_file>")
        print("Example: python scripts/render-template-test.py capability-charter.j2 test-data/sap-028-test.json")
        sys.exit(1)

    template_name = sys.argv[1]
    test_data_file = sys.argv[2]

    # Load test data
    with open(test_data_file, encoding='utf-8') as f:
        data = json.load(f)

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates/sap'))
    template = env.get_template(template_name)

    # Render template
    output = template.render(**data)

    # Print to stdout (with UTF-8 encoding for Windows compatibility)
    sys.stdout.reconfigure(encoding='utf-8')
    print(output)

if __name__ == '__main__':
    main()
