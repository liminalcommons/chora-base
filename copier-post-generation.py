#!/usr/bin/env python3
"""
Copier Post-Generation Hook

Runs after template generation to:
1. Initialize directory structure
2. Set up git repository (if enabled)
3. Display next steps

Author: Claude (Anthropic)
Created: 2025-11-21
Template: chora-base v1.0.0
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, cwd: Path = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run shell command and return result."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"Output: {e.stderr}")
        if check:
            raise
        return e


def create_directories(project_dir: Path, config: dict):
    """Create required directories based on enabled SAPs."""
    directories = []

    # SAP-001: Inbox Workflow
    if config.get('_sap_001_enabled'):
        directories.extend([
            'inbox/incoming/coordination',
            'inbox/incoming/tasks',
            'inbox/incoming/context',
            'inbox/active',
            'inbox/completed',
        ])

    # SAP-010: Memory System
    if config.get('_sap_010_enabled'):
        directories.extend([
            '.chora/memory/events',
            '.chora/memory/knowledge/notes',
            '.chora/memory/profiles',
            '.chora/memory/queries',
        ])

    # SAP-008: Automation Dashboard
    if config.get('_sap_008_enabled'):
        directories.append('logs')

    # Create all directories
    for directory in directories:
        dir_path = project_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)

    return len(directories)


def initialize_git(project_dir: Path):
    """Initialize git repository."""
    try:
        # Initialize git
        run_command(['git', 'init'], cwd=project_dir)

        # Add all files
        run_command(['git', 'add', '.'], cwd=project_dir)

        # Initial commit
        run_command([
            'git', 'commit', '-m',
            'Initial commit from chora-base template\n\n🤖 Generated with chora-base'
        ], cwd=project_dir)

        return True
    except subprocess.CalledProcessError:
        return False


def fix_copier_src_path(project_dir: Path):
    """
    Fix _src_path in .copier-answers.yml if it points to temp directory.

    Copier clones templates to temp directories, which breaks 'copier update'.
    This function detects temp paths and replaces them with the GitHub URL.
    """
    answers_file = project_dir / '.copier-answers.yml'
    if not answers_file.exists():
        return False

    # Read current content
    with open(answers_file, 'r') as f:
        content = f.read()

    # Check if _src_path points to temp directory
    if '/T/copier' in content or '/tmp/copier' in content or '/var/folders' in content:
        # Replace with GitHub URL
        import re
        # Look for _src_path line with temp directory
        pattern = r'(_src_path:\s+)(/[^\n]+(?:tmp|T)/copier[^\n]*)'
        replacement = r'\1https://github.com/liminalcommons/chora-base.git'
        new_content = re.sub(pattern, replacement, content)

        if new_content != content:
            # Write back
            with open(answers_file, 'w') as f:
                f.write(new_content)
            return True

    return False


def make_scripts_executable(project_dir: Path):
    """Make shell scripts executable."""
    script_files = [
        'scripts/pre-push-check.sh',
    ]

    for script in script_files:
        script_path = project_dir / script
        if script_path.exists():
            os.chmod(script_path, 0o755)


def display_next_steps(config: dict):
    """Display post-generation next steps."""
    print("\n" + "=" * 70)
    print("✅ PROJECT GENERATED SUCCESSFULLY")
    print("=" * 70)
    print(f"\nProject: {config.get('project_name', 'Unknown')}")
    print(f"Location: {Path.cwd()}")
    print(f"SAPs enabled: {config.get('_sap_count', 0)}")
    print("")

    print("📋 NEXT STEPS:")
    print("")

    step = 1

    # Step: Install dependencies
    if config.get('use_poetry'):
        print(f"{step}. Install dependencies:")
        print("   poetry install")
        print("   poetry shell")
        step += 1
    elif config.get('use_python'):
        print(f"{step}. Install dependencies:")
        print(f"   python{config.get('python_version', '3.11')} -m venv venv")
        print("   source venv/bin/activate  # macOS/Linux")
        print("   # venv\\Scripts\\activate   # Windows")
        print("   pip install -r requirements.txt")
        step += 1

    # Step: Verify installation
    print(f"{step}. Verify installation:")
    print("   just --list")
    print("   just status")
    step += 1

    # Step: Initialize git (if not already done)
    if config.get('use_git'):
        print(f"{step}. Git repository initialized ✅")
        step += 1

    # Step: SAP-specific setup
    if config.get('_sap_015_enabled'):
        print(f"{step}. Set up Beads task management:")
        print("   bd list  # Verify Beads CLI installed")
        step += 1

    if config.get('_sap_001_enabled'):
        print(f"{step}. Check inbox status:")
        print("   just inbox-status")
        step += 1

    if config.get('_sap_051_enabled'):
        print(f"{step}. Install pre-push hook (optional):")
        print("   just pre-push-install")
        step += 1

    # Step: Read documentation
    print(f"{step}. Read documentation:")
    print("   - README.md for project overview")
    print("   - docs/GETTING-STARTED.md for detailed setup")
    if config.get('_sap_010_enabled'):
        print("   - .chora/CLAUDE.md for Claude-specific guidance")
    step += 1

    print("")
    print("=" * 70)
    print("🚀 Happy coding!")
    print("=" * 70)
    print("")


def main():
    """Main post-generation hook."""
    # Get project directory (current working directory after generation)
    project_dir = Path.cwd()

    # Load copier answers to determine configuration
    answers_file = project_dir / '.copier-answers.yml'
    if not answers_file.exists():
        print("Warning: .copier-answers.yml not found, skipping post-generation setup")
        sys.exit(0)

    # Parse YAML (simple parsing, no pyyaml dependency in hook)
    config = {}
    with open(answers_file, 'r') as f:
        for line in f:
            if ':' in line and not line.strip().startswith('#'):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                # Convert boolean strings
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                # Strip quotes
                elif value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                # Convert numbers
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                config[key] = value

    print("\n🔧 Running post-generation setup...\n")

    # Step 1: Fix copier _src_path (must run before git init to avoid dirty repo)
    if fix_copier_src_path(project_dir):
        print("✅ Fixed _src_path for copier update support")

    # Step 2: Create directories
    num_dirs = create_directories(project_dir, config)
    print(f"✅ Created {num_dirs} directories")

    # Step 3: Make scripts executable
    make_scripts_executable(project_dir)
    print("✅ Made scripts executable")

    # Step 4: Initialize git (if enabled and not already initialized)
    if config.get('use_git') and not (project_dir / '.git').exists():
        if initialize_git(project_dir):
            print("✅ Initialized git repository")
        else:
            print("⚠️  Failed to initialize git repository (non-blocking)")

    # Step 5: Display next steps
    display_next_steps(config)


if __name__ == '__main__':
    main()
