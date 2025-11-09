#!/usr/bin/env python3
"""Platform information utility for cross-platform development.

Reports OS, Python version, architecture, PATH, and tool availability.
Useful for debugging platform-specific issues and validating setup.

Usage:
    python scripts/platform-info.py
    python scripts/platform-info.py --json  # Output as JSON
"""

import json
import os
import platform
import shutil
import sys
from pathlib import Path


def is_wsl():
    """Detect if running in Windows Subsystem for Linux."""
    if platform.system() != "Linux":
        return False
    try:
        with open("/proc/version", "r", encoding='utf-8') as f:
            return "microsoft" in f.read().lower()
    except FileNotFoundError:
        return False


def check_tool_availability():
    """Check availability of common development tools."""
    tools = {
        "python": sys.executable,
        "git": shutil.which("git"),
        "just": shutil.which("just"),
        "docker": shutil.which("docker"),
        "node": shutil.which("node"),
        "npm": shutil.which("npm"),
    }
    return {name: path is not None for name, path in tools.items()}


def get_platform_info():
    """Gather comprehensive platform information."""
    info = {
        "os": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor() or "unknown",
            "is_wsl": is_wsl(),
        },
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "compiler": platform.python_compiler(),
            "executable": sys.executable,
            "prefix": sys.prefix,
            "base_prefix": sys.base_prefix,
            "in_venv": sys.prefix != sys.base_prefix,
        },
        "environment": {
            "cwd": str(Path.cwd()),
            "home": os.environ.get("HOME") or os.environ.get("USERPROFILE", "unknown"),
            "path_separator": os.pathsep,
            "file_separator": os.sep,
            "encoding": sys.getdefaultencoding(),
            "filesystem_encoding": sys.getfilesystemencoding(),
        },
        "tools": check_tool_availability(),
    }

    # Add Windows-specific info
    if platform.system() == "Windows":
        info["windows"] = {
            "wsl_available": shutil.which("wsl") is not None,
            "powershell_version": platform.win32_ver()[0] if hasattr(platform, 'win32_ver') else "unknown",
        }

    # Add macOS-specific info
    if platform.system() == "Darwin":
        info["macos"] = {
            "version": platform.mac_ver()[0],
        }

    return info


def format_human_readable(info):
    """Format platform info as human-readable text."""
    output = []
    output.append("=" * 60)
    output.append("Platform Information")
    output.append("=" * 60)
    output.append("")

    # OS Information
    output.append("Operating System:")
    output.append(f"  System:     {info['os']['system']}")
    output.append(f"  Release:    {info['os']['release']}")
    output.append(f"  Machine:    {info['os']['machine']}")
    output.append(f"  Processor:  {info['os']['processor']}")
    if info['os']['is_wsl']:
        output.append(f"  WSL:        Yes (Windows Subsystem for Linux)")
    output.append("")

    # Python Information
    output.append("Python:")
    output.append(f"  Version:    {info['python']['version']}")
    output.append(f"  Implementation: {info['python']['implementation']}")
    output.append(f"  Executable: {info['python']['executable']}")
    output.append(f"  Virtual Env: {'Yes' if info['python']['in_venv'] else 'No'}")
    if info['python']['in_venv']:
        output.append(f"  Venv Path:  {info['python']['prefix']}")
    output.append("")

    # Environment
    output.append("Environment:")
    output.append(f"  Working Dir: {info['environment']['cwd']}")
    output.append(f"  Home Dir:    {info['environment']['home']}")
    output.append(f"  Path Sep:    '{info['environment']['path_separator']}'")
    output.append(f"  File Sep:    '{info['environment']['file_separator']}'")
    output.append(f"  Encoding:    {info['environment']['encoding']}")
    output.append(f"  FS Encoding: {info['environment']['filesystem_encoding']}")
    output.append("")

    # Tool Availability (use ASCII-compatible characters for Windows compatibility)
    output.append("Tool Availability:")
    for tool, available in info['tools'].items():
        status = "[YES]" if available else "[NO ]"
        output.append(f"  {status} {tool}")
    output.append("")

    # Platform-specific info
    if "windows" in info:
        output.append("Windows-Specific:")
        output.append(f"  WSL Available: {'Yes' if info['windows']['wsl_available'] else 'No'}")
        output.append("")

    if "macos" in info:
        output.append("macOS-Specific:")
        output.append(f"  Version: {info['macos']['version']}")
        output.append("")

    output.append("=" * 60)

    return "\n".join(output)


def main():
    """Main entry point."""
    # Check if --json flag is provided
    output_json = "--json" in sys.argv

    # Gather platform information
    info = get_platform_info()

    # Output in requested format
    if output_json:
        print(json.dumps(info, indent=2))
    else:
        print(format_human_readable(info))


if __name__ == "__main__":
    main()
