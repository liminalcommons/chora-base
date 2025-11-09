#!/usr/bin/env python3
"""[SCRIPT_NAME] - [Brief description]

[Detailed description of what this script does]

Usage:
    python scripts/[script-name].py --arg value
    python scripts/[script-name].py --help

Examples:
    # Example 1
    python scripts/[script-name].py --output ./results

    # Example 2
    python scripts/[script-name].py --input data.json --format csv

Exit codes:
    0 - Success
    1 - Error
    2 - Invalid usage
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

# Configure UTF-8 output for Windows console compatibility
# CRITICAL: Required for any script that uses emojis or Unicode characters
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

VERSION = "1.0.0"


def load_config(config_path: Path) -> dict:
    """Load configuration from JSON file

    Args:
        config_path: Path to config file

    Returns:
        dict: Configuration data

    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file is invalid JSON
    """
    # CRITICAL: Always use encoding='utf-8' for file I/O
    # Windows defaults to cp1252 which causes silent corruption
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_results(output_path: Path, data: dict) -> None:
    """Save results to JSON file

    Args:
        output_path: Path to output file
        data: Data to save
    """
    # Ensure parent directory exists (cross-platform)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # CRITICAL: Always use encoding='utf-8' for file I/O
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_home_directory() -> Path:
    """Get user home directory (cross-platform)

    Returns:
        Path: User home directory

    Example:
        Unix/Mac: /home/username or /Users/username
        Windows: C:\\Users\\username
    """
    # GOOD: pathlib handles Windows/Mac/Linux differences
    return Path.home()

    # BAD: Don't hardcode paths
    # return Path("~/")  # Doesn't expand on Windows
    # return Path("/home/user")  # Unix-only


def build_file_path(base_dir: Path, *parts: str) -> Path:
    """Build file path (cross-platform)

    Args:
        base_dir: Base directory
        *parts: Path components

    Returns:
        Path: Complete file path

    Example:
        Unix/Mac: /base/subdir/file.txt
        Windows: C:\\base\\subdir\\file.txt
    """
    # GOOD: Use pathlib's / operator (cross-platform)
    result = base_dir
    for part in parts:
        result = result / part
    return result

    # BAD: Don't concatenate strings with /
    # return Path(f"{base_dir}/{parts[0]}/{parts[1]}")  # Unix-only!


def main() -> int:
    """Main entry point

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    parser = argparse.ArgumentParser(
        description="[Script description]",
        epilog="See docs/[documentation].md for detailed usage"
    )

    # GOOD: Use type=Path for path arguments (not str)
    parser.add_argument(
        '--output',
        type=Path,
        required=True,
        help='Output directory for results'
    )

    parser.add_argument(
        '--input',
        type=Path,
        help='Input file to process'
    )

    parser.add_argument(
        '--format',
        choices=['json', 'csv', 'yaml'],
        default='json',
        help='Output format (default: json)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {VERSION}'
    )

    args = parser.parse_args()

    # Verbose logging example
    if args.verbose:
        print(f"🔍 Running {Path(__file__).name} v{VERSION}")
        print(f"   Output: {args.output}")
        print(f"   Format: {args.format}")

    try:
        # Example: Load input file if provided
        if args.input:
            if not args.input.exists():
                print(f"❌ Error: Input file not found: {args.input}", file=sys.stderr)
                return 1

            data = load_config(args.input)
            if args.verbose:
                print(f"✅ Loaded {len(data)} items from {args.input}")

        # Example: Process data
        results = {
            "version": VERSION,
            "format": args.format,
            "processed": True,
            # Add emoji example (requires UTF-8 reconfiguration above)
            "status": "✅ Success"
        }

        # Example: Build output path (cross-platform)
        output_file = build_file_path(args.output, "results", f"output.{args.format}")

        # Example: Save results
        save_results(output_file, results)

        print(f"✅ Results saved to: {output_file}")
        return 0

    except FileNotFoundError as e:
        print(f"❌ Error: File not found: {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
