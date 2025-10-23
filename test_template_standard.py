#!/usr/bin/env python3
"""Test NAMESPACES.md.jinja with standard Jinja2 delimiters."""

from jinja2 import Environment
from datetime import datetime

# Custom strftime filter
def strftime_filter(value, fmt):
    """Format datetime or string 'now' as date."""
    if value == "now":
        return datetime.now().strftime(fmt)
    return value

# Create environment with STANDARD delimiters ({{ }}, {% %})
env = Environment(
    variable_start_string="{{",
    variable_end_string="}}",
    block_start_string="{%",
    block_end_string="%}",
    comment_start_string="{#",
    comment_end_string="#}",
    keep_trailing_newline=True,
    trim_blocks=True,
    lstrip_blocks=True,
)

# Add strftime filter
env.filters['strftime'] = strftime_filter

# Test data
test_data = {
    "project_name": "Test Project",
    "project_slug": "test-project",
    "package_name": "test_project",
    "mcp_namespace": "testproject",
    "mcp_enable_namespacing": True,
    "mcp_validate_names": True,
}

# Read and render the problematic template
try:
    with open("template/NAMESPACES.md.jinja") as f:
        template = env.from_string(f.read())

    result = template.render(**test_data)

    print("✓ NAMESPACES.md.jinja syntax is VALID with standard delimiters!")
    print("✓ Template RENDERS successfully!")
    print(f"  Rendered {len(result)} characters")
    print()
    print("First 500 characters of output:")
    print("-" * 60)
    print(result[:500])
    print("-" * 60)

except Exception as e:
    print(f"✗ FAILED: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
