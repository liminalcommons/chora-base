#!/usr/bin/env python3
"""
Extract executable code examples from documentation and generate test file.

Finds all markdown files with `test_extraction: true` in frontmatter,
extracts code blocks with language tags, and generates test file:
tests/integration/test_from_docs.py

This ensures documentation examples stay executable and synchronized with code.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install PyYAML")
    sys.exit(1)


class TestExtractor:
    """Extract tests from documentation code examples."""

    # Directories to check
    DOC_DIRS = ["user-docs", "project-docs", "dev-docs"]

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.docs_with_tests: List[Tuple[Path, Dict]] = []  # (path, frontmatter)
        self.extracted_tests: List[str] = []

    def run(self) -> None:
        """Run test extraction and generate test file."""
        print(f"Extracting tests from documentation in {self.root_dir}...")
        print()

        # Step 1: Find docs with test_extraction: true
        self._find_docs_with_tests()

        if not self.docs_with_tests:
            print("No documents found with test_extraction: true in frontmatter.")
            print("Skipping test file generation.")
            return

        print(f"Found {len(self.docs_with_tests)} documents with test_extraction: true")
        print()

        # Step 2: Extract code blocks
        for md_file, frontmatter in self.docs_with_tests:
            self._extract_tests_from_doc(md_file, frontmatter)

        if not self.extracted_tests:
            print("No testable code blocks found (need language-tagged code blocks)")
            return

        # Step 3: Generate test file
        self._generate_test_file()

    def _find_docs_with_tests(self) -> None:
        """Find all docs with test_extraction: true in frontmatter."""
        for doc_dir in self.DOC_DIRS:
            dir_path = self.root_dir / doc_dir
            if not dir_path.exists():
                continue

            for md_file in dir_path.rglob("*.md"):
                frontmatter = self._parse_frontmatter(md_file)
                if frontmatter and frontmatter.get("test_extraction") is True:
                    self.docs_with_tests.append((md_file, frontmatter))

    def _parse_frontmatter(self, md_file: Path) -> Dict | None:
        """Parse YAML frontmatter from markdown file."""
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            return None

        # Check for frontmatter (--- ... ---)
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if not match:
            return None

        # Parse YAML
        try:
            frontmatter = yaml.safe_load(match.group(1))
            if not isinstance(frontmatter, dict):
                return None
            return frontmatter
        except yaml.YAMLError:
            return None

    def _extract_tests_from_doc(self, md_file: Path, frontmatter: Dict) -> None:
        """Extract testable code blocks from a markdown file."""
        content = md_file.read_text(encoding="utf-8")

        # Find all code blocks with language tag
        # Pattern: ```language\ncode\n```
        code_blocks = re.findall(
            r"```(python|bash|sh)\n(.*?)```", content, re.DOTALL
        )

        if not code_blocks:
            return

        doc_title = frontmatter.get("title", md_file.name)
        doc_rel_path = md_file.relative_to(self.root_dir)

        for idx, (lang, code) in enumerate(code_blocks, start=1):
            if lang == "python":
                self._extract_python_test(doc_title, doc_rel_path, code, idx)
            # Note: Bash/shell tests could be added in future enhancement

    def _extract_python_test(
        self, doc_title: str, doc_path: Path, code: str, idx: int
    ) -> None:
        """Extract a Python code block as a test."""
        # Skip code blocks that are just examples without assertions
        if "assert" not in code and "raise" not in code:
            return

        # Clean up code (remove comments that might break tests)
        code = code.strip()

        # Generate test function name (safe identifier)
        safe_title = re.sub(r"[^a-zA-Z0-9_]", "_", doc_title.lower())
        test_name = f"test_{safe_title}_example_{idx}"

        # Generate test function
        test_code = f'''
def {test_name}():
    """
    Test extracted from documentation: {doc_title}
    Source: {doc_path}
    Example {idx}
    """
{self._indent(code, 4)}
'''

        self.extracted_tests.append(test_code)

    def _indent(self, text: str, spaces: int) -> str:
        """Indent text by specified number of spaces."""
        indent = " " * spaces
        return "\n".join(indent + line if line.strip() else line for line in text.split("\n"))

    def _generate_test_file(self) -> None:
        """Generate tests/integration/test_from_docs.py."""
        output_dir = self.root_dir / "tests" / "integration"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "test_from_docs.py"

        # Generate file header
        header = '''"""
Tests extracted from documentation code examples.

This file is auto-generated by scripts/extract_tests.py.
Do not edit manually - update the documentation instead.
"""

import pytest
from pathlib import Path
import sys

# Add src to path for imports
src_dir = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_dir))

'''

        # Combine header + tests
        content = header + "\n".join(self.extracted_tests)

        # Write to file
        output_file.write_text(content, encoding="utf-8")

        print(f"✅ Generated {output_file}")
        print(f"   Extracted {len(self.extracted_tests)} test functions")
        print()
        print("Run tests with: pytest tests/integration/test_from_docs.py")


def main():
    """Main entry point."""
    # Assume script is in scripts/ directory, project root is parent
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent

    extractor = TestExtractor(root_dir)
    extractor.run()


if __name__ == "__main__":
    main()
