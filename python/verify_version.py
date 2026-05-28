"""Verify that the tag version matches pyproject.toml version."""

import re
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: verify_version.py <version>", file=sys.stderr)
        sys.exit(1)

    expected = sys.argv[1]
    pyproject = Path(__file__).resolve().parent / "pyproject.toml"

    if not pyproject.exists():
        print(f"pyproject.toml not found at {pyproject}", file=sys.stderr)
        sys.exit(1)

    content = pyproject.read_text()
    m = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if not m:
        print("Could not find version in pyproject.toml", file=sys.stderr)
        sys.exit(1)

    actual = m.group(1)
    if expected != actual:
        print(f"Version mismatch: tag={expected}, pyproject.toml={actual}", file=sys.stderr)
        sys.exit(1)

    print(f"Version verified: {actual}")


if __name__ == "__main__":
    main()
