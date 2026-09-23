from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

IGNORED_DIRS = {
    ".git",
    ".next",
    "node_modules",
    "__pycache__",
}

BAD_NAME_PATTERNS = [
    re.compile(r"(^|/)\.DS_Store$"),
    re.compile(r"\.pyc$"),
    re.compile(r"\.pyo$"),
    re.compile(r"\.pem$"),
    re.compile(r"\.p12$"),
    re.compile(r"\.key$"),
    re.compile(r"service[-_]?account.*\.json$", re.I),
    re.compile(r".*-sa\.json$", re.I),
    re.compile(r"credentials.*\.json$", re.I),
]

REQUIRED_PATHS = [
    "apps/backend/main.py",
    "apps/backend/app/routers/cloud.py",
    "apps/command-center/app/page.tsx",
    "docs/PHASE10_CLOUD_SETUP.md",
]

def iter_files():
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue
        if path.is_file():
            yield path, rel.as_posix()

def main() -> int:
    errors: list[str] = []

    for required in REQUIRED_PATHS:
        if not (ROOT / required).is_file():
            errors.append(f"Missing required file: {required}")

    for path, rel in iter_files():
        if any(pattern.search(rel) for pattern in BAD_NAME_PATTERNS):
            errors.append(f"Unwanted/generated/credential-like file: {rel}")
        if rel == ".env":
            errors.append("Local .env must not be committed: .env")

    if errors:
        print("Repository verification FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository verification PASSED")
    print("No unwanted generated or credential-like files were found.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
