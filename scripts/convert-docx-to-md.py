#!/usr/bin/env python3
"""
Convert .docx files to markdown using mammoth.

Usage:
    python scripts/convert-docx-to-md.py <input.docx> <output.md>
    python scripts/convert-docx-to-md.py --batch <directory>
"""

import sys
import mammoth
from pathlib import Path


def convert_docx_to_markdown(docx_path: Path, md_path: Path) -> None:
    """Convert a single .docx file to markdown."""
    print(f"Converting {docx_path.name}...")

    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_markdown(docx_file)
        markdown = result.value

        # Write markdown output
        with open(md_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown)

        # Print any messages (warnings/errors)
        if result.messages:
            print(f"  Messages for {docx_path.name}:")
            for message in result.messages:
                print(f"    - {message}")

        print(f"  Created {md_path.name}")


def convert_batch(directory: Path) -> None:
    """Convert all .docx files in a directory to markdown."""
    docx_files = list(directory.glob("*.docx"))

    if not docx_files:
        print(f"No .docx files found in {directory}")
        return

    print(f"Found {len(docx_files)} .docx file(s) to convert\n")

    for docx_path in docx_files:
        # Create .md filename (replace .docx with .md)
        md_path = docx_path.with_suffix(".md")
        convert_docx_to_markdown(docx_path, md_path)
        print()


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/convert-docx-to-md.py <input.docx> <output.md>")
        print("  python scripts/convert-docx-to-md.py --batch <directory>")
        sys.exit(1)

    if sys.argv[1] == "--batch":
        if len(sys.argv) < 3:
            print("Error: --batch requires a directory argument")
            sys.exit(1)
        directory = Path(sys.argv[2])
        if not directory.is_dir():
            print(f"Error: {directory} is not a directory")
            sys.exit(1)
        convert_batch(directory)
    else:
        if len(sys.argv) < 3:
            print("Error: Single file conversion requires input and output paths")
            sys.exit(1)
        docx_path = Path(sys.argv[1])
        md_path = Path(sys.argv[2])

        if not docx_path.exists():
            print(f"Error: {docx_path} does not exist")
            sys.exit(1)

        convert_docx_to_markdown(docx_path, md_path)


if __name__ == "__main__":
    main()
