from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".git", ".next", "node_modules", "__pycache__"}
BAD = [
    re.compile(r"(^|/)\.DS_Store$"),
    re.compile(r"\.pyc$"),
    re.compile(r"\.pyo$"),
    re.compile(r"(^|/)\.env$"),
    re.compile(r"\.pem$"),
    re.compile(r"\.p12$"),
    re.compile(r"\.key$"),
    re.compile(r"service[-_]?account.*\.json$", re.I),
    re.compile(r"credentials.*\.json$", re.I),
]
REQUIRED = [
    "README.md",
    "apps/backend/main.py",
    "apps/command-center/app/page.tsx",
    "docs/FINAL_QA.md",
    "docs/DEMO_RUNBOOK.md",
    "docs/DEMO_PRESENTATION.md",
]

def main() -> int:
    errors = []

    for item in REQUIRED:
        if not (ROOT / item).is_file():
            errors.append(f"Missing required release file: {item}")

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if any(part in IGNORED for part in Path(rel).parts):
            continue
        if any(pattern.search(rel) for pattern in BAD):
            errors.append(f"Release hygiene violation: {rel}")

    if errors:
        print("RELEASE CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("RELEASE CHECK PASSED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
