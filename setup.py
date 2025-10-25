#!/usr/bin/env python3
"""
Chora-Base v3.0.0 Setup Script

Optional CLI helper for setting up chora-base projects.
AI agents should read AGENT_SETUP_GUIDE.md instead.

Usage:
    python setup.py [target_directory]

Example:
    python setup.py my-mcp-server
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional


def print_header():
    """Print welcome message."""
    print("=" * 60)
    print("Chora-Base v3.0.0 Setup")
    print("=" * 60)
    print()


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_semver(version: str) -> bool:
    """Validate semantic version format."""
    pattern = r'^\d+\.\d+\.\d+$'
    return bool(re.match(pattern, version))


def validate_slug(slug: str) -> bool:
    """Validate project slug format."""
    pattern = r'^[a-z][a-z0-9-]+$'
    return bool(re.match(pattern, slug))


def validate_package_name(name: str) -> bool:
    """Validate Python package name."""
    pattern = r'^[a-z][a-z0-9_]+$'
    return bool(re.match(pattern, name))


def get_git_config(key: str) -> Optional[str]:
    """Get git config value."""
    try:
        result = subprocess.run(
            ['git', 'config', '--get', key],
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except FileNotFoundError:
        return None


def derive_slug(project_name: str) -> str:
    """Derive project slug from project name."""
    slug = project_name.lower()
    slug = slug.replace(' ', '-').replace('_', '-')
    return slug


def derive_package_name(project_slug: str) -> str:
    """Derive package name from project slug."""
    return project_slug.replace('-', '_')


def derive_namespace(package_name: str) -> str:
    """Derive MCP namespace from package name."""
    return package_name.replace('_', '')


def gather_variables() -> Dict[str, str]:
    """Gather all required variables from user."""
    print("Project Configuration")
    print("-" * 60)
    print()

    variables = {}

    # Project name
    while True:
        project_name = input("Project name (e.g., 'MCP GitHub'): ").strip()
        if project_name:
            variables['project_name'] = project_name
            break
        print("  Error: Project name cannot be empty")

    # Auto-derive slug and package name
    project_slug = derive_slug(project_name)
    package_name = derive_package_name(project_slug)
    mcp_namespace = derive_namespace(package_name)

    print(f"\nDerived values:")
    print(f"  Project slug: {project_slug}")
    print(f"  Package name: {package_name}")
    print(f"  MCP namespace: {mcp_namespace}")

    # Ask if user wants to change derived values
    if input("\nUse these derived values? [Y/n]: ").lower() in ('', 'y', 'yes'):
        variables['project_slug'] = project_slug
        variables['package_name'] = package_name
        variables['mcp_namespace'] = mcp_namespace
    else:
        # Let user override
        while True:
            slug = input(f"Project slug [{project_slug}]: ").strip() or project_slug
            if validate_slug(slug):
                variables['project_slug'] = slug
                break
            print("  Error: Invalid slug (must start with lowercase letter, use hyphens)")

        pkg = derive_package_name(variables['project_slug'])
        while True:
            package = input(f"Package name [{pkg}]: ").strip() or pkg
            if validate_package_name(package):
                variables['package_name'] = package
                break
            print("  Error: Invalid package name (must be valid Python identifier)")

        ns = derive_namespace(variables['package_name'])
        variables['mcp_namespace'] = input(f"MCP namespace [{ns}]: ").strip() or ns

    print()

    # Project description
    variables['project_description'] = input("Project description: ").strip()

    # Author info
    default_author = get_git_config('user.name') or 'Your Name'
    default_email = get_git_config('user.email') or 'your.email@example.com'

    variables['author_name'] = input(f"Author name [{default_author}]: ").strip() or default_author

    while True:
        email = input(f"Author email [{default_email}]: ").strip() or default_email
        if validate_email(email):
            variables['author_email'] = email
            break
        print("  Error: Invalid email address")

    # GitHub username
    default_github = variables['author_name'].lower().replace(' ', '-')
    variables['github_username'] = input(f"GitHub username [{default_github}]: ").strip() or default_github

    # Python version
    variables['python_version'] = input("Python version [3.11]: ").strip() or "3.11"

    # Project version
    while True:
        version = input("Initial version [0.1.0]: ").strip() or "0.1.0"
        if validate_semver(version):
            variables['project_version'] = version
            break
        print("  Error: Invalid version (must be X.Y.Z)")

    # License
    variables['license'] = input("License [MIT]: ").strip() or "MIT"

    print()
    return variables


def copy_static_template(target_dir: Path):
    """Copy all static-template files to target directory."""
    static_template = Path(__file__).parent / "static-template"

    if not static_template.exists():
        print(f"Error: static-template/ not found at {static_template}")
        sys.exit(1)

    print(f"Copying static template to {target_dir}...")

    # Copy entire directory
    shutil.copytree(static_template, target_dir, dirs_exist_ok=True)

    print("✓ Copied static template")


def rename_package_directories(target_dir: Path, package_name: str):
    """Rename __package_name__ directories to actual package name."""
    placeholder = "__package_name__"

    # Find all __package_name__ directories
    for root, dirs, files in os.walk(target_dir):
        if placeholder in dirs:
            old_path = Path(root) / placeholder
            new_path = Path(root) / package_name

            print(f"Renaming {old_path.relative_to(target_dir)} → {new_path.relative_to(target_dir)}")
            shutil.move(str(old_path), str(new_path))

    print("✓ Renamed package directories")


def process_blueprints(target_dir: Path, variables: Dict[str, str]):
    """Process blueprint files with variable substitution."""
    blueprint_dir = Path(__file__).parent / "blueprints"

    if not blueprint_dir.exists():
        print(f"Error: blueprints/ not found at {blueprint_dir}")
        sys.exit(1)

    print("Processing blueprints...")

    # Blueprint file mappings (blueprint name -> target path)
    blueprint_mappings = {
        'pyproject.toml.blueprint': 'pyproject.toml',
        'README.md.blueprint': 'README.md',
        'AGENTS.md.blueprint': 'AGENTS.md',
        'CHANGELOG.md.blueprint': 'CHANGELOG.md',
        'ROADMAP.md.blueprint': 'ROADMAP.md',
        '.gitignore.blueprint': '.gitignore',
        '.env.example.blueprint': '.env.example',
        'package__init__.py.blueprint': f'src/{variables["package_name"]}/__init__.py',
        'server.py.blueprint': f'src/{variables["package_name"]}/mcp/server.py',
        'mcp__init__.py.blueprint': f'src/{variables["package_name"]}/mcp/__init__.py',
    }

    for blueprint_file, target_path in blueprint_mappings.items():
        blueprint = blueprint_dir / blueprint_file

        if not blueprint.exists():
            print(f"  Warning: Blueprint not found: {blueprint_file}")
            continue

        # Read blueprint
        content = blueprint.read_text()

        # Replace all variables (handle both {{ var }} and {{var}} formats)
        for var_name, var_value in variables.items():
            # With spaces (Jinja2 style)
            placeholder_spaces = f"{{{{ {var_name} }}}}"
            content = content.replace(placeholder_spaces, var_value)

            # Without spaces
            placeholder_no_spaces = f"{{{{{var_name}}}}}"
            content = content.replace(placeholder_no_spaces, var_value)

        # Check for unreplaced placeholders
        if "{{" in content and not content.startswith("#!"):  # Allow shebangs
            remaining = re.findall(r'\{\{(\w+)\}\}', content)
            print(f"  Warning: Unreplaced placeholders in {target_path}: {remaining}")

        # Write to target
        output_path = target_dir / target_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)

        print(f"  ✓ {target_path}")

    print("✓ Processed blueprints")


def initialize_git(target_dir: Path, variables: Dict[str, str]):
    """Initialize git repository if not exists."""
    git_dir = target_dir / ".git"

    if git_dir.exists():
        print("Git repository already exists, adding files...")
        subprocess.run(['git', 'add', '.'], cwd=target_dir, check=True)
        subprocess.run([
            'git', 'commit', '-m',
            f'Apply chora-base v3.0.0 template\n\nProject: {variables["project_name"]}'
        ], cwd=target_dir, check=False)
    else:
        print("Initializing git repository...")
        subprocess.run(['git', 'init'], cwd=target_dir, check=True)
        subprocess.run(['git', 'add', '.'], cwd=target_dir, check=True)
        subprocess.run([
            'git', 'commit', '-m',
            f'Initial commit from chora-base v3.0.0\n\n' +
            f'Project: {variables["project_name"]}\n' +
            f'Package: {variables["package_name"]}\n' +
            f'Template: https://github.com/liminalcommons/chora-base'
        ], cwd=target_dir, check=True)

    print("✓ Initialized git repository")


def validate_setup(target_dir: Path, package_name: str) -> bool:
    """Validate the generated project."""
    print("\nValidating setup...")

    # Check critical files
    required_files = [
        'pyproject.toml',
        'README.md',
        'AGENTS.md',
        f'src/{package_name}/__init__.py',
        f'src/{package_name}/mcp/server.py',
        f'src/{package_name}/memory/event_log.py',
        f'src/{package_name}/utils/validation.py',
    ]

    all_good = True
    for file in required_files:
        path = target_dir / file
        if path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ Missing: {file}")
            all_good = False

    # Check for unreplaced placeholders in key files
    key_files = ['pyproject.toml', 'README.md', f'src/{package_name}/mcp/server.py']
    for file in key_files:
        path = target_dir / file
        if path.exists():
            content = path.read_text()
            if "{{" in content:
                print(f"  ⚠ Unreplaced placeholders in {file}")
                all_good = False

    if all_good:
        print("\n✅ Validation passed!")
    else:
        print("\n⚠ Validation found issues (see above)")

    return all_good


def main():
    """Main setup procedure."""
    print_header()

    # Get target directory
    if len(sys.argv) > 1:
        target_dir = Path(sys.argv[1])
    else:
        target_dir_name = input("Target directory name: ").strip()
        if not target_dir_name:
            print("Error: Target directory required")
            sys.exit(1)
        target_dir = Path(target_dir_name)

    # Check if directory exists
    if target_dir.exists() and any(target_dir.iterdir()):
        print(f"\nWarning: Directory {target_dir} is not empty!")
        if input("Continue anyway? [y/N]: ").lower() not in ('y', 'yes'):
            print("Aborted.")
            sys.exit(0)

    # Create target directory
    target_dir.mkdir(parents=True, exist_ok=True)

    print()

    # Gather variables
    variables = gather_variables()

    # Confirm
    print("Summary:")
    print("-" * 60)
    for key, value in sorted(variables.items()):
        print(f"  {key}: {value}")
    print()

    if input("Proceed with setup? [Y/n]: ").lower() not in ('', 'y', 'yes'):
        print("Aborted.")
        sys.exit(0)

    print()
    print("=" * 60)
    print("Setting up project...")
    print("=" * 60)
    print()

    try:
        # Step 1: Copy static template
        copy_static_template(target_dir)

        # Step 2: Rename package directories
        rename_package_directories(target_dir, variables['package_name'])

        # Step 3: Process blueprints
        process_blueprints(target_dir, variables)

        # Step 4: Initialize git
        initialize_git(target_dir, variables)

        # Step 5: Validate
        validate_setup(target_dir, variables['package_name'])

        print()
        print("=" * 60)
        print("✅ Setup complete!")
        print("=" * 60)
        print()
        print(f"Project: {variables['project_name']}")
        print(f"Location: {target_dir.absolute()}")
        print()
        print("Next steps:")
        print(f"  1. cd {target_dir}")
        print("  2. Run tests: pytest")
        print("  3. Start dev server: ./scripts/dev-server.sh")
        print(f"  4. Implement your MCP server in src/{variables['package_name']}/mcp/server.py")
        print()

    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
