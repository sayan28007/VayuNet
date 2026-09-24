from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]

DOCS = [
    "README.md",
    "docs/ARCHITECTURE.md",
    "docs/SETUP.md",
    "docs/DEPLOYMENT.md",
    "docs/FINAL_QA.md",
    "docs/DEMO_RUNBOOK.md",
    "docs/DEMO_PRESENTATION.md",
    "docs/SUBMISSION_CHECKLIST.md",
]

def main() -> int:
    missing = 0
    print("VayuNet submission manifest")

    for rel in DOCS:
        path = ROOT / rel
        if not path.is_file():
            missing += 1
            print(f"MISSING  {rel}")
        else:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
            print(f"OK       {rel}  {digest}")

    if missing:
        print(f"Manifest incomplete: {missing} required item(s) missing.")
        return 1

    print("Manifest complete.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
